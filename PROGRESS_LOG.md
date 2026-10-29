# Nightlies — Progress Log

**Repo:** https://github.com/The412Banner/Nightlies
**Local path:** `/data/data/com.termux/files/home/Nightlies`
**Rules:** No pull requests ever. Log every change. Push commits as needed.

---

## Session — 2026-10-29

### [feat] — VKD3D-Proton 3.1 stable: repack workflow (2026-10-29, feat/vkd3d-stable-repack, dry run)
**Why:** upstream released vkd3d-proton v3.1 (2026-10-28, tag commit `4522cc1a`). The nightly already built that exact commit (`VKD3D-Proton-3.1-4522cc1a` + arm64ec, first in `nightly-20261028-152656`), but the stable releases `Vkd3d-proton` / `VKD3D-PROTON-ARM` stopped at 3.0.1. The user asked for a stable 3.1 named, packed and listed like 3.0.1, made standalone on this repo by repackaging the nightly.

#### Findings
- 3.0.1 on both releases is a copy of an older Winlator WCP Hub (Arihany) build: zstd tar (2 MiB window), entries owned 0/0, `profile.json` versionName `3.0.1` / `3.0.1-arm64ec`, versionCode 0, description "Built on the Winlator WCP Hub (Upstream: Hans-Kristian Arntzen)". The hub has an x64 3.1 now (128 MiB zstd window), its arm64ec 3.1 build failed (run 40772378838, `i686-w64-mingw32-gcc` missing).
- Nightly x64 VKD3D DLLs are NOT stripped (`.debug_*` sections, 990–12417 symbols): the AIO `build-vkd3d` job relies on meson `-Dstrip=true`, which only strips on `meson install`, and copies DLLs from the build dir. `build-vkd3d-arm64ec` runs `llvm-strip --strip-all` itself, so arm64ec is clean. Not changed here.
- `nightlies_components.json` lists every `.wcp` on the two releases automatically (verName = filename without extension). `winlator-contents/contents.json` is hand-edited per stable release.

#### What changed
- New `.github/workflows/vkd3d-stable-repack.yml` + `scripts/vkd3d-stable-repack.py`: takes the nightly pair built from the upstream tag commit (hash-checked against the release digest), `llvm-strip --strip-all`, proves code/data sections and exports are unchanged, writes `profile.json` in the 3.0.1 format (versionName `3.1` / `3.1-arm64ec`, versionCode 0, description "Built on Banners Nightlies (Upstream: Hans-Kristian Arntzen)"), packs root-owned tar + zstd -3, re-checks the packed files, then uploads `vkd3d-proton-3.1.wcp` → `Vkd3d-proton` and `vkd3d-proton-arm64ec-3.1.wcp` → `VKD3D-PROTON-ARM`, sets "Current version: 3.1" in both notes, and dispatches `nightlies-components-json.yml`. Push to the feature branch = dry run.
- Local run of the strip/pack/verify steps on the real nightly files: passed; x64 `d3d12.dll` 507904 → 131072 B, `d3d12core.dll` 6615040 → 5332992 B.

#### Device test
- NOT device-tested.

## Session — 2026-10-26

### [feat] — Rutabaga-26.10.22 added to the Rutabaga driver feed (2026-10-26, main, published)
**Why:** GameHub released `rutabaga-26.10.22` (component id 481, tzst MD5 `ba48e1219c92a9c033ec180452bfba03`). The user asked to repackage it like the other three and add it to the feed and release.

#### What changed
- Repackaged as `Rutabaga-26.10.22.zip` = `meta.json` + `libvulkan_freedreno.so` (same layout as the older three). Zip sha256 `f4efa850eb0f0661587ac65c87fb067c92950390c258171ff2889fe21edb9937`; downloaded back from the release, hash matches.
- Uploaded to release `rutabaga-drivers` (new asset, nothing replaced; release stays non-Latest).
- `rutabaga_drivers.json`: new first entry `Rutabaga-26.10.22`.
- Release notes: added a 26.10.22 line.

#### What the build is (strings + decoded built-in game profiles)
- Mesa 26.3.0-devel git-6e2cf3d72b (not in upstream Mesa), built 2026-10-22 with NDK clang 17.0.2.
- Mesh shaders run through compute, A8xx cube-map fix and A8xx IB virtual alias: same code as Max's (maxjivi05) WinNative Turnip patches (WinNative-Emu/Drivers PR #6, also in Droid-Deck/Drivers `patches/linux`).
- New profiles: Final Fantasy VII Rebirth (compute mesh shaders, Wave32 option, 64-wide subgroups), Final Fantasy XVI; `TU_FF7_CP_COPY` / `TU_FF7_CP_UPDATE`; 007 First Light gets `tu_sync_renderpass_cache`; KGSL wait-any fences. AC4 debug log removed.

#### Device test
- NOT device-tested.

#### Note
- The feed itself (`60a70836`, 2026-10-13, three builds) was never logged here.

---

## Session — 2026-09-16

### [fix] — Keep Banners-Turnip Wayland builds out of the GPU driver catalog and the nightly bundle (2026-09-16)
**Banners-Turnip releases will also carry `Turnip-<tag>[-variant]-Wayland.zip`**. These are Linux-style Vulkan ICDs for Bannerlator Wayland containers, imported as a Wayland game driver, not AdrenoTools GPU drivers.

