# AlgorithmTeachingAssistant

> ACM/ICPC 竞赛算法教学助手 - 基于本地 RAG 知识库的苏格拉底式教学系统

## 项目简介

**AlgorithmTeachingAssistant** 是一个基于 **RAG（检索增强生成）** 的算法教学助手，专为 ACM/ICPC/OI 竞赛选手设计。系统采用 **苏格拉底式教学法**，通过引导性提问帮助学生深入理解算法原理，培养独立解题能力。

### 核心特点

- **本地优先**：使用本地嵌入模型，保护隐私，无需外部 API
- **多语言支持**：中文、英文、代码三种嵌入模型自动切换
- **增量更新**：基于文件哈希的增量索引构建
- **苏格拉底式教学**：引导性提问而非直接灌输
- **难度自适应**：根据学生水平动态调整题目难度

## 项目结构

```
AlgorithmTeachingAssistant/
├── SKILL.md                    # 核心指令文件
├── README.md                   # 项目说明文档
├── package.json                # Node.js 配置
├── .github/workflows/          # GitHub Actions 自动化流程
│   └── daily-update.yml        # 每日 OI-wiki 更新任务
├── models/                     # 本地嵌入模型
│   ├── bge-small-zh-v1.5/      # 中文语义模型
│   ├── bge-small-en-v1.5/      # 英文语义模型
│   └── jina-embeddings-v2-base-code/  # 代码嵌入模型
├── scripts/                    # Python 脚本模块
│   ├── common.py               # 通用工具函数
│   ├── retrieve.py             # 知识检索模块
│   ├── build_index.py          # 索引构建脚本
│   ├── update_wiki.py          # OI-wiki 更新脚本
│   ├── demo.py                 # 演示程序
│   ├── test_basic.py           # 基础测试
│   ├── migrate.py              # 数据迁移
│   └── requirements.txt        # 依赖清单
└── references/db/              # RAG 知识库
    ├── INDEX.md                # 全局索引
    ├── TAGS.md                 # 标签索引
    ├── SUMMARY.md              # 全局摘要
    ├── summaries/              # 6个核心模块摘要
    ├── markdown/               # Markdown 文档（463+文件）
    ├── code/                   # 代码示例（458+文件）
    ├── doc/docs/               # OI Wiki 原始文档
    ├── embeddings/             # ChromaDB 向量索引
    └── file_hash.json          # 增量更新哈希记录
```

## 数据源说明

知识库的核心文档来源于 **OI-wiki** 项目：

