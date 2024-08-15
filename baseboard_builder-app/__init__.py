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

#TODO: research rotation and scale

import bpy
from mathutils import Matrix, Vector

bl_info = {
    "name" : "Baseboard Builder",
    "author" : "Lukas Tomasek",
    "description" : "Baseboard builder",
    "blender" : (4, 0, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "doc_url": "https://github.com/lukastomasek/blender-automation-tools",
    "category" : "Generic"
}

class Utils():

    @staticmethod 
    def duplicate_object(original):
        new = original.copy()
        new.data = original.data.copy()
        new.name = original.name

        return new

    @staticmethod
    def constains_id(target, id):
        return id in target

    
    @staticmethod
    def check_intersection_with_walls(obj):
        """
        Checks if the object with the given name intersects with any walls.
        Walls are identified by their names ending with '_walls'.
        """
        # Get the object by name
        if obj is None:
            print(f"Object '{obj_name}' not found.")
            return None

        def get_world_bound_box(obj):
            """
            Converts the local bounding box coordinates of an object to world coordinates.
            """
            return [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]

        def check_intersection(obj, other_obj):
            """
            Checks if two objects intersect based on their bounding boxes.
            """
            obj_bbox_world = get_world_bound_box(obj)
            other_obj_bbox_world = get_world_bound_box(other_obj)

            # Check if bounding boxes intersect
            return any(corner in other_obj_bbox_world for corner in obj_bbox_world)

        # Get all wall objects
        wall_objects = [o for o in bpy.data.objects if o.name.endswith('_walls')]

        # Check for intersections
        intersecting_walls = [wall for wall in wall_objects if check_intersection(obj, wall)]

        if intersecting_walls:
            print(f"'{obj.name}' intersects with the following walls:")
            for wall in intersecting_walls:
                self.report({'INFO'},(f"- {wall.name}"))
        else:
            print(f"'{obj.name}' does not intersect with any walls.")

        return intersecting_walls

class Panel(bpy.types.Panel):
    bl_label = 'Baseboard Builder'
    bl_name = 'Baseboard Automation Tools'
    bl_idname = 'baseboard_builder_automation_tools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Baseboard Builder")
        col = layout.column(align=True)
        col.operator("baseboard.generate", text="Generate Baseboards")


class Generate(bpy.types.Operator):
    bl_idname = "baseboard.generate"
    bl_label = "Generate Baseboards"  

    def execute(self, context):
        self.create(context)
        self.report({'INFO'}, "Baseboard generated")

        return {'FINISHED'}

    def create(self, context):
        planes = [] 
        baseboard_placeholder = bpy.data.objects['baseboard_placeholder']
        default_height = 0.111787

        if baseboard_placeholder is None:
            self.report({'ERROR'}, "Baseboard placeholder not found")
            return

        baseboard_id = 'BaseBoard1'
        placeholder_children = baseboard_placeholder.children
        baseboard = bpy.data.objects.get(baseboard_id)
        target_collection = bpy.data.collections.get('Scene Collection')

        for child in placeholder_children:
            for plane in child.children:
                 planes.append(plane)

        for plane in planes:
            parent = plane.parent
            new_baseboard = baseboard.copy()
            new_baseboard.data = baseboard.data.copy()

            new_baseboard.location = Vector((plane.location.x, plane.location.y, default_height))
            new_baseboard.name = plane.name
            new_baseboard.rotation_mode = 'XYZ'
            bpy.context.collection.objects.link(new_baseboard)
            new_baseboard.parent = parent

            # Unlink the original plane from all collections
            for collection in plane.users_collection:
                collection.objects.unlink(plane)

            # Remove the original plane from Blender's data
            bpy.data.objects.remove(plane, do_unlink=True)
            
    
        collection = bpy.data.collections.get('Collection')

        if collection is None:
            self.report({'ERROR'}, "Collection not found")
            return

        for obj in collection.objects:
            if baseboard_id in obj.name:
                collection.objects.unlink(obj)
                bpy.data.objects.remove(obj, do_unlink=True)

        planes = []
      

classes = (
 Panel,
 Generate,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
   for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__init__":
    register()