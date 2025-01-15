bl_info = {
    "name": "Geometry to MDD",
    "author": "Shader Expert",
    "version": (1, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > DonyanScripts Tab",
    "description": "Export Geometry Nodes Animation as Alembic (ABC) and Convert to MDD",
    "category": "3D View",
}

import bpy
import os

class ExportGeometryToABC(bpy.types.Operator):
    """Export selected object's Geometry Nodes animation to Alembic (.abc)"""
    bl_idname = "export.geometry_to_abc"
    bl_label = "Export Geometry Nodes to ABC"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        # 检查是否有选中物体
        if obj is None:
            self.report({'ERROR'}, "No object selected. Please select an object.")
            return {'CANCELLED'}
        
        # 检查 Blender 文件是否已保存
        blend_dir = os.path.dirname(bpy.data.filepath)
        if not blend_dir:
            self.report({'ERROR'}, "Please save the Blender file before exporting.")
            return {'CANCELLED'}
        
        # 输出路径
        abc_path = os.path.join(blend_dir, f"{obj.name}.abc")
        try:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            # 导出 Alembic 文件
            bpy.ops.wm.alembic_export(
                filepath=abc_path,
                selected=True,
                use_instancing=False
            )
            self.report({'INFO'}, f"Successfully exported to {abc_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error exporting to ABC: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class ImportABCAndExportMDD(bpy.types.Operator):
    """Import Alembic (.abc), convert to MDD, and import back"""
    bl_idname = "import.abc_to_mdd"
    bl_label = "Import ABC and Export to MDD"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 检查是否保存 Blender 文件
        blend_dir = os.path.dirname(bpy.data.filepath)
        if not blend_dir:
            self.report({'ERROR'}, "Please save the Blender file before importing.")
            return {'CANCELLED'}

        # Alembic 文件路径
        obj = context.object
        if obj is None:
            self.report({'ERROR'}, "No object selected. Please select an object.")
            return {'CANCELLED'}
        
        abc_path = os.path.join(blend_dir, f"{obj.name}.abc")
        if not os.path.exists(abc_path):
            self.report({'ERROR'}, f"Alembic file not found: {abc_path}")
            return {'CANCELLED'}

        try:
            # 导入 Alembic 文件
            bpy.ops.wm.alembic_import(filepath=abc_path)
            imported_obj = bpy.context.selected_objects[0]

            # MDD 文件路径
            mdd_path = os.path.join(blend_dir, f"{imported_obj.name}.mdd")
            bpy.ops.object.select_all(action='DESELECT')
            imported_obj.select_set(True)
            bpy.context.view_layer.objects.active = imported_obj

            # 导出为 MDD 文件
            bpy.ops.export_shape.mdd(
                filepath=mdd_path,
                frame_start=bpy.context.scene.frame_start,
                frame_end=bpy.context.scene.frame_end
            )
            self.report({'INFO'}, f"Successfully exported to {mdd_path}")

            # 导入 MDD 文件
            bpy.ops.import_shape.mdd(filepath=mdd_path)
            self.report({'INFO'}, f"Successfully imported MDD from {mdd_path}")
        except Exception as e:
            self.report({'ERROR'}, f"Error during ABC to MDD conversion: {str(e)}")
            return {'CANCELLED'}
        
        return {'FINISHED'}

class GeometryToMDDPanel(bpy.types.Panel):
    """Geometry to MDD 的面板"""
    bl_label = "Geometry to MDD Tools"
    bl_idname = "VIEW3D_PT_geometry_to_mdd"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DonyanScripts"

    def draw(self, context):
        layout = self.layout
        layout.operator(ExportGeometryToABC.bl_idname, text="Export to Alembic (.abc)")
        layout.operator(ImportABCAndExportMDD.bl_idname, text="Import ABC and Export to MDD")

# 注册和卸载函数
def register():
    bpy.utils.register_class(GeometryToMDDPanel)
    bpy.utils.register_class(ExportGeometryToABC)
    bpy.utils.register_class(ImportABCAndExportMDD)

def unregister():
    bpy.utils.unregister_class(ExportGeometryToABC)
    bpy.utils.unregister_class(ImportABCAndExportMDD)
    bpy.utils.unregister_class(GeometryToMDDPanel)

if __name__ == "__main__":
    register()