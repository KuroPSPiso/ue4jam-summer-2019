import bpy

C = bpy.context 
D = bpy.data
O = bpy.ops

def set_vertex_group(mesh, vertex_group):
    #Make a new list for all vertice indexes
    index_list = [0]*len(mesh.data.vertices)
    #Populate index list with vertice indexes
    mesh.data.vertices.foreach_get('index', index_list)   
    #Set mesh vertex group
    mesh.vertex_groups[vertex_group].add(index_list, 1, 'REPLACE')
    
def add_child_bone(bone_name, parent_bone, wheel_mesh):
    #Create a new bone
    new_bone = armature_data.data.edit_bones.new(bone_name)
    #Set bone's size
    new_bone.head = (0,0,0)
    new_bone.tail = (0,100,0)
    #Set bone's parent
    new_bone.parent = parent_bone
    #Set bone's location to wheel
    new_bone.matrix = wheel_mesh.matrix_world
    return new_bone

#Set variables for vehicle base and wheel meshes
vehicle_base = D.objects.get('VehicleBase')
wheel_RL = D.objects.get('Wheel_RL')
wheel_RR = D.objects.get('Wheel_RR')
wheel_FL = D.objects.get('Wheel_FL')
wheel_FR = D.objects.get('Wheel_FR')

#Set vehicle base as active
C.view_layer.objects.active = vehicle_base

#Select all vehicle meshes
vehicle_base.select_set(state=True)
wheel_RL.select_set(state=True)
wheel_RR.select_set(state=True)
wheel_FL.select_set(state=True)
wheel_FR.select_set(state=True)

#Set object mode
O.object.mode_set(mode='OBJECT', toggle=True)

#Set all object origins to geometry center
O.object.origin_set(type='ORIGIN_GEOMETRY', center = 'MEDIAN')

#Apply object transform
O.object.transform_apply(location = False, rotation = True, scale = True)

#Create armature object
armature = D.armatures.new('Armature')
armature_object = D.objects.new('Armature', armature)

#Link armature object to our scene
C.collection.objects.link(armature_object)

#Make armature variable
armature_data = D.objects[armature_object.name]

#Set armature active
C.view_layer.objects.active = armature_data

#Set armature selceted
armature_data.select_set(state=True)

#Set edit mode
O.object.mode_set(mode='EDIT', toggle=False)

#Set bones In front and show axis
armature_data.show_in_front = True
armature_data.data.show_axes = True

#Add root bone
root_bone = armature_data.data.edit_bones.new('Root')
#Set its orientation and size
root_bone.head = (0,0,0)
root_bone.tail = (0,100,0)
#Set its location to vehicle base mesh
root_bone.matrix = vehicle_base.matrix_world

#Add wheel bones to armature
add_child_bone('RL', root_bone, wheel_RL)
add_child_bone('RR', root_bone, wheel_RR)
add_child_bone('FL', root_bone, wheel_FL)
add_child_bone('FR', root_bone, wheel_FR)

#Set object mode
O.object.mode_set(mode='OBJECT', toggle=True)

#Select vehicle meshes
vehicle_base.select_set(state=True)
wheel_RL.select_set(state=True)
wheel_RR.select_set(state=True)
wheel_FL.select_set(state=True)
wheel_FR.select_set(state=True)

#Set armature active
C.view_layer.objects.active = armature_data

#Parent meshes to armature with empty groups
O.object.parent_set(type='ARMATURE_NAME')

#Set mesh vertex groups/weightpaint mesh
set_vertex_group(vehicle_base, 'Root')
set_vertex_group(wheel_RL, 'RL')
set_vertex_group(wheel_RR, 'RR')
set_vertex_group(wheel_FL, 'FL')
set_vertex_group(wheel_FR, 'FR')

#Deselect all objects
O.object.select_all(action='DESELECT')
#Set pose mode
O.object.mode_set(mode='POSE', toggle=True)