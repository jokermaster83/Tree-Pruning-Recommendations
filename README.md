## ✂️ Pruning Recommendation System Based on 3D Branch Classification

本项目基于果树枝条的三维层级分类结果，结合**农业修剪规则**，自动识别需要修剪的枝条类型并输出推荐列表。该系统适用于现代果树精准修剪任务，提升果树管理智能化水平。

---

### 📌 项目简介

输入一个已完成树枝分类的结果（如层级标签、空间结构等），系统自动分析枝条的空间姿态、生长方向和竞争关系，识别出以下三类待剪枝：

* 🟥 **背上枝**（Dorsal branches）
* 🟩 **内膛枝/向心枝**（Centripetal branches）
* 🟦 **竞争枝**（Competitive branches）

并输出这些枝条的空间位置与属性信息，供人工或机器人修剪使用。

---

### 🎯 功能特性

* ✅ 支持从树枝层级分类结果中自动识别剪枝对象
* ✅ 可输出剪枝建议的空间位置、类型与对应的父分支信息
* ✅ 模块化设计，可与三维重建、树枝分类模块直接对接
* ✅ 支持添加剪枝规则，如角度阈值、重叠度、密度限制等

---

### 🖼️ 示例结果

> 可视化图待补充，建议展示不同颜色标记不同类型剪枝枝条的点云。

---

### 🗂️ 项目结构

```bash
Pruning-Recommendation/
│
├── pruning/                         # 核心剪枝算法
│   ├── __init__.py
│   ├── pruning_rules.py             # 剪枝规则实现
│   └── pruning_recommender.py       # 剪枝推荐主逻辑
│
├── data/
│   ├── branch_hierarchy.json        # 输入：树枝层级分类结构
│   └── skeleton_points.ply          # 输入：骨架结构点云
│
├── results/
│   └── pruning_result.json          # 输出：剪枝建议数据
│
├── run.py                           # 一键运行脚本
├── requirements.txt
└── README.md
```

---

### ⚙️ 环境安装

```bash
python -m venv venv
venv\Scripts\activate  # 或 source venv/bin/activate
pip install -r requirements.txt
```

---

### 🚀 快速开始

```bash
python run.py --input ./data/branch_hierarchy.json --output ./results/
```

---

### 📤 输出说明

输出文件：`results/pruning_result.json`

```json
[
  {
    "branch_id": 17,
    "type": "dorsal",
    "parent_branch": 4,
    "length": 0.28,
    "angle_with_parent": 125.3,
    "start_point": [1.34, 2.25, 0.84]
  },
  ...
]
```

字段说明：

| 字段名                 | 含义                                            |
| ------------------- | --------------------------------------------- |
| `branch_id`         | 被剪枝条的唯一 ID                                    |
| `type`              | 剪枝类型：`dorsal` / `centripetal` / `competitive` |
| `parent_branch`     | 所属上级枝条 ID                                     |
| `angle_with_parent` | 与父枝夹角（用于判断姿态）                                 |
| `start_point`       | 枝条起点坐标（修剪定位）                                  |

---

### ✂️ 剪枝规则说明（默认）

| 类型  | 判定依据（示例）               |
| --- | ---------------------- |
| 背上枝 | 与主干向上生长，夹角 > 120°，位置靠上 |
| 向心枝 | 朝向主干中心生长，内膛区域密集        |
| 竞争枝 | 与主枝同方向、长度接近、角度小于20°    |

可根据树种和管理策略修改 `pruning_rules.py` 自定义规则。

---

### 🧪 单元测试

```bash
pytest tests/
```

---

### 🔗 上游依赖项目

* [Tree-Branch-Classification](https://github.com/jokermaster83/Tree-Branch-Classification)：提供枝条层级结构与拓扑信息

---

### 🧑‍💻 作者信息

* Author: **龚文俊 Gong Wenjun**
* GitHub: [@jokermaster83](https://github.com/jokermaster83)
* Email: `3430387198@qq.com`

---

### 📜 License

MIT License


