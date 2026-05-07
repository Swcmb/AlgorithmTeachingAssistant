# 模型下载指南

本项目需要以下三个本地嵌入模型才能正常运行：

## 模型列表

| 语言/类型 | 模型名称 | 下载地址 | 模型大小 |
|-----------|----------|----------|----------|
| 中文 | BAAI/bge-small-zh-v1.5 | [Hugging Face](https://huggingface.co/BAAI/bge-small-zh-v1.5) | ~430MB |
| 英文 | BAAI/bge-small-en-v1.5 | [Hugging Face](https://huggingface.co/BAAI/bge-small-en-v1.5) | ~430MB |
| 代码 | jina-embeddings-v2-base-code | [Hugging Face](https://huggingface.co/jinaai/jina-embeddings-v2-base-code) | ~1.1GB |

## 下载方法

### 方法一：使用 git clone（推荐）

```bash
# 创建模型目录
mkdir -p models

# 克隆中文模型
git clone https://huggingface.co/BAAI/bge-small-zh-v1.5 models/bge-small-zh-v1.5

# 克隆英文模型
git clone https://huggingface.co/BAAI/bge-small-en-v1.5 models/bge-small-en-v1.5

# 克隆代码模型
git clone https://huggingface.co/jinaai/jina-embeddings-v2-base-code models/jina-embeddings-v2-base-code
```

### 方法二：手动下载

1. 访问每个模型的 Hugging Face 页面
2. 点击 "Files and versions" 标签
3. 下载以下必要文件：
   - `config.json`
   - `model.safetensors`（或 `pytorch_model.bin`）
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `vocab.txt`（或 `vocab.json`）
   - `modules.json`
   - `1_Pooling/config.json`

4. 将下载的文件组织到对应的目录中：
   ```
   models/
   ├── bge-small-zh-v1.5/
   ├── bge-small-en-v1.5/
   └── jina-embeddings-v2-base-code/
   ```

## 目录结构要求

每个模型目录应包含以下文件：

```
bge-small-zh-v1.5/              # 或其他模型名称
├── 1_Pooling/
│   └── config.json              # 池化层配置
├── config.json                  # 模型配置
├── model.safetensors            # 模型权重（推荐）
├── pytorch_model.bin            # 模型权重（备用）
├── tokenizer.json               # Tokenizer 配置
├── tokenizer_config.json        # Tokenizer 配置
├── vocab.txt                    # 词表文件
├── modules.json                 # 模块配置
└── sentence_bert_config.json    # Sentence-BERT 配置（部分模型）
```

## 验证安装

下载完成后，运行以下命令验证模型是否正确安装：

```bash
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('models/bge-small-zh-v1.5'); print('中文模型加载成功')"
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('models/bge-small-en-v1.5'); print('英文模型加载成功')"
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('models/jina-embeddings-v2-base-code'); print('代码模型加载成功')"
```

## 注意事项

1. **模型文件较大**：三个模型总共约 2GB，请确保有足够的磁盘空间
2. **网络要求**：下载需要良好的网络连接，建议使用 Hugging Face 国内镜像
3. **git 忽略**：模型目录已添加到 `.gitignore`，不会被提交到版本控制
4. **模型版本**：请使用指定版本的模型，其他版本可能不兼容

## 常见问题

### Q: 下载速度慢怎么办？

A: 可以尝试使用 Hugging Face 镜像站，或者使用 `git clone` 时添加代理：

```bash
# 设置代理（示例）
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy http://proxy.example.com:8080

# 克隆模型
git clone https://huggingface.co/BAAI/bge-small-zh-v1.5 models/bge-small-zh-v1.5

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy
```

### Q: 模型文件缺失怎么办？

A: 如果缺少某些文件，模型可能无法正常加载。请重新下载完整的模型文件，或检查是否有文件被遗漏。

### Q: 是否支持其他模型？

A: 当前系统仅支持上述三个指定的模型。如需使用其他模型，请修改 `scripts/retrieve.py` 和 `scripts/build_index.py` 中的模型配置。