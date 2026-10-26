# Verified public release

## Current: mobile studio UX patch

- Site: https://seoshiro.github.io/noctilume-studio/
- Published source: `e2f2bf59eaae1c119182d0b5c2002746c61279d8`
- Successful build/deploy: https://github.com/seoshiro/noctilume-studio/actions/runs/40376475121
- Remote main was checked at that source before dispatch; `release.json` reports the same commit and `complete: true`.
- `node scripts/verify-public.mjs https://seoshiro.github.io/noctilume-studio/` passed all 13 actual public SHA-256 comparisons against the local build of the exact accepted source.
- `app/main.js`: `90e52f5cc0df419bc8b869b7ee585b536d83b101c9b2cf20751bff36241261ca`
- `app/main.css`: `01839d676838307532c45d1d82566eff712ec41efb62e07da0b4d47853526541`
- All Blender source/model and generated media hashes remain unchanged from the initial release below.

Independent review ACCEPT; 7/7 Node tests, TypeScript and full build passed. Live mobile configuration, actual GLB, rotation/Resume, persistence, normalized share URL, Reset, landscape layout and video ended/restart/offscreen pause passed. Normal live console errors/warnings were empty. Detailed reproductions, recovery checks and honest hardware/emulation limits are in [UX-PATCH.md](UX-PATCH.md).

Only final release documentation is committed after this deployment; it does not change the published web files. No additional purchases, credentials, generation, or Windows policy changes were required.

## Initial release (superseded)

- Site: https://seoshiro.github.io/noctilume-studio/
- Published source: `7876fc99eb35dec91758124eb8c9c72629a08c9c`
- Successful build/deploy: https://github.com/seoshiro/noctilume-studio/actions/runs/40363214791
- `release.json` reports the same commit and `complete: true`.
- `node scripts/verify-public.mjs https://seoshiro.github.io/noctilume-studio/` passed all 13 live file SHA-256 comparisons against the local build of that exact source.

Representative live hashes:

| File | SHA-256 |
| --- | --- |
| app/main.js | 9acfe5f5d03fe47e8cc6403df1ac70abcbf72554a0e231caa24fed9ffc9de09e |
| assets/eclipse.glb | c427b188cf84a79bb1eea9dfc188cf81bacd0275feb15b48629ce4804cb87d1f |
| assets/editorial-room.webp | c3f3e984ed8f47f40c4ef14c0a4f728b2d844cbdc22a63db0fb17ac01f830ed5 |
| assets/light-study.mp4 | 56488ef4ec5c27e5b23f23a58ee1fa311920378d6c7304166f594778d1e97cf7 |
| index.html | be5f1ecec4341955312e2a5b25dcd5e9538b64a073d0bb03839a1fad972fdc3e |

Live browser smoke confirmed actual GLB, explicit silent video playback to 10 seconds, zero brightness persistence, copied share link and Reset. Independent final visual audit accepted the exact main.js hash above, at desktop and mobile sizes. No purchase, new credential or Windows security-policy change was required.

Limits: true device touch hardware, forced WebGL context loss and runtime emulation of reduced-motion/save-data were not tested through the available browser API. Their code paths were reviewed; real missing-GLB recovery was exercised successfully. Static view simulates light approximately and does not change finish. The lamp remains an explicitly fictional concept.

This documentation records the published release; later documentation-only commits do not change the deployed web files.
