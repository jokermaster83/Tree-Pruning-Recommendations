import open3d as o3d
import numpy as np

# 读取点云PLY文件
pcd = o3d.io.read_point_cloud("Data\ply\demo.ply")

# 计算法线，搜索半径1cm，只考虑邻域内的30个点
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# 1、自定义法线朝向
pcd.orient_normals_to_align_with_direction([0,1,0])

# 2、朝向相机位置
pcd.orient_normals_towards_camera_location([0,0,0])

# 3、最小生成树
# pcd.orient_normals_consistent_tangent_plane(10)

o3d.visualization.draw_geometries([pcd], point_show_normal=True, window_name="法线估计",
                                  width=1024, height=768,
                                  left=50, top=50,
                                  mesh_show_back_face=False)  # 可视化点云和法线