#### What changed
- `.github/workflows/nightlies-components-json.yml`: the Banners-Turnip loop skips assets whose name ends in `-wayland.zip`. They stay out of `banners-turnip_drivers.json`, which Bannerlator's built-in "Banners-Turnip" driver source reads, and out of every `drivers.json` the mirror workflows rebuild from it (kimchi / mtr / stevenmxz / white).
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`: after `gh release download --pattern "Turnip-*.zip"`, `rm -f ./artifacts/Turnip-*-Wayland.zip`, so the AIO nightly bundles only the Android drivers.
- Checked: both files parse (js-yaml), and the Python block compiles. No catalog content changes until a release with Wayland zips exists.

---

## Session — 2026-09-15

### [feat] — Publish workflow for a DXVK stable set, server-side only (2026-09-16)
**New dispatch-only `dxvk-stable-publish.yml` + `.github/release-notes/dxvk-3.1.1.md`. Moves
finished assets GitHub-to-GitHub; nothing is ever uploaded from a workstation.**

#### What changed
- **`.github/workflows/dxvk-stable-publish.yml` (new).** Inputs: `version`, `build_run_id`
  (the `dxvk-stable-patched.yml` run holding the four patched artifacts), `asset_revision`,
  `nightly_tag`, `combined_tag`, and `dry_run`. Steps: pull the 4 patched artifacts by run
  id via `gh run download`, pull the 2 vanilla `.wcp` assets off the nightly release via
  `gh release download`, rename all six to their published names, verify, then upload.
- **Vanilla pair is RENAME ONLY.** `DXVK-v<ver>.wcp` → `dxvk-<ver>.wcp` and
  `DXVK-v<ver>-arm64ec.wcp` → `dxvk-arm64ec-<ver>.wcp`. They are never unpacked,
  recompressed or re-profiled — they are upstream's own release binaries. The workflow
  `cmp`s each renamed file against its source to prove the rename really was a rename.
- **Verification gates every upload.** `scripts/verify-dxvk-wcp.sh` plus a filename ↔
  `profile.json` versionName assertion driven by a six-row table. Any mismatch fails the
  job *before* the first upload, so a bad file can never be published.
- **Additive by construction.** Each per-flavour release gets ONE file via
  `gh release upload --clobber`, which replaces only a same-named asset and leaves every
  other asset alone; the job also asserts each release's asset count never decreases. The
  target release must already exist — this workflow never creates a per-flavour release.
- Combined release: tag `dxvk-<version>`, title `DXVK <version> Stable — all flavors`,
  not a pre-release, all six files, body read verbatim from the committed notes file.

#### Verifier fix required by the vanilla ARM64EC asset
`DXVK-v3.1.1-arm64ec.wcp` stores its members **without** the `./` prefix
(`system32/d3d11.dll`), while every other `.wcp` uses `./system32/d3d11.dll`. Both are valid
tar and install identically, but `verify-dxvk-wcp.sh` matched members literally and rejected
the flat layout. It now normalises a leading `./` away before matching. Confirmed: all six
files pass, where the vanilla ARM64EC one previously failed.

#### Decision: the combined release does NOT take the "Latest" badge
`gh release create` would mark a non-prerelease as Latest by default. In this repo the
nightly holds Latest (currently `nightly-20260916-023850`), so the combined release is
created with `--latest=false` — non-prerelease as asked, but it does not displace the
nightly, and the next nightly will not silently undo it either.

#### PUBLISHED — DXVK 3.1.1, all six flavours (2026-09-16)
Dry run `35053418721` first (all six verified, both upload steps **skipped**, nothing
written), then the real publish run **`35053481208` — success**, both on `main` `b86c7884`.
Combined release: https://github.com/The412Banner/Nightlies/releases/tag/dxvk-3.1.1

| file | release | assets before → after | bytes | sha256 |
|---|---|---|---|---|
| `dxvk-3.1.1.wcp` | `Dxvk` | 13 → 14 | 8,460,648 | `5733f66be140f2be5c3f47d36025c79bdf53daca1b990827c3a3dc733aa8bc7d` |
| `dxvk-arm64ec-3.1.1.wcp` | `Dxvk-arm64ec` | 9 → 10 | 6,311,178 | `719e238d96d3e13c6089a295aa9413d35b42ed1764b5ae9ccbf5c7028f9230e8` |
| `dxvk-gplasync-3.1.1-1.wcp` | `Dxvk-gplasync` | 11 → 12 | 8,776,848 | `51a06efbb8463ca75253aff52850a4e4cf4b27fbc431e216facfd23609a0f404` |
| `dxvk-gplasync-arm64ec-3.1.1-1.wcp` | `Dxvk-gplasync-arm64ec` | 10 → 11 | 6,318,968 | `e229df557c366cb4257372fb7f8edb02023ce982bd7b8ff9c196d79ccc30bfea` |
| `dxvk-binsem-gplasync-3.1.1-1.wcp` | `Dxvk-binsem-gplasync` | 2 → 3 | 8,783,156 | `e02c5d7258191c500d3a65b506aaf6ef658c7454560a7d76821faff31266b36d` |
| `dxvk-binsem-gplasync-arm64ec-3.1.1-1.wcp` | `Dxvk-binsem-gplasync-arm64ec` | 2 → 3 | 6,321,195 | `4d3a7128669797646f87a67e3889c4e32ea6640b32eb348e6fa95dfaad97131d` |

Post-publish checks, done against the **live** releases, not the runner:
- Every per-flavour release gained exactly **+1** asset; none lost any.
- All six re-downloaded and re-verified from the release — all PASS, and the four patched
  sha256s are identical to the build artifacts from run `35052836695`, so the exact bytes
  that were built are the bytes that shipped.
- Rename-only proven: published `dxvk-3.1.1.wcp` and `dxvk-arm64ec-3.1.1.wcp` are
  `cmp`-identical to the nightly's `DXVK-v3.1.1.wcp` / `DXVK-v3.1.1-arm64ec.wcp`.
- The nightly release is untouched (43 assets, all 8 of its own `DXVK-v3.1.1*` files intact).
- The repo's "Latest" badge is still `nightly-20260916-023850`, as intended.
- The release body is the notes file verbatim (differs only by one trailing newline), and
  upstream's anti-virus false-positive warning is present.

#### Files touched
- `.github/workflows/dxvk-stable-publish.yml` (new)
- `.github/release-notes/dxvk-3.1.1.md` (new, verbatim)
- `scripts/verify-dxvk-wcp.sh` (member-path normalisation)

---

### [feat] — Stable-tag DXVK builds: gplasync + binsem from the upstream release tag (2026-09-15, branch `feat/dxvk-stable-patched`)
**New dispatch-only workflow `dxvk-stable-patched.yml` + shared verifier `scripts/verify-dxvk-wcp.sh`. ARTIFACTS ONLY — no release, no upload, no tag.**

#### Why
The all-in-one nightly builds its four gplasync/binsem DXVK flavours from doitsujin/dxvk
**master**, which drifts ahead of the release tag the moment upstream merges anything. On
2026-09-15 upstream cut **v3.1.1** (`b1a1c99ab52b`) and master was already **21 commits
ahead** (`7df3596e`) — so the nightly's gplasync/binsem assets are NOT the stable release.
The nightly's two *vanilla* DXVK jobs were already pinned to the stable release; the four
patched flavours had no stable counterpart. This workflow is it.

#### What changed
- **`.github/workflows/dxvk-stable-patched.yml` (new).** `workflow_dispatch` only. Inputs:
  `dxvk_version` (empty ⇒ resolves the latest upstream stable via
  `gh api repos/doitsujin/dxvk/releases/latest`) and `asset_revision` (the `-N` suffix).
  Reusable as-is on every future upstream stable.
  - `resolve` job peels the tag to a commit **once** and hands it to every build job, which
    asserts `git rev-parse HEAD` equals it and **fails** on mismatch — a job can never
    quietly build a different base.
  - `build-std` (ubuntu-latest, mingw-w64 + `package-release.sh`) and `build-arm64ec`
    (ubuntu-24.04, LLVM-MinGW 20251104 cross build), each a 2-entry matrix
    (`gplasync`, `binsem`) ⇒ the four flavours. Recipes copied from the nightly's
    `build-dxvk` / `build-dxvk-arm64ec` / `build-dxvk-binsem` / `build-dxvk-binsem-arm64ec`,
    with the clone changed to `--branch <tag>`.
  - **No fallback base.** The nightly's DXVK jobs fall back to a pinned v3.0 +
    `gplasync-3.0-1` tree so the nightly always ships. That behaviour is wrong for a
    stable asset — shipping a different base under a 3.1.1 label would make the asset a
    lie — so every patch/verify failure here is fatal and the job stops.
  - Packaging matches the published stable assets exactly: std ⇒ `tar -cJf` (xz -6),
    arm64ec ⇒ `tar --use-compress-program='zstd -19 -T0'`; `profile.json` + `system32/` +
    `syswow64/`; type `DXVK`, `versionCode 0`, versionName `<tag>-<suffix>`, descriptions
    copied verbatim from the published `3.1-1` assets.
  - Artifact filenames: `dxvk-gplasync-<ver>-<rev>.wcp`,
    `dxvk-gplasync-arm64ec-<ver>-<rev>.wcp`, `dxvk-binsem-gplasync-<ver>-<rev>.wcp`,
    `dxvk-binsem-gplasync-arm64ec-<ver>-<rev>.wcp`.
- **`scripts/verify-dxvk-wcp.sh` (new).** Gate every `.wcp` before upload: archive opens,
  `profile.json` is valid JSON with the expected type/versionName/versionCode/description,
  the literal `${system32}`/`${syswow64}` placeholders survived packaging, every `files[]`
  source really exists in the archive, the 5×2 DLL set is complete, and each DLL is a PE of
  the right flavour. Validated locally against all four published `3.1-1` assets (pass) and
  three deliberate mismatches (fail).

#### Patch behaviour against the stable tag (checked before writing the workflow)
Ph42oN publishes no per-release gplasync patch past `3.0-1`; from 3.1 on only
`dxvk-gplasync-master.patch` exists, authored against master. Against the `v3.1.1` tree:
- `git apply` **rejects** it (`src/dxvk/dxvk_graphics.cpp:1420 patch does not apply`).
- `patch -p1 --fuzz=3` **applies**, all hunks, one at fuzz 2 — `dxvk_graphics.cpp` hunk #4,
  the `m_async = false;` line in `DxvkGraphicsPipeline::getOptimizedPipeline`. The only
  context drift is that master has `status.store(status, std::memory_order_release)` where
  the tag still has `status.store(status)`; the added line lands in the identical place.
- `dxvk-binary-semaphores.patch` layers on top, also via `--fuzz=3` (hunks at fuzz 1 and
  fuzz 2, both landing correctly — `m_useTimeline` env read in the `DxvkSubmissionQueue`
  ctor and the `m_useTimeline`/binary-pool members in `dxvk_queue.h`).
So the tolerant `patch --fuzz=3` the nightly uses is **required** here, and the workflow
gates every apply behind a dry run that is fatal on failure.

#### ARM64EC note for the verifier
An ARM64EC PE carries the **AMD64** machine type in its COFF header, so `file` reports both
std and arm64ec `system32` DLLs as `PE32+ … x86-64` — the machine type cannot tell them
apart. The verifier discriminates on the ARM64EC-only sections `.hexpthk` (x64→ARM64 entry
thunks) and `.a64xrm` (ARM64X range map), plus the CHPE load-config pointer via
`llvm-readobj` where available. Confirmed against the published assets: the arm64ec
`system32` DLLs carry both markers and a non-zero `CHPEMetadataPointer`, the std ones carry
neither.

#### CI-GREEN
- Run `35051699762` (`3dd72499`) — all 5 jobs success; first cut, ARM64EC still zstd level 3.
- Run `35052836695` (`98804cb0`) — all 5 jobs success; the zstd -19 fix. **This is the run
  whose four artifacts are the deliverable.** All four jobs logged
  `CHECKED OUT DXVK COMMIT: b1a1c99ab52b687cf950d62c88bc2fa316b41663` and
  `meson project version: 3.1.1`.
- `workflow_dispatch` only registers from the DEFAULT branch, so the workflow could not be
  dispatched while it lived only on this branch. It was validated with a temporary
  branch-scoped `push:` trigger, removed again in the final commit — the workflow ships
  dispatch-only. A push run passes no inputs, so this also proved the default
  "resolve the latest upstream stable myself" path (it found `v3.1.1` on its own).
- Artifacts (run `35052836695`), **not uploaded anywhere** — the user publishes them:

  | artifact | bytes | sha256 |
  |---|---|---|
  | `dxvk-gplasync-3.1.1-1.wcp` | 8,776,848 | `51a06efbb8463ca75253aff52850a4e4cf4b27fbc431e216facfd23609a0f404` |
  | `dxvk-gplasync-arm64ec-3.1.1-1.wcp` | 6,318,968 | `e229df557c366cb4257372fb7f8edb02023ce982bd7b8ff9c196d79ccc30bfea` |
  | `dxvk-binsem-gplasync-3.1.1-1.wcp` | 8,783,156 | `e02c5d7258191c500d3a65b506aaf6ef658c7454560a7d76821faff31266b36d` |
  | `dxvk-binsem-gplasync-arm64ec-3.1.1-1.wcp` | 6,321,195 | `4d3a7128669797646f87a67e3889c4e32ea6640b32eb348e6fa95dfaad97131d` |

#### Compression: the ARM64EC assets are zstd **-19**, not tar's default
Measured against the published `3.1-1` assets rather than assumed:
- **std** — recompressing the published `dxvk-binsem-gplasync-3.1-1.wcp` payload with plain
  `tar -cJf` reproduces **7,797,976 bytes, its exact published size**. So the standard
  assets are ordinary xz -6 and the jobs keep `tar -cJf`. A higher xz preset was rejected:
  -9 would shrink the asset ~1 MB but raises the *decoder's* memory need from 8 MB to
  64 MB, which is not worth it for an asset unpacked on a phone.
- **arm64ec** — `tar --zstd` means level 3 and yields **13.3 MB**, but the published
  `dxvk-gplasync-arm64ec-3.1-1.wcp` is **6,319,391 bytes**; recompressing our own payload at
  `zstd -19` gives **6,319,088** — a 303-byte delta on 6.3 MB, i.e. the 3.1→3.1.1 code
  difference. The published ARM64EC assets are therefore level 19, and the AIO's bare
  `tar --zstd` would have handed users a **2.1x larger download for identical DLLs**. The
  ARM64EC jobs use `zstd -19 -T0`; decompression stays an 8 MB window and is already proven
  on device by the existing published assets.

#### Known size difference vs the 3.1 assets (std only, not a packaging bug)
The std `3.1.1` archives come out ~1 MB larger than the published `3.1` ones (8.78 MB vs
7.80 MB) even though the packaging is byte-for-byte the same recipe and the *uncompressed*
payloads are the same size (44,631,130 vs 44,627,032 B, every DLL within 4 KB). The 3.1.1
DLLs simply compress ~12% worse — different mingw-w64 GCC codegen on today's runner image
than when the 3.1 asset was built. Nothing to fix; noted so the size jump is not mistaken
for a stripping or packaging regression later.

#### Files touched
- `.github/workflows/dxvk-stable-patched.yml` (new)
- `scripts/verify-dxvk-wcp.sh` (new)
- No existing workflow modified — `new-All-in-one-nightly+zips-latest-stable.yml` untouched.

---

## Session — 2026-08-28

### [feat] — Vanilla DXVK build jobs added to the all-in-one nightly (2026-08-28, `d64ace24` on `main`)
**Two new jobs in `new-All-in-one-nightly+zips-latest-stable.yml`, both pinned to the latest upstream stable release:**
- `build-dxvk-vanilla` (std x64/x86) — repackages upstream's official `dxvk-<ver>.tar.gz` → `DXVK-v<ver>.wcp`, versionName `v<ver>`. No compile. Artifact `dxvk-vanilla`.
- `build-dxvk-arm64ec-vanilla` — cross-compiles arm64ec (LLVM-MinGW 20251104; mirrors the arm64ec gplasync job minus patches) → `DXVK-v<ver>-arm64ec.wcp`, versionName `v<ver>-arm64ec`. Artifact `dxvk-arm64ec-vanilla`.
- Wired into `create-release` `needs:`; artifacts auto-collected via existing `download-artifact merge-multiple` + `*.wcp/*.zip` upload.
- **CI-GREEN:** validated on branch run `33215950780` — both vanilla jobs success (also all 4 gplasync/binsem DXVK jobs).

#### Reconciliation note (parallel work by another session)
While this was on branch `feat/dxvk-vanilla-aio-jobs`, `origin/main` independently gained the **same gplasync fix** (`d402935e` — DxvkAttachment shadow field, identical `.view` member-access approach) plus a **compile-guard hardening** (`e81c0fb2` — real compile guard with v3.0 fallback). So my duplicate patch fix (branch commit `158288d2`) was **dropped**; only the vanilla-jobs commit was cherry-picked onto `origin/main` (`52458184` → `d64ace24`). No clobber. Both features coexist (verified: 14 jobs, both vanilla jobs + the v3.0 compile-guard fallback present).

#### ⚠️ Known: FEXCore master breakage (NOT DXVK, left for now per user)
`Build FEXCore` + `(PPA flavor)` fail on FEX **master** `config_generator.py:425 assert "AffectsCodeGen" in op_vals` — a recent FEX commit added/renamed a config option without the marker. FEX passed at 21:14 + in the 20:31 nightly. Blocks the nightly publish (hard `needs`) until upstream fixes it or FEX is pinned. Documented; no action this session.

---

## Session — 2026-08-06

### [feat] — Add D7VK (DirectDraw/D3D7) all-in-one component (2026-08-06)
**Branch `feat/d7vk-aio-component` → FF-merged to `main` (`5d6ceb4e`); real publish run `31136317325` success.**

#### What changed
- New `build-d7vk` job in `new-All-in-one-nightly+zips-latest-stable.yml`. Builds
  `WinterSnowfall/d7vk` **`devel`** branch (pinned `--branch devel`) — the 2.x PRODUCT
  line (latest v2.x tags). Deliberately NOT `master` (that's a DXVK-3.0.2-rebase line; the
  `v3.0.2` tag + meson `version:'3.0.2'` are the DXVK base, not the d7vk product version).
- Reuses the DXVK harness (mingw + ccache keyed to devel HEAD + glslang). **32-bit only**
  (package-release.sh `opt_32_only=1`); ships ONLY `syswow64/ddraw.dll` (statically links
  own d3d9 → self-contained; does not touch container DXVK d3d9/d3d11/dxgi).
- **GCC/mingw shim (required):** devel uses clang-only `std::sqrtf` (libstdc++/mingw doesn't
  expose it in `std::`) → rewrite to `std::sqrt` before building. Plus fallback to last
  product tag if devel still won't build.
- Version label `<latest-product-tag>-<commit>-nightly` (e.g. `v2.1-bc3b29b9e-nightly`).
  Artifacts `d7vk-<version>.{tzst,wcp,zip}`. `.tzst` = drop-in refresh for the app's bundled
  `assets/ddrawrapper/d7vk.tzst`. profile.json type `D7VK`.
- create-release wired: `needs`, version env, built-components + files-included tables,
  README block, upstream-status array, and `*.tzst` added to the release + nightly-latest
  upload globs. `nightlies-components-json.yml` classifies `d7vk-*` as type `D7VK`.
  `Upstream-watcher.yml` tracks `WinterSnowfall/d7vk` (HEAD=devel) → new commits trigger a
  nightly and show under "What changed".
- Published: `nightly-20260807-010254` + `nightly-latest` carry `d7vk-v2.1-bc3b29b9e-nightly.
  {tzst,wcp,zip}`; manifest has 2 D7VK entries.
- ⚠️ Known convention gap: the auto-manifest derives `verName` from the FILENAME stem
  (`d7vk-…`, needed so the classifier greps "d7vk"), which differs from the .wcp's
  profile.json versionName (`v2.1-…`). Pre-existing for all manifest components; the
  winlator-contents catalog uses the correct version-matching verName.

#### Files touched
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`
- `.github/workflows/Upstream-watcher.yml`
- `.github/workflows/nightlies-components-json.yml`
- `PROGRESS_LOG.md`

## Session — 2026-07-03

### [feat] — FEX build naming: stable (on-tag) vs nightly (+N drift) (2026-07-03)
**PR #8 → merged to `main` (squash, tip `5a64177`).**

#### Problem
`git describe --tags --abbrev=0` strips the `-N-gSHA` suffix, so a FEX build cut from a
commit *past* a release tag was named identically to the true on-tag release. Today's HEAD
`1d695f6db` is **2 commits past the `FEX-2607` tag** (tag at `1cc4b93e`) yet shipped as clean
`FEX-2607` — indistinguishable from an exact-tag release.

#### Fix
Name by distance from the nearest FEX tag (`git rev-list <tag>..HEAD --count`):
- exactly on tag → **`FEXCore-<ver>-stable`** (non-PPA) / **`FEXCore-<ver>-stable-ppa`** (PPA)
- N past tag → **`FEX-<ver>+N-Nightly-<sha>`** / `…-PPA`

Applied to both FEX blocks in the all-in-one nightly (non-PPA + PPA; PPA `VERSION_SHORT`
flows to profile.json), the standalone-nightly fallback, and the PPA-stable file-stem.
VKD3D/DXVK/Box64 untouched. `+` survives GitHub asset upload. Post-merge test runs:
standalone auto-produced `FEX-2607+2-Nightly-1d695f6db`; all-in-one produced both flavors'
drift names. Retro-renamed today's mislabeled `nightly-latest` FEX assets to `+2` and
repointed the 4 pinned URLs in `nightlies_components.json`.

#### Files touched
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`
- `.github/workflows/fexcore-standalone-nightly.yml`
- `.github/workflows/fexcore-ppa-stable.yml` (file-stem → `FEXCore-<ver>-stable-ppa`)
- `nightlies_components.json`

---

### [chore] — Cut FEXCore 2607 stables (non-PPA + PPA) from the exact tag (2026-07-03)
Built from `FEX-2607` (commit `1cc4b93e`), delivered to device `/sdcard/Download`:
- Non-PPA: release `fexcore-nightly-20260703-142726` → `FEXCore-2607-stable.wcp/.zip`
- PPA: release `fexcore-ppa-FEX-2607-1cc4b93e7` → `FEXCore-2607-stable-ppa.wcp/.zip`

Cleanups: deleted a stray `glslang-master-linux-Release.zip` swept into both releases by the
`*.zip` upload glob (**TODO:** exclude glslang from the glob). Note the standalone workflow
hardcodes `make_latest:true`; `nightly-latest` is a prerelease so can't hold Latest anyway.

**PPA-fidelity decompile (ours vs `nickppa` vs official-2605):** no official 2607 PPA exists
yet (Launchpad newest = 2605). Ours = faithful mirror (bylaws clang 21.1.0, DWARF,
`//fex-emu/HostThunks`, +0.2% size vs official 2605). `nickppa` = genuine 2607 (99.99%
instruction-identical) but NOT PPA-faithful ("PPA build flags" false — standard HostThunks
path; "No strip" misleading — zero DWARF). All run games identically.

---

### [research] — FEXCore unixlib transition (2607+): DECISION = WAIT (2026-07-03)
FEX 2607 now ships **4 files** for Wine (2 PE DLL + 2 native `.so` unixlib); `.so` is a
companion, not a replacement. Optional now, likely mandatory "in a few months" (FEX PRs
#5612/#5637, merged 06-28→06-30). Loads via custom `NtQueryVirtualMemory(MemoryWineLoadUnixLibByName)`
needing FEX-patched Wine. Bannerlator's Protons (9.0 + 11.0-5) are **bionic NDK** builds
with **no loader** → adding `.so` to the FEX nightly wcp does nothing (glibc ABI, wrong dir,
no loader). `.so` belong in a rebuilt bionic Proton, not the FEX wcp. **Decision: keep FEX
nightlies DLL-only; do NOT rebuild Proton yet** — wait for FEX to stabilize (triggers:
official 2607 PPA / 2608 tag / unixlib made non-optional). No workflow change.

---

## Session — 2026-07-02

### [feat] — All-in-one DXVK builds track upstream master + vendored Ph42oN master gplasync patch (2026-07-02)
**Branch:** `feat/dxvk-master-gplasync` (`5056457a`) → **merged to `main` via merge commit `0ca2ebe2`** (no-ff, branch deleted).

#### Problem
The 2026-06-30 v3.0 pin fixed the red runs but froze all 4 gplasync DXVK assets at the
v3.0 commit `97fe0c66` — every hourly release republished a byte-identical DXVK while the
release header looked new. Requirement: every DXVK build = upstream `doitsujin/dxvk`
**latest master commit** + Ph42oN's **newest master gplasync patch** ("true gplasync"),
with the patch vendored in this repo. Scope: all-in-one workflow only (nvapi no longer
built; standalone workflow left pinned/untouched).

#### Fix (`new-All-in-one-nightly+zips-latest-stable.yml`, all 4 gplasync jobs: std / arm64ec / binsem / binsem-arm64ec)
- Clone dxvk **master** (dropped `--branch v3.0`) and apply the vendored
  `patches/dxvk-gplasync-master.patch` via `patch -p1 --fuzz=3` (`git apply` rejects it on
  master due to context drift; fuzz applies it — 1 hunk at fuzz 2).
- **Refreshed the stale vendored master patch** to Ph42oN's newest (`40b31c3`, 2026-06-28)
  — the stale local copy was the root cause of the 6/30 breakage.
- **Fallback, never hard-fail:** dry-run the master patch first; on failure → re-clone
  `v3.0` + newly vendored `patches/dxvk-gplasync-3.0-1.patch` + `::warning::` telling us to
  re-vendor. Version/hash computed from whichever tree actually built.
- binsem layer switched `git apply` → `patch --fuzz=3` for the same drift tolerance
  (verified it applies cleanly on today's master).
- **Safety:** `create-release` gated `if: github.ref == 'refs/heads/main'` — branch
  dispatches build everything but can never publish or clobber `nightly-latest`.

#### Proof
Branch dispatch run `28557132326`: **all 14 jobs green**, release correctly skipped.
Artifacts confirm the master path executed (not the fallback): all 4 variants =
`…-eea51bab.wcp` (dxvk master HEAD at build time), not `97fe0c66`. Filenames keep the
dynamic `v3.0-` `git describe` prefix by choice (rolls to v3.1 automatically when upstream
tags it). Build-proven only — not device-tested.

#### Shipped + follow-ups (same session)
- Manual `main` dispatch run `28557928482` all-green → **release `nightly-20260702-011327`
  published and `nightly-latest` refreshed with all 4 DXVK variants at `eea51bab`** —
  the fix is live in production.
- **Issue #7** (Betaminos, "DXVK stuck at 97fe0c66?") — the report that surfaced the bug —
  answered with the full root-cause/fix explanation and **closed** with the release as proof.
- `3e2bdc97` (display-only metadata, ships from the *next* nightly): VKD3D profile.json
  `description` raw-hash → attribution line matching the DXVK style; FEX-PPA `versionName`
  bare `2605` → `FEX-2605-PPA` (deliberately overrides the old byte-for-byte PPA-metadata
  mirror on that one field; comment updated). `versionCode` 0/1 values left alone by
  decision — nothing version-compares wcps today.

---

## Session — 2026-06-30

### [fix] — Pin DXVK v3.0 + switch to Ph42oN's official gplasync-3.0-1 patch (the "revert to curl once upstream rebases" follow-up) (2026-06-30)
**Branch:** `fix/dxvk-gplasync-3.0-pin` (`c6e81909`) → **merged to `main` via merge commit `f881c5ce`** (no-ff; main had advanced to `65a6041` w/ a components-json auto-commit, so a real merge — no conflicts, only the 3 DXVK workflow YAMLs).

#### Problem
The vendored `patches/dxvk-gplasync-master.patch` from the 2026-06-03 session drifted AGAIN.
All 4 DXVK jobs went red for 30+ consecutive "All-in-One Emulation Nightlies" runs (Box64 /
VKD3D / FEXCore stayed green), failing at the **"Clone & Patch DXVK"** step. DXVK `HEAD`
(floating) moved past the rebased patch → hunks no longer apply:
- `src/dxvk/dxvk_context.cpp:6668` → patch does not apply
- `src/dxvk/dxvk_graphics.cpp:1415` → patch does not apply
Last failed run at diagnosis: `28432926425`.

#### Fix
The 2026-06-03 note said "revert to curl once he rebases upstream main." That condition is
now MET: DXVK upstream tagged **`v3.0`**, and Ph42oN published **`dxvk-gplasync-3.0-1.patch`**
(2026-06-28, GitLab `Ph42oN/dxvk-gplasync`). So we stop chasing floating `HEAD`:
1. **Pin the clone** to `--branch v3.0` in all DXVK jobs (no more `git describe` of a moving
   target driving the build source).
2. **Switch the gplasync source** from the vendored master patch back to the official tagged
   patch, curl'd from `https://gitlab.com/Ph42oN/dxvk-gplasync/-/raw/main/patches/dxvk-gplasync-3.0-1.patch`.
3. ⚠️ **Applied via `patch -p1 --fuzz=3`, NOT `git apply`** — the official 3.0-1 patch was built
   against a slightly different DXVK 3.0 source blob than the `v3.0` git tag (context.cpp blob
   `c84cf342` vs tag `d8da03e3`; one hunk's leading context line is `GpIndependentSets);` in the
   patch vs `GpDirtyDepthBias));` in the tag). `git apply` refuses on that context mismatch;
   `patch --fuzz=3` applies cleanly (one hunk needs fuzz 1, rest are pure offsets, anchoring on
   the unique `getPipelineHandle`/`updateRenderTargets` lines). Documented inline in the YAML.
   Added `patch` to the 4 DXVK apt installs.
4. The 2 BinSem jobs **keep `git apply` for `dxvk-binary-semaphores.patch`** — it still applies
   clean against `v3.0` with no rebase (touches only `dxvk_cmdlist.{cpp,h}` / `dxvk_queue.{cpp,h}`,
   no gplasync overlap). Verified locally (exit 0) and on CI.

#### Verification
- **Branch CI run `28435269627`** — all 14 build jobs green incl. all 4 DXVK
  (GPLAsync / ARM64EC / BinSem GPLAsync / BinSem ARM64EC), all built from DXVK `v3.0` commit
  `97fe0c66`. (The branch run's only red was the `Update README` push step — it auto-commits +
  pushes and only works on the default branch; irrelevant to DXVK.)
- **Post-merge manual dispatch on `main` — run `28436548767`: `success`, ALL jobs green**,
  including `Create Nightly Release` and its `Update README` step (confirming the branch-run
  red was purely a non-default-branch artifact). Release `nightly-20260630-101231` published
  (Latest) + rolling `nightly-latest` refreshed, both carrying v3.0-built DXVK.
- Build-proven + release-published. DXVK 3.0 runtime rendering NOT yet device-tested.

#### Files touched
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml` (orchestrator — 4 DXVK jobs)
- `.github/workflows/dxvk-binsem-nightly.yml` (`base_ref` default `master`→`v3.0`; both BinSem jobs)
- `.github/workflows/dxvk-standalone-nightly.yml` (all 4 jobs)

#### Flagged / not done
- `dxvk-stable-matrix-nightly.yml` **intentionally untouched** — no drift bug (it already pins
  per-version tags + version-matched local patches for 2.5–2.7.1, never the master patch).
  Adding a 3.0 row = separate enhancement (needs committed local `dxvk-gplasync-3.0-1.patch` +
  `dxvk-binary-semaphores-3.0.patch`).
- Optional hardening: guard the `Update README` step with `if: github.ref == 'refs/heads/main'`
  so non-default-branch dispatches go fully green. Out of scope here.

---

## Session — 2026-06-03

### [fix] — Rebase + vendor gplasync master patch (DXVK cc418519 broke it); fix build-dxvk checkout (2026-06-03)
**Commits:** `84d41ff` (patch rebase + vendor), `b38eb9b` (build-dxvk checkout)

#### Problem
All 4 DXVK gplasync jobs went red starting 2026-06-01. Root cause: DXVK upstream
commit `cc418519` ("[dxvk] Fix thread synchronization on pipeline compiles") rewrote
`DxvkGraphicsPipeline::getOptimizedPipeline` in `src/dxvk/dxvk_graphics.cpp`:
- `m_fastPipelines.insert({ key, handle })` → `m_fastPipelines.emplace(std::piecewise_construct, …)`
- single compile path → `if (entry.second) { …compile…; return handle; } else { …spin-wait… }`

Ph42oN's `dxvk-gplasync-master.patch` (upstream main, last touched 2025-12-29 — he had
NOT fixed it) anchors `m_async = false;` on the old `insert` block → `patch does not apply`
at `dxvk_graphics.cpp:1397`. Jobs clone DXVK `HEAD` (floating), so it broke live.

#### Fix
1. **Rebased the patch** — only one hunk changed: moved `m_async = false;` into the new
   `if (entry.second)` compile branch, right before its `return handle;`. Preserves the
   original semantics (reset on the actual-compile path only; cache-hit early-return does
   not reset). All other hunks + the binsem patch (touches cmdlist/queue, unaffected) apply
   clean. Verified `git apply --check` exit 0 on pristine DXVK HEAD `840d147`; binsem applies
   on top.
2. **Vendored** the rebased patch at `patches/dxvk-gplasync-master.patch` and switched all 4
   DXVK jobs from `curl …Ph42oN…|git apply` to `git apply "$GITHUB_WORKSPACE/patches/dxvk-gplasync-master.patch"`.
   Trade-off: no longer auto-tracks Ph42oN — **revert to curl once he rebases upstream main.**
3. `build-dxvk` (plain GPLAsync std job) had NO `actions/checkout` (it only ever curl'd the
   patch) → first re-run failed with `can't open patch … No such file or directory`. Added a
   `Checkout (for patch file)` step (the other 3 DXVK jobs already had one).

#### Verification
- Run `26873026129` — all 4 DXVK jobs green (compiled + packaged): Build DXVK (GPLAsync),
  Build DXVK BinSem (GPLAsync), Build DXVK (ARM64EC), Build DXVK BinSem (ARM64EC).
- Build-proven only; runtime async-correctness under the new sync model NOT device-tested.
- Filed-issue-on-Ph42oN: drafted, not posted (no GitLab creds in env).

#### Files touched
- `patches/dxvk-gplasync-master.patch` (vendored, rebased)
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml` (4 jobs → local apply; build-dxvk checkout)

---

## Session — 2026-05-13

### [feat] — Surface Banners-Turnip releases in nightlies_components.json (2026-05-13)

#### What changed
- `nightlies-components-json.yml` already fetched all Banners-Turnip releases on every run, but the loop body appended only to `turnip_driver_entries[]` (→ `banners-turnip_drivers.json` + `drivers.json`) and explicitly skipped `entries[]` (→ `nightlies_components.json`), per a "catalog stays focused on emulator/translation layers" policy.
- Flipped the policy: turnip entries now `entries.append(entry)` alongside the existing `turnip_driver_entries.append(entry)`. `banners-turnip_drivers.json` and `drivers.json` still written exactly as before (mirror workflows in kimchi/stevenmxz/mtr/white/all-in-one are unaffected).
- Result: on next run of the watcher, `nightlies_components.json` gains a `type: "GpuDriver"` row per turnip `.zip` asset across all Banners-Turnip tags. Subsequent runs idempotently re-scan all tags, so new releases land automatically with no state file.

#### Files touched
- `.github/workflows/nightlies-components-json.yml` (lines 193-195: replaced 3-line "NOT added" comment + lone append with two appends)

#### Trigger
- Watcher runs on `workflow_run` (completed) + cron + `workflow_dispatch`. Will pick up automatically on the next trigger, or can be kicked manually with `gh workflow run nightlies-components-json.yml`.

---

## Session — 2026-05-08

### [feat] — Add `.wcp.xz` Wine + Proton entries to components catalog (2026-05-08)
**Commits:** `ff7c02c` (initial add) → re-applied as `d004d9d` after watcher wipe

#### What changed
- Manually added `wine-11.3-arm64ec` and `proton-10-arm64ec` to `nightlies_components.json` (158 → 160). Both back `.wcp.xz` assets in the `Proton/wine` release that the watcher's `.wcp` / `.zip` filter currently skips.
- First add (`ff7c02c`) was wiped by the watcher (`86fec95`, regenerated back to 158). Recovered via rebase + re-insert in `d004d9d`.

#### Files touched
- `nightlies_components.json`

#### Known follow-up
- Watcher (`nightlies-components-json.yml`) only ingests `.wcp` / `.zip`; any `.wcp.xz` adds remain a manual-maintenance burden until the workflow is taught to include them.

---

### [docs] — Add Component Catalog (JSON Index) section to README (2026-05-08)
**Commit:** `c42b2d1`

#### What changed
- New top-level section between the intro and "Latest Nightly Releases" pointing to `The412Banner/winlator-contents` and the raw `contents.json` URL, so Winlator-family clients have a discoverable entry point for the catalog.

#### Files touched
- `README.md`

---

### [chore] — Strip `nightly-latest` entries from components catalog (2026-05-08)
**Commit:** `b2d392e`

#### What changed
- Removed all 22 `nightly-latest` rolling-tag entries (160 → 138): 8 Box64 · 4 DXVK · 4 VKD3D · 4 WOWBox64 · 2 FEXCore.
- Reason: `nightly-latest` entries duplicated archived versions and carried type/filename mismatches (WOWBox64 builds filed under Box64 and vice versa).
- Mirrored the same delete to `winlator-contents/contents.json` (`5b0bfc9` on that repo).

#### Files touched
- `nightlies_components.json`

#### Known follow-up
- Workflow `nightlies-components-json.yml` lines 98–115 unconditionally re-fetch the `nightly-latest` tag, so this delete will be reverted on the next workflow run unless those lines are removed.

---

## Session — 2026-03-23

### [fix] — Add actions: write permission to Create Nightly Release job (2026-03-23)
**Commit:** `278522f`

#### What changed
- `new-All-in-one-nightly+zips-latest-stable.yml`: added `actions: write` to the `Create Nightly Release` job's `permissions` block
- Root cause: `gh workflow run nightlies-components-json.yml` requires `actions: write` on `GITHUB_TOKEN`; job only had `contents: write`, causing HTTP 403 on every run

#### Files touched
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`

---

## Session — 2026-03-06

### [feat] — Dynamic release notes + upstream change tracking (2026-03-06)
**Commit:** `c783331`

#### What changed

**Upstream-watcher.yml:**
- Added `NAMES` array mapping each repo URL to a friendly display name
- Before overwriting `upstream_hashes.txt`, captures old hash per repo to detect what changed
- For each changed repo: fetches commit message + date from GitHub API
- Builds `CHANGED_JSON` array (repo, name, old hash, new hash, full hash, message, date)
- Writes `upstream_changes.json` with `triggered_at` timestamp + `changed` array
- Commits both `upstream_hashes.txt` and `upstream_changes.json` when changes detected
- Triggers `new-All-in-one-nightly+zips-latest-stable.yml` (unchanged trigger mechanism)

**new-All-in-one-nightly+zips-latest-stable.yml (create-release job):**
- Added `actions/checkout@v4` step so the job can read `upstream_changes.json`
- Added `Build Release Body` step:
  - Queries GitHub API live for all 6 upstream repos (latest commit hash, message, date)
  - Marks any repo updated in last 24h with 🆕 badge in status table
  - Reads `upstream_changes.json` — if written within the last 3 hours, generates "🔄 What Triggered This Build" table with old→new commit links
  - Writes full release body to `release_body.md`
- Switched from `body:` (static inline) to `body_path: release_body.md` in softprops action
- Added disclaimer to top of every nightly release body:
  `⚠️ DISCLAIMER: NIGHTLY BUILDS ARE NOT ALWAYS STABLE OR RECOMMENDED! USE AT YOUR OWN RISK! STABLE RELEASES ARE ALWAYS BEST TO USE!`

#### Files touched
- `.github/workflows/Upstream-watcher.yml`
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`

---

### [chore] — Disclaimer added to all existing nightly releases (2026-03-06)
**Method:** `gh release edit` loop via CLI (no commit)

#### What changed
- Prepended disclaimer to all 9 existing nightly release descriptions:
  - nightly-20260306-143533
  - nightly-20260306-135338
  - nightly-20260306-124048
  - nightly-20260306-112704
  - nightly-20260306-103204
  - nightly-20260306-090646
  - nightly-20260306-073819
  - nightly-20260305-223528
  - nightly-20260305-192208
- Non-nightly releases (Steam-clients, Bionic-Ludashi-proton, Box64, FexCore, etc.) left untouched

---

### [docs] — Progress log created (2026-03-06)
**Commit:** (this file)
#### What changed
- Created PROGRESS_LOG.md to track all changes to this repo going forward

---

## Session — 2026-03-11

### [feat] — Proton Bleeding-Edge ARM64EC standalone workflow (2026-03-11)
**Commits:** `491632a` (initial), `9943fa9`→`e9c28db` (release notes fix)

#### What changed

**New file: `.github/workflows/proton-bleeding-edge-nightly.yml`**
- Standalone workflow to build ValveSoftware/wine `bleeding-edge` branch with GameNative Android + ARM64EC patches
- Schedules every 6 hours + `workflow_dispatch` (inputs: `wine_ref`, `gamenative_ref`, `target_app_id`, `force_build`)
- **Job 0 — sync-scripts:** Fetches all build scripts/patches from Pepelespooder/proton-arm64-nightlies via GitHub API, compares byte-for-byte, commits any changes to `proton-scripts/`. Gracefully skips if upstream unavailable. Local copies act as permanent fallback.
- **Job 2 — build:** Clones ValveSoftware/wine + GameNative/proton-wine, applies patches from `proton-scripts/`, downloads LLVM MinGW 20250920 (bylaws) + NDK r27d + termuxfs aarch64, compiles full ARM64EC Wine, packages `.wcp` (zstd-tar) and `.wcp.xz` (XZ-tar + prefixPack) with SHA256
- **Job 3 — release:** Queries GitHub API live for wine bleeding-edge commit info, builds styled release notes matching all-in-one format, always publishes a release (no skip gate), updates and commits `proton-latest.json`
- Release tag format: `proton-bleeding-edge-{date}-{hash}-run{N}`
- Release is always pre-release

**New file: `proton-scripts/`** (39 files)
- Full backup of all build dependencies from Pepelespooder's repo
- `scripts/` — 26 Python/shell scripts (filter_patches.py, patch_build_script.py, fix_*.py, generate_profile.py, create-proton-wcp.sh, verify_required_markers.py, etc.)
- `ge-second-pass/test-bylaws/` — 2 BYLAWS patch overrides
- `ge-second-pass/focus/`, `keyboard/`, `mouse/`, `performance/` — additional patches
- `patches/` — dlls_winex11_drv_window_c.patch

**New file: `proton-latest.json`**
- Tracks last built Wine hash, version name, WCP/WCP.XZ filenames + SHA256 checksums, release tag
- Read by release job to determine old hash for "What Triggered" section

**Modified: `.github/workflows/Upstream-watcher.yml`**
- Added ValveSoftware/wine `bleeding-edge` branch tracking (separate from the main 5-repo loop)
- Stored under key `https://github.com/ValveSoftware/wine@bleeding-edge: <hash>` in `upstream_hashes.txt`
- New output: `wine_changed` (true when wine bleeding-edge HEAD changes)
- New output: `anything_changed` (true when any hash changed — used for commit step)
- New trigger step: `gh workflow run "proton-bleeding-edge-nightly.yml"` fires when `wine_changed == true`
- Existing `changed` output still triggers all-in-one nightly as before

#### Release note format (matching all-in-one style)
- Disclaimer at top
- `### 🚀 Proton Bleeding-Edge Build: {tag}`
- `### 🔄 What Triggered This Build` — old→new wine hash table when hash changed; "Scheduled/manual" otherwise
- `### 📊 Upstream Status` — wine bleeding-edge commit with 🆕 badge if updated in last 24h
- `### 📦 Built Components` — Proton ARM64EC row with commit link
- `### 📦 Files Included` — WCP + WCP.XZ with sha256 note

#### Bug fixed
- **Heredoc PY terminator not found (run6):** Triple-quoted f-string content had zero YAML indentation. YAML calculated min-indent=0 so stripped nothing — the `PY` end-marker kept 10 leading spaces in the shell script and bash never matched it. Fixed by replacing `f"""..."""` with `list` + `"\n".join()` so all lines stay indented inside the Python block.

#### Files touched
- `.github/workflows/proton-bleeding-edge-nightly.yml` (new)
- `.github/workflows/Upstream-watcher.yml`
- `proton-scripts/` (new directory, 39 files)
- `proton-latest.json` (new)

---

## Session — 2026-03-11 (continued)

### [fix] — Rebase conflict fix + release description improvements (2026-03-11)
**Commit:** `dfacb3f`

#### What changed
- `git pull --rebase -X ours` in "Commit proton-latest.json" step — concurrent runs no longer fail with a merge conflict; current run's version of `proton-latest.json` always wins
- Added `⬇️ Download` section to release description with a per-file table (file name, description, link) and a "Which file do I need?" callout explaining `.wcp` vs `.wcp.xz`

#### Files touched
- `.github/workflows/proton-bleeding-edge-nightly.yml`

---

### [fix] — sync-scripts rebase conflict fix (2026-03-11)
**Commit:** `76645fe`

#### What changed
- `git pull --rebase -X ours` also applied to the sync-scripts job commit step (same race condition as release job — if two concurrent runs both detect upstream script changes, the second would conflict)

#### Files touched
- `.github/workflows/proton-bleeding-edge-nightly.yml`

---

### [feat] — Auto-update README with latest releases after every build (2026-03-11)
**Commits:** `35fb31a` (proton README), `6142553` (all-in-one README + combined section)

#### What changed

**README.md:**
- Replaced single `## 🍷 Latest Proton Bleeding-Edge Release` section with a combined `## 🌙 Latest Nightly Releases` section containing two sub-sections:
  - `### 📦 All-in-One Emulation Nightly` — updated by all-in-one workflow; markers: `<!-- NIGHTLY-LATEST-START/END -->`
  - `### 🍷 Proton Bleeding-Edge ARM64EC` — updated by proton workflow; markers: `<!-- PROTON-LATEST-START/END -->`

**proton-bleeding-edge-nightly.yml (Create GitHub Release step):**
- Python block also rewrites `README.md` between `PROTON-LATEST-START/END` markers after writing release notes
- Table shows: release link, wine commit link + message, date, asset download link
- Commit step stages `README.md` alongside `proton-latest.json`

**new-All-in-one-nightly+zips-latest-stable.yml (create-release job):**
- New `Update README with latest nightly` step after `Create GitHub Release`
- Python block rewrites `README.md` between `NIGHTLY-LATEST-START/END` markers
- Table shows: release link, FEX commit+version, VKD3D std+ARM64EC commits, DXVK std+ARM64EC commits, Box64 repo links, asset download link
- Commits and pushes `README.md` with `git pull --rebase -X ours`

#### Files touched
- `README.md`
- `.github/workflows/proton-bleeding-edge-nightly.yml`
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`

---

## Session — 2026-03-16

### [feat] — Kimchi Driver Mirror workflow (2026-03-16)
**Commit:** `0d9bd05`

#### What changed

**New file: `.github/workflows/kimchi-driver-mirror.yml`**
- Mirrors all releases from K11MCH1/AdrenoToolsDrivers (154 releases, 200 assets, ~938 MB total)
- Runs daily at 06:00 UTC + `workflow_dispatch` (optional `force_full_sync` boolean input)
- **Storage:** actual `.zip` files uploaded as assets on a persistent `kimchi-drivers` release (pre-release, never deleted); filenames prefixed with sanitized tag name to avoid collisions (e.g. `v26.0.0-rc08_Turnip_v26.0.0_R8.zip`)
- **Index:** `kimchi/drivers.json` committed to repo — contains `updated_at`, `source`, `mirror_release`, `total_releases`, `total_assets`, and per-release asset list with `name`, `mirror_name`, `size`, `original_url`, `mirror_url`, `published_at`
- **Incremental:** skips assets already present in the mirror release (by name) or already in `drivers.json` with a `mirror_url`; `force_full_sync` re-downloads everything
- `timeout-minutes: 360` — initial full sync can take up to 6h
- `git pull --rebase -X ours` on drivers.json commit step

#### Files touched
- `.github/workflows/kimchi-driver-mirror.yml` (new)
- `kimchi/drivers.json` (created on first run)

---

## Session — 2026-03-18

## Session — 2026-03-21

### [feat] — MTR manual_entries.json + v3.0.0 drivers (2026-03-21)
**Commit:** TBD

#### What changed
- Created `mtr/manual_entries.json` — static list of manually added drivers that survive workflow reruns; any entry whose filename isn't already in the source repo sync is appended to `mtr/drivers.json` after each run
- Added new "Merge manual entries" step to `mtr-driver-mirror.yml` — runs between "Download and mirror" and "Write root mtr_drivers.json"; reads `mtr/manual_entries.json` and appends missing entries by name
- Updated commit step to also stage `mtr/manual_entries.json`
- Added `Turnip_MTR_v3.0.0-b_Axxx.zip` and `Turnip_MTR_v3.0.0-p_Axxx.zip` (manually uploaded to mtr-drivers release, not yet in maxjivi05's repo) to all three JSON files: `mtr/drivers.json`, `mtr_drivers.json`, `drivers.json`

#### Files touched
- `mtr/manual_entries.json` (new)
- `mtr/drivers.json` (total_assets 33→35, two v3.0.0 entries added)
- `mtr_drivers.json` (two v3.0.0 entries added)
- `drivers.json` (two v3.0.0 entries inserted after v2.0.0-p)
- `.github/workflows/mtr-driver-mirror.yml` (new "Merge manual entries" step + manual_entries.json staged in commit)

---

### [feat] — Add MTR v3.2.0-b and v3.2.0-p to JSON tracking (2026-03-25)
**Commit:** `9d2da14`

#### What changed
- Added `Turnip_MTR_v3.2.0-b_Axxx` and `Turnip_MTR_v3.2.0-p_Axxx` entries to `mtr/drivers.json` (total_assets 35→37)
- Added matching `GpuDriver` entries to `mtr_drivers.json`
- Both entries point to mirror URLs under the `mtr-drivers` release tag

#### Files touched
- `mtr/drivers.json`
- `mtr_drivers.json`

---

### [fix] — Replace DXVK-NVAPI with Turnip in upstream status table (2026-03-18)
**Commit:** `e238ebb`

#### What changed
- Removed `jp7677/dxvk-nvapi` from `REPOS` array in `create-release` job status table
- Replaced with `The412Banner/Banners-Turnip`
- `NAMES` array updated: `"DXVK-NVAPI"` → `"Turnip (Banners)"`
- Upstream status table now shows Turnip commit status instead of the removed NVAPI project

#### Files touched
- `.github/workflows/new-All-in-one-nightly+zips-latest-stable.yml`

## 2026-09-06 — VKD3D-Proton relax_wave_size experimental build (artifact-only)

**Why:** Serious Sam Shatterverse (UE 5.5.4, SM6-only, `[WaveSize(32)]` compute shaders) dies at frame 1 on Adreno 750 / Turnip (subgroup range 64..128): vkd3d `d3d12_device_validate_shader_meta` rejects 39 compute PSOs (`Required WaveSize range [32, 32], but supported range is [64, 128]`) → UE `80070057` → RenderThread null-PSO AV.

**What:** new workflow `.github/workflows/vkd3d-wave-relax.yml` (workflow_dispatch, artifact-only, no release, no catalog change) builds upstream vkd3d-proton pinned at `d01924b6` (same commit as the installed `3.0.1-d01924b6-1` profile) with `patches/vkd3d-proton-relax-wave-size.patch`:
- new `VKD3D_CONFIG` flags `relax_wave_size` / `no_relax_wave_size` (`config_flag_decl.h`, `reserved0` 26→24 to keep the 96-bit STATIC_ASSERT)
- `device.c`: relax flag is DEFAULT-ON (set in `vkd3d_instance_deduce_config_flags_from_environment` unless `no_relax_wave_size`); `d3d12_device_validate_shader_meta` no longer returns false when the required range misses the device range — one-time WARN instead
- `state.c`: `vkd3d_setup_shader_stage` clamps `requiredSubgroupSize` into `[minSubgroupSize, maxSubgroupSize]` (32 → 64 on Adreno) so Vulkan never sees an illegal size
- dxil-spirv untouched (verified: WaveGetLaneCount lowers to dynamic `BuiltInSubgroupSize`, no `OpExecutionMode SubgroupSize` emitted)
- x64 + x86 only (game is x64; syswow64 for profile parity). profile versionName `3.1.0-wave64-relax` / versionCode 1 → installs as `3.1.0-wave64-relax-1`.
- Patch does NOT apply to upstream master (`35bdee14`, uses `d3d12_caps.options1.WaveLaneCount*` + ALLOW_WAVE32 machinery) — re-derive if ever rebased.

**Caveat:** shaders assuming exactly 32 lanes for wave intrinsics may mis-render; this is a compat hack, not a fix. Device-proof pending.
- ✅ BUILD GREEN 2026-09-06 23:44 — run 34080400659 (headSha `c9a1bf89`), artifact `vkd3d-wave64-relax`. `VKD3D-Proton-3.1.0-wave64-relax.wcp` sha256 `935fc1e48e3ba92a6d22292d5028c3aa2adeff5ea6ecfb7c28285d3db52249d8` (4.68 MB; profile.json + system32 x64 + syswow64 i386, byte sizes identical to the stock d01924b6 profile; `relax_wave_size` string present in both d3d12core.dll). Staged to device `/sdcard/Download/VKD3D-Proton-3.1.0-wave64-relax.wcp`. NOT installed into any container; device-proof pending.
