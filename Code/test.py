import open3d as o3d
import numpy as np

ply_path = "Data\ply\demo3_100.ply"
pcd = o3d.io.read_point_cloud(ply_path)

o3d.visualization.draw_geometries([pcd])
