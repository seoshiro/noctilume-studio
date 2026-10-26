# NOCTILUME / Eclipse

An independent editorial portfolio for a **fictional sculptural lamp**. Primary language Russian; complete English interface. No product sales, reviews, manufacturing or certification claims.

The design explores a 350 mm champagne aluminium ring, continuous frosted inner light, 12° lean, narrow stem and weighted dark circular base. The intended geometry is authored in Blender, never substituted by browser primitives.

## Run

Node 22+ recommended. `npm ci --ignore-scripts`, `npm test`, `npm run typecheck`, `npm run build`, then `npm run preview` (loopback port 4173). Builds use official **esbuild-wasm**, requiring no native compiler executable. The release build refuses to run without the real Blender outputs and required cloud media. `npm run build:preview` permits an explicitly incomplete local review.

## Blender

`blender --background --factory-startup --python blender/create_noctilume.py`

Actual authoring and verification used an existing **cloud Blender 4.3.2**, after installed Windows Blender 5.2 was blocked by local Application Control. Windows security policy stayed unchanged. The final reproducible source is `blender/create_noctilume.py`; `blender/eclipse.py` is the earlier unexecuted prototype.

The source saves `noctilume-eclipse.blend`, GLB, manifest and three 1800 px PNG renders alongside itself. Optimized WebP copies were prepared for the site. Final repository names are `blender/eclipse.blend`, `public/assets/eclipse.glb`, `eclipse-poster.webp`, `eclipse-detail.webp` and `eclipse-transparent.webp`. The verified GLB has 17 meshes and 24,172 triangles; 499,660 bytes; Y-up/metres; height 0.4799 m; no cameras, lights or environment. No external Blender add-ons.

## Interaction

- Studio brightness, temperature and finish persist under localStorage key `noctilume:v1`; validated URL parameters `b`, `k`, `f` take priority.
- Share generates a configuration URL; a selectable field recovers from clipboard denial. Reset restores defaults and clears configuration parameters.
- Desktop hero loads 3D lazily. Small screens, save-data and reduced-motion start with the Blender poster and offer explicit 3D. Drag or left/right keys rotate; movement can be paused. Failed WebGL/model loading retains the poster and offers retry.
- Video is a silent 10-second abstract study with explicit play/pause and native controls. It pauses offscreen or when the page is hidden. It does not loop.
- Colour and light intensity are visual simulations, not measured photometry. Static mode does not simulate finish.

## Sources and rights

Original site and Blender source: MIT, see LICENSE. Generated project media and their provenance are listed in [docs/ASSETS.md](docs/ASSETS.md). React, Three.js and esbuild are MIT; TypeScript is Apache-2.0. Font families Cormorant Garamond and Manrope use the SIL Open Font License via Google Fonts. No analytics, account backend, paid API, trials or additional purchases.

## Release status

See [QA report](docs/QA.md) for actual checked results and outstanding gates. This repository is separate from all existing portfolio, LUCENT, GLACIER and Roblox projects.
