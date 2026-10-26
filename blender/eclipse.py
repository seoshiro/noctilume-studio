"""Eclipse — original NOCTILUME concept, Blender 5.x. No external add-ons.
blender --background --factory-startup --python blender/eclipse.py -- --render
"""
import bpy, math, os, sys
from mathutils import Vector
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'public', 'assets')
os.makedirs(ASSETS, exist_ok=True)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def material(name, color, metallic=0, roughness=.4, emission=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Metallic'].default_value=metallic; p.inputs['Roughness'].default_value=roughness
    if emission:
        p.inputs['Emission Color'].default_value=(*color,1); p.inputs['Emission Strength'].default_value=emission
    return m
champagne=material('Champagne | brushed aluminium',(.55,.42,.25),1,.29)
black=material('Ink | anodised aluminium',(.019,.022,.024),.8,.31)
diffuser=material('Diffuser | continuous frosted light', (1,.69,.35),0,.3,4)
floor=material('Warm limestone',(.23,.205,.17),0,.7)
def finish(obj,name,mat):
    obj.name=name; obj.data.materials.append(mat)
    for p in obj.data.polygons:p.use_smooth=True
    return obj
def cylinder(name,r,depth,z,mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=r,depth=depth,location=(0,0,z))
    o=finish(bpy.context.object,name,mat)
    mod=o.modifiers.new('Machined edge radius','BEVEL');mod.width=.002;mod.segments=3
    o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL')
    return o
base=cylinder('Eclipse | weighted circular base',.112,.018,.009,black)
stem=cylinder('Eclipse | narrow vertical stem',.006,.13,.078,champagne)
def ring(name,radius,width,depth,mat):
    # Rounded rectangular annular extrusion, in XZ, 12 degree backward lean.
    n=192; vertices=[]; faces=[]
    for i in range(n):
        a=2*math.pi*i/n
        for r,y in [(radius-width/2,-depth/2),(radius+width/2,-depth/2),(radius+width/2,depth/2),(radius-width/2,depth/2)]:
            x,z=r*math.cos(a),r*math.sin(a)
            tilt=math.radians(12)
            vertices.append((x,y*math.cos(tilt)-z*math.sin(tilt),.315+y*math.sin(tilt)+z*math.cos(tilt)))
    for i in range(n):
        for j in range(4):faces.append((4*i+j,4*((i+1)%n)+j,4*((i+1)%n)+(j+1)%4,4*i+(j+1)%4))
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update()
    o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);finish(o,name,mat)
    mod=o.modifiers.new('Soft machined edges','BEVEL');mod.width=.0014;mod.segments=3
    o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
    return o
outer=ring('Eclipse | sculpted champagne ring',.165,.020,.028,champagne)
inner=ring('Eclipse | uninterrupted inner diffuser',.1535,.005,.021,diffuser)
lamp=[base,stem,outer,inner]
bpy.ops.object.select_all(action='DESELECT')
for o in lamp:o.select_set(True)
bpy.context.view_layer.objects.active=outer
bpy.ops.export_scene.gltf(filepath=os.path.join(ASSETS,'eclipse.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_materials='EXPORT')
# Presentation scene excluded from GLB.
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.001));finish(bpy.context.object,'Limestone stage',floor)
def area(name,location,power,color,size,target=(0,0,.25)):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size
    o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=location;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Large warm key',(-.5,-.5,.8),55,(1,.84,.64),.7)
area('Cool edge',(.4,.25,.7),75,(.65,.74,1),.5)
area('Metal strip',(.5,-.1,.4),20,(1,.95,.85),.2)
area('Diffused ring spill',(0,-.035,.29),2,(1,.6,.26),.28,(0,-.3,0))
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.1,.09,.075,1);world.node_tree.nodes['Background'].inputs[1].default_value=.3
camdata=bpy.data.cameras.new('Portrait camera');cam=bpy.data.objects.new('Portrait camera',camdata);bpy.context.collection.objects.link(cam)
cam.location=(.62,-1.15,.65);cam.rotation_euler=(Vector((0,0,.25))-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=.72;bpy.context.scene.camera=cam
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.render.resolution_x=1200;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='WEBP';scene.render.image_settings.quality=90
scene.render.filepath=os.path.join(ASSETS,'eclipse-poster.webp')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','eclipse.blend'))
if '--render' in sys.argv:bpy.ops.render.render(write_still=True)
print('NOCTILUME_EXPORT_COMPLETE',os.path.getsize(os.path.join(ASSETS,'eclipse.glb')))
