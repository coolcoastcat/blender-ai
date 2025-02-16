import bpy
import math
import random
import mathutils

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

def create_cat_body():
    # Create main body - adjusted position for laptop interaction
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0.8))
    body = bpy.context.active_object
    body.scale = (1.2, 1.1, 0.8)
    
    # Create head - bigger, rounder head
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(0.8, 0, 1.3))
    head = bpy.context.active_object
    head.scale = (0.7, 0.7, 0.6)  # Rounder head
    
    # Create big eyes
    for x in [-0.15, 0.15]:  # Eye positions
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=(1.2, x, 1.4))
        eye = bpy.context.active_object
        eye.scale = (0.4, 0.4, 0.4)  # Big round eyes
        
        # Create eye shine
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.03, location=(1.25, x, 1.45))
        shine = bpy.context.active_object
        shine_mat = bpy.data.materials.new(name="EyeShine")
        shine_mat.use_nodes = True
        shine_mat.node_tree.nodes["Principled BSDF"].inputs['Emission'].default_value = (1, 1, 1, 1)
        shine.data.materials.append(shine_mat)
    
    # Create pointier ears
    for x, y in [(0.15, 0.3), (0.15, -0.3)]:
        bpy.ops.mesh.primitive_cone_add(radius1=0.12, depth=0.25, location=(0.9 + x, y, 1.8))
        ear = bpy.context.active_object
        ear.rotation_euler = (0.2, 0.1, 0.2 if y > 0 else -0.2)
    
    # Create tail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, location=(-1.2, 0, 0.8))
    tail = bpy.context.active_object
    tail.rotation_euler = (0, 1.2, 0)
    
    # Create paws - positioned on laptop
    paw_positions = [
        (1.4, 0.3, 0.45),  # Left paw on laptop
        (1.4, -0.3, 0.45)  # Right paw on laptop
    ]
    for pos in paw_positions:
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, location=pos)
        paw = bpy.context.active_object
        paw.scale = (0.3, 0.2, 0.1)
    
    # Create smile - using primitive curve instead of curve.new
    bpy.ops.curve.primitive_bezier_curve_add(location=(1.1, 0, 1.1))
    smile = bpy.context.active_object
    smile.name = "CatSmile"
    smile.data.dimensions = '3D'
    
    # Adjust smile points for a proper curve
    points = smile.data.splines[0].bezier_points
    points[0].co = (0, 0.15, 0)
    points[1].co = (0, -0.15, 0)
    points[0].handle_right = (0.1, 0.1, 0)
    points[1].handle_left = (0.1, -0.1, 0)
    points[0].handle_left = (-0.1, 0.1, 0)
    points[1].handle_right = (-0.1, -0.1, 0)
    
    # Add thickness to the smile
    smile.data.bevel_depth = 0.01
    
    # Position smile on the front of the face
    smile.location = (1.20, 0, 1.2)  # Moved 0.15 meters closer to cat
    # Rotate 90 degrees only on Y axis
    smile.rotation_euler = (0, math.radians(90), 0)
    smile.scale = (1, 0.7, 1)
    
    # Create legs connecting body to paws
    leg_positions = [
        {
            'start': (0.6, 0.6, 0.6),    # Right front shoulder
            'end': (1.4, 0.3, 0.45),     # Right front paw
            'name': 'RightFrontLeg'
        },
        {
            'start': (0.6, -0.6, 0.6),   # Left front shoulder
            'end': (1.4, -0.3, 0.45),    # Left front paw
            'name': 'LeftFrontLeg'
        }
    ]
    
    for leg in leg_positions:
        start = leg['start']
        end = leg['end']
        
        # Calculate leg properties
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        length = math.sqrt(dx**2 + dy**2 + dz**2)
        
        # Create leg cylinder
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.15,
            depth=length,
            location=(
                (start[0] + end[0])/2,
                (start[1] + end[1])/2,
                (start[2] + end[2])/2
            )
        )
        leg_obj = bpy.context.active_object
        leg_obj.name = leg['name']
        
        # Calculate rotation
        direction = mathutils.Vector((dx, dy, dz))
        rot_quat = direction.to_track_quat('-Z', 'Y')
        leg_obj.rotation_euler = rot_quat.to_euler()
        
        # Scale leg to be thinner
        leg_obj.scale = (0.4, 0.4, 1.0)
        
        # Add slight bend in middle (for more natural look)
        bpy.ops.object.modifier_add(type='SIMPLE_DEFORM')
        bend_mod = leg_obj.modifiers[-1]
        bend_mod.deform_method = 'BEND'
        bend_mod.angle = math.radians(15)
        bend_mod.deform_axis = 'X'

