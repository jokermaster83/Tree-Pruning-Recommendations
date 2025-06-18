import pandas as pd
import numpy as np

swc_path = "0.Data\swc\\virtual_demo.swc"

# 读取SWC文件
data = pd.read_csv(swc_path, sep=' ', comment='#', header=None)
data.columns = ['PointNo', 'Label', 'X', 'Y', 'Z', 'Radius', 'Parent']


# 1.将Parent值为-1的非根节点的Label改为6；
start_nodes = data[data['Parent'] == -1]

# 将所有父节点为-1的非根节点类型设置为叶子节点，即Label==6
for index, node in start_nodes.iterrows():
    if node['Label'] != 1:
        data.at[index, 'Label'] = 6

# 检测是否存在Label值为1的根节点
root_nodes = data[data['Label'] == 1]

# 如果不存在根节点，找到Y值最小的节点，设置为根节点，并将其Label值更改为1
if root_nodes.empty:
    min_y_node = data.loc[data['Y'].idxmin()]
    data.at[min_y_node['PointNo'], 'Label'] = 1
# # 2.修复断裂树枝节点
# 定义函数计算两个节点的空间距离
def calculate_distance(node1, node2):
    distance = np.sqrt((node1['X'] - node2['X'])**2 + (node1['Y'] - node2['Y'])**2 + (node1['Z'] - node2['Z'])**2)
    return distance

# 找出所有叶子节点
leaf_nodes = data[data['Label'] == 6]

# 遍历所有叶子节点，计算两两之间的距离
for i in range(len(leaf_nodes)):
    for j in range(i+1, len(leaf_nodes)):
        node1 = leaf_nodes.iloc[i]
        node2 = leaf_nodes.iloc[j]
        distance = calculate_distance(node1, node2)
        
        # 若距离小于0.050，则处理这两个节点
        if distance < 0.050:
            print("节点 {} 和节点 {} 之间的距离为：{}".format(node1['PointNo'], node2['PointNo'], distance))
            
            # 节点类型更改为Label=0
            data.loc[data['PointNo'] == node1['PointNo'], 'Label'] = 0
            data.loc[data['PointNo'] == node2['PointNo'], 'Label'] = 0
            
            # 若其中一个节点的父节点为-1，则将-1改写为另一个节点的PointNO值
            if node1['Parent'] == -1:
                data.loc[data['PointNo'] == node1['PointNo'], 'Parent'] = node2['PointNo']
            elif node2['Parent'] == -1:
                data.loc[data['PointNo'] == node2['PointNo'], 'Parent'] = node1['PointNo']


# 3.修复节点的连接顺序
# 找到根节点，也就是Label等于1的节点
root_node = data[data['Label'] == 1].iloc[0]
node_list = [root_node]

# 遍历构建链表，直到遇到第一个节点Parent值为-1的叶子节点 (Label == 6)
while True:
    last_node = node_list[-1]
    parent_point_no = last_node['Parent']
    parent_node = data[data['PointNo'] == parent_point_no].iloc[0]
    node_list.append(parent_node)
    if parent_node['Label'] == 6 and parent_node['Parent'] == -1:
        break 

reversed_node_list = node_list[::-1]

def update_parent_values(reversed_node_list, original_data):
    # 更新反转后的节点列表中的数据到原始数据框中
    for i, node in enumerate(reversed_node_list[:-1]): # 不包括最后一个节点
        original_data.loc[original_data['PointNo'] == node['PointNo'], 'Parent'] = reversed_node_list[i+1]['PointNo']

    # 最后一个节点的父节点设置为其字节点的PointNo值
    last_node = reversed_node_list[-1]
    child_node = original_data[original_data['Parent'] == last_node['PointNo']].iloc[0]
    original_data.loc[original_data['PointNo'] == last_node['PointNo'], 'Parent'] = child_node['PointNo']

    # 子节点的Label改为1，最后一个节点的Label改为0
    original_data.loc[original_data['PointNo'] == child_node['PointNo'], 'Label'] = 1
    original_data.loc[original_data['PointNo'] == last_node['PointNo'], 'Label'] = 0

# 调用函数更新原始数据框中的 Parent 字段值
update_parent_values(reversed_node_list, data)

# 保存修复后的数据到新的SWC文件，包括标题行
with open(swc_path, 'w') as f:
    f.write("# SWC format file\n")
    f.write("# PointNo Label X Y Z Radius Parent\n")
    f.write("# Labels:\n")
    f.write("# 0 = undefined, 1 = root point, 5 = fork point, 6 = end point\n")
    data.to_csv(f, sep=' ', header=False, index=False, na_rep='None')



