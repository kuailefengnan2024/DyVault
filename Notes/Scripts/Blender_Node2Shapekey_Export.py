bl_info = {
    "name": "Geometry to MDD",
    "author": "Shader Expert",
    "version": (1, 3, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > DonyanScripts Tab",
    "description": "Export Geometry Nodes Animation as Alembic (ABC) and Convert to MDD with Frame Range Selection",
    "category": "3D View",
}

import bpy
import os

class GeometryToMDDOperator(bpy.types.Operator):
    """Export selected object's Geometry Nodes animation to Alembic (.abc) and convert it to MDD in one step"""
    bl_idname = "object.geometry_to_mdd"
    bl_label = "Export Geometry to MDD"
    bl_options = {'REGISTER', 'UNDO'}

    # 属性：用户可以选择结束帧
    frame_end: bpy.props.IntProperty(
        name="End Frame",
        description="End frame for exporting animation",
        default=250,  # 默认结束帧
        min=1
    )

    def execute(self, context):
        obj = context.object

        # 检查是否有选中物体
        if obj is None:
            self.report({'ERROR'}, "No object selected. Please select an object.")
            return {'CANCELLED'}

        # 检查 Blender 文件是否已保存
        blend_dir = os.path.dirname(bpy.data.filepath)
        if not blend_dir:
            self.report({'ERROR'}, "Please save the Blender file before proceeding.")
            return {'CANCELLED'}

        # Alembic 文件和 MDD 文件路径
        abc_path = os.path.join(blend_dir, f"{obj.name}.abc")
        mdd_path = os.path.join(blend_dir, f"{obj.name}.mdd")

        try:
            # 导出 Alembic 文件
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.wm.alembic_export(
                filepath=abc_path,
                selected=True,
                use_instancing=False
            )
            self.report({'INFO'}, f"Successfully exported to {abc_path}")

            # 导入 Alembic 文件
            bpy.ops.wm.alembic_import(filepath=abc_path)
            imported_obj = bpy.context.selected_objects[0]

            # 检查是否支持 MDD 导出功能
            if not hasattr(bpy.ops, "export_shape.mdd"):
                self.report({'ERROR'}, "MDD export operator not found. Ensure you have the necessary plugin installed.")
                return {'CANCELLED'}

            # 导出为 MDD 文件
            bpy.ops.object.select_all(action='DESELECT')
            imported_obj.select_set(True)
            bpy.context.view_layer.objects.active = imported_obj

            bpy.ops.export_shape.mdd(
                filepath=mdd_path,
                frame_start=bpy.context.scene.frame_start,
                frame_end=self.frame_end  # 使用用户选择的结束帧
            )
            self.report({'INFO'}, f"Successfully exported to {mdd_path}")

            # 导入 MDD 文件
            bpy.ops.import_shape.mdd(filepath=mdd_path)
            self.report({'INFO'}, f"Successfully imported MDD from {mdd_path}")

        except Exception as e:
            self.report({'ERROR'}, f"An error occurred: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

    def invoke(self, context, event):
        # 在用户点击操作按钮时弹出对话框以设置参数
        return context.window_manager.invoke_props_dialog(self)

class GeometryToMDDPanel(bpy.types.Panel):
    """Geometry to MDD 的工具面板"""
    bl_label = "Geometry to MDD"
    bl_idname = "VIEW3D_PT_geometry_to_mdd"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DonyanScripts"

    def draw(self, context):
        layout = self.layout
        layout.operator(GeometryToMDDOperator.bl_idname, text="Export to MDD (with Frame Range)")

# 注册和卸载函数
def register():
    bpy.utils.register_class(GeometryToMDDOperator)
    bpy.utils.register_class(GeometryToMDDPanel)

def unregister():
    bpy.utils.unregister_class(GeometryToMDDOperator)
    bpy.utils.unregister_class(GeometryToMDDPanel)

if __name__ == "__main__":
    register()