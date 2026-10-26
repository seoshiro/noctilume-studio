"""NOCTILUME — Eclipse 35. Original procedural product model.
Reproduce: /usr/bin/blender -b --python create_noctilume.py
All dimensions meters. Blender 4.3.2; no external dependencies or addons.
"""
import bpy, math, os, json, hashlib, sys
from mathutils import Vector, Matrix
from math import sin, cos, pi
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for data in list(bpy.data.materials): bpy.data.materials.remove(data)
sc=bpy.context.scene
sc.unit_settings.system='METRIC'; sc.unit_settings.length_unit='METERS'
sc.render.engine='CYCLES'; sc.cycles.device='CPU'; sc.cycles.samples=256
sc.cycles.use_adaptive_sampling=True; sc.cycles.adaptive_threshold=.015; sc.cycles.sample_clamp_indirect=2.0; sc.cycles.sample_clamp_direct=8.0
sc.cycles.use_denoising=False
sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'
sc.render.resolution_percentage=100
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Medium High Contrast'
sc.view_settings.exposure=-.7
root=bpy.data.collections.new('NOCTILUME_Eclipse35'); sc.collection.children.link(root)
studio=bpy.data.collections.new('Studio_RENDER_ONLY'); sc.collection.children.link(studio)


def move(obj,collection=root):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    collection.objects.link(obj); return obj

def material(name, color, metallic=0.0, rough=.35, emission=None):
    m=bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metallic; p.inputs['Roughness'].default_value=rough
    if emission:
        p.inputs['Emission Color'].default_value=(*emission[0],1); p.inputs['Emission Strength'].default_value=emission[1]
    m.diffuse_color=(*color,1); return m
metal=material('Metal_Champagne',(.63,.47,.29),.87,.29)
p=metal.node_tree.nodes.get('Principled BSDF'); (p.inputs.get('Anisotropic IOR Level') or p.inputs.get('Anisotropic')).default_value=.42
# Fine directional brushed microstructure, render only; clean physical PBR values export to glTF.
t=metal.node_tree.nodes.new('ShaderNodeTexNoise'); t.inputs['Scale'].default_value=180; t.inputs['Detail'].default_value=2
tex=metal.node_tree.nodes.new('ShaderNodeTexCoord'); mapping=metal.node_tree.nodes.new('ShaderNodeVectorMath'); mapping.operation='MULTIPLY'; mapping.inputs[1].default_value=(1,1,38)
metal.node_tree.links.new(tex.outputs['Generated'],mapping.inputs[0]); metal.node_tree.links.new(mapping.outputs[0],t.inputs['Vector'])
bump=metal.node_tree.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.12; bump.inputs['Distance'].default_value=.000035
metal.node_tree.links.new(t.outputs['Fac'],bump.inputs['Height']); metal.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
edge=material('Metal_Edge',(.75,.59,.39),.88,.20)
diff=material('Diffuser',(.96,.83,.62),.0,.32,((1.0,.72,.38),3.5))
dark=material('Base_Dark',(.032,.035,.037),.30,.33)
seam=material('Recess_Shadow',(.041,.038,.032),.5,.32)
rubber=material('Feet_Elastomer',(.015,.017,.018),.0,.8)

# Rounded rectangular toroidal sweep, not an ordinary torus.
TILT=math.radians(-12); ROT=Matrix.Rotation(TILT,3,'X'); CENTER=Vector((0,.017,.306))

def rounded_profile(r0,r1,d0,d1,b,steps=3):
    out=[]
    for cr,cd,start in [(r1-b,d1-b,0),(r0+b,d1-b,90),(r0+b,d0+b,180),(r1-b,d0+b,270)]:
        for j in range(steps+1):
            a=math.radians(start+j*90/steps); out.append((cr+b*cos(a),cd+b*sin(a)))
    return out

def lathe(name,profile,n=160,mat=metal,axis='ring',offset=(0,0,0)):
    verts=[]; faces=[]; k=len(profile)
    for i in range(n):
        a=2*pi*i/n
        for r,d in profile:
            if axis=='ring': v=ROT@Vector((r*cos(a),d,r*sin(a)))+CENTER+Vector(offset)
            else: v=Vector((r*cos(a)+offset[0],r*sin(a)+offset[1],d+offset[2]))
            verts.append(v)
    for i in range(n):
        for j in range(k):
            if axis=='ring': faces.append((i*k+j,i*k+(j+1)%k,((i+1)%n)*k+(j+1)%k,((i+1)%n)*k+j))
            else: faces.append((i*k+j,((i+1)%n)*k+j,((i+1)%n)*k+(j+1)%k,i*k+(j+1)%k))
    me=bpy.data.meshes.new(name+'_mesh'); me.from_pydata(verts,[],faces); me.materials.append(mat); me.update()
    ob=bpy.data.objects.new(name,me); root.objects.link(ob)
    for f in me.polygons: f.use_smooth=True
    return ob

housing=lathe('01_Annular_aluminum_housing',rounded_profile(.1636,.175,-.0125,.0125,.0012,2),160)
liner=lathe('02_Recessed_opal_continuous_liner',rounded_profile(.1572,.1642,-.009,.009,.0015,2),160, diff)
# Circumferential front/rear assembly seams and extremely fine brighter chamfer.
lathe('03_Front_machined_edge',rounded_profile(.1738,.17515,-.0127,-.0114,.00032,1),160,edge)
lathe('04_Rear_shell_join',[(.17485,.0060),(.17508,.0060),(.17508,.0065),(.17485,.0065)],128,seam)
lathe('05_Inner_reflector_lip',rounded_profile(.16325,.1641,-.0104,-.0096,.0002,1),160,edge)

# Base: low solid-looking machined disc, inset elastomer tray, three feet.
lathe('06_Weighted_machined_base',rounded_profile(.0001,.098,.007,.020,.0024,2),96,metal,'base')
lathe('07_Base_charcoal_underside',rounded_profile(.0001,.094,.0036,.0088,.0013,1),96,dark,'base')
lathe('08_Base_bright_perimeter',rounded_profile(.0966,.0981,.0081,.0090,.0003,1),96,edge,'base')


def cylinder(name,radius,depth,loc,mat=metal,vertices=64,bevel=.001):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=radius,depth=depth,location=loc)
    ob=move(bpy.context.object); ob.name=name; ob.data.materials.append(mat)
    if bevel:
        mod=ob.modifiers.new('Machined edge radii','BEVEL'); mod.width=bevel; mod.segments=2
        bpy.context.view_layer.objects.active=ob; bpy.ops.object.modifier_apply(modifier=mod.name)
    for p in ob.data.polygons: p.use_smooth=True
    wn=ob.modifiers.new('Area weighted surface normals','WEIGHTED_NORMAL'); wn.keep_sharp=True; wn.weight=50
    bpy.context.view_layer.objects.active=ob; bpy.ops.object.modifier_apply(modifier=wn.name)
    return ob

def rod(name,a,b,r,mat=metal,vertices=48):
    a=Vector(a); b=Vector(b); o=cylinder(name,r,(b-a).length,(a+b)/2,mat,vertices,.0007)
    o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o
bottom=ROT@Vector((0,0,-.172))+CENTER
# Stem remains slender but visibly engineered; socket joins below annular housing.
rod('09_Slender_continuous_stem',(0,.002,.020),bottom+Vector((0,0,.004)),.0048)
cylinder('10_Stem_recessed_mount',.0081,.0034,(0,.002,.0202),edge,64,.0005)
# A discreet rotary dimmer offset right and toward the viewer, with a narrow black gasket.
cylinder('11_Dimmer_gasket',.0118,.0012,(.050,-.035,.0205),seam,64,.0003)
cylinder('12_Brushed_dimmer_dial',.0108,.0054,(.050,-.035,.0230),metal,96,.0010)
# Fine radial indicator notch, physical inset not branding.
bpy.ops.mesh.primitive_cube_add(size=1,location=(.050,-.0407,.02563)); notch=move(bpy.context.object); notch.name='13_Dimmer_index'; notch.dimensions=(.0007,.0042,.00014); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); notch.data.materials.append(seam)
for i,a in enumerate([30,150,270]):
    a=math.radians(a); cylinder('14_Foot_%d'%(i+1),.009,.0029,(.069*cos(a),.069*sin(a),.0021),rubber,32,.0007)
# Rear connector aperture + discrete power lead collar; no cable in web silhouette.
port=cylinder('15_Rear_power_port',.0037,.0015,(0,.0937,.0122),dark,48,.0004); port.rotation_euler[0]=pi/2

# A named empty supplies an obvious semantic root for consumers.
anchor=bpy.data.objects.new('ECLIPSE_35_ROOT',None); root.objects.link(anchor)
for ob in list(root.objects):
    if ob!=anchor: ob.parent=anchor
anchor['product']='NOCTILUME / Eclipse 35'; anchor['units']='meters'; anchor['ring_diameter_m']=.35; anchor['tilt_degrees']=12
anchor['frontend_emission_material']='Diffuser'; anchor['frontend_note']='Set Diffuser emissiveIntensity between 0 and 3.5. Use neutral environment or studio lights for metal.'

# Product-only glTF, no scene lights/cameras/ground dependencies.
bpy.ops.object.select_all(action='DESELECT')
for ob in root.objects: ob.select_set(True)
bpy.context.view_layer.objects.active=anchor
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT,'noctilume-eclipse.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_materials='EXPORT',export_cameras=False,export_lights=False,export_extras=True,export_animations=False)

