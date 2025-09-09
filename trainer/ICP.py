from simpleicp import PointCloud, SimpleICP
import numpy as np
import open3d as o3d
import numpy as np
import copy
def fuse_pcd_to_global(global_pcd, local_pcd, T):
    local_pcd.transform(T)
    global_pcd += local_pcd
    return
def load_pcd(pcd_path):
    pcd = o3d.io.read_point_cloud(pcd_path)
    return pcd
def crop_pcd(pcd):
    # Filter out points that are too far away
    aabb = o3d.geometry.AxisAlignedBoundingBox(np.array([-40, -40, -40]), np.array([40, 40, 40]))
    pcd = pcd.crop(aabb)
    return pcd
def apply_mask(pcd, mask):
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    norm = np.asarray(pcd.normals)
    points = points[mask.flatten()]
    colors = colors[mask.flatten()]
    norm = norm[mask.flatten()]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    pcd.normals = o3d.utility.Vector3dVector(norm)
    return pcd
def draw_registration_result(target, source, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    fuse_pcd_to_global(target_temp, source_temp, transformation)
    # Write ply
    o3d.io.write_point_cloud("source_temp.ply", target_temp)
    return

def simpleICP(pcd0,pcd1):
    mask = np.ones((376, 1408), dtype=bool)
    mask[:10, :] = False
    mask[-10:, :] = False
    mask[:, :10] = False
    mask[:, -10:] = False
    pcd0 = apply_mask(pcd0, mask)
    pcd0 = crop_pcd(pcd0)
    #print("Load second point cloud")
    pcd1 = apply_mask(pcd1, mask)
    pcd1 = crop_pcd(pcd1)
    # Read point clouds from xyz files into n-by-3 numpy arrays
    X_fix = np.asarray(pcd0.points)
    X_mov = np.asarray(pcd1.points)
    # Create point cloud objects
    pc_fix = PointCloud(X_fix, columns=["x", "y", "z"])
    pc_mov = PointCloud(X_mov, columns=["x", "y", "z"])
    # Create simpleICP object, add point clouds, and run algorithm!
    icp = SimpleICP()
    icp.add_point_clouds(pc_fix, pc_mov)
    H, X_mov_transformed, rigid_body_transformation_params, distance_residuals = icp.run(max_overlap_distance=3.0)
    return H