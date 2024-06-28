# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# === HELPFUL LINKS ===
# Official docs: https://docs.blender.org/api/current/index.html
# https://blender.stackexchange.com/questions/57306/how-to-create-a-custom-ui/57332#57332
#======================

import bpy

bl_info = {
    "name" : "3dStaged Automation Tools",
    "author" : "Lukas Tomasek",
    "description" : "3dStaged Automation Tools",
    "blender" : (4, 0, 0),
    "version" : (0, 0, 1),
    "location" : "Tool -> 3dStaged Automation Tools",
    "warning" : "",
    "doc_url": "https://github.com/lukastomasek/blender-automation-tools",
    "category" : "Generic"
}

class Utils():
    @staticmethod
    def remove_empty():
        parent = bpy.context.active_object

        if not parent:
            return "No Object Selected"

        for child in parent.children:
            if child.name.endswith(".001"):
                name = child.name.replace(".001", "")
                child.name = name
                bpy.context.view_layer.objects.active = parent
                parent.select_set(True)
                bpy.ops.object.delete()

                return "FINISHED"


        return "FINISHED"
    

class SceneProperties(bpy.types.PropertyGroup):
    # OBJ export not supported from blender yet
    export_options: bpy.props.EnumProperty(
        items=[
            ('GLB', 'GLB', 'gltf binary'),
            # ('OBJ', 'OBJ', 'wavefront obj'),
            ('FBX', 'FBX', 'binary fbx'),
        ],
        name="export_options",
        description="Export Options",
        default="GLB"
    )

class ApplyAllTransforms(bpy.types.Operator):
    bl_idname = "object.apply_all_transforms"
    bl_label = "Apply All Transforms"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        if selected_objects:
         for obj in selected_objects:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True, properties=True)
        
            self.report({'INFO'}, "All transforms applied")
        else:
            self.report({'ERROR'}, "No objects selected")

        return {'FINISHED'}

class MergeByDistance(bpy.types.Operator):
    bl_idname = "mesh.merge_by_distance"
    bl_label = "Merge By Distance"

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        if selected_objects and bpy.context.object.mode == 'EDIT':
         for obj in selected_objects:
            select_mode = bpy.context.tool_settings.mesh_select_mode[:]
            # only apply if mesh is in `face` mode
            if select_mode[2]:
               bpy.ops.mesh.remove_doubles(threshold=0.01)
               
            self.report({'INFO'}, "All objects merged")
        else:
            self.report({'ERROR'}, "No Face selected")


        return {'FINISHED'}

class ApplyCollisionAndDecimate(bpy.types.Operator):
    bl_idname = "modifier.apply_collision_and_decimate"
    bl_label = "Apply Collision and Decimate"

    material_data: bpy.props.StringProperty(
        name="m_skc",
        description="m_skc",
        default="m_skc"
    )

    # https://docs.google.com/document/d/1UZVHVROdbnWFJATT-PnoRUZ5j9nBbaqzSBvj_PGpKbA/edit    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        original_object = bpy.context.object

        if selected_objects:
            bpy.ops.object.duplicate()
            skeleton_obj = bpy.context.selected_objects[0]
            skeleton_obj.name = original_object.name + "_" + "a_skc"
            skeleton_obj.modifiers.new(name="Collision", type="COLLISION")

            decimate_mod = skeleton_obj.modifiers.new(name="Decimate", type="DECIMATE")
            decimate_mod.ratio = 0.5

            # remove previous materials and create new one
            skeleton_material = bpy.data.materials.new(self.material_data)
            skeleton_material.alpha_threshold = 0
            skeleton_material.blend_method = 'HASHED'
            skeleton_material.use_nodes = True
            principled_bsdf = skeleton_material.node_tree.nodes.get('Principled BSDF')

            if principled_bsdf:
                principled_bsdf.inputs['Alpha'].default_value = 0

            skeleton_obj.data.materials.clear()
            skeleton_obj.data.materials.append(skeleton_material)

            skeleton_obj.parent = original_object
            skeleton_obj.select_set(False)
            
            self.report({'INFO'}, "All modifiers applied")
        else:
            self.report({'ERROR'}, "No objects selected")

        return {'FINISHED'}

class ExportModel(bpy.types.Operator):
    bl_idname = "export.model"
    bl_label = "Export Model"

    copyright_text: bpy.props.StringProperty(
        name="Copyright",
        description="©Unreserved Inc. All rights reserved",
        default="Copyright:©Unreserved Inc. All rights reserved"
    )

    def execute(self, context):
        msg = Utils.remove_empty()

        self.report({'INFO'}, msg)

        export_options = context.scene.my_props.export_options

        if export_options == 'GLB':
            bpy.ops.export_scene.gltf('INVOKE_DEFAULT', export_copyright=self.copyright_text, use_selection=True, use_visible=True )
        elif export_options == 'OBJ':
              print('Exporting OBJ not supported from blender yet')  
        elif export_options == 'FBX':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', use_selection=True, use_visible=True, object_types={'MESH'}, use_space_transform=True)
        else:
            self.report({'ERROR'}, "No export options selected")

        self.report({'INFO'}, "Model exported")

        return {'FINISHED'}


class RemoveEmpty(bpy.types.Operator):
    bl_idname = "object.remove_empty"
    bl_label = "Remove Empty"

    def execute(self, context):
        msg = Utils.remove_empty()

        self.report({'INFO'}, msg)

        return {'FINISHED'}

class Panel(bpy.types.Panel):
    bl_label = '3dStaged'
    bl_name = '3dStaged Automation Tools'
    bl_idname = '3dstaged_automation_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
       layout = self.layout
       scene = context.scene
       my_props = scene.my_props 
    
       self.draw_object_window(context, layout=layout)

       self.draw_mesh_window(context, layout=layout)

       self.draw_modifiers_window(context, layout=layout)
       
       self.draw_export_window(context, layout=layout, my_props=my_props)

    def draw_object_window(self, context, layout):
        layout.label(text="Object")
        col = layout.column(align=True)
        col.operator("object.apply_all_transforms", text="Apply All Transforms")
        col.separator()
        col.operator("object.remove_empty", text="Remove Empty")
        layout.separator()

    def draw_mesh_window(self, context, layout):
        layout.label(text="Mesh")
        col = layout.column(align=True) 
        col.operator("mesh.merge_by_distance", text="Merge By Distance")
        layout.separator()

    def draw_modifiers_window(self, context, layout):
        layout.label(text="Modifiers")
        col = layout.column(align=True)
        col.operator('modifier.apply_collision_and_decimate', text="Apply Collision and Decimate")
        layout.separator()

    def draw_export_window(self, context, layout, my_props):
        layout.label(text="Export")
        col = layout.column(align=True)
        col.prop(my_props, "export_options", text="Options", expand=False)
        col.separator(factor=2)
        col.operator('export.model', text="Export Model")
        layout.separator()

classes = (
    Panel,
    ApplyAllTransforms,
    MergeByDistance,
    ApplyCollisionAndDecimate,
    ExportModel,
    SceneProperties,
    RemoveEmpty
)
        
def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.my_props = bpy.props.PointerProperty(type=SceneProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_props

if __name__ == "__init__":
    register()