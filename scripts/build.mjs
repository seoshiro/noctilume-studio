import * as esbuild from 'esbuild-wasm';
import {mkdir,readFile,writeFile,cp,stat,rm} from 'node:fs/promises';
const incomplete=process.argv.includes('--incomplete');
const required=['public/assets/eclipse.glb','public/assets/eclipse-poster.webp','public/assets/editorial-room.webp','public/assets/light-study.mp4','public/assets/light-study-poster.webp','blender/eclipse.blend'];
const missing=[];for(const f of required)try{if(!(await stat(f)).size)missing.push(f)}catch{missing.push(f)}
if(missing.length&&!incomplete)throw Error('Release media gate: missing '+missing.join(', '));
if(missing.length)console.warn('INCOMPLETE LOCAL PREVIEW - missing: '+missing.join(', '));
await mkdir('dist',{recursive:true});
await esbuild.build({entryPoints:['src/main.tsx'],bundle:true,minify:true,sourcemap:false,format:'esm',splitting:true,outdir:'dist/app',target:'es2022',jsx:'automatic',entryNames:'main',chunkNames:'[name]-[hash]',logLevel:'info'});
await cp('public','dist',{recursive:true});
const html=(await readFile('index.html','utf8')).replace('<script type="module" src="/src/main.tsx"></script>','<link rel="stylesheet" href="./app/main.css"/><script type="module" src="./app/main.js"></script>');
await writeFile('dist/index.html',html);await writeFile('dist/.nojekyll','');esbuild.stop();
