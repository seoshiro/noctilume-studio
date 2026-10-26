# Build and QA report

2026-10-26. Story: discover object -> configure light -> preserve/share -> play silent film -> understand the fictional concept.

| Check | Result | Evidence |
| --- | --- | --- |
| Settings tests | PASS | 5/5 Node tests: URL priority, bounds, corrupt/refused storage parsing, partial links and share roundtrip |
| TypeScript and full WASM build | PASS | Actual native scene and all required media present; esbuild-wasm, no native compiler binary |
| Runtime dependency audit | PASS | npm audit --omit=dev: 0 vulnerabilities |
| Actual Blender authoring | PASS | Existing cloud Blender 4.3.2: native reopen, GLB reimport, three renders verified; 17 meshes / 24,172 triangles / 499,660 byte GLB |
| Consumer media transfer | PASS | All nine files decoded from pinned public media-ingest commit e69e013d97c4b8bd898529c6d59073ca133d71b9; byte lengths and SHA-256 matched |
| Desktop/mobile independent browser audit | PASS | Real browser 1280x720, 390x844 and 320 px overflow check; actual GLB/video, RU/EN, persistence, URL priority, reset/share and sliders |
| History regression | PASS | Actual Chrome: 32% -> film -> studio -> 100% -> Back gave URL/UI 32%; Forward gave URL/UI 100% |
| Pause/manual/Resume | PASS independent runtime audit | Paused frame counter 35 -> 35, manual 36, Resume 86; no console errors in normal audit |
| Final metallic shading | FIXED, VISUALLY CHECKED | Custom dark studio reflection map, controlled exposure, isotropic PBR compatibility for texture-free GLB; bronze base visible without white clipping in fresh Chrome frame |
| Material story | FIXED | Copy, alt text and swatch describe actual champagne upper base with dark lower rim; original Blender detail render integrated |
| Controlled model failure and retry | PASS | Local dist GLB temporarily renamed: real HTTP 404 -> poster/retry, settings 68/2700 preserved -> file restored -> Retry -> actual model ready. Source asset unchanged |
| Reduced-motion/save-data | SOURCE REVIEW ONLY | Automatic model load skipped; static poster with explicit opt-in, reduced-motion defaults to paused. Media preference emulation unavailable through browser API |
| Actual WebGL context-loss event / physical touch hardware | NOT TESTED | Renderer creation and context-loss handlers reviewed; model-loader failure recovery exercised. Pointer controls tested in mobile viewport |
| Native Windows Blender 5.2 | BLOCKED, NOT REQUIRED FOR RELEASE | Installed executable exits C0E90002 before Python; existing cloud Blender provided actual native scene. No Windows protection changes |
| Public deployment and hashes | PENDING | Integration commit and Pages release followed by independent live byte verification |

The original GLB remains unmodified. Cycles procedural brushing is render-only; the web renderer uses texture-free PBR, with anisotropy disabled for compatibility. Colour and brightness are visual simulations, not measured photometry. Static mode does not change finish. No backend, analytics, sales or accounts.
