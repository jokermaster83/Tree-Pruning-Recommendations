import pandas as pd
import numpy as np

def calculate_distance(node1, node2):
    return np.sqrt((node1['X'] - node2['X'])**2 + (node1['Y'] - node2['Y'])**2 + (node1['Z'] - node2['Z'])**2)

def repair_swc(swc_path):
    try:
        # Read SWC file
        data = pd.read_csv(swc_path, sep=' ', comment='#', header=None)
        data.columns = ['PointNo', 'Label', 'X', 'Y', 'Z', 'Radius', 'Parent']

        # Set Label of non-root nodes with Parent=-1 to 6 (leaf nodes)
        start_nodes = data[data['Parent'] == -1]
        for index, node in start_nodes.iterrows():
            if node['Label'] != 1:
                data.at[index, 'Label'] = 6

        # Ensure existence of a root node (Label=1)
        root_nodes = data[data['Label'] == 1]
        if root_nodes.empty:
            min_y_node = data.loc[data['Y'].idxmin()]
            data.at[min_y_node['PointNo'], 'Label'] = 1

        # Repair disconnected branches
        leaf_nodes = data[data['Label'] == 6]
        for i in range(len(leaf_nodes)):
            for j in range(i+1, len(leaf_nodes)):
                node1 = leaf_nodes.iloc[i]
                node2 = leaf_nodes.iloc[j]
                if calculate_distance(node1, node2) < 0.050:
                    data.loc[data['PointNo'].isin([node1['PointNo'], node2['PointNo']]), 'Label'] = 0
                    for node, parent in [(node1, node2), (node2, node1)]:
                        if node['Parent'] == -1:
                            data.loc[data['PointNo'] == node['PointNo'], 'Parent'] = parent['PointNo']

        # Fix node connections
        root_node = data[data['Label'] == 1].iloc[0]
        node_list = [root_node]
        while True:
            last_node = node_list[-1]
            parent_point_no = last_node['Parent']
            parent_node = data[data['PointNo'] == parent_point_no].iloc[0]
            node_list.append(parent_node)
            if parent_node['Label'] == 6 and parent_node['Parent'] == -1:
                break 

        reversed_node_list = node_list[::-1]

        for i, node in enumerate(reversed_node_list[:-1]):
            data.loc[data['PointNo'] == node['PointNo'], 'Parent'] = reversed_node_list[i+1]['PointNo']
        last_node = reversed_node_list[-1]
        child_node = data[data['Parent'] == last_node['PointNo']]
        if child_node.empty:
            raise ValueError("Last node has no child node")
        child_node = child_node.iloc[0]
        data.loc[data['PointNo'] == last_node['PointNo'], 'Parent'] = child_node['PointNo']
        data.loc[data['PointNo'] == child_node['PointNo'], 'Label'] = 1
        data.loc[data['PointNo'] == last_node['PointNo'], 'Label'] = 0

        # Save repaired data to a new SWC file
        with open(swc_path, 'w') as f:
            f.write("# SWC format file\n")
            f.write("# PointNo Label X Y Z Radius Parent\n")
            f.write("# Labels:\n")
            f.write("# 0 = undefined, 1 = root point, 5 = fork point, 6 = end point\n")
            data.to_csv(f, sep=' ', header=False, index=False, na_rep='None')
    except Exception as e:
        return str(e)

# Call the function with the SWC file path
swc_path = "Data\swc\demo2_100.swc" 
error = repair_swc(swc_path)
if error:
    print("Error occurred during SWC repair:", error)
else:
    print("SWC file repaired successfully.")
