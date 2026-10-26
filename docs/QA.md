# Build and QA - working report

2026-10-26. Story: discover object  configure light  preserve or share  play silent study  understand fictional concept.

| Check | Result | Evidence |
| --- | --- | --- |
| Settings validation / URL priority / persistence parsing / corrupt storage / link roundtrip | PASS | node --test, 5 tests, 0 failures |
| Native Blender 5.2 launch | BLOCKED | installed signed executable exits C0E90002 before Python; confirmed launcher did not expose a window after approval |
| Initial Vite build | BLOCKED | Application Control blocked native Rollup module; no policy changes made |
| WASM build replacement | PASS for incomplete local preview | official esbuild-wasm: main 236 KB, lazy scene 582 KB before gzip; TypeScript passed |
| Mandatory cloud media | CREATED, TRANSFER PENDING | parent generated and visually checked image, silent video and poster; local Library helper download failed |
| Desktop browser, 1519?730 | PARTIAL PASS | real Chrome first slice inspected; model/media absent so visual final gate stays open |
| Mobile browser, 390?844 requested viewport | PARTIAL PASS | 375 CSS px layout width equals scrollWidth, no horizontal overflow; no auto-loaded canvas; final assets absent |
| Keyboard studio / share | PASS | brightness Home+ArrowRight  1%, temperature End  4000K, Graphite, copied URL b=1/k=4000/f=graphite |
| Persistence / URL / locale / reset | PASS | reload retained 1/4000/Graphite; EN deep link 37/2300/Champagne overrode storage; Reset restored 68/2700/Champagne and removed config params |
| Model failure | PARTIAL PASS | missing GLB leads to retry; missing poster now has intentional text fallback. Actual context-loss recovery still needs real model |
| Motion / video / touch hardware | NOT TESTED | no real GLB/video locally yet; pointer mobile controls still to verify |
| Independent audit | PENDING | parent coordinates |
| Public deployment and actual asset hashes | NOT DEPLOYED | mandatory media/Blender/audit gates |

Known limitation: static poster simulates brightness/temperature approximately; finish changes require 3D. localStorage refusal preserves working in-memory controls and share URL. No backend or accounts required.
