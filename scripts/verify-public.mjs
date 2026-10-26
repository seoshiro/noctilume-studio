import {readFile} from 'node:fs/promises';import {createHash} from 'node:crypto';
const base=new URL(process.argv[2]);if(base.protocol!=='https:')throw Error('Use the actual HTTPS public site URL.');
const local=JSON.parse(await readFile('dist/release.json','utf8'));
if(!local.complete)throw Error('Incomplete local build cannot verify a release.');
const remote=await fetch(new URL('release.json',base),{cache:'no-store'}).then(r=>{if(!r.ok)throw Error('Public release manifest '+r.status);return r.json()});
if(remote.commit!==local.commit)throw Error('Public commit differs from local release: '+remote.commit);
for(const [path,sha] of Object.entries(local.files)){const response=await fetch(new URL(path,base),{cache:'no-store'});if(!response.ok)throw Error(path+' HTTP '+response.status);const got=createHash('sha256').update(new Uint8Array(await response.arrayBuffer())).digest('hex');if(got!==sha)throw Error(path+' hash mismatch');console.log('PASS',path,sha)}
console.log('PUBLIC_RELEASE_VERIFIED',remote.commit);