def create_laptop():
    print("\n=== Starting Laptop Creation ===")
    
    laptop_parts = []
    
    # Create laptop base - positioned for cat interaction
    bpy.ops.mesh.primitive_cube_add(location=(1.8, 0, 0.4))  # Moved closer for paw interaction
    base = bpy.context.active_object
    base.scale = (0.8, 0.6, 0.05)
    base.rotation_euler = (0, 0, math.radians(90))
    base.name = "Laptop_Base"
    laptop_parts.append(base)
    
    # Create screen - connected to back edge of base
    screen_x = base.location.x + 0.6  # Position at back edge
    screen_y = base.location.y
    screen_z = base.location.z + 0.4  # Raise to connect with base
    
    bpy.ops.mesh.primitive_cube_add(location=(screen_x, screen_y, screen_z))
    screen = bpy.context.active_object
    screen.scale = (0.8, 0.6, 0.02)
    screen.rotation_euler = (math.radians(-60), 0, math.radians(90))  # Adjusted angle
    screen.name = "Laptop_Screen"
    laptop_parts.append(screen)
    
    # Create keyboard surface
    bpy.ops.mesh.primitive_cube_add(location=(1.8, 0, 0.42))  # Match base position
    keyboard = bpy.context.active_object
    keyboard.scale = (0.75, 0.55, 0.01)
    keyboard.rotation_euler = (0, 0, math.radians(90))
    keyboard.name = "Laptop_Keyboard"
    
    # Add screen glow material
    screen_mat = bpy.data.materials.new(name="ScreenGlow")
    screen_mat.use_nodes = True
    nodes = screen_mat.node_tree.nodes
    nodes.clear()
    
    # Create emission node for screen glow
    emission = nodes.new('ShaderNodeEmission')
    output = nodes.new('ShaderNodeOutputMaterial')
    emission.inputs['Strength'].default_value = 2.0
    emission.inputs['Color'].default_value = (0.2, 0.4, 0.8, 1.0)
    screen_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    print("Created screen glow material")
    
    # Apply material to screen
    if screen.data.materials:
        screen.data.materials[0] = screen_mat
    else:
        screen.data.materials.append(screen_mat)
    print(f"Applied glow material to screen: {len(screen.data.materials)} materials")
    
    # Create a darker material for base and keyboard
    laptop_mat = bpy.data.materials.new(name="LaptopBody")
    laptop_mat.use_nodes = True
    laptop_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.1, 0.1, 0.1, 1)
    
    # Apply laptop body material
    base.data.materials.append(laptop_mat)
    keyboard.data.materials.append(laptop_mat)
    print("Applied laptop body materials")
    
    print("\nCreated laptop parts:")
    for part in laptop_parts:
        print(f"- {part.name}: location={part.location}")
    
    return laptop_parts  # Return references to prevent garbage collection

def create_calico_material():
    fur_mat = bpy.data.materials.new(name="CalicoCat")
    fur_mat.use_nodes = True
    nodes = fur_mat.node_tree.nodes
    links = fur_mat.node_tree.links
    
    nodes.clear()
    
    # Create nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    color_mix1 = nodes.new('ShaderNodeMixRGB')  # Mix white and orange
    color_mix2 = nodes.new('ShaderNodeMixRGB')  # Mix previous result with black
    noise1 = nodes.new('ShaderNodeTexNoise')    # For orange patches
    noise2 = nodes.new('ShaderNodeTexNoise')    # For black patches
    mapping = nodes.new('ShaderNodeMapping')
    tex_coord = nodes.new('ShaderNodeTexCoord')
    
    # Setup noise for orange patches
    noise1.inputs['Scale'].default_value = 2.5
    noise1.inputs['Detail'].default_value = 2.0
    noise1.inputs['Roughness'].default_value = 0.7
    
    # Setup noise for black patches
    noise2.inputs['Scale'].default_value = 3.0
    noise2.inputs['Detail'].default_value = 2.0
    noise2.inputs['Roughness'].default_value = 0.6
    
    # Setup color mixing
    color_mix1.blend_type = 'MIX'
    color_mix1.inputs[1].default_value = (1, 1, 1, 1)          # White
    color_mix1.inputs[2].default_value = (0.9, 0.5, 0.2, 1)    # Peach/orange
    
    color_mix2.blend_type = 'MIX'
    color_mix2.inputs[2].default_value = (0.1, 0.12, 0.2, 1)   # Navy/black
    
    # Setup fur properties
    principled.inputs['Roughness'].default_value = 0.9
    principled.inputs['Sheen'].default_value = 1.0
    principled.inputs['Sheen Tint'].default_value = 0.6
    principled.inputs['Transmission'].default_value = 0.1  # For fur translucency
    
    # Connect nodes
    links.new(tex_coord.outputs['UV'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise1.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise2.inputs['Vector'])
    links.new(noise1.outputs['Fac'], color_mix1.inputs['Fac'])
    links.new(noise2.outputs['Fac'], color_mix2.inputs['Fac'])
    links.new(color_mix1.outputs['Color'], color_mix2.inputs[1])
    links.new(color_mix2.outputs['Color'], principled.inputs['Base Color'])
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    
    return fur_mat

def setup_scene():
    # Create floor
    bpy.ops.mesh.primitive_plane_add(size=10)
    floor = bpy.context.active_object
    
    # Add lighting
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 7))
    sun = bpy.context.active_object
    sun.data.energy = 5
    
    # Add fill light
    bpy.ops.object.light_add(type='AREA', location=(-3, -3, 4))
    fill = bpy.context.active_object
    fill.data.energy = 3
    
    # Add camera
    bpy.ops.object.camera_add(location=(4, -4, 3))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(60), 0, math.radians(45))
    bpy.context.scene.camera = camera

