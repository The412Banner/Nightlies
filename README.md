<p align="center">
  <img src="/img.png" width="500" title="The412Banner Nightly Repo">
</p>

<h1 align="center">The412Banner Nightly Repo for Winlator & Emulation</h1>

<p align="center">
  <a href="https://github.com/The412Banner/Nightlies/actions/workflows/new-All-in-one-nightly+zips-latest-stable.yml"><img src="https://github.com/The412Banner/Nightlies/actions/workflows/new-All-in-one-nightly+zips-latest-stable.yml/badge.svg" alt="All-in-One Nightly"></a>
</p>

Welcome to my nightly repository for Windows-emulation components on Android. This repository automatically builds and packages the latest upstream commits from projects like DXVK, VKD3D-Proton, Box64, and FEXCore into ready-to-use `.wcp` (Winlator Component Package) files.

> **Note:** Nightly workflows run automatically and update every hour, and a full daily build is processed at **03:30 AM EST / 08:30 AM UTC**.

A special thanks to [Arihany](https://github.com/Arihany/WinlatorWCPHub), StevenMXZ, Pypetto-Crypto, Max, and Nick417. Much of the structure here was inspired by their fantastic work in the emulation community. 

---

## 📇 Component Catalog (JSON Index)

A single JSON index of every component published here — point any compatible Winlator-family client at the raw URL below to auto-discover available `.wcp` / `.wcp.xz` builds.

| | |
| :--- | :--- |
| **Repo** | [The412Banner/winlator-contents](https://github.com/The412Banner/winlator-contents) |
| **Raw URL** | `https://raw.githubusercontent.com/The412Banner/winlator-contents/main/contents.json` |

---

## 📦 Releases — Stable & Nightly

> 🟢 **Stable** — curated archives of versioned `.wcp` builds on **fixed, never-changing tags** (the hourly nightlies otherwise bury these on the back pages of [Releases](https://github.com/The412Banner/Nightlies/releases)).
> 🌙 **Nightly** — freshest upstream commit, auto-built hourly with a full daily build at **03:30 AM EST / 08:30 AM UTC**. *Not always stable — use at your own risk.* Every component ships together in the rolling [`nightly-latest`](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) release.

| Component | 🟢 Stable Archive | 🌙 Nightly |
| :--- | :--- | :---: |
| **DXVK (GPLAsync)** | [Standard](https://github.com/The412Banner/Nightlies/releases/tag/Dxvk-gplasync) · [ARM64EC](https://github.com/The412Banner/Nightlies/releases/tag/Dxvk-gplasync-arm64ec) | [Latest](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) |
| **DXVK (BinSem · GPLAsync)** | [Standard](https://github.com/The412Banner/Nightlies/releases/tag/Dxvk-binsem-gplasync) · [ARM64EC](https://github.com/The412Banner/Nightlies/releases/tag/Dxvk-binsem-gplasync-arm64ec) | [Latest](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) |
| **DXVK-Sarek** *(older GPUs / GL fallback)* | [Sarek](https://github.com/The412Banner/Nightlies/releases/tag/DXVK-SAREK) · [Async](https://github.com/The412Banner/Nightlies/releases/tag/DXVK-SAREK-ASYNC) · [Async ARM64EC](https://github.com/The412Banner/Nightlies/releases/tag/DXVK-SAREK-ASYNC-ARM64EC) | — |
| **VKD3D-Proton (D3D12)** | [Standard](https://github.com/The412Banner/Nightlies/releases/tag/Vkd3d-proton) · [ARM64EC](https://github.com/The412Banner/Nightlies/releases/tag/VKD3D-PROTON-ARM) | [Latest](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) |
| **D7VK (DDraw/D3D7)** | — | [Latest](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) |
| **Box64** | [glibc](https://github.com/The412Banner/Nightlies/releases/tag/Box64) · [Bionic](https://github.com/The412Banner/Nightlies/releases/tag/Box64-Bionic) · [Hybrid](https://github.com/The412Banner/Nightlies/releases/tag/Box64-Hybrid) | [Latest](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) |
| **WOWBox64** | [Archive](https://github.com/The412Banner/Nightlies/releases/tag/Wowbox64) | [Latest](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) |
| **FEXCore** | [Archive](https://github.com/The412Banner/Nightlies/releases/tag/FexCore) · [PPA-flavor](https://github.com/The412Banner/Nightlies/releases/tag/fexcore-ppa-FEX-2608-e869aa644) | [Latest](https://github.com/The412Banner/Nightlies/releases/tag/nightly-latest) |
| **Proton / Wine** | [Proton 11](https://github.com/The412Banner/Nightlies/releases/tag/Proton-11) · [Prefix pack (P10-4)](https://github.com/The412Banner/Nightlies/releases/tag/P10-4-prefixpack) | — |

<details>
<summary>🔧 <b>Exact nightly commits / versions</b> (current all-in-one build)</summary>

<!-- NIGHTLY-LATEST-START -->
| | |
| :--- | :--- |
| **Release** | [🔗 nightly-20260910-123809](https://github.com/The412Banner/Nightlies/releases/tag/nightly-20260910-123809) |
| **FEXCore** | [`e431bfe0f`](https://github.com/FEX-Emu/FEX/commit/e431bfe0f) — FEX-2609+14-Nightly-e431bfe0f |
| **VKD3D-Proton (Std)** | [`0bd10357`](https://github.com/HansKristian-Work/vkd3d-proton/commit/0bd10357) |
| **VKD3D-Proton (ARM64EC)** | [`0bd10357`](https://github.com/HansKristian-Work/vkd3d-proton/commit/0bd10357) |
| **DXVK (GPLAsync)** | [`8759acd1`](https://github.com/doitsujin/dxvk/commit/8759acd1) |
| **DXVK (ARM64EC)** | [`8759acd1`](https://github.com/doitsujin/dxvk/commit/8759acd1) |
| **DXVK BinSem (GPLAsync)** | [`8759acd1`](https://github.com/doitsujin/dxvk/commit/8759acd1) — set `DXVK_DISABLE_TIMELINE_SEMAPHORES=1` to activate |
| **DXVK BinSem (ARM64EC)** | [`8759acd1`](https://github.com/doitsujin/dxvk/commit/8759acd1) — set `DXVK_DISABLE_TIMELINE_SEMAPHORES=1` to activate |
| **D7VK (DDraw/D3D7)** | [`11764daca`](https://github.com/WinterSnowfall/d7vk/commit/11764daca) — DDraw Wrapper slot; `.tzst` = bundled-asset refresh |
| **Box64** | [ptitSeb/box64](https://github.com/ptitSeb/box64/commits/main) + [Pipetto/box64](https://github.com/Pipetto-crypto/box64/commits/main) |
| **Turnip** | [v26.3.0-20260910-r2](https://github.com/The412Banner/Banners-Turnip/releases/tag/v26.3.0-20260910-r2) — Turnip v26.3.0-20260910-r2 |
| **Files** | [`.wcp` and `.zip` — scroll to Assets](https://github.com/The412Banner/Nightlies/releases/tag/nightly-20260910-123809) |
<!-- NIGHTLY-LATEST-END -->

</details>

<details>
<summary>📁 <b>Other permanent releases</b> (Steam, driver mirrors, backups)</summary>
<br>
<ul>
  <li><b>Steam:</b> <a href="https://github.com/The412Banner/Nightlies/releases/tag/Steam-clients">Steam-clients</a> · <a href="https://github.com/The412Banner/Nightlies/releases/tag/Steam-agent">Steam-agent</a></li>
  <li><b>Driver mirrors:</b> <a href="https://github.com/The412Banner/Nightlies/releases/tag/stevenmxz-drivers">StevenMXZ</a> · <a href="https://github.com/The412Banner/Nightlies/releases/tag/white-drivers">whitebelyash</a> · <a href="https://github.com/The412Banner/Nightlies/releases/tag/mtr-drivers">Mr. Purple</a> · <a href="https://github.com/The412Banner/Nightlies/releases/tag/kimchi-drivers">Kimchi</a></li>
  <li><b>Misc:</b> <a href="https://github.com/The412Banner/Nightlies/releases/tag/Personal-packs">Personal-packs</a> · <a href="https://github.com/The412Banner/Nightlies/releases/tag/Backup-Winlator-Builds">Backup Winlator builds</a> · <a href="https://github.com/The412Banner/Nightlies/releases/tag/Star-compose-test">Star-compose test</a></li>
</ul>
</details>

---

## 📱 My Other Projects

- [**BannerHub**](https://github.com/The412Banner/bannerhub) — A fully patched GameHub 5.3.5 ReVanced build with a built-in Component Manager, BCI launcher button, online component downloader, performance toggles, and more.
- [**Banners Component Injector**](https://github.com/The412Banner/BannersComponentInjector) — A no-root Android app to browse, download, and seamlessly inject these WCP components directly into GameHub Lite and other Winlator variants.
- [**Banners No-PC Retroid Overclock**](https://github.com/The412Banner/Banners-No-PC-Retroid-Overclock) — Rooting and overclocking tools for Retroid Snapdragon 865 devices.
- [**Ayaneo PocketFit Tools**](https://github.com/The412Banner/Ayaneo-PocketFit-tools) — A helper repository for rooting your Ayaneo Pocket Fit.

---

## 🎮 Recommended Emulators & Builds

*For a comprehensive and up-to-date ranking of emulators, check out [this emulation guide](https://the412banner.github.io/emulator-ranking/).*

*Also for Turnip driver releases [Here](https://www.reddit.com/r/OdinHandheld/s/oAifHPSTlc) *


### Bionic Builds

| Build | Description |
|:---:|---|
| [**Bannerlator**](https://github.com/The412Banner/Bannerlator/releases) | The412Banner's own Winlator build — fully rebuilt Jetpack Compose / Material 3 UI, built-in Steam store (JavaSteam) with Goldberg auto-patching, in-game ReShade, themeable accents, and a file manager with favorites. |
| [**Winlator-CMod**](https://github.com/coffincolors/winlator/releases) | Baseline Bionic build with excellent controller support. |
| [**Winlator-Ludashi**](https://github.com/StevenMXZ/Winlator-Ludashi/releases) | Keeps up with the latest upstream code while remaining close to vanilla. Great performance. |
| [**GameNative**](https://github.com/utkarshdalal/GameNative/releases) | Supports both glibc and bionic, featuring a sleek UI and Steam, Epic, GOG, and Amazon Games integration. |
| [**Unofficial GameNative Performance**](https://github.com/maxjivi05/GameNative-Performance/releases) | MaxesTechReview fork supporting glibc/bionic, reworked UI with storefront integrations, and additional performance improvements. |
| [**Winlator-REF4IK**](https://github.com/REF4IK/winlator-ref4ik-/releases) | Enhanced performance monitoring and reworked input controls with numerous QoL improvements. |

### GameHub Builds

| Build | Description |
|:---:|---|
| [**Official GameHub**](https://gamehub.xiaoji.com/) | The original GameHub released by Gamesir. |
| [**Official GameHub Lite**](https://github.com/Producdevity/gamehub-lite/releases) | A community-maintained modified version of GameHub for educational purposes. |
| [**Unofficial GameHub Lite**](https://github.com/ItzDFPlayer/gamehub-lite) | A fork of the Official GameHub Lite updated to run on the GameHub v5.3.5 build with v5.3.3 features. |
| [**GameHub Brasil**](https://github.com/winlatorbrasil/gamehub-brasil/releases) | A Brazilian fork of GameHub, adapted and maintained with a focus on performance, compatibility, and accessibility. |
| [**BannerHub**](https://github.com/The412Banner/bannerhub/releases) | A patched GameHub 5.3.5 ReVanced build featuring a Component Manager, online component downloader, BCI launcher, and performance toggles. |

---

## ⚙️ Additional Packages & Drivers

### 🔥 Adreno GPU Drivers

| Source | Description |
|:---:|---|
| [**StevenMXZ**](https://github.com/StevenMXZ/freedreno_turnip-CI/releases) | Mesa Turnip drivers (ELITE) |
| [**whitebelyash**](https://github.com/whitebelyash/freedreno_turnip-CI/releases) | Mesa Turnip drivers (ELITE) |
| [**K11MCH1**](https://github.com/K11MCH1/AdrenoToolsDrivers/releases) | Qualcomm proprietary drivers + Mesa Turnip drivers |
| [**GameNative**](https://gamenative.app/drivers/) | Qualcomm proprietary drivers + Mesa Turnip drivers |
| [**zoerakk**](https://github.com/zoerakk/qualcomm-adreno-driver/releases) | Qualcomm proprietary drivers (ELITE) |
| [**Mr. Purple**](https://github.com/MrPurple666/purple-turnip/releases) | Turnip Drivers - Secret Console |

<details>
  <summary>💡 <b>Quick Info: Driver Types</b></summary>
  <br> 
  <ul>
    <li><b>Qualcomm Proprietary:</b> Extracted from the official Adreno driver of a recent device. Emulation may show reduced performance or rendering glitches.</li>
    <li><b>Mesa Turnip:</b> Open-source Mesa driver with broader Vulkan support and emulator-friendly behavior. Often much more stable across devices.</li>
  </ul>
</details>

### 📦 Windows Runtime Packages

| Type | Link |
|---|---|
| **Visual C++ 2015–2022** | [x64](https://aka.ms/vs/17/release/vc_redist.x64.exe) \| [x86](https://aka.ms/vs/17/release/vc_redist.x86.exe) \| [ARM64](https://aka.ms/vs/17/release/vc_redist.arm64.exe) |
| **Wine-Mono** | [.NET runtime for Wine](https://dl.winehq.org/wine/wine-mono/) *(Install only if the built-in tool fails)* |
| **Wine-Gecko** | [HTML engine for Wine](https://dl.winehq.org/wine/wine-gecko/) *(Install only if the built-in tool fails)* |
| **DirectX (June 2010)** | [Legacy DirectX Runtime](https://download.microsoft.com/download/8/4/a/84a35bf1-dafe-4ae8-82af-ad2ae20b6b14/directx_Jun2010_redist.exe) *(Install only if missing Legacy DLLs)* |
| **PhysX Legacy** | [Nvidia PhysX Legacy](https://www.nvidia.com/content/DriverDownload-March2009/confirmation.php?url=/Windows/9.13.0604/PhysX-9.13.0604-SystemSoftware-Legacy.msi&lang=us&type=Other) *(Install only if an old game requests it)* |

> **Tip:** Install only the minimum necessary runtimes. If you need older VC++ redistributables, try an [AIO package here](https://www.techpowerup.com/download/visual-c-redistributable-runtime-package-all-in-one/).

---

## 💬 Community & Support (Discord)

Join the community to discuss emulation, get support, and share findings:

- [**The412Banner's Discord**](https://discord.gg/n8S4G2WZQ4) *(My personal channel)*
- [**Official GameHub Lite (Emuready)**](https://discord.gg/emuready-1380826875961540648)
- [**MaxesTechReview**](https://discord.gg/9ySMdArY4s)
- [**Emugear International**](https://discord.gg/94PzWBsHHh)
- [**Emucore (Kimchi's Discord)**](https://discord.gg/ZmXUZybNpU)
- [**Ryan Retro**](https://discord.gg/9n6VUzv424)

---

## 🏆 Credits & Licenses

Third-party components used for packaging retain their original upstream licenses. WCP packages redistribute unmodified (or minimally patched) binaries. All copyrights and credits belong to the original authors:

- **FEX:** [FEX-Emu](https://github.com/FEX-Emu)
- **Box64:** [ptitSeb](https://github.com/ptitSeb)
- **DXVK:** [Philip Rebohle (doitsujin)](https://github.com/doitsujin)
- **DXVK-Sarek:** [pythonlover02](https://github.com/pythonlover02)
- **DXVK-GPLAsync Patch:** [Ph42oN](https://gitlab.com/Ph42oN)
- **DXVK Binary-Semaphores Patch:** [leegao](https://github.com/leegao)
- **VKD3D-Proton:** [Hans-Kristian Arntzen](https://github.com/HansKristian-Work)
- **Freedreno Turnip Driver:** [Mesa3D](https://mesa3d.org/)

*Thank you to Max and Nick for their help with GitHub Actions workflows!*

---
<sub>☕ [Support on Ko-fi](https://ko-fi.com/the412banner)</sub>
