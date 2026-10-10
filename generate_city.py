import bpy
import random
import math

# Clean up existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Grid parameters (Center at origin)
blocks_x = 10
blocks_y = 10
block_size = 24.0
road_width = 6.0
city_span_x = blocks_x * block_size + (blocks_x + 1) * road_width
city_span_y = blocks_y * block_size + (blocks_y + 1) * road_width

# Materials
def get_or_create_mat(name, color, roughness=0.5, metallic=0.2, emission=None):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        if emission:
            bsdf.inputs['Emission Color'].default_value = emission
            bsdf.inputs['Emission Strength'].default_value = 1.5
    return mat

ground_mat = get_or_create_mat("GroundMat", (0.05, 0.07, 0.1, 1.0), roughness=0.8, metallic=0.1)
road_mat = get_or_create_mat("RoadMat", (0.02, 0.03, 0.04, 1.0), roughness=0.9, metallic=0.0)

tower_mats = [
    get_or_create_mat("GlassTowerBlue", (0.1, 0.25, 0.45, 1.0), roughness=0.1, metallic=0.8, emission=(0.02, 0.1, 0.2, 1.0)),
    get_or_create_mat("GlassTowerTeal", (0.08, 0.35, 0.35, 1.0), roughness=0.15, metallic=0.7, emission=(0.02, 0.15, 0.15, 1.0)),
    get_or_create_mat("OfficeTowerGray", (0.18, 0.2, 0.25, 1.0), roughness=0.3, metallic=0.5),
    get_or_create_mat("FinancialTowerGold", (0.45, 0.35, 0.15, 1.0), roughness=0.2, metallic=0.85, emission=(0.1, 0.08, 0.02, 1.0)),
    get_or_create_mat("TechTowerCyber", (0.12, 0.12, 0.18, 1.0), roughness=0.2, metallic=0.6, emission=(0.05, 0.2, 0.4, 1.0)),
]

# Ground Base Plane
bpy.ops.mesh.primitive_plane_add(size=max(city_span_x, city_span_y) * 1.5, location=(0, 0, -0.1))
ground = bpy.context.active_object
ground.name = "PlazaGround"
ground.data.materials.append(ground_mat)

start_x = -((blocks_x * block_size) + ((blocks_x - 1) * road_width)) / 2.0
start_y = -((blocks_y * block_size) + ((blocks_y - 1) * road_width)) / 2.0

random.seed(42)

for i in range(blocks_x):
    for j in range(blocks_y):
        cx = start_x + i * (block_size + road_width) + block_size / 2.0
        cy = start_y + j * (block_size + road_width) + block_size / 2.0
        
        # Distance from center for skyscraper clustering
        dist = math.sqrt(cx**2 + cy**2)
        max_dist = math.sqrt((city_span_x/2)**2 + (city_span_y/2)**2)
        center_factor = max(0.15, 1.0 - (dist / max_dist))
        
        # Determine building height
        height = random.uniform(15.0, 40.0) + (center_factor ** 1.5) * 80.0
        
        # Add primary skyscraper
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(cx, cy, height / 2.0))
        tower = bpy.context.active_object
        b_width = block_size * random.uniform(0.65, 0.85)
        b_depth = block_size * random.uniform(0.65, 0.85)
        tower.scale = (b_width, b_depth, height)
        tower.name = f"Tower_{i}_{j}"
        
        # Assign material based on district
        mat = random.choice(tower_mats)
        tower.data.materials.append(mat)
        
        # Podium / roof antenna for tall financial towers
        if height > 70:
            antenna_h = height * 0.15
            bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=antenna_h, location=(cx, cy, height + antenna_h/2.0))
            spire = bpy.context.active_object
            spire.name = f"Spire_{i}_{j}"
            spire.data.materials.append(tower_mats[3]) # Gold / beacon

# Export glTF binary (.glb)
output_path = bpy.path.abspath('//city.glb')
bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
print(f"High-quality Financial District City exported to {output_path}")