- **来源仓库**: [OI-wiki/OI-wiki](https://github.com/OI-wiki/OI-wiki)
- **数据目录**: `references/db/doc/docs/`
- **更新方式**: 通过稀疏检出（sparse checkout）仅拉取 `docs` 目录
- **更新频率**: GitHub Actions 每日自动同步

### 初始化命令

```bash
cd references/db/doc
git init
git remote add origin https://github.com/OI-wiki/OI-wiki.git
git config core.sparsecheckout true
git fetch --depth=1 --filter=blob:none origin master
git sparse-checkout init --cone
git sparse-checkout set docs
git checkout master
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+（用于 npx skill 安装）
- 依赖包：`chromadb`, `sentence-transformers`, `jieba`
- 本地嵌入模型（需要提前下载）

### 模型下载

本项目使用三个本地嵌入模型，需要提前下载。详细的下载指引请参考 [models/README.md](models/README.md)。

```bash
# 克隆中文模型
git clone https://huggingface.co/BAAI/bge-small-zh-v1.5 models/bge-small-zh-v1.5

# 克隆英文模型
git clone https://huggingface.co/BAAI/bge-small-en-v1.5 models/bge-small-en-v1.5

# 克隆代码模型
git clone https://huggingface.co/jinaai/jina-embeddings-v2-base-code models/jina-embeddings-v2-base-code
```

| 语言/类型 | 模型名称 | 大小 |
|-----------|----------|------|
| 中文 | BAAI/bge-small-zh-v1.5 | ~430MB |
| 英文 | BAAI/bge-small-en-v1.5 | ~430MB |
| 代码 | jina-embeddings-v2-base-code | ~1.1GB |

> **注意**: 模型文件较大（约 2GB），已添加到 `.gitignore`，不会被提交到版本控制。

### 安装方式

#### 方式一：使用 npx skill 安装（推荐）

```bash
npx skill install https://github.com/Swcmb/AlgorithmTeachingAssistant
```

#### 方式二：手动克隆安装

```bash
# 克隆仓库
git clone https://github.com/Swcmb/AlgorithmTeachingAssistant
cd AlgorithmTeachingAssistant

# 安装 Python 依赖
pip install -r scripts/requirements.txt
```

### 构建索引

```bash
# 增量构建（推荐）
python -m scripts.build_index

# 全量重建
python -m scripts.build_index --rebuild

# 查看统计信息
python -m scripts.build_index --stats
```

### 执行检索

```bash
# 基本检索
python -m scripts.retrieve --query "动态规划背包问题" --top_k 5

# 按分类过滤
python -m scripts.retrieve --query "树状数组" --category ds --top_k 3
```

### 更新 OI-wiki

```bash
# 检查更新并同步
python -m scripts.update_wiki

# 更新后自动重建索引
python -m scripts.update_wiki --rebuild

# 强制更新（不检查）
python -m scripts.update_wiki --force
```

## 本地嵌入模型

系统使用以下本地模型进行向量嵌入，支持语言自动检测：

| 语言/类型 | 模型名称 | 路径 |
|-----------|----------|------|
| 中文 | BAAI/bge-small-zh-v1.5 | `models/bge-small-zh-v1.5` |
| 英文 | BAAI/bge-small-en-v1.5 | `models/bge-small-en-v1.5` |
| 代码 | jina-embeddings-v2-base-code | `models/jina-embeddings-v2-base-code` |

### 语言检测机制

- **代码模式**：检测 `def/class/import/function/return/#include/std::` 等关键词
- **中文模式**：中文字符占比超过 30%
- **英文模式**：其他情况

## 知识库模块分类

| 分类 | 核心内容 | 文件数量 |
|------|----------|----------|
| **basic** | 复杂度、枚举、模拟、排序、二分、分治、贪心 | ~50+ |
| **dp** | 背包、区间、状压、树形、数位、DP优化 | ~80+ |
| **ds** | 并查集、树状数组、线段树、平衡树、分块 | ~90+ |
| **graph** | DFS/BFS、最短路、MST、SCC、网络流、二分图 | ~120+ |
| **string** | 哈希、KMP、Trie、AC自动机、后缀自动机 | ~60+ |
| **math** | 数论、组合数学、线性代数、多项式、博弈论 | ~60+ |

## 苏格拉底式教学方法

### 提问层次金字塔

| 层次 | 类型 | 示例 | 目的 |
|------|------|------|------|
| Level 1 | 事实性问题 | "这个算法的时间复杂度是多少？" | 检验基础认知 |
| Level 2 | 理解性问题 | "为什么需要使用这种数据结构？" | 检验理解深度 |
| Level 3 | 应用性问题 | "用这个算法怎么解决这个问题？" | 检验应用能力 |
| Level 4 | 分析评价问题 | "这种方法和另一种方法各有什么优缺点？" | 培养深度思考 |

### 实战提问技巧

1. **反问追击**：答对时追问思路，答错时引导反思
2. **对比启发**：通过场景对比帮助理解概念差异
3. **极端假设**：通过极端情况理解本质原理
4. **错误引导**：故意给出错误思路让学生纠正
5. **角色互换**：让学生当老师，加深理解

## API 使用示例

```python
from scripts.retrieve import KnowledgeRetriever, RAGPipeline

# 初始化检索器
retriever = KnowledgeRetriever(use_local_models=True)

# 执行查询
results = retriever.search(
    query="Dijkstra 最短路径",
    top_k=5,
    category="graph"  # 可选：basic/dp/ds/graph/math/string
)

# 使用 RAG 管道
pipeline = RAGPipeline(retriever)
result = pipeline.query("什么是动态规划", top_k=3)

# 处理结果
for result in results:
    print(f"标题: {result['title']}")
    print(f"分类: {result['category']}")
    print(f"评分: {result['score']}")
    print(f"摘要: {result['summary']}")
    print(f"来源: {result['source']}")
```

## 典型使用场景

| 场景 | 输入示例 | 处理流程 |
|------|----------|----------|
| 概念理解 | "什么是动态规划？" | 引导提问 → 解释核心思想 → 复杂度分析 |
| 算法实现 | "用Python实现Dijkstra算法" | 引导描述步骤 → 提供代码 → 复杂度分析 |
| 解题思路 | "如何解决最长公共子序列问题？" | 问题分析 → 状态定义 → 转移方程推导 |
| 代码调试 | "我的二分查找总是死循环" | 追问代码逻辑 → 引导发现问题 → 边界条件分析 |

## 学习路线

### 入门阶段
- 语言基础（Python/C++）
- 模拟/枚举
- 基础排序
- 前缀和/差分
- 二分查找

### 提高阶段
- 贪心算法
- 基础动态规划
- DFS/BFS
- 并查集
- STL容器

### 进阶阶段
- 区间DP/背包DP
- 最短路算法
- 线段树/树状数组
- 字符串哈希/KMP

### 高级阶段
- 状压DP/树形DP
- 网络流
- 平衡树
- 后缀自动机
- 数论/组合数学

## 自动化更新

项目配置了 GitHub Actions 每日自动更新：

```yaml
# .github/workflows/daily-update.yml
on:
  schedule:
    - cron: '0 0 * * *'  # 每天UTC时间0点执行
  workflow_dispatch:       # 支持手动触发

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r scripts/requirements.txt
      - run: python -m scripts.update_wiki --rebuild
      - run: git add references/db/ && git commit -m "chore: daily OI-wiki update"
```

## 核心组件关系

```
用户请求 → 苏格拉底式教学引导 → RAGPipeline → KnowledgeRetriever → LocalEmbeddingFunction → ChromaDB
                                                         │
                                                         └── 备选方案：关键词检索
```

## 开发说明

### 目录职责

| 目录 | 职责 |
|------|------|
| `scripts/` | Python 脚本，包含检索、索引构建、Wiki更新等核心功能 |
| `models/` | 本地嵌入模型文件 |
| `references/db/` | RAG 知识库，包含文档、代码和向量索引 |
| `.github/workflows/` | CI/CD 自动化配置 |

### 代码规范

- 遵循 PEP 8 编码规范
- 使用中文注释
- 保持函数单一职责
- 提供完整的文档字符串

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！

---

*AlgorithmTeachingAssistant v3.2.0*

