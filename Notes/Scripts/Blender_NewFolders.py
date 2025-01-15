bl_info = {
    "name": "Create Folder Structure and Save",
    "author": "Folder Master",
    "version": (1, 0, 3),
    "blender": (2, 82, 0),
    "location": "View3D > Sidebar > DonyanScripts Tab",
    "description": "Create a folder structure and save the current Blender file",
    "category": "File",
}

import bpy
import os
from datetime import datetime


class CreateFolderStructureOperator(bpy.types.Operator):
    """创建文件夹结构并保存当前的 Blender 文件"""
    bl_idname = "object.create_folder_structure"
    bl_label = "Create Folder Structure and Save"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # 获取用户输入的目录和文件夹名称
        directory = context.scene.directory
        folder_name = context.scene.folder_name

        # 错误提示：检查目录是否设置
        if not directory:
            self.report({'ERROR'}, "请指定一个有效的目录路径")
            return {'CANCELLED'}

        # 错误提示：检查文件夹名称是否设置
        if not folder_name:
            self.report({'ERROR'}, "请指定文件夹名称")
            return {'CANCELLED'}

        try:
            # 获取当前日期并组合文件夹名称
            current_date = datetime.now().strftime("%y%m%d")
            full_folder_name = f"{current_date}_{folder_name}"

            # 主文件夹路径
            base_dir = os.path.join(directory, full_folder_name)

            # 定义需要创建的子文件夹
            subfolders = ['Sketch', 'Tex', 'Blender', 'Output', 'Fbx', 'Postprocess']

            # 创建主文件夹及子文件夹
            os.makedirs(base_dir, exist_ok=True)
            for subfolder in subfolders:
                os.makedirs(os.path.join(base_dir, subfolder), exist_ok=True)

            # 保存当前 Blender 文件到 "Blender" 子文件夹
            blender_subfolder = os.path.join(base_dir, 'Blender')
            new_blend_file_path = os.path.join(blender_subfolder, f"{folder_name}.blend")

            # 如果未保存过当前 Blender 文件，直接保存新文件
            if not bpy.data.filepath:
                bpy.ops.wm.save_as_mainfile(filepath=new_blend_file_path)
            else:
                # 如果当前文件已存在路径，另存为新文件
                bpy.ops.wm.save_as_mainfile(filepath=new_blend_file_path)

            self.report({'INFO'}, f"文件夹 {full_folder_name} 和所有子文件夹创建成功，Blender 文件已保存！")
            return {'FINISHED'}

        except Exception as e:
            # 捕获意外错误并报告
            self.report({'ERROR'}, f"发生错误: {str(e)}")
            return {'CANCELLED'}


class DonyanScriptsPanel(bpy.types.Panel):
    """DonyanScripts 主工具面板"""
    bl_label = "Donyan Scripts"
    bl_idname = "VIEW3D_PT_donyan_scripts"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DonyanScripts"

    def draw(self, context):
        layout = self.layout
        layout.label(text="DonyanScripts 工具合集")
        layout.separator()


class CreateFolderStructureSubPanel(bpy.types.Panel):
    """创建文件夹结构工具的子面板"""
    bl_label = "Create Folder Structure"
    bl_idname = "VIEW3D_PT_create_folder_structure"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DonyanScripts"
    bl_parent_id = "VIEW3D_PT_donyan_scripts"  # 挂载到主面板

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "directory")  # 目录输入框
        layout.prop(context.scene, "folder_name")  # 文件夹名称输入框
        layout.operator(CreateFolderStructureOperator.bl_idname)  # 按钮绑定功能


# 注册和卸载函数
def register():
    # 添加自定义属性到 Scene
    bpy.types.Scene.directory = bpy.props.StringProperty(
        name="Directory",
        description="选择一个目录来创建文件夹结构",
        default="D:\\BaiduSyncdisk\\工作整理",  # 默认路径保留
        subtype='DIR_PATH'
    )
    bpy.types.Scene.folder_name = bpy.props.StringProperty(
        name="Folder Name",
        description="为主文件夹指定名称",
        default=""
    )

    # 注册类
    bpy.utils.register_class(DonyanScriptsPanel)  # 注册主面板
    bpy.utils.register_class(CreateFolderStructureSubPanel)  # 注册子面板
    bpy.utils.register_class(CreateFolderStructureOperator)  # 注册操作器


def unregister():
    # 删除自定义属性
    del bpy.types.Scene.directory
    del bpy.types.Scene.folder_name

    # 注销类
    bpy.utils.unregister_class(DonyanScriptsPanel)
    bpy.utils.unregister_class(CreateFolderStructureSubPanel)
    bpy.utils.unregister_class(CreateFolderStructureOperator)


if __name__ == "__main__":
    register()