import open3d as o3d
import trimesh as tm
import skeletor as sk
import subprocess


obj_path = "Data\obj\demo.obj"
obj_path2 = "Data\obj\demo_1000.obj"
ply_path = "Data\ply\demo.ply"
swc_path = "Data\swc\demo.swc"

# 读取模型文件
mesh = o3d.io.read_triangle_mesh(obj_path)

# 降采样
pcd= mesh.sample_points_poisson_disk(5000)  # 指定点云采样数目

# # 去噪（统计滤波）
# res = pcd.remove_statistical_outlier(20, 0.5)  # 统计方法剔除
# pcd = res[0]  # 返回点云，和点云索引

o3d.io.write_point_cloud(ply_path, pcd)

# # 坐标系转换（调用meshlab软件功能）
# subprocess.run(['meshlabserver', '-i', ply_path, '-o', ply_path, '-s', 'transform.mlx'])

# # 计算点云法向量
# pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# 点云转网格（调用meshlab软件功能）
# subprocess.run(['meshlab', ply_path,  obj_path2, meshlab_script])

# SEMC骨架提取
# 加载点云
mesh = tm.load_mesh(obj_path2)

# 预处理
fixed = sk.pre.fix_mesh(mesh, remove_disconnected=1100, inplace=True)
cont = sk.pre.contract(fixed, epsilon=1e-06, SL=1.8)

# 骨架化
skel = sk.skeletonize.by_teasar(cont, inv_dist=0.3)

# 优化处理
sk.post.clean_up(skel, inplace=True)
sk.post.radii(skel, method='knn')

# 骨架可视化
skel.show(mesh=True)
skel.save_swc(swc_path)


# o3d.visualization.draw_geometries([pcd])

