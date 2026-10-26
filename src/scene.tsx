import {useEffect,useRef} from 'react';
import * as THREE from 'three';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {RoomEnvironment} from 'three/examples/jsm/environments/RoomEnvironment.js';
type Props={settings:{brightness:number;temperature:number;finish:string};hero:boolean;paused:boolean;en:boolean;onReady:()=>void;onError:()=>void};
export default function Scene(props:Props){
 const host=useRef<HTMLDivElement>(null);const latest=useRef(props);latest.current=props;
 useEffect(()=>{const el=host.current!;let renderer:THREE.WebGLRenderer;let disposed=false;let raf=0;let model:THREE.Group|undefined;let visible=true;let failed=false;let interacted=false;const fail=()=>{if(failed||disposed)return;failed=true;latest.current.onError()};
 try{renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:'low-power'});}catch{fail();return}
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.75));renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.2;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;el.appendChild(renderer.domElement);
 const canvas=renderer.domElement;canvas.tabIndex=0;canvas.setAttribute('role','img');canvas.setAttribute('aria-label',props.en?'Interactive Eclipse model. Drag or use left and right arrow keys.':'���ࠪ⨢��� ������ Eclipse. ���ﭨ� ��� �ᯮ���� ��५�� ����� � ��ࠢ�.');
 const scene=new THREE.Scene();const pmrem=new THREE.PMREMGenerator(renderer);const room=new RoomEnvironment();const env=pmrem.fromScene(room,.04);scene.environment=env.texture;room.dispose();pmrem.dispose();
 const camera=new THREE.PerspectiveCamera(35,1,.01,100);camera.position.set(3,1.7,6);const controls=new OrbitControls(camera,canvas);controls.target.set(0,0,0);controls.enablePan=false;controls.enableZoom=false;controls.minPolarAngle=Math.PI*.3;controls.maxPolarAngle=Math.PI*.58;controls.enableDamping=true;controls.autoRotate=false;
 const key=new THREE.DirectionalLight(0xffe4bd,5);key.position.set(-3,4,3);scene.add(key);const edge=new THREE.DirectionalLight(0xc5d7ff,3);edge.position.set(3,2,-2);scene.add(edge);scene.add(new THREE.AmbientLight(0xffffff,.4));
 const glow=new THREE.PointLight(0xffa94b,1.8,4,2);glow.position.set(0,0,1);scene.add(glow);
 const plane=new THREE.Mesh(new THREE.PlaneGeometry(40,40),new THREE.MeshStandardMaterial({color:0x171715,roughness:.85}));plane.rotation.x=-Math.PI/2;plane.position.y=-1.65;scene.add(plane);
 const timeout=setTimeout(fail,18000);
 new GLTFLoader().load('./assets/eclipse.glb',g=>{if(disposed){g.scene.traverse(o=>{if(o instanceof THREE.Mesh){o.geometry.dispose();(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>m.dispose())}});return}if(failed)return;clearTimeout(timeout);model=g.scene;const box=new THREE.Box3().setFromObject(model);const center=box.getCenter(new THREE.Vector3());const scale=3.1/box.getSize(new THREE.Vector3()).y;model.position.copy(center).multiplyScalar(-scale);model.scale.setScalar(scale);const group=new THREE.Group();group.add(model);model=group;scene.add(model);latest.current.onReady()},undefined,fail);
 const size=()=>{const w=el.clientWidth,h=el.clientHeight;if(!w||!h)return;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix()};const ro=new ResizeObserver(size);ro.observe(el);size();
 const io=new IntersectionObserver(es=>{visible=es[0].isIntersecting});io.observe(el);
 const pointer=()=>{interacted=true};canvas.addEventListener('pointerdown',pointer);
 const keyboard=(e:KeyboardEvent)=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();interacted=true;if(model)model.rotation.y+=(e.key==='ArrowLeft'?-.12:.12)}};canvas.addEventListener('keydown',keyboard);
 const lost=(e:Event)=>{e.preventDefault();fail()};canvas.addEventListener('webglcontextlost',lost);
 const clock=new THREE.Clock();let last='';
 function frame(){if(disposed)return;raf=requestAnimationFrame(frame);if(!visible||document.hidden||failed)return;const p=latest.current;const signature=JSON.stringify(p.settings);if(model&&signature!==last){last=signature;const warmth=(p.settings.temperature-2200)/1800;const color=new THREE.Color().setRGB(1,.46+warmth*.38,.15+warmth*.55);model.traverse(o=>{if(!(o instanceof THREE.Mesh))return;const mats=Array.isArray(o.material)?o.material:[o.material];mats.forEach((m:THREE.MeshStandardMaterial)=>{if(m.name.startsWith('Champagne')){m.color.set(p.settings.finish==='graphite'?0x292c2d:0xb49a70);m.roughness=p.settings.finish==='graphite'?.38:.28}if(m.name.startsWith('Diffuser')){m.color.copy(color).multiplyScalar(.35+p.settings.brightness/150);m.emissive.copy(color);m.emissiveIntensity=p.settings.brightness/35}})});glow.color.copy(color);glow.intensity=p.settings.brightness/30}
 const time=clock.getElapsedTime();if(model&&!p.paused&&!interacted){const rect=el.getBoundingClientRect();const scroll=p.hero?Math.max(-1,Math.min(1,-rect.top/innerHeight))*.35:0;model.rotation.y=Math.sin(time*.16)*.18+scroll}controls.update();renderer.render(scene,camera)}frame();
 return()=>{disposed=true;cancelAnimationFrame(raf);clearTimeout(timeout);ro.disconnect();io.disconnect();controls.dispose();canvas.removeEventListener('pointerdown',pointer);canvas.removeEventListener('keydown',keyboard);canvas.removeEventListener('webglcontextlost',lost);scene.traverse(o=>{if(o instanceof THREE.Mesh){o.geometry.dispose();(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>m.dispose())}});env.dispose();renderer.dispose();canvas.remove()}
 },[]);
 return <div className="three-scene" ref={host}/>;
}
