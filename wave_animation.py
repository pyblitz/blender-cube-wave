# Cube Wave Animation - Blender Python Course, Lesson 1
# Our plan, written first as comments:
# Step 1: clear the old scene, so we start empty
# Step 2: make 9 cubes in a loop, each with its own color
# Step 3: wave keyframes - every cube rises and falls, one after another
# Step 4: add a camera and a light, so we can see and render the wave
# Step 5: scene settings - 40 frames, playing at 24 frames per second

import bpy
import math

# Step 1: clear the old scene, so we start empty
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# Step 2: make 9 cubes in a loop, each with its own color
CUBE_COUNT = 9
SPACING = 2.4
WAVE_HEIGHT = 1.2
WAVE_BASE = 2.2
CUBE_COLORS = [
    (1.0, 0.2, 0.2, 1.0),   # red
    (1.0, 0.5, 0.1, 1.0),   # orange
    (1.0, 0.9, 0.1, 1.0),   # yellow
    (0.2, 0.8, 0.2, 1.0),   # green
    (0.1, 0.8, 0.8, 1.0),   # cyan
    (0.2, 0.4, 1.0, 1.0),   # blue
    (0.6, 0.2, 0.9, 1.0),   # purple
    (1.0, 0.3, 0.7, 1.0),   # pink
    (0.9, 0.9, 0.9, 1.0),   # white
]

cubes = []
for i in range(CUBE_COUNT):
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, WAVE_BASE))
    cube = bpy.context.active_object
    cube.name = "WaveCube_" + str(i + 1)
    cube.location.x = (i - 4) * SPACING

    material = bpy.data.materials.new(name="CubeColor_" + str(i + 1))
    material.use_nodes = True
    material.node_tree.nodes["Principled BSDF"].inputs[
        "Base Color"].default_value = CUBE_COLORS[i]
    # Workbench renders use the viewport display color, not the nodes,
    # so set that too - otherwise every cube renders flat grey
    material.diffuse_color = CUBE_COLORS[i]
    cube.data.materials.append(material)
    cubes.append(cube)

# a dark floor, so the wave has something to stand on
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
floor = bpy.context.active_object
floor.name = "Floor"
floor_material = bpy.data.materials.new(name="FloorColor")
floor_material.use_nodes = True
floor_material.node_tree.nodes["Principled BSDF"].inputs[
    "Base Color"].default_value = (0.08, 0.08, 0.1, 1.0)
floor_material.diffuse_color = (0.08, 0.08, 0.1, 1.0)
floor.data.materials.append(floor_material)

# Step 3: wave keyframes - every cube rises and falls, one after another
# Each cube gets the same wave, but starting a little later than the
# one before it. That delay is what makes the wave travel sideways.
WAVE_FRAMES = [1, 20, 40]
for i, cube in enumerate(cubes):
    delay = i * 0.7
    for frame in WAVE_FRAMES:
        angle = 2 * math.pi * (frame - 1) / 40 + delay
        cube.location.z = WAVE_BASE + WAVE_HEIGHT * math.sin(angle)
        cube.keyframe_insert(data_path="location", frame=frame)
    # smooth sine easing, so the motion never looks jerky
    action = cube.animation_data.action
    strip = action.layers[0].strips[0]
    for slot in action.slots:
        for fcurve in strip.channelbag(slot).fcurves:
            for point in fcurve.keyframe_points:
                point.interpolation = "SINE"

# Step 4: add a camera and a light, so we can see and render the wave
bpy.ops.object.camera_add(location=(0, -24, 11))
camera = bpy.context.active_object
camera.name = "WaveCamera"
camera.rotation_euler = (1.2, 0, 0)
camera.data.lens = 35
bpy.context.scene.camera = camera

bpy.ops.object.light_add(type="SUN", location=(5, -5, 10))
sun = bpy.context.active_object
sun.name = "WaveSun"
sun.data.energy = 3

# Step 5: scene settings - 40 frames, playing at 24 frames per second
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 40
scene.render.fps = 24
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
# Workbench already renders with material colors and studio light
# by default, so no extra shading settings are needed here

print("Cube Wave ready: " + str(len(cubes)) + " cubes, "
      + str(len(WAVE_FRAMES)) + " keyframes each, 40 frames at 24 fps")
