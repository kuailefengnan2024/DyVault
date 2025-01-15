bl_info = {
    "name": "BakeNodeMotion",
    "author": "Your Name",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Tool > BakeNodeMotion",
    "description": "将几何节点动画烘焙为普通动画",
    "category": "Animation",
}

import bpy


# 定义烘焙函数
def bake_geometry_nodes_animation(start_frame, end_frame):
    # 获取当前活动对象
    active_obj = bpy.context.object
    if not active_obj:
        bpy.ops.object.dialog_operator('INVOKE_DEFAULT', message="请先选择一个对象！")
        return

    # 创建依赖图
    depsgraph = bpy.context.evaluated_depsgraph_get()

    # 创建一个新的网格和对象，用于存储烘焙后的动画
    baked_mesh = bpy.data.meshes.new("BakedMesh")
    baked_object = bpy.data.objects.new("BakedObject", baked_mesh)
    bpy.context.collection.objects.link(baked_object)

    # 遍历帧并烘焙动画
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)
        evaluated_obj = active_obj.evaluated_get(depsgraph)

        # 从当前帧的几何节点创建新的网格
        evaluated_mesh = bpy.data.meshes.new_from_object(evaluated_obj)
        baked_object.data = evaluated_mesh

        # 插入关键帧（位置、旋转、缩放）
        baked_object.location = active_obj.location
        baked_object.keyframe_insert(data_path="location", frame=frame)
        baked_object.rotation_euler = active_obj.rotation_euler
        baked_object.keyframe_insert(data_path="rotation_euler", frame=frame)
        baked_object.scale = active_obj.scale
        baked_object.keyframe_insert(data_path="scale", frame=frame)

    # 恢复到当前帧
    bpy.context.scene.frame_set(bpy.context.scene.frame_current)


# 定义操作类
class OBJECT_OT_BakeGeometryNodes(bpy.types.Operator):
    """烘焙几何节点动画"""
    bl_idname = "object.bake_geometry_nodes"
    bl_label = "烘焙几何节点动画"
    bl_options = {'REGISTER', 'UNDO'}

    start_frame: bpy.props.IntProperty(
        name="开始帧",
        default=1,
        min=1,
        description="动画烘焙的开始帧"
    )
    end_frame: bpy.props.IntProperty(
        name="结束帧",
        default=100,
        min=1,
        description="动画烘焙的结束帧"
    )

    def execute(self, context):
        bake_geometry_nodes_animation(self.start_frame, self.end_frame)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


# 定义面板类
class VIEW3D_PT_BakeGeometryNodesPanel(bpy.types.Panel):
    """UI面板"""
    bl_label = "BakeNodeMotion"
    bl_idname = "VIEW3D_PT_bake_geometry_nodes"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.operator(OBJECT_OT_BakeGeometryNodes.bl_idname)


# 注册和注销
classes = [OBJECT_OT_BakeGeometryNodes, VIEW3D_PT_BakeGeometryNodesPanel]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()