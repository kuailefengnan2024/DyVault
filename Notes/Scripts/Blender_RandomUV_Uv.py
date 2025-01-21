import bpy
import bmesh
import random

bl_info = {
    "name": "随机排布UV块",
    "author": "Donyan",
    "version": (1, 6),
    "blender": (3, 6, 0),
    "location": "UV Editor > 工具",
    "description": "将8x8的UV块随机排布，保持每块内部结构完整",
    "warning": "",
    "category": "UV",
}

class UVEditorPanel(bpy.types.Panel):
    bl_label = "随机排布UV块"
    bl_idname = "IMAGE_PT_randomize_uv_blocks"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "工具"

    def draw(self, context):
        layout = self.layout
        layout.operator("uv.randomize_uv_blocks", text="随机排布UV块")

class RandomizeUVBlocksOperator(bpy.types.Operator):
    bl_idname = "uv.randomize_uv_blocks"
    bl_label = "随机排布UV块"
    bl_description = "将8x8的UV块随机排布，保持每块内部结构完整"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            # 获取当前活动对象
            obj = context.object
            if not obj or obj.type != "MESH":
                self.report({"ERROR"}, "请选中一个网格对象并确保在UV编辑模式中")
                return {"CANCELLED"}

            # 确保进入编辑模式
            if bpy.context.mode != "EDIT_MESH":
                self.report({"ERROR"}, "请进入编辑模式后再运行此操作")
                return {"CANCELLED"}
            
            # 获取当前网格的 BMesh 数据
            bm = bmesh.from_edit_mesh(obj.data)
            uv_layer = bm.loops.layers.uv.verify()  # 获取 UV 层

            # 定义 UV 网格的大小
            grid_size = 8  # 8x8 的 UV 网格
            block_size = 1.0 / grid_size  # 每个 UV 块的宽和高

            # 构建 UV 块的位置网格
            uv_positions = [(x * block_size, y * block_size) for y in range(grid_size) for x in range(grid_size)]

            # 随机打乱 UV 位置
            random.shuffle(uv_positions)

            # 存储每个 UV 块（以面片为单位分组）
            uv_blocks = []  # 存储所有 UV 块
            visited_faces = set()  # 已处理的面片集合

            def find_connected_faces(start_face):
                """递归查找所有相连的面片，构成一个 UV 块"""
                stack = [start_face]
                connected_faces = []

                while stack:
                    face = stack.pop()
                    if face in visited_faces:
                        continue
                    connected_faces.append(face)
                    visited_faces.add(face)

                    # 查找与当前面片相连的面片
                    for edge in face.edges:
                        for linked_face in edge.link_faces:
                            if linked_face not in visited_faces:
                                stack.append(linked_face)

                return connected_faces

            # 遍历所有面片，查找 UV 块
            for face in bm.faces:
                if face in visited_faces:
                    continue  # 跳过已处理的面片

                # 查找一个 UV 块
                connected_faces = find_connected_faces(face)
                uv_blocks.append(connected_faces)

            # 如果 UV 块数量超过 64，则限制为 64
            if len(uv_blocks) > len(uv_positions):
                self.report({"WARNING"}, "UV 块数量超过 64，多余的 UV 块将被忽略")
                uv_blocks = uv_blocks[:len(uv_positions)]

            # 遍历每个 UV 块，并将其整体移动到新的随机位置
            for uv_block, (new_origin_x, new_origin_y) in zip(uv_blocks, uv_positions):
                # 计算当前 UV 块的左下角位置
                min_x = float("inf")
                min_y = float("inf")
                for face in uv_block:
                    for loop in face.loops:
                        uv = loop[uv_layer].uv
                        min_x = min(min_x, uv.x)
                        min_y = min(min_y, uv.y)

                # 计算偏移量
                offset_x = new_origin_x - min_x
                offset_y = new_origin_y - min_y

                # 移动整个 UV 块
                for face in uv_block:
                    for loop in face.loops:
                        uv = loop[uv_layer].uv
                        uv.x += offset_x
                        uv.y += offset_y

            # 更新网格以反映更改
            bmesh.update_edit_mesh(obj.data)
            self.report({"INFO"}, "UV 块随机排布完成")
            return {"FINISHED"}

        except Exception as e:
            # 如果发生错误，报告错误信息
            self.report({"ERROR"}, f"发生错误: {e}")
            return {"CANCELLED"}

def register():
    bpy.utils.register_class(UVEditorPanel)
    bpy.utils.register_class(RandomizeUVBlocksOperator)

def unregister():
    bpy.utils.unregister_class(UVEditorPanel)
    bpy.utils.unregister_class(RandomizeUVBlocksOperator)

if __name__ == "__main__":
    register()