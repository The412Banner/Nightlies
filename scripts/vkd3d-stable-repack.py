#!/usr/bin/env python3
"""Checks and profile writer for vkd3d-stable-repack.yml.

  check-src  <dir> <x64|arm64ec> <versionName>   unpacked nightly .wcp
  same-code  <before_dir> <after_dir>            strip removed only debug info/symbols
  profile    <dir> <versionName>                 write profile.json in the stable format
  check-pkg  <dir> <x64|arm64ec> <versionName>   unpacked stable .wcp
"""
import hashlib
import json
import os
import struct
import sys

DLLS = ("system32/d3d12.dll", "system32/d3d12core.dll",
        "syswow64/d3d12.dll", "syswow64/d3d12core.dll")
LAYOUT = sorted(("profile.json",) + DLLS)
MACHINE = {0x8664: "AMD64", 0x14C: "I386", 0xA641: "ARM64EC"}
SYSTEM32_MACHINE = {"x64": "AMD64", "arm64ec": "ARM64EC"}
REQUIRED_EXPORT = {"d3d12.dll": "D3D12CreateDevice", "d3d12core.dll": "D3D12SDKVersion"}
DESCRIPTION = "Built on Banners Nightlies (Upstream: Hans-Kristian Arntzen)"


def fail(msg):
    print(f"::error::{msg}")
    sys.exit(1)


def parse_pe(path):
    data = open(path, "rb").read()
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe:pe + 4] != b"PE\0\0":
        fail(f"{path}: not a PE file")
    machine, nsec = struct.unpack_from("<HH", data, pe + 4)
    sym_ptr, nsym = struct.unpack_from("<II", data, pe + 12)
    opt_size = struct.unpack_from("<H", data, pe + 20)[0]
    opt = pe + 24
    magic = struct.unpack_from("<H", data, opt)[0]
    dd = opt + (96 if magic == 0x10B else 112)
    sections = []
    for i in range(nsec):
        s = opt + opt_size + 40 * i
        name = data[s:s + 8].rstrip(b"\0").decode("latin-1")
        vsize, va, rsize, rptr = struct.unpack_from("<IIII", data, s + 8)
        sections.append((name, va, vsize, rsize, rptr))

    def off(rva):
        for _, va, vsize, rsize, rptr in sections:
            if va <= rva < va + max(vsize, rsize):
                return rva - va + rptr
        fail(f"{path}: RVA {rva:#x} outside every section")

    def cstr(o):
        return data[o:data.index(b"\0", o)].decode("latin-1")

    # ARM64EC images keep the AMD64 machine value; they are told apart by a
    # CHPE metadata pointer in the 64-bit load config (offset 0xC8).
    lc_rva, lc_size = struct.unpack_from("<II", data, dd + 8 * 10)
    if machine == 0x8664 and lc_rva and lc_size >= 0xD0:
        lc = off(lc_rva)
        if struct.unpack_from("<I", data, lc)[0] >= 0xD0 and struct.unpack_from("<Q", data, lc + 0xC8)[0]:
            machine = 0xA641

    exports = []
    exp_rva = struct.unpack_from("<I", data, dd)[0]
    if exp_rva:
        e = off(exp_rva)
        count, names = struct.unpack_from("<I", data, e + 24)[0], struct.unpack_from("<I", data, e + 32)[0]
        for i in range(count):
            exports.append(cstr(off(struct.unpack_from("<I", data, off(names) + 4 * i)[0])))

    code = {}
    for name, va, vsize, rsize, rptr in sections:
        if name.startswith(".debug") or name.startswith("/"):
            continue
        n = min(vsize, rsize) if vsize else rsize
        code[name] = (va, vsize, hashlib.sha256(data[rptr:rptr + n]).hexdigest())

    return {
        "machine": MACHINE.get(machine, hex(machine)),
        "nsym": nsym,
        "sym_ptr": sym_ptr,
        "sections": [s[0] for s in sections],
        "exports": sorted(exports),
        "code": code,
    }


def check_layout(d):
    found = sorted(os.path.relpath(os.path.join(r, f), d) for r, _, fs in os.walk(d) for f in fs)
    if found != LAYOUT:
        fail(f"{d}: files {found}, expected {LAYOUT}")


def check_dlls(d, variant):
    for rel in DLLS:
        info = parse_pe(os.path.join(d, rel))
        want = SYSTEM32_MACHINE[variant] if rel.startswith("system32/") else "I386"
        if info["machine"] != want:
            fail(f"{d}/{rel}: machine {info['machine']}, expected {want}")
        need = REQUIRED_EXPORT[os.path.basename(rel)]
        if need not in info["exports"]:
            fail(f"{d}/{rel}: does not export {need}")
        print(f"  {rel:24s} {info['machine']:8s} {os.path.getsize(os.path.join(d, rel)):>9} B  "
              f"symbols={info['nsym']}  exports={len(info['exports'])}  sections={' '.join(info['sections'])}")


def check_profile(d, version_name, exact):
    p = json.load(open(os.path.join(d, "profile.json")))
    if p.get("type") != "VKD3D":
        fail(f"{d}/profile.json: type {p.get('type')!r}, expected 'VKD3D'")
    if p.get("versionName") != version_name:
        fail(f"{d}/profile.json: versionName {p.get('versionName')!r}, expected {version_name!r}")
    if exact and open(os.path.join(d, "profile.json")).read() != profile_text(version_name):
        fail(f"{d}/profile.json is not in the stable format")


def profile_text(version_name):
    return json.dumps({
        "type": "VKD3D",
        "versionName": version_name,
        "versionCode": 0,
        "description": DESCRIPTION,
        "files": [{"source": rel, "target": "${%s}/%s" % tuple(rel.split("/"))} for rel in DLLS],
    }, indent=2) + "\n"


def main():
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "check-src":
        d, variant, version_name = args
        check_layout(d)
        check_profile(d, version_name, exact=False)
        check_dlls(d, variant)
    elif cmd == "same-code":
        before, after = args
        for rel in DLLS:
            a, b = parse_pe(os.path.join(before, rel)), parse_pe(os.path.join(after, rel))
            if a["code"] != b["code"] or a["exports"] != b["exports"] or a["machine"] != b["machine"]:
                fail(f"{rel}: stripping changed more than debug info and symbols")
            print(f"  {rel:24s} code/data sections and exports identical ({len(a['code'])} sections)")
    elif cmd == "profile":
        d, version_name = args
        with open(os.path.join(d, "profile.json"), "w") as f:
            f.write(profile_text(version_name))
    elif cmd == "check-pkg":
        d, variant, version_name = args
        check_layout(d)
        check_profile(d, version_name, exact=True)
        check_dlls(d, variant)
        for rel in DLLS:
            info = parse_pe(os.path.join(d, rel))
            if info["nsym"] or info["sym_ptr"] or any(s.startswith((".debug", "/")) for s in info["sections"]):
                fail(f"{d}/{rel}: still carries debug info or a symbol table")
    else:
        fail(f"unknown command {cmd}")
    print(f"{cmd} ok: {' '.join(args)}")


if __name__ == "__main__":
    main()
