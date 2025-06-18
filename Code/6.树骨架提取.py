import skeletor as sk
import trimesh as tm

def skeletonize(obj_path, swc_path):
    # loading the obj file
    mesh = tm.load_mesh(obj_path)

    # pre-processing
    fixed = sk.pre.fix_mesh(mesh, remove_disconnected=1100, inplace=True)
    cont = sk.pre.contract(fixed, epsilon=1e-06, SL=1.8)

    # skeletonization
    skel = sk.skeletonize.by_teasar(cont, inv_dist=0.3)

    # post-processing
    sk.post.clean_up(skel, inplace=True)
    # sk.post.radii(skel, method='knn')


    skel.show(mesh=True)
    skel.save_swc(swc_path)


obj_path = r"Data\obj\virtual_demo3.obj"
swc_path = r"Data\swc\virtual_demo3.swc"

skeletonize(obj_path, swc_path)
