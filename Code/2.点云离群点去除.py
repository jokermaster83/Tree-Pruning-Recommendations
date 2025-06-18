import open3d as o3d
import numpy as np

ply_path = r"Data\ply\demo2_25.ply"

pcd = o3d.io.read_point_cloud(ply_path)
o3d.visualization.draw_geometries([pcd])

res = pcd.remove_statistical_outlier(20, 0.5)  # 统计方法剔除
print("原始点云中点的个数为：", np.asarray(pcd.points).shape[0])

pcd = res[0]
o3d.visualization.draw_geometries([pcd])
print("去噪后点云中点的个数为：", np.asarray(pcd.points).shape[0])

# 保存去噪后的点云
output_ply_path = "Data/ply/demo2_25.ply"
o3d.io.write_point_cloud(output_ply_path, pcd)
print("已保存去噪后的点云至:", output_ply_path)