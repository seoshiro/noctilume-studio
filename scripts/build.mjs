import * as esbuild from 'esbuild-wasm';
import {mkdir,readFile,writeFile,cp,stat,lstat,rm,readdir} from 'node:fs/promises';
import {resolve,sep} from 'node:path';import {fileURLToPath} from 'node:url';import {createHash} from 'node:crypto';
const incomplete=process.argv.includes('--incomplete');
const required=['public/assets/eclipse.glb','public/assets/eclipse-poster.webp','public/assets/editorial-room.webp','public/assets/light-study.mp4','public/assets/light-study-poster.webp','blender/eclipse.blend'];
const missing=[];for(const f of required)try{if(!(await stat(f)).size)missing.push(f)}catch{missing.push(f)}
if(missing.length&&!incomplete)throw Error('Release media gate: missing '+missing.join(', '));
if(missing.length)console.warn('INCOMPLETE LOCAL PREVIEW — missing: '+missing.join(', '));
const projectRoot=fileURLToPath(new URL('..',import.meta.url));const buildDir=resolve(projectRoot,'dist');
if(resolve('.')!==resolve(projectRoot)||!buildDir.startsWith(resolve(projectRoot)+sep))throw Error('Run build from the project root.');
try{if((await lstat(buildDir)).isSymbolicLink())throw Error('Refusing linked build directory');await rm(buildDir,{recursive:true,force:true})}catch(e){if(e.code!=='ENOENT')throw e}
await mkdir(buildDir,{recursive:true});
await esbuild.build({entryPoints:['src/main.tsx'],bundle:true,minify:true,sourcemap:false,format:'esm',splitting:true,outdir:'dist/app',target:'es2022',jsx:'automatic',entryNames:'main',chunkNames:'[name]-[hash]',logLevel:'info'});
await cp('public','dist',{recursive:true});
const html=(await readFile('index.html','utf8')).replace('<script type="module" src="/src/main.tsx"></script>','<link rel="stylesheet" href="./app/main.css"/><script type="module" src="./app/main.js"></script>');
await writeFile('dist/index.html',html);await writeFile('dist/.nojekyll','');
async function hashes(dir,prefix=''){const result={};for(const item of await readdir(dir,{withFileTypes:true})){const key=prefix+item.name;if(item.isDirectory())Object.assign(result,await hashes(resolve(dir,item.name),key+'/'));else result[key]=createHash('sha256').update(await readFile(resolve(dir,item.name))).digest('hex')}return result}
await writeFile('dist/release.json',JSON.stringify({commit:process.env.GITHUB_SHA||'local-preview',complete:!missing.length,files:await hashes(buildDir)},null,2));esbuild.stop();
