bl_info = {
    "name": "Vertex Alpha Setter",
    "author": "Matías Avilés Pollak",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools",
    "description": "Paints Alpha Vertex in a specific tone",
    "doc_url": "https://github.com/Desayuno64/VertexAlphaSetter",
    "category": "Vertex Paint",
}

import bpy
import bmesh

def set_vertex_alpha(alpha):
    # get the active object and its data
    obj = bpy.context.active_object
    mesh = obj.data

    # enter edit mode and get the bmesh
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(mesh)

    # make a list of selected vertices
    selected_verts = [v for v in bm.verts if v.select]

    # get the active vertex color layer
    col_layer = bm.loops.layers.color.active

    # assign the alpha value to the selected vertices, overwriting the existing values
    for vert in selected_verts:
        for loop in vert.link_loops:
            color = loop[col_layer]
            color[3] = alpha  # set the alpha value
            loop[col_layer] = color

    # update the mesh with the modified bmesh
    bmesh.update_edit_mesh(mesh)

    # exit edit mode
    bpy.ops.object.mode_set(mode='OBJECT')

class SetVertexAlphaOperator(bpy.types.Operator):
    """Set the alpha value of selected vertices"""
    bl_idname = "object.set_vertex_alpha"
    bl_label = "Set Vertex Alpha"

    def execute(self, context):
        set_vertex_alpha(context.scene.alpha_value)
        return {'FINISHED'}

class VIEW3D_PT_VertexAlphaSetter(bpy.types.Panel):
    bl_label = "Vertex Alpha Setter"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tool"
    
    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, 'alpha_value')
        layout.operator("object.set_vertex_alpha")

def register():
    bpy.utils.register_class(SetVertexAlphaOperator)
    bpy.utils.register_class(VIEW3D_PT_VertexAlphaSetter)
    bpy.types.Scene.alpha_value = bpy.props.FloatProperty(name="Alpha Value", default=0.5)

def unregister():
    bpy.utils.unregister_class(SetVertexAlphaOperator)
    bpy.utils.unregister_class(VIEW3D_PT_VertexAlphaSetter)
    del bpy.types.Scene.alpha_value

if __name__ == "__main__":
    register()