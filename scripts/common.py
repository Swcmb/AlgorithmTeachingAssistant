#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AlgorithmTeachingAssistant - 通用工具模块
提供文件处理、文本操作、配置管理等通用功能
"""

import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


def compute_file_hash(file_path: Path) -> str:
    """计算文件的 SHA256 哈希值"""
    h = hashlib.sha256()
    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(file_path: Path) -> Dict[str, Any]:
    """加载 JSON 文件"""
    if file_path.exists():
        return json.loads(file_path.read_text(encoding="utf-8"))
    return {}


def save_json(file_path: Path, data: Dict[str, Any], indent: int = 2):
    """保存数据到 JSON 文件"""
    file_path.write_text(
        json.dumps(data, indent=indent, ensure_ascii=False), 
        encoding="utf-8"
    )


def read_file(file_path: Path) -> str:
    """读取文件内容"""
    return file_path.read_text(encoding="utf-8", errors="ignore")


def tokenize_chinese(text: str) -> List[str]:
    """中文文本分词，保留英文单词作为整体"""
    tokens = []
    for word in text.lower().split():
        cjk_chars = re.findall(r'[\u4e00-\u9fff]', word)
        if cjk_chars and len(cjk_chars) == len(word):
            tokens.extend(cjk_chars)
        else:
            tokens.append(word)
    return tokens


def chunk_text(content: str, chunk_size: int = 500) -> List[str]:
    """将文本切分为指定大小的块"""
    chunks = []
    buffer = ""
    for line in content.split("\n"):
        if len(buffer) + len(line) > chunk_size and buffer:
            chunks.append(buffer.strip())
            buffer = line + "\n"
        else:
            buffer += line + "\n"
    if buffer.strip():
        chunks.append(buffer.strip())
    return chunks


def extract_metadata(file_path: Path, data_root: Path) -> Dict[str, Any]:
    """从文件路径提取元数据"""
    rel = file_path.relative_to(data_root)
    parts = rel.parts
    category = parts[0] if parts else "other"
    title = file_path.stem.replace("_", " ").replace("-", " ")
    
    tags = []
    for part in rel.parts[:3]:
        tags.extend(part.replace("_", " ").replace("-", " ").split())
    
    return {
        "source": str(rel),
        "category": category,
        "title": title,
        "tags": tags[:5],
        "file_type": file_path.suffix.lstrip("."),
    }


def format_results(results: List[Dict[str, Any]]) -> str:
    """格式化检索结果为可读字符串"""
    if not results:
        return "  (无结果)"
    
    lines = [f"\n检索结果（共 {len(results)} 条）", "=" * 55]
    for i, result in enumerate(results, 1):
        lines.append(f"\n  [{i}] {result.get('title', '')}")
        lines.append(f"  分类: {result.get('category', '')}  |  评分: {result.get('score', '')}")
        lines.append(f"  来源: {result.get('source', '')}")
        summary = result.get('summary', '')
        lines.append(f"  摘要: {summary[:200]}{'...' if len(summary) > 200 else ''}")
        if result.get("tags"):
            lines.append(f"  标签: {', '.join(result['tags'])}")
        lines.append("  " + "-" * 50)
    
    return "\n".join(lines)


def ensure_dir(path: Path):
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)


def get_project_root() -> Path:
    """获取项目根目录"""
    return Path(__file__).resolve().parent.parent