# Mobile studio UX patch — 2026-10-26

Scope: configure the lamp while seeing the result, then preserve/share settings and continue through the film. Existing editorial design, Blender scene and generated media are retained.

## Confirmed defects and fixes

| Reproduction | Fix | Regression evidence |
| --- | --- | --- |
| At 390×844, focusing Temperature put the original 430 px preview at y=-315 px, hiding most of the lamp | Compact section-bounded sticky preview, tighter controls, separate tool row, no nested scroll container; short landscape uses two columns | Real Chrome viewport matrix below; temperature and finish remain accessible alongside the lamp |
| Empty URL values or null/array/boolean stored values became brightness 0 / 2200 K | Reject structurally invalid numeric values; preserve safe defaults | Two failing Node regressions captured before fix; 7/7 tests pass after fix |
| A URL temperature of 2351 K disagreed with the native slider's 100 K steps | Normalize validated temperature to the control's step | 2351 → 2400 K regression test |
| Actual video HTTP 404 left the custom control saying Pause; retry could be overwritten by a stale play promise | Error resets playback UI; retry reloads the media; request identity ignores stale promises; intentional AbortError is not a load failure; playing clears error | Real dist-only 404 → Play/error → restore file → one Play → readyState 4/error null → ended at 10 s |

## Verification

- Chrome viewport emulation: 320×568, 360×640, 390×844, 430×932, 768×1024, 740×360, 1280×720. No document horizontal overflow in the measured matrix. Studio layout overflow remains `visible`, without an inner scroll trap.
- At 320×568, sticky preview y=0..231; Temperature y=389..433. The rotate buttons and motion button have separate 44 px targets. At 740×360, preview and sliders occupy separate columns.
- Real Blender GLB used for brightness, temperature and both finishes; keyboard rotation/manual pause/explicit Resume exercised. Reduced-motion fixture paused rendering, manual input woke it, Resume advanced the frame counter.
- Back/Forward: 32% → film → studio → 100% → Back restored URL/UI 32%, Forward restored 100%.
- Runtime storage refusal preserves editing and a shareable URL. Corrupt-storage fixture restores 68% / 2700 K. Clipboard refusal provides a selectable complete link.
- Local WebGL-disabled fixture shows poster/retry and preserves 42% / 3300 K / Graphite. Actual `WEBGL_lose_context` extension event recovered through Retry with the same settings.
- Reduced-motion and save-data JavaScript fixtures skip automatic model loading. Explicit reduced-motion opt-in starts paused. These are controlled app-runtime simulations, not changes to browser/OS preferences.
- Explicit silent video playback reaches 10 seconds and returns to Play. Leaving an actively playing video paused it at 0.999 s.

Fixtures: `node scripts/serve.mjs --qa`, then `?fixture=storage-denied`, `storage-corrupt`, `clipboard-denied`, `reduced-motion`, `save-data`, `webgl-disabled`, or `context-loss`. The server binds loopback only; fixture scripts are never included in `dist` or Pages. Add `qa=1` for the existing render counter. Real missing-file tests temporarily rename only a generated dist asset and restore it afterwards.

Remaining limits: no physical Android touch/device testing, no emulated dynamic address-bar/notch hardware, and no OS-level reduced-motion/save-data preference emulation. CSS uses small viewport height and safe-area inset; pointer pan-y and relevant CSS paths are reviewed. The supplied private recording is not included in the repository.

## Accepted and published

- Independent final smoke: ACCEPT for source `e2f2bf59eaae1c119182d0b5c2002746c61279d8`, with matching main.js hash. Desktop 1280×720, mobile 390×844 and landscape 740×360: preview and active controls visible, no overflow; validation/share normalization, history, reset and video lifecycle passed. Reviewer did not force HTTP 404; that recovery is supported by the separate recorded local runtime check above.
- Pages run [40376475121](https://github.com/seoshiro/noctilume-studio/actions/runs/40376475121) completed successfully for that exact source.
- Public site: https://seoshiro.github.io/noctilume-studio/ . `verify-public.mjs` matched all 13 actual public files to the same local release build, including HTML, JS, CSS, GLB and every image/video.
- Live 390×844: actual GLB ready; preview y=0..291, Temperature y=435..479, finish group y=507..615. Graphite, temperature, brightness 0, manual rotation → Resume and Share worked with visible result. Live 740×360 retained the two-column layout.
- Live settings 0% / 4000 K / Graphite survived reload and a clean-URL return. Empty brightness and 2351 K produced 68% / 2400 K, and Share serialized those normalized values. Reset restored 68% / 2700 K / Champagne.
- Live video ended at 10 seconds, readyState 4, error null; restart followed by leaving the section paused at 0.995 seconds. Captured normal live console errors/warnings: none.

Native browser zoom could not be confirmed through the available viewport interface; no physical-device claim is made. The final documentation commit does not change deployed web bytes. See RELEASE.md for exact hashes and release identity.
