import open3d as o3d


# 文件路径列表
ply_paths = [
    "Data/ply/demo3_100.ply",
    "Data/ply/demo3_75.ply",
    "Data/ply/demo3_50.ply",
    "Data/ply/demo3_25.ply"
]

# 对应的图片保存路径列表
image_paths = [
    "Data/images/demo3_100.png",
    "Data/images/demo3_75.png",
    "Data/images/demo3_50.png",
    "Data/images/demo3_25.png"
]

# 统一颜色
color = [0, 0.5, 0]  # 绿色

# 保存图片的函数
def save_point_cloud_image(pcd, filename):
    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)
    vis.add_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()
    vis.capture_screen_image(filename)
    vis.destroy_window()

# 处理每个点云文件并保存图片
for ply_path, image_path in zip(ply_paths, image_paths):
    pcd = o3d.io.read_point_cloud(ply_path)
    pcd.paint_uniform_color(color)
    save_point_cloud_image(pcd, image_path)


