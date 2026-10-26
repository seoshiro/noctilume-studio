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

Independent review and new public deployment: pending at this checkpoint. The previous verified release remains recorded in RELEASE.md.
