# Test on Blender 3.6.1

bl_info = {
	"name": "Remove unused Vertex Groups and Bones",
	"author": "Aoirusann",
	"version": (1, 0),
	"blender": (3, 6, 1),
	"location": "In search (Edit > Operator Search) type 'Remove Unused'",
	"description": "Remove the unused vertex groups from mesh objects and remove the unused bones from armature objects.",
	"doc_url": "https://github.com/aoirusann/BlenderAddon_RemoveUnuseVertexGroupsAndBones",
	"category": "Model",
}

import bpy
import copy

# 1. Select some mesh objects whose vertex groups will be checked.
# 2. F3 - Remove Unused VeretxGroups
# 3. The vertex groups with empty weights on the mesh objects should be removed.
class RemoveUnusedVertexGroups(bpy.types.Operator):
    """Remove Unused VertexGroups"""
    bl_idname = "armature.remove_unused_vertexgroups"
    bl_label = "Remove Unused Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    ## From https://gist.github.com/OptoCloud/55f1c61f4deea619bf5b39cb21781f6a


    ## Remove empty vertex groups and shape keys
    ## Credits:
    ##    https://blender.stackexchange.com/questions/237599/is-there-a-way-to-automatically-delete-shape-keys-that-are-identical-to-the-basi
    ##    https://blender.stackexchange.com/questions/16517/how-to-quickly-remove-all-zero-weight-vertex-groups

    def execute(self, context):
        if bpy.context.mode != 'OBJECT':
            self.report({"ERROR"}, "Must be in object mode!")
            return {"CANCELLED"}

        def survey(obj):
            '''Collect the highest vertex weight in each vertex group'''
            maxWeight = {}
            for i in obj.vertex_groups:
                maxWeight[i.index] = 0

            for v in obj.data.vertices:
                for g in v.groups:
                    gn = g.group 
                    w = obj.vertex_groups[g.group].weight(v.index)
                    if (maxWeight.get(gn) is None or w>maxWeight[gn]):
                        maxWeight[gn] = w
            return maxWeight

        for obj in bpy.context.selected_objects:
            if obj.type != 'MESH':
                self.report({"WARNING"}, f"{obj.name} is not a mesh, so nothing will happen on it.")
                continue
            self.report({"INFO"}, f"Processing {obj.name}...")

            maxWeight = survey(obj)
            ka = []
            ka.extend(maxWeight.keys())
            ka.sort(key=lambda gn: -gn) # Inverse it, so remove can works well.
            for gn in ka:
                if maxWeight[gn]<=0:
                    self.report({"INFO"}, f"Remove {obj.vertex_groups[gn].name}")
                    obj.vertex_groups.remove(obj.vertex_groups[gn]) # actually remove the group
            self.report({"INFO"}, f"Processed {obj.name}.")

        self.report({"INFO"}, f"All mesh objects are checked.")
        return {'FINISHED'}



# 1. Select some mesh objects whose vertex groups will be checked.
# 2. Ctrl+Click select an armature object whose bone will be removed.
# 3. F3 - Remove Unused Bones
# 4. The bones which are not referred by the mesh objects on the armature object should be removed.
class RemoveUnusedBones(bpy.types.Operator):
    """Remove Unused Bones"""
    bl_idname = "armature.remove_unused_bones"
    bl_label = "Remove Unused Bones"
    bl_options = {'REGISTER', 'UNDO'}

    def _dps(self, bone: bpy.types.Bone, vertex_groups: set[str], visited: set[str], armature: bpy.types.Object) -> bool:
        if bone.name in visited:
            return bone.name in armature.data.edit_bones.keys()
        visited.add(bone.name)

        # If any of the child is kept, this bone should be kept too
        should_kept = False
        children = copy.copy(bone.children)
        for child in children:
            should_kept |= self._dps(child, vertex_groups, visited, armature)
        if should_kept:
            return True

        # Otherwise check if this bone is being used
        if bone.name in vertex_groups:
            return True

        # Remove this unused bone
        self.report({"INFO"}, "Remove " + bone.name)
        armature.data.edit_bones.remove(bone)
        return False

    def execute(self, context):
        # UserInput Check
        # The last object should be an armature, and the others should be meshes
        if len(bpy.context.selectable_objects) == 0:
            self.report({"ERROR"}, "Nothing is selected. Please select some meshes and an armature (which should be the last one).")
            return {"CANCELLED"}
        obj_armature: bpy.types.Object = bpy.context.active_object
        if obj_armature.type != "ARMATURE":
            self.report({"ERROR"}, "The last object must be an armature whose bones are to be removed.")
            return {"CANCELLED"}
        objs_mesh: list[bpy.types.Object] = []
        for obj in bpy.context.selected_objects:
            if obj.type == "MESH":
                objs_mesh.append(obj)
        
        # Debug output
        self.report({"INFO"}, "Armature: " + obj_armature.name)
        self.report({"INFO"}, "Meshs: " + ",".join([obj_mesh.name for obj_mesh in objs_mesh]))

        # Enter edit mode
        obj_mode = obj_armature.mode # memo the current mode
        bpy.ops.object.mode_set(mode="EDIT")
        
        # Collect all the vertex groups being used
        vertex_groups: set[str] = set()
        for obj_mesh in objs_mesh:
            vertex_groups = vertex_groups.union(obj_mesh.vertex_groups.keys())
        
        # Debug output
        self.report({"INFO"}, "Vertex Groups: " + ",".join(vertex_groups))

        # Depth-first search on the armature
        visited: set[str] = set()
        for bone in obj_armature.data.edit_bones:
            self._dps(bone, vertex_groups, visited, obj_armature)

        # Exit edit mode
        bpy.ops.object.mode_set(mode=obj_mode)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(RemoveUnusedBones)
    bpy.utils.register_class(RemoveUnusedVertexGroups)


def unregister():
    bpy.utils.unregister_class(RemoveUnusedBones)
    bpy.utils.unregister_class(RemoveUnusedVertexGroups)


if __name__ == "__main__":
    register()