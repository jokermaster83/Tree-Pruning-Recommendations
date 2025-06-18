# # # 2023/6/7 13:41
import numpy as np
import open3d as o3d


# 读取点云PLY文件
pcd = o3d.io.read_point_cloud('0.Data\ply\demo_denoise.ply')


# 顶点法线估计(按n键隐藏或者显示法向量,按-或+缩小或者放大点云的体积)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))



# 平滑法向量
# pcd.orient_normals_consistent_tangent_plane(k=10)

# # Ball重建
# radii = [0.005, 0.01, 0.02, 0.04,1.0]    
# #半径列表中存储多个半径值，这意味着 Ball Pivoting 算法将进行四次迭代，每次使用不同的半径值来进行重建。
# #最终生成的模型 rec_mesh 将综合这四次迭代的结果，以获得更全面的表面覆盖和细节。
# mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(radii))

# # 泊松重建
# with o3d.utility.VerbosityContextManager(
#         o3d.utility.VerbosityLevel.Debug) as cm:
#     mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
#         pcd, depth=9)

# alpha重建
alpha = 0.055
print(f"alpha={alpha:.3f}")
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)

# 点云转为网格之后进行三维可视化
o3d.visualization.draw_geometries([pcd, mesh])
# o3d.visualization.draw_geometries([pcd2, mesh2])

# 保存网格化(mesh)后的模型为PLY文件
# o3d.io.write_triangle_mesh("0.Data\ply\demo2_denoise_mesh.ply", mesh)



