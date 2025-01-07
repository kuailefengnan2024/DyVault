bl_info = {
    "name": "Create Folder Structure and Save",
    "blender": (2, 82, 0),
    "category": "File",
}

import bpy # type: ignore
import os
from datetime import datetime

class CreateFolderStructureOperator(bpy.types.Operator):
    bl_idname = "object.create_folder_structure"
    bl_label = "Create Folder Structure and Save"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        directory = context.scene.directory
        folder_name = context.scene.folder_name
        
        if not directory:
            self.report({'ERROR'}, "请指定一个目录")
            return {'CANCELLED'}

        if not folder_name:
            self.report({'ERROR'}, "请指定文件夹名称")
            return {'CANCELLED'}

        # 获取当前日期
        current_date = datetime.now().strftime("%y%m%d")
        full_folder_name = f"{current_date}_{folder_name}"

        # 设置要创建的主目录路径
        base_dir = os.path.join(directory, full_folder_name)

        # 定义子文件夹
        subfolders = ['Sketch', 'Tex', 'Blender', 'Output', 'Fbx', 'Postprocess']

        # 创建主文件夹
        os.makedirs(base_dir, exist_ok=True)

        # 创建子文件夹
        for subfolder in subfolders:
            os.makedirs(os.path.join(base_dir, subfolder), exist_ok=True)

        # 保存当前Blender文件到Blender子文件夹
        blender_subfolder = os.path.join(base_dir, 'Blender')
        os.makedirs(blender_subfolder, exist_ok=True)

        # 获取当前Blender文件的路径
        current_blend_file = bpy.data.filepath
        new_blend_file_path = os.path.join(blender_subfolder, f"{folder_name}.blend")

        # 如果当前没有打开的Blender文件，先保存
        if not current_blend_file:
            bpy.ops.wm.save_as_mainfile(filepath=new_blend_file_path)
        else:
            # 如果已经有打开的文件，直接重命名并保存
            bpy.ops.wm.save_as_mainfile(filepath=new_blend_file_path)

        self.report({'INFO'}, f"文件夹 {full_folder_name} 和子文件夹创建成功，Blender文件已保存！")
        return {'FINISHED'}

class CreateFolderStructurePanel(bpy.types.Panel):
    bl_label = "Folder Structure Creator"
    bl_idname = "OBJECT_PT_folder_creator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "directory")
        layout.prop(context.scene, "folder_name")
        layout.operator(CreateFolderStructureOperator.bl_idname)

def register():
    bpy.types.Scene.directory = bpy.props.StringProperty(
        name="Directory",
        description="Directory to create folder structure",
        default="D:\\BaiduSyncdisk\\工作整理",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.folder_name = bpy.props.StringProperty(
        name="Folder Name",
        description="Name for the main folder",
        default=""
    )
    
    bpy.utils.register_class(CreateFolderStructureOperator)
    bpy.utils.register_class(CreateFolderStructurePanel)

def unregister():
    del bpy.types.Scene.directory
    del bpy.types.Scene.folder_name
    
    bpy.utils.unregister_class(CreateFolderStructureOperator)
    bpy.utils.unregister_class(CreateFolderStructurePanel)

if __name__ == "__main__":
    register()