DXVK **3.2** — built from the upstream stable tag (`1011dd97`), not from master.

Upstream released 3.2 on 26 November 2026.

## Which file do I want?

| File | Use it for |
|---|---|
| `dxvk-3.2.wcp` | Plain upstream DXVK. Start here. |
| `dxvk-gplasync-3.2-1.wcp` | Async shader compilation (Ph42oN's GPLAsync). Fewer shader stutters, at the cost of occasional missing effects for a frame or two. |
| `dxvk-arm64ec-3.2.wcp` | The same as the plain build, compiled for ARM64EC containers. |
| `dxvk-gplasync-arm64ec-3.2-1.wcp` | GPLAsync, ARM64EC. |

Each one is also attached to its own flavour release, so existing links keep working.

**No BinSem build for 3.2.** The binary-semaphores patch no longer applies to the 3.2 code. The Turnip timeline-semaphore slowdown it worked around is fixed in Mesa itself (e984ef29, MR 44838). The 3.1.1 BinSem builds stay in [Dxvk-binsem-gplasync](https://github.com/The412Banner/Nightlies/releases/tag/Dxvk-binsem-gplasync) and [Dxvk-binsem-gplasync-arm64ec](https://github.com/The412Banner/Nightlies/releases/tag/Dxvk-binsem-gplasync-arm64ec).

## What's in upstream 3.2

- **Present timing:** with `VK_EXT_present_timing`, more even frame pacing when a game runs full screen at a refresh rate the display is not set to, and with the built-in limiter (`dxvk.maxFrameRate`). Upstream says it needs V-Sync on and either a recent Gamescope with `ENABLE_GAMESCOPE_WSI=1` or a Wayland Proton on a compositor with `commit-timing-v1`; XWayland and Windows do not support it.
- Rewritten Reflex support (fixes some games locked to 10 FPS with Reflex on).
- Better VRAM eviction on cards with little VRAM.
- Fewer stutters from D3D11 resource uploads, and better shader code in various cases.
- Updated `libdisplay-info` (fixes HDR detection on some devices, such as the ROG Ally).
- Fixes for stale images in VR, render-target clears on shared images, and stale DXGI back buffers with incremental presentation.
- D3D11 target-independent rasterization on drivers with `VK_NV_framebuffer_mixed_samples`.
- `VK_EXT_descriptor_heap` turned off on AMD's Windows driver.
- Game fixes: 7 Days to Die, Aniimo, Deadlock, Fallout New Vegas, Quantum Break, Ridiculous Space Battles, Sid Meier's Pirates!, Supreme Commander: Forged Alliance.

Full list: [upstream release notes](https://github.com/doitsujin/dxvk/releases/tag/v3.2).

## Notes on these builds

- The plain builds are upstream's own release binaries, repackaged.
- ARM64EC builds are compiled here from the same tag; upstream ships no ARM64EC binaries.
- GPLAsync has no per-release patch for 3.2 yet, so Ph42oN's current patch is applied to the stable tag.
- Every `.wcp` carries a `profile.json` whose version name matches its file name.
- Not tested on a device yet.

Upstream: Philip Rebohle (doitsujin/dxvk) · GPLAsync patch: Ph42oN