# Editorial studio: soft neutral ivory, broad reflection cards with warm rim.
world=bpy.data.worlds.new('Warm neutral studio'); sc.world=world; world.use_nodes=True
world.node_tree.nodes['Background'].inputs[0].default_value=(.20,.225,.255,1); world.node_tree.nodes['Background'].inputs[1].default_value=.32
floor=material('Studio_Ivory',(.72,.68,.59),0,.66)
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,0)); plane=move(bpy.context.object,studio); plane.name='Studio floor'; plane.data.materials.append(floor)

def aim(obj,target): obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
def light(name,loc,power,size,color=(1,1,1),target=(0,0,.24),size_y=None):
    data=bpy.data.lights.new(name,'AREA'); data.energy=power*.32; data.color=color
    data.shape='RECTANGLE'; data.size=size; data.size_y=size_y or size
    ob=bpy.data.objects.new(name,data); studio.objects.link(ob); ob.location=loc; aim(ob,target); return ob
light('Key — tall silk',(-.55,-.48,.85),45,.50,(1,.88,.72),size_y=.9)
light('Fill — cool silk',(.6,-.15,.55),28,.35,(.82,.9,1),size_y=.75)
light('Edge — rear strip',(.15,.45,.7),65,.25,(1,.91,.78),size_y=.65)
light('Overhead',(0,-.05,1.1),20,.55,(1,1,1))
# Soft emitted practical contribution from liner can be lit by Cycles directly.
camdata=bpy.data.cameras.new('Editorial camera'); cam=bpy.data.objects.new('Editorial camera',camdata); studio.objects.link(cam); sc.camera=cam
cam.location=(.49,-.91,.49); aim(cam,(0,.005,.243)); camdata.type='ORTHO'; camdata.ortho_scale=.66; camdata.lens=70
sc.render.resolution_x=1800; sc.render.resolution_y=1800
sc.render.film_transparent=False
sc.render.filepath=os.path.join(OUT,'noctilume-eclipse-poster.png')
# Mild physically motivated bloom, not a thick neon halo.
sc.use_nodes=True; nt=sc.node_tree; nt.nodes.clear()
rl=nt.nodes.new('CompositorNodeRLayers'); glow=nt.nodes.new('CompositorNodeGlare'); glow.glare_type='FOG_GLOW'; glow.quality='HIGH'; glow.threshold=1.8; glow.size=7; glow.mix=-.92
comp=nt.nodes.new('CompositorNodeComposite'); nt.links.new(rl.outputs['Image'],glow.inputs['Image']); nt.links.new(glow.outputs['Image'],comp.inputs['Image'])
# Save native model and fully reproducible studio before rendering.
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'noctilume-eclipse.blend'),compress=True)

meshes=[o for o in root.objects if o.type=='MESH']; tris=0
for o in meshes: o.data.calc_loop_triangles(); tris+=len(o.data.loop_triangles)
manifest={'product':'NOCTILUME Eclipse 35','authoring':'Original procedural design authored in installed Blender','blender_version':bpy.app.version_string,'units':'meters','ring_diameter_m':.35,'height_m':round(max((o.matrix_world@Vector(v.co)).z for o in meshes for v in o.data.vertices),4),'ring_back_tilt_degrees':12,'mesh_objects':len(meshes),'vertices':sum(len(o.data.vertices) for o in meshes),'triangles':tris,'materials':[m.name for m in [metal,edge,diff,dark,seam,rubber]],'emission_material':'Diffuser','default_emission_strength':3.5,'front_axis_blender':'-Y','front_axis_gltf':'+Z','glb_has_cameras':False,'glb_has_lights':False,'glb_has_baked_environment':False,'notes':['Procedural brushing is render-only; GLB uses texture-free PBR materials.','Use a neutral studio environment or large soft lights in frontend to show metallic reflections.','Model includes opal liner, machined seams, control dial, three feet, underside and power port.','Root is centered at base origin; GLB is Y-up, real-world meters.']}
with open(os.path.join(OUT,'asset-manifest.json'),'w') as f: json.dump(manifest,f,indent=2)
print('MODEL_READY '+json.dumps(manifest),flush=True)
bpy.ops.render.render(write_still=True)
print('POSTER_READY',flush=True)
# Close detail: intersection of ring, stem, and dial to show manufactured tolerances.
cam.location=(.43,-.57,.33); aim(cam,(.022,-.005,.075)); camdata.ortho_scale=.285
sc.render.resolution_x=1800; sc.render.resolution_y=1350
sc.render.filepath=os.path.join(OUT,'noctilume-eclipse-detail.png')
bpy.ops.render.render(write_still=True)
print('DETAIL_READY',flush=True)
# Web-friendly transparent beauty with all product normals/materials intact.
cam.location=(.49,-.91,.49); aim(cam,(0,.005,.243)); camdata.ortho_scale=.60
sc.render.resolution_x=1800; sc.render.resolution_y=1800
plane.hide_render=True; sc.render.film_transparent=True
sc.render.filepath=os.path.join(OUT,'noctilume-eclipse-transparent.png')
bpy.ops.render.render(write_still=True)
print('TRANSPARENT_READY',flush=True)
