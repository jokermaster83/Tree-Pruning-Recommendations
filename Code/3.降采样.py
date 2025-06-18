import open3d as o3d
import numpy as np

obj_path = "Data\obj\\demo2.obj"
mesh = o3d.io.read_triangle_mesh(obj_path)


print("----------100%----------")
pcd1 = mesh.sample_points_poisson_disk(63543)
print("下采样之后点的个数为：", np.asarray(pcd1.points).shape[0])
print("----------75%----------")
# 降采样
pcd2 = mesh.sample_points_poisson_disk(47658)  # 指定点云采样数目
print("下采样之后点的个数为：", np.asarray(pcd2.points).shape[0])

print("----------50%----------")
pcd3 = mesh.sample_points_poisson_disk(31772)
print("下采样之后点的个数为：", np.asarray(pcd3.points).shape[0])

print("----------25%----------")
pcd4 = mesh.sample_points_poisson_disk(15886)
print("下采样之后点的个数为：", np.asarray(pcd4.points).shape[0])

# # 保存
o3d.io.write_point_cloud("Data\ply\\demo2_100.ply",pcd1)
o3d.io.write_point_cloud("Data\ply\\demo2_75.ply", pcd2)
o3d.io.write_point_cloud("Data\ply\\demo2_50.ply", pcd3)
o3d.io.write_point_cloud("Data\ply\\demo2_25.ply", pcd4)




