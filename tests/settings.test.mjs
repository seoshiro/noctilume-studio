import {test} from 'node:test';import assert from 'node:assert/strict';import {defaults,readSettings,validateSettings,shareURL} from '../src/settings.mjs';
test('URL settings override saved session',()=>assert.deepEqual(readSettings('?b=32&k=3200&f=graphite',{getItem:()=>JSON.stringify(defaults)}),{brightness:32,temperature:3200,finish:'graphite'}));
test('hostile/invalid bounds clamp safely',()=>assert.deepEqual(validateSettings({brightness:999,temperature:'bad',finish:'<script>'}),{brightness:100,temperature:2700,finish:'champagne'}));
test('corrupt or inaccessible storage recovers',()=>{assert.deepEqual(readSettings('',{getItem:()=>'{'}),defaults);assert.deepEqual(readSettings('',{getItem:()=>{throw Error()}}),defaults)});
test('partial links retain safe defaults',()=>assert.deepEqual(readSettings('?b=0'),{...defaults,brightness:0}));
test('shared configuration round trips including lamp off',()=>{const s={brightness:0,temperature:4000,finish:'graphite'};const u=new URL(shareURL('https://example.com/noctilume-studio/?lang=en',s));assert.equal(u.hash,'#studio');assert.equal(u.searchParams.get('lang'),'en');assert.deepEqual(readSettings(u.search),s)});