def animate_cat():
    # Get the tail object
    tail = bpy.data.objects['Cylinder']
    
    # Get paws and legs
    right_paw = None
    left_paw = None
    right_leg = None
    left_leg = None
    
    # Find our paw and leg objects
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and isinstance(obj.data, bpy.types.Mesh):
            loc = obj.location
            if abs(loc[1] - 0.3) < 0.1 and abs(loc[2] - 0.45) < 0.1:  # Right paw
                right_paw = obj
            elif abs(loc[1] + 0.3) < 0.1 and abs(loc[2] - 0.45) < 0.1:  # Left paw
                left_paw = obj
        elif obj.name == 'RightFrontLeg':
            right_leg = obj
        elif obj.name == 'LeftFrontLeg':
            left_leg = obj
    
    print(f"Found animation objects - Right paw: {right_paw}, Left paw: {left_paw}")
    print(f"Found legs - Right leg: {right_leg}, Left leg: {left_leg}")
    
    # Create typing animation
    for frame in range(50):
        # Tail swishing
        tail.rotation_euler.z = math.sin(frame * 0.2) * 0.3
        tail.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        # Breathing animation for body
        for obj in bpy.data.objects:
            if obj.type == 'MESH' and obj.name.startswith('Sphere'):
                obj.scale.z = 1 + math.sin(frame * 0.1) * 0.02
                obj.keyframe_insert(data_path="scale", frame=frame)
        
        # Typing animation for paws
        if right_paw and left_paw:
            # Right paw types faster than left paw
            right_offset = math.sin(frame * 0.8) * 0.05  # Faster, smaller movement
            left_offset = math.sin(frame * 0.6) * 0.07   # Slower, larger movement
            
            # Animate right paw
            right_paw.location.z = 0.45 + right_offset
            right_paw.keyframe_insert(data_path="location", frame=frame)
            
            # Animate left paw
            left_paw.location.z = 0.45 + left_offset
            left_paw.keyframe_insert(data_path="location", frame=frame)
            
            # Animate legs to follow paws
            if right_leg:
                right_leg.scale.z = 1 + right_offset * 0.5
                right_leg.keyframe_insert(data_path="scale", frame=frame)
            
            if left_leg:
                left_leg.scale.z = 1 + left_offset * 0.5
                left_leg.keyframe_insert(data_path="scale", frame=frame)

# Create the scene
print("\n=== Starting Scene Creation ===")
print("Initial objects:", bpy.data.objects.keys())

setup_scene()
print("\nAfter setup_scene, objects:", bpy.data.objects.keys())

# Create laptop first
create_laptop()
print("\nAfter create_laptop, objects:", bpy.data.objects.keys())

# Now create cat
create_cat_body()
print("\nAfter create_cat_body, objects:", bpy.data.objects.keys())

# Add debug prints before and after material application
print("\n=== Starting Material Application ===")
calico_material = create_calico_material()
print("Created calico material")

print("\nObjects before material application:")
for obj in bpy.data.objects:
    if obj.type == 'MESH':  # Only print material info for mesh objects
        print(f"- {obj.name}: {len(obj.data.materials)} materials")

# Apply materials
for obj in bpy.data.objects:
    if obj.type == 'MESH':  # Only apply materials to mesh objects
        if 'Laptop' in obj.name:
            print(f"Preserving materials for laptop part: {obj.name}")
            continue
        if obj.name == 'Plane':
            print(f"Skipping material for {obj.name}")
            continue
        print(f"Applying calico material to {obj.name}")
        obj.data.materials.append(calico_material)

print("\nFinal objects in scene:")
for obj in bpy.data.objects:
    if obj.type == 'MESH':  # Only print material info for mesh objects
        print(f"- {obj.name}: location={obj.location}, materials={len(obj.data.materials)}")
    else:
        print(f"- {obj.name}: location={obj.location}, type={obj.type}")

# Set up animation
bpy.context.scene.frame_end = 50
animate_cat()

# Render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080 