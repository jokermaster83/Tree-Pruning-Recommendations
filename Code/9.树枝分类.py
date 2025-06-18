import pandas as pd
import numpy as np
import open3d as o3d

swc_path = "0.Data\swc\\virtual_demo3.swc"

# 读取SWC文件
data = pd.read_csv(swc_path, sep=' ', comment='#', header=None)
data.columns = ['PointNo', 'Label', 'X', 'Y', 'Z', 'Radius', 'Parent']    
data['PointNo'] = data['PointNo'].astype(int)

# 添加结点
points = o3d.geometry.PointCloud()
points.points = o3d.utility.Vector3dVector(data[['X', 'Y', 'Z']].values)

# 添加颜色数组
num_points = len(points.points)
colors = np.ones((num_points, 3))  

# 找到根节点，标记为黑色
root_indices = data[data['Label'] == 1].index
colors[root_indices] = [0, 1, 1]  # Black color

# 找到分支节点，标记为红色
fork_indices = data[data['Label'] == 5].index
colors[fork_indices] = [1, 0, 0]  # Red color

# 找到叶子节点，标记为蓝色
end_indices = data[data['Label'] == 6].index
colors[end_indices] = [0, 0, 1]  # Blue color

# 找到未定义点，标记为绿色
undefined_indices = data[data['Label'] == 0].index
colors[undefined_indices] = [0, 0, 1]  # Green color

# 划分链表的类别
main_branch = []
branch_1_lists = []
branch_2_lists = []
branch_3_lists = []
# 划分分叉节点的等级
fork_level = {
    652:2,
    656:2,
    657:2,
    665:2,
    668:2,
    1991:2,
    697:2,
    1244:2,
    640:2,
    699:2,
    704:2,
    721:2,
    1990:2,
    730:2,
    732:2,
    733:2,
    1235:2,
    1970:2,
    701:2,
    634:2,
    632:2,
    629:2,
    1734:2,
    1256:2,
    1255:2,
    1252:2,
    545:2,
    1245:2,
    2018:2,
    2012:2,
    2008:2,
    594:2,
    602:2,
    607:2,
    610:2,
    613:2,
    614:2,
    616:2,
    624:2,
    1969:2,
    1962:2,
    1226:2,
    1946:2,
    939:2,
    947:2,
    956:2,
    961:2,
    980:2,
    1818:2,
    1817:2,
    1807:2,
    1686:2,
    1706:2,
    1710:2,
    1035:2,
    1717:2,
    1726:2,
    1728:2,
    1099:2,
    1740:2,
    1832:2,
    492:2,
    1835:2,
    907:2,
    1222:2,
    800:2,
    1201:2,
    1193:2,
    1190:2,
    1905:2,
    1894:2,
    831:2,
    835:2,
    844:2,
    847:2,
    1888:2,
    1878:2,
    1178:2,
    876:2,
    895:2,
    899:2,
    1845:2,
    490:2,
    1261:2,
    474:2,
    110:2,
    112:2,
    118:2,
    121:2,
    123:2,
    127:2,
    135:2,
    137:2,
    141:2,
    147:2,
    150:2,
    170:2,
    178:2,
    183:2,
    191:2,
    1511:2,
    1519:2,
    2323:2,
    1447:2,
    1545:2,
    1547:2,
    2284:2,
    201:2,
    1562:2,
    1583:2,
    2246:2,
    2243:2,
    48:2,
    64:2,
    1564:2,
    204:2,
    169:2,
    223:2,
    1349:2,
    1342:2,
    1367:2,
    372:2,
    1330:2,
    387:2,
    1640:2,
    346:2,
    2096:2,
    418:2,
    1651:2,
    436:2,
    2077:2,
    2070:2,
    2061:2,
    2059:2,
    1642:2,
    1351:2,
    2142:2,
    311:2,
    1360:2,
    243:2,
    247:2,
    251:2,
    2202:2,
    1355:2,
    318:2,
    2192:2,
    2186:2,
    1097:2,
    2178:2,
    297:2,
    1352:2,
    310:2,
    308:2
    # 614:2,
    # 144:2,
    # 437:2,
    # 161:2,
    # 164:2,
    # 354:2,
    # 398:2,
    # 538:2,
    # 532:2,
    # 531:2,
    # 340:2,
    # 443:2,
    # 444:2,
    # 498:2,
    # 272:2,
    # 483:2,
    # 285:2,
    # 141:2,
    # 288:2,
    # 140:2,
    # 435:2,
    # 595:2,
    # 427:2,
    # 585:2,
    # 383:2,
    # 133:2,
    # 44:2,
    # 61:2,
    # 75:2,
    # 76:2,
    # 78:2,
    # 377:2,
    # 376:2,
    # 126:2,
    # 60:2,
    # 466:2
    # 
    # 185:2,
    # 192:2,
    # 145:2,
    # 207:2,
    # 94:2,
    # 180:2,
    # 232:2,
    # 45:2,
    # 7:2,
    # 173:2,
    # 86:2,
    # 71:2
    #
    # 1365: 2,
    # 1355: 2,
    # 220: 2,
    # 8: 2
    # 933: 2
    # 1563:2,
    # 1598:2,
    # 1203:2,
    # 1362:2,
    # 922:2,
    # 1175:2,
    # 356:2,
    # 1586:2

}

for point_no, level in fork_level.items():
    data.loc[data['PointNo'] == point_no, 'ForkLevel'] = level

first_fork_nodes = data[(data['Label'] == 5) & (~data['PointNo'].isin(fork_level.keys()))]
for point_no in first_fork_nodes['PointNo']:
    fork_level[point_no] = 1

def build_branch_lists(start_point_no):
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
# 将节点类型为5、6的全部节点放入新列表中
key_nodes = data[data["Label"].isin([5,6])]["PointNo"].tolist()

for node in key_nodes:
    start_point_no = node
    chain = build_branch_lists(start_point_no)

    # 检查链表是否为空
    if not chain:
        continue

    start_node_level = fork_level.get(chain[0][0])
    end_node_level = fork_level.get(chain[-1][0])
    
    if chain[0][-1] == chain[-1][-1]:
        if start_node_level == end_node_level == 2 :
            branch_2_lists.append(chain)  #chain标记为branch 2
        elif start_node_level == end_node_level == 1:
            branch_1_lists.append(chain) #chain标记为branch 1
        else:
            branch_2_lists.append(chain) #chain标记为branch 2
    else:
        if end_node_level == 2:
            branch_3_lists.append(chain) #chain标记为branch 3
        elif end_node_level == 1:
            branch_2_lists.append(chain) #chain标记为branch 2
        else:
            main_branch.append(chain)  #chain标记为main_branch

# 简化节点颜色设置过程
def set_color(chain_list, color):
    for chain in chain_list:
        for node in chain:
            # 将节点编号转换为整数索引
            index = np.where(data['PointNo'].values == node[0])[0]
            if index:
                colors[index[0]] = color

# main_branch：树干
set_color(main_branch, [0, 0, 0])
# branch_1：一级枝
set_color(branch_1_lists, [1, 0, 0])

# branch_2:二级枝
set_color(branch_2_lists, [0, 0, 1])

# branch_3:三级枝
set_color(branch_3_lists, [0, 1, 0])        

# 将颜色数组应用到点云
points.colors = o3d.utility.Vector3dVector(colors)


# 创建可视化窗口
vis = o3d.visualization.Visualizer()
vis.create_window()

# 将骨架添加到可视化窗口 
lines = o3d.geometry.LineSet()
lines.points = o3d.utility.Vector3dVector(data[['X', 'Y', 'Z']].values)
lines.lines = o3d.utility.Vector2iVector(data[['PointNo', 'Parent']].values)
vis.add_geometry(points)
vis.add_geometry(lines)

# 更新可视化窗口
vis.poll_events()
vis.update_renderer()
vis.run()

# 关闭可视化窗口
vis.destroy_window()
