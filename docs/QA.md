# Build and QA report

Latest accepted UX patch and public verification: [UX-PATCH.md](UX-PATCH.md), deployed source `e2f2bf59eaae1c119182d0b5c2002746c61279d8`, Pages run `40376475121`. It adds compact mobile preview/controls, numeric normalization and media retry recovery, with 7/7 tests and all 13 live hashes matched. The historical initial-release checks below remain as provenance; the newer report supersedes their runtime-test limitations where explicitly tested.

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
| Public deployment and hashes | PASS | Pages workflow 40363214791 succeeded for release 7876fc99eb35dec91758124eb8c9c72629a08c9c; all 13 live files matched local SHA-256 including HTML/JS/CSS/GLB/image/video |

The original GLB remains unmodified. Cycles procedural brushing is render-only; the web renderer uses texture-free PBR, with anisotropy disabled for compatibility. Colour and brightness are visual simulations, not measured photometry. Static mode does not change finish. No backend, analytics, sales or accounts.

Live smoke: real 3D loaded; explicit silent video completed at 10.0 seconds with readyState 4/error null/muted true; brightness 0 survived reload and Share link; Reset restored 68 percent. Independent final visual recheck ACCEPT for identical main.js hash 9acfe5f5d03fe47e8cc6403df1ac70abcbf72554a0e231caa24fed9ffc9de09e. See RELEASE.md.
