import pandas as pd
import numpy as np
import open3d as o3d

def visualize_swc(swc_path):
    try:
        # Read SWC file
        data = pd.read_csv(swc_path, sep=' ', comment='#', header=None)
        data.columns = ['PointNo', 'Label', 'X', 'Y', 'Z', 'Radius', 'Parent']    
        data['PointNo'] = data['PointNo'].astype(int)

        # Add points
        points = o3d.geometry.PointCloud()
        points.points = o3d.utility.Vector3dVector(data[['X', 'Y', 'Z']].values)

        # Initialize colors
        num_points = len(points.points)
        colors = np.ones((num_points, 3))  

        # Find root nodes and mark them as black
        root_indices = data[data['Label'] == 1].index
        colors[root_indices] = [0, 1, 1]  # Black color

        # Find fork nodes and mark them as red
        fork_indices = data[data['Label'] == 5].index
        colors[fork_indices] = [1, 0, 0]  # Red color

        # Find end nodes and mark them as blue
        end_indices = data[data['Label'] == 6].index
        colors[end_indices] = [0, 0, 1]  # Blue color

        # Find undefined points and mark them as green
        undefined_indices = data[data['Label'] == 0].index
        colors[undefined_indices] = [0, 1, 0]  # Green color

        # Define branch levels
        fork_level = {
            1126:2,
            3369:2,
            3399:2,
            2099:2,
            2088:2,
            2054:2,
            3468:2,
            1938:2,
            3585:2,
            3591:2,
            1776:2,
            1769:2,
            3616:2,
            3762:2,
            2971:2,
            1124:2,
            1117:2,
            1092:2,
            3917:2,
            1035:2,
            1023:2,
            3356:2,
            2196:2,
            3352:2,
            3345:2,
            2970:2,
            3086:2,
            2905:2,
            2895:2,
            2861:2,
            2831:2,
            3096:2,
            2744:2,
            979:2,
            2730:2,
            3105:2,
            3147:2,
            2579:2,
            2510:2,
            3201:2,
            3238:2,
            3324:2,
            2280:2,
            2262:2,
            3103:2,
            3072:2,
            217:2,
            4212:2,
            244:2,
            265:2,
            280:2,
            331:2,
            542:2,
            466:2,
            320:2,
            460:2,
            4351:2,
            364:2,
            934:2,
            212:2,
            4362:2,
            756:2,
            75:2,
            84:2,
            199:2,
            65:2,
            85:2,
            91:2,
            123:2,
            926:2,
            147:2,
            4383:2,
            191:2,
            109:2
            # 1365: 2,
            # 1355: 2,
            # 220: 2,
            # 8: 2
            # Add more fork levels if needed
            # 933:2
            # 1563:2,
            # 1598:2,
            # 1203:2,
            # 1362:2,
            # 922:2,
            # 1175:2,
            # 356:2,
            # 1586:2
        }

        # Identify first level fork nodes
        first_fork_nodes = data[(data['Label'] == 5) & (~data['PointNo'].isin(fork_level.keys()))]
        for point_no in first_fork_nodes['PointNo']:
            fork_level[point_no] = 1

        # Function to build chain lists
        def build_chain_list(start_point_no):
            chain = []
            current_point_no = start_point_no
            current_node = data[data['PointNo'] == current_point_no].iloc[0]
            chain.append((current_node['PointNo'], current_node['Parent'], current_node['Label']))
            current_point_no = current_node['Parent']

            while True:
                current_node = data[data['PointNo'] == current_point_no].iloc[0]
                chain.append((current_node['PointNo'], current_node['Parent'], current_node['Label']))
                current_point_no = current_node['Parent']
                if current_node['Label'] != 0:
                    break
            return chain

        # Split nodes into lists based on their labels
        main_branch = []
        branch_1_lists = []
        branch_2_lists = []
        branch_3_lists = []

        for point_no, level in fork_level.items():
            data.loc[data['PointNo'] == point_no, 'ForkLevel'] = level

        for node in data[data["Label"].isin([5,6])]["PointNo"].tolist():
            start_point_no = node
            chain = build_chain_list(start_point_no)

            if not chain:  # Check if chain is empty
                continue

            start_node_level = fork_level.get(chain[0][0])
            end_node_level = fork_level.get(chain[-1][0])

            if chain[0][-1] == chain[-1][-1]:
                if start_node_level == end_node_level == 2 :
                    branch_2_lists.append(chain)
                elif start_node_level == end_node_level == 1:
                    branch_1_lists.append(chain)
                else:
                    branch_2_lists.append(chain)
            else:
                if end_node_level == 2:
                    branch_3_lists.append(chain)
                elif end_node_level == 1:
                    branch_2_lists.append(chain)
                else:
                    main_branch.append(chain)

        # Function to set colors for chain lists
        def set_color(chain_list, color):
            for chain in chain_list:
                for node in chain:
                    index = np.where(data['PointNo'].values == node[0])[0]
                    if index:
                        colors[index[0]] = color

        # Set colors for different branch levels
        set_color(main_branch, [0, 0, 0])   # Main branch
        set_color(branch_1_lists, [1, 0, 0])  # Branch 1
        set_color(branch_2_lists, [0, 0, 1])  # Branch 2
        set_color(branch_3_lists, [0, 1, 0])  # Branch 3

        # Apply colors to point cloud
        points.colors = o3d.utility.Vector3dVector(colors)

        # Create visualization window
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        # Add skeleton to visualization window 
        lines = o3d.geometry.LineSet()
        lines.points = o3d.utility.Vector3dVector(data[['X', 'Y', 'Z']].values)
        lines.lines = o3d.utility.Vector2iVector(data[['PointNo', 'Parent']].values)
        vis.add_geometry(points)
        vis.add_geometry(lines)

        # Update visualization window
        vis.poll_events()
        vis.update_renderer()
        vis.run()

        # Close visualization window
        vis.destroy_window()

    except Exception as e:
        print("Error:", e)

# Call the function with the SWC file path
swc_path = "0.Data\swc\\demo4.swc"
visualize_swc(swc_path)
