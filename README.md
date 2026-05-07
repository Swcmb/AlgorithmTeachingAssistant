# AlgorithmTeachingAssistant

ACM/ICPC竞赛算法教学助手，基于本地RAG知识库提供精准的算法知识检索和苏格拉底式教学指导。

## 🚀 功能特点

- **算法知识检索**：基于RAG知识库进行语义检索，快速定位相关知识点
- **苏格拉底式教学**：引导学生主动思考，培养独立解题能力
- **学习路径规划**：根据学生水平提供个性化学习建议
- **代码指导**：提供Python/C++代码模板和实现技巧

## 📁 目录结构

```
AlgorithmTeachingAssistant/
├── SKILL.md                    # 核心指令文件
├── README.md                   # 项目说明文档
├── package.json                # Node.js 配置
└── scripts/
    ├── common.py               # 通用工具函数
    ├── retrieve.py             # 知识检索模块
    ├── build_index.py          # 索引构建脚本
    ├── demo.py                 # 演示程序
    ├── test_basic.py           # 基础测试脚本
    └── requirements.txt        # Python依赖清单
└── references/db/              # RAG知识库
    ├── INDEX.md, TAGS.md, SUMMARY.md
    ├── summaries/              # 6个核心模块摘要
    ├── markdown/               # Markdown文档（463+文件）
    ├── code/                   # 代码示例（458+文件）
    └── embeddings/             # ChromaDB向量索引
```

## 📦 安装方式

### 依赖安装

```bash
# 安装 Python 依赖
cd scripts
pip install -r requirements.txt

# 或使用 conda
conda create -n algo-assistant python=3.10
conda activate algo-assistant
pip install chromadb sentence-transformers
```

## 🚀 使用说明

### 命令行工具

```bash
# 执行知识检索
python -m scripts.retrieve --query "动态规划" --top_k 5

# 按分类过滤检索
python -m scripts.retrieve --query "链表" --category ds --top_k 3

# 更新索引（增量）
python -m scripts.build_index

# 重建索引（全量）
python -m scripts.build_index --rebuild

# 查看统计信息
python -m scripts.build_index --stats

# 运行演示程序
python -m scripts.demo

# 运行测试
python -m scripts.test_basic
```

### Python API

```python
from scripts.retrieve import KnowledgeRetriever, RAGPipeline

# 初始化检索器
retriever = KnowledgeRetriever()

# 执行查询
results = retriever.search(
    query="Dijkstra 最短路径",
    top_k=5,
    category="graph"  # 可选：basic/dp/ds/graph/math/string
)

# 使用 RAG 管道
pipeline = RAGPipeline(retriever)
result = pipeline.query("什么是动态规划", top_k=3)

print(f"分析结果: {result['analysis']}")
print(f"相关来源: {result['sources']}")
```

## 🔧 模块分类

| 模块 | 核心内容 |
|------|---------|
| 算法基础 (basic) | 复杂度、枚举、模拟、排序、二分、分治、贪心 |
| 动态规划 (dp) | 背包、区间、状压、树形、数位、DP优化 |
| 数据结构 (ds) | 并查集、树状数组、线段树、平衡树、分块 |
| 图论 (graph) | DFS/BFS、最短路、MST、SCC、网络流、二分图 |
| 字符串 (string) | 哈希、KMP、Trie、AC自动机、后缀自动机 |
| 数学 (math) | 数论、组合数学、线性代数、多项式、博弈论 |

## 🎯 触发场景

当用户说以下内容时自动触发：
- 学习相关：学算法、ACM训练、竞赛刷题、算法入门
- 专题相关：动态规划、图论、数据结构、数论、OI、ICPC、Codeforces、LeetCode
- 系统相关：请检索、查询知识库

## 📝 测试用例

| 测试项 | 输入 | 预期输出 |
|--------|------|---------|
| 概念理解 | "什么是动态规划？" | 定义、核心思想、适用条件、例题 |
| 算法实现 | "用Python实现Dijkstra算法" | 完整代码、复杂度分析、示例 |
| 解题思路 | "如何解决最长公共子序列问题？" | 问题分析、状态定义、转移方程 |
| 代码调试 | "我的二分查找总是死循环" | 错误分析、边界处理、正确实现 |

## 📄 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！