#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AlgorithmTeachingAssistant - 知识库索引构建
扫描 references/db/ 下的文档和代码，构建向量索引
"""

import argparse
from pathlib import Path
from typing import Dict, List

from .common import (
    compute_file_hash, load_json, save_json, read_file, 
    chunk_text, extract_metadata, ensure_dir, get_project_root
)

PROJECT_ROOT = get_project_root()
DATA_ROOT = PROJECT_ROOT / "references" / "db"


class IndexBuilder:
    def __init__(self, rebuild: bool = False):
        self.data_root = DATA_ROOT
        self.hash_file = self.data_root / "file_hash.json"
        self.vector_db_path = self.data_root / "embeddings" / "chroma_db"
        self.metadata_file = self.data_root / "embeddings" / "metadata.json"
        ensure_dir(self.vector_db_path)
        self.rebuild = rebuild
        self.embedding_func = None
        self._init_embedding()

    def _init_embedding(self):
        try:
            from chromadb.utils import embedding_functions
            self.embedding_func = embedding_functions.DefaultEmbeddingFunction()
        except Exception:
            pass

    def _collect_files(self) -> List[Path]:
        files = []

        targets = [
            (self.data_root / "doc" / "docs", ["*.md"]),
            (self.data_root / "markdown", ["*.md"]),
            (self.data_root / "summaries", ["*.md"]),
            (self.data_root / "code", ["*.py", "*.cpp", "*.java", "*.c", "*.h", "*.hpp"]),
        ]

        for base, patterns in targets:
            if not base.exists():
                continue
            for pattern in patterns:
                files.extend(base.rglob(pattern))

        return files

    def _detect_changes(self, files: List[Path]) -> List[Path]:
        old = load_json(self.hash_file)
        new = {}
        changed = []

        for f in files:
            key = str(f.relative_to(self.data_root))
            h = compute_file_hash(f)
            new[key] = h
            if self.rebuild or key not in old or old[key] != h:
                changed.append(f)

        save_json(self.hash_file, new)
        return changed

    def _process_files(self, files: List[Path]):
        docs, metas, ids = [], [], []
        for f in files:
            try:
                content = read_file(f)
            except Exception as e:
                print(f"  ⚠ 读取失败 {f.name}: {e}")
                continue

            meta = extract_metadata(f, self.data_root)
            for i, chunk in enumerate(chunk_text(content)):
                ids.append(f"{meta['source']}_{i}")
                docs.append(chunk)
                metas.append(meta)
        return docs, metas, ids

    def _upsert_vectors(self, docs, metas, ids):
        try:
            from chromadb import PersistentClient
            client = PersistentClient(path=str(self.vector_db_path))
            if self.rebuild:
                try:
                    client.delete_collection("algorithm_docs")
                except Exception:
                    pass
            col = client.get_or_create_collection(
                name="algorithm_docs",
                embedding_function=self.embedding_func,
            )
            col.add(documents=docs, metadatas=metas, ids=ids)
        except Exception as e:
            print(f"\n  ⚠ ChromaDB 不可用 ({e})，仅更新哈希记录")
            print("  安装: pip install chromadb")

    def _save_metadata(self, total: int, updated: int, chunks: int):
        save_json(self.metadata_file, {
            "total_files": total,
            "updated_files": updated,
            "total_chunks": chunks,
            "collection": "algorithm_docs",
        })

    def run(self):
        print("=" * 50)
        print("  AlgorithmTeachingAssistant 索引构建")
        print("=" * 50)
        print(f"  数据目录: {self.data_root}")
        print(f"  模式: {'全量重建' if self.rebuild else '增量更新'}")
        print()

        files = self._collect_files()
        print(f"  扫描到 {len(files)} 个文件")

        changed = self._detect_changes(files)
        print(f"  需要处理 {len(changed)} 个文件")

        if not changed:
            print("\n  ✅ 没有文件变化，无需更新")
            return

        docs, metas, ids = self._process_files(changed)
        if not docs:
            return

        self._upsert_vectors(docs, metas, ids)
        self._save_metadata(len(files), len(changed), len(docs))
        print(f"\n  ✅ 索引构建完成（{len(docs)} 个文档块）")


def main():
    parser = argparse.ArgumentParser(description="AlgorithmTeachingAssistant 索引构建")
    parser.add_argument("--rebuild", "-r", action="store_true", help="全量重建")
    parser.add_argument("--stats", "-s", action="store_true", help="显示统计")
    args = parser.parse_args()

    builder = IndexBuilder(rebuild=args.rebuild)

    if args.stats:
        meta_file = DATA_ROOT / "embeddings" / "metadata.json"
        hash_file = DATA_ROOT / "file_hash.json"
        if meta_file.exists():
            m = load_json(meta_file)
            print("索引统计:")
            for k, v in m.items():
                print(f"  {k}: {v}")
        if hash_file.exists():
            h = load_json(hash_file)
            print(f"  文件哈希记录: {len(h)} 条")
    else:
        builder.run()


if __name__ == "__main__":
    main()