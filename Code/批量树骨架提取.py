import skeletor as sk
import trimesh as tm
import os

def skeletonize_batch(obj_paths, swc_paths):
    for obj_path, swc_path in zip(obj_paths, swc_paths):
        # loading the obj file
        mesh = tm.load_mesh(obj_path)

        # pre-processing
        fixed = sk.pre.fix_mesh(mesh, remove_disconnected=1100, inplace=True)
        cont = sk.pre.contract(fixed, epsilon=1e-06, SL=1.8)

        # skeletonization
        skel = sk.skeletonize.by_teasar(cont, inv_dist=0.3)

        # post-processing
        sk.post.clean_up(skel, inplace=True)

        # Save SWC file
        skel.save_swc(swc_path)

        # Save 3D visualization
        image_folder = "Data\images\skeleton"
        os.makedirs(image_folder, exist_ok=True)
        image_path = os.path.join(image_folder, os.path.splitext(os.path.basename(obj_path))[0] + ".png")
        skel.show(mesh=True, save_image_path=image_path)

# 文件路径列表
obj_paths = [
    "Data/ply/demo3_100.ply",
    "Data/ply/demo3_75.ply",
    "Data/ply/demo3_50.ply",
    "Data/ply/demo3_25.ply"
]

swc_paths = [
    "Data/swc/demo3_100.swc",
    "Data/swc/demo3_75.swc",
    "Data/swc/demo3_50.swc",
    "Data/swc/demo3_25.swc"
]

# 进行批量处理
skeletonize_batch(obj_paths, swc_paths)
