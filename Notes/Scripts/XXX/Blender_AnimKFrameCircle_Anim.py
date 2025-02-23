bl_info = {
    "name": "Circular Animation K-Frame Tool",
    "author": "DonyanScripts",
    "version": (1, 7),
    "blender": (3, 6, 0),
    "location": "View3D > Tool Shelf > DonyanScripts",
    "description": "为选中的对象添加位置、缩放和旋转的循环动画，并清除动画",
    "category": "Animation",
}

import bpy
import random
import math

# 主面板类
class DONYAN_PT_CircularAnimationPanel(bpy.types.Panel):
    bl_label = "Circular Animation K-Frame"
    bl_idname = "DONYAN_PT_CircularAnimationPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "DonyanScripts"

    def draw(self, context):
        layout = self.layout
        layout.label(text="设置圆环动画参数：")
        layout.prop(context.scene, "circle_radius")
        layout.prop(context.scene, "total_frames")
        layout.prop(context.scene, "position_random_strength")
        layout.prop(context.scene, "scale_random_strength")
        layout.prop(context.scene, "rotation_random_strength")
        layout.operator("donyan.create_circular_animation", text="创建循环动画")
        layout.separator()  # 添加分隔线
        layout.operator("donyan.clear_animation", text="清除动画并重置")

# 创建动画的操作类
class DONYAN_OT_CreateCircularAnimation(bpy.types.Operator):
    bl_label = "Create Circular Animation"
    bl_idname = "donyan.create_circular_animation"
    bl_description = "为选中的对象创建位置、缩放和旋转的循环动画"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object  # 获取当前选中的对象
        if obj is None:
            self.report({'ERROR'}, "没有选中任何对象！")
            return {'CANCELLED'}

        radius = context.scene.circle_radius
        total_frames = context.scene.total_frames
        pos_strength = context.scene.position_random_strength
        scale_strength = context.scene.scale_random_strength
        rot_strength = context.scene.rotation_random_strength

        # 验证总帧数是否合理
        if total_frames < 10:
            self.report({'ERROR'}, "总帧数必须大于或等于10！")
            return {'CANCELLED'}

        # 清除已有关键帧
        if obj.animation_data:
            obj.animation_data_clear()

        # 保存初始的缩放和旋转
        initial_scale = obj.scale.copy()
        initial_rotation = obj.rotation_euler.copy()

        # 计算五等分的关键帧
        keyframes = [int(i * total_frames / 5) for i in range(6)]

        # 用于存储首帧的数据（位置、缩放、旋转）
        first_frame_data = {}

        # 添加关键帧
        for i, frame in enumerate(keyframes):
            # 位置
            angle = math.radians((frame / total_frames) * 360)  # 根据帧数计算角度
            random_pos_offset = random.uniform(-pos_strength, pos_strength) if i != 5 else first_frame_data["pos_offset"]
            x = radius * math.cos(angle + random_pos_offset)
            y = radius * math.sin(angle + random_pos_offset)

            # 缩放
            random_scale = random.uniform(1 - scale_strength, 1 + scale_strength) if i != 5 else first_frame_data["scale"]

            # 旋转
            random_rotation = random.uniform(-rot_strength, rot_strength) if i != 5 else first_frame_data["rotation"]

            # 保存首帧的数据
            if i == 0:
                first_frame_data["pos_offset"] = random_pos_offset
                first_frame_data["scale"] = random_scale
                first_frame_data["rotation"] = random_rotation

            # 设置位置
            obj.location = (x, y, obj.location.z)
            obj.keyframe_insert(data_path="location", frame=frame)

            # 设置缩放
            obj.scale = (initial_scale[0] * random_scale,
                         initial_scale[1] * random_scale,
                         initial_scale[2] * random_scale)
            obj.keyframe_insert(data_path="scale", frame=frame)

            # 设置旋转
            obj.rotation_euler = (initial_rotation[0] + random_rotation,
                                  initial_rotation[1] + random_rotation,
                                  initial_rotation[2] + random_rotation)
            obj.keyframe_insert(data_path="rotation_euler", frame=frame)

        # 确保首帧和末帧数据完全一致
        obj.location = (radius * math.cos(math.radians(0) + first_frame_data["pos_offset"]),
                        radius * math.sin(math.radians(0) + first_frame_data["pos_offset"]),
                        obj.location.z)
        obj.scale = (initial_scale[0] * first_frame_data["scale"],
                     initial_scale[1] * first_frame_data["scale"],
                     initial_scale[2] * first_frame_data["scale"])
        obj.rotation_euler = (initial_rotation[0] + first_frame_data["rotation"],
                              initial_rotation[1] + first_frame_data["rotation"],
                              initial_rotation[2] + first_frame_data["rotation"])

        # 插入末尾帧关键帧
        obj.keyframe_insert(data_path="location", frame=total_frames)
        obj.keyframe_insert(data_path="scale", frame=total_frames)
        obj.keyframe_insert(data_path="rotation_euler", frame=total_frames)

        self.report({'INFO'}, f"循环动画已成功创建！总帧数：{total_frames}")
        return {'FINISHED'}

# 清除动画并重置的操作类
class DONYAN_OT_ClearAnimation(bpy.types.Operator):
    bl_label = "Clear Animation and Reset"
    bl_idname = "donyan.clear_animation"
    bl_description = "清除选中对象的动画数据并重置变换"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object  # 获取当前选中的对象
        if obj is None:
            self.report({'ERROR'}, "没有选中任何对象！")
            return {'CANCELLED'}

        # 清除动画数据
        if obj.animation_data:
            obj.animation_data_clear()

        # 删除所有与动画相关的 fcurves
        if obj.animation_data is not None and obj.animation_data.action is not None:
            obj.animation_data.action.fcurves.clear()

        # 重置位置、缩放和旋转
        obj.location = (0.0, 0.0, 0.0)
        obj.scale = (1.0, 1.0, 1.0)
        obj.rotation_euler = (0.0, 0.0, 0.0)

        self.report({'INFO'}, "动画数据已清除，变换已重置！")
        return {'FINISHED'}

# 注册属性
def register():
    bpy.utils.register_class(DONYAN_PT_CircularAnimationPanel)
    bpy.utils.register_class(DONYAN_OT_CreateCircularAnimation)
    bpy.utils.register_class(DONYAN_OT_ClearAnimation)
    bpy.types.Scene.circle_radius = bpy.props.FloatProperty(
        name="圆环半径",
        description="设置旋转圆环的半径",
        default=5.0,
        min=0.1,
        max=100.0
    )
    bpy.types.Scene.total_frames = bpy.props.IntProperty(
        name="总帧数",
        description="设置循环动画的总帧数",
        default=60,
        min=10,
        max=1000
    )
    bpy.types.Scene.position_random_strength = bpy.props.FloatProperty(
        name="位置随机强度",
        description="控制位置随机偏移强度（可正可负）",
        default=0.2,
        min=0.0,
        max=5.0
    )
    bpy.types.Scene.scale_random_strength = bpy.props.FloatProperty(
        name="缩放随机强度",
        description="控制缩放随机偏移强度（可正可负）",
        default=0.1,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.rotation_random_strength = bpy.props.FloatProperty(
        name="旋转随机强度",
        description="控制旋转随机偏移强度（可正可负）",
        default=0.2,
        min=0.0,
        max=3.14  # 最大为pi弧度（180度）
    )

def unregister():
    bpy.utils.unregister_class(DONYAN_PT_CircularAnimationPanel)
    bpy.utils.unregister_class(DONYAN_OT_CreateCircularAnimation)
    bpy.utils.unregister_class(DONYAN_OT_ClearAnimation)
    del bpy.types.Scene.circle_radius
    del bpy.types.Scene.total_frames
    del bpy.types.Scene.position_random_strength
    del bpy.types.Scene.scale_random_strength
    del bpy.types.Scene.rotation_random_strength

if __name__ == "__main__":
    register()