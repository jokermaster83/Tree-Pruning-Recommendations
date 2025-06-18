import open3d as o3d
import numpy as np

def right_to_left_hand_conversion(points):
    # 逆时针旋转90度，将y轴和z轴交换
    converted_points = np.copy(points)
    converted_points[:, [1, 2]] = converted_points[:, [2, 1]]
    return converted_points

# 读取PLY文件
input_file = "0.Data\Plum_Dataset\PLY\\4.ply"
point_cloud = o3d.io.read_point_cloud(input_file)

# 提取点云数据并转换为NumPy数组
points_np = np.asarray(point_cloud.points)

# 执行右手坐标到左手坐标的转换
converted_points = right_to_left_hand_conversion(points_np)

# 创建新的Open3D点云对象
converted_point_cloud = o3d.geometry.PointCloud()
converted_point_cloud.points = o3d.utility.Vector3dVector(converted_points)

# 保存转换后的点云为PLY文件
output_file = "0.Data\Plum_Dataset\PLY\\4.ply"
o3d.io.write_point_cloud(output_file, converted_point_cloud)

# 可视化转换后的点云
o3d.visualization.draw_geometries([converted_point_cloud], window_name="Converted Point Cloud")
