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

import bpy

bl_info = {
    "name" : "3dStaged Automation Tools",
    "author" : "Lukas Tomasek",
    "description" : "3dStaged Automation Tools",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


class Panel(bpy.types.Panel):
 bl_label = '3dStaged Automation Tools'
 bl_name = '3dStaged Automation Tools'
 bl_idname = '3dstaged_automation_tools'
 bl_space_type = 'VIEW_3D'
 bl_region_type = 'UI'
 bl_category = 'Tool'

 def draw(self, context):
    layout = self.layout
    scene = context.scene

    layout.label(text="3dStaged Automation Tools")

def register():
    bpy.utils.register_class(Panel)

def unregister():
    bpy.utils.unregister_class(Panel)