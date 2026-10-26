// Explicit loopback-only fixtures; never copied to dist or enabled by the release build.
export function fixtureScript(name){
 const fixtures={
  'storage-denied':()=>{Object.defineProperty(window,'localStorage',{get(){throw new DOMException('Local QA storage refusal','SecurityError')}})},
  'storage-corrupt':()=>{const fake={getItem:()=>'{"brightness":null,"temperature":"","finish":"graphite"}',setItem(){}};Object.defineProperty(window,'localStorage',{value:fake})},
  'clipboard-denied':()=>{Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new DOMException('Local QA clipboard refusal','NotAllowedError'))}})},
  'reduced-motion':()=>{const original=window.matchMedia.bind(window);window.matchMedia=q=>{const m=original(q);if(q==='(prefers-reduced-motion: reduce)')Object.defineProperty(m,'matches',{value:true});return m}},
  'save-data':()=>{Object.defineProperty(navigator,'connection',{value:{saveData:true}})},
  'webgl-disabled':()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return String(type).includes('webgl')?null:original.call(this,type,...args)}},
  'context-loss':()=>{addEventListener('DOMContentLoaded',()=>{const b=document.createElement('button');b.textContent='QA: lose studio context';b.style.cssText='position:fixed;right:8px;bottom:8px;z-index:999;background:white;color:black;padding:12px';b.onclick=()=>{const c=document.querySelector('#studio canvas');if(c)c.getContext('webgl2')?.getExtension('WEBGL_lose_context')?.loseContext()};document.body.append(b)})}
 };
 return fixtures[name]?`<script>(${fixtures[name].toString()})()</script>`:'';
}
