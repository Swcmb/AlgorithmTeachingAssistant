#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AlgorithmTeachingAssistant - 知识检索模块
支持 ChromaDB 向量检索 + 备选关键词检索
"""

import argparse
from pathlib import Path
from typing import Dict, List, Optional

from .common import (
    load_json, save_json, read_file, tokenize_chinese,
    format_results, ensure_dir, get_project_root
)

PROJECT_ROOT = get_project_root()
DATA_ROOT = PROJECT_ROOT / "references" / "db"


class KnowledgeRetriever:
    def __init__(self):
        self.data_root = DATA_ROOT
        self.vector_db_path = self.data_root / "embeddings" / "chroma_db"
        self.summaries_dir = self.data_root / "summaries"
        self.markdown_dir = self.data_root / "markdown"
        self.docs_dir = self.data_root / "doc" / "docs"
        self.collection = None
        self._init_vector_db()

    def _init_vector_db(self):
        try:
            from chromadb import PersistentClient
            client = PersistentClient(path=str(self.vector_db_path))
            self.collection = client.get_collection("algorithm_docs")
        except Exception:
            pass

    def search(self, query: str, top_k: int = 5, category: Optional[str] = None) -> List[Dict]:
        if self.collection is not None:
            result = self._vector_search(query, top_k, category)
            if result:
                return result
        return self._fallback_search(query, top_k, category)

    def _vector_search(self, query: str, top_k: int, category: Optional[str]) -> List[Dict]:
        try:
            kwargs = {"query_texts": [query], "n_results": top_k}
            if category:
                kwargs["where"] = {"category": category}
            raw = self.collection.query(**kwargs)

            results = []
            for i in range(min(top_k, len(raw["documents"][0]))):
                doc = raw["documents"][0][i]
                results.append({
                    "title": raw["metadatas"][0][i].get("title", ""),
                    "summary": doc[:300] + "..." if len(doc) > 300 else doc,
                    "source": raw["metadatas"][0][i].get("source", ""),
                    "category": raw["metadatas"][0][i].get("category", ""),
                    "tags": raw["metadatas"][0][i].get("tags", []),
                    "score": round(1.0 - raw["distances"][0][i], 4),
                })
            return results
        except Exception:
            return []

    def _fallback_search(self, query: str, top_k: int, category: Optional[str]) -> List[Dict]:
        keywords = tokenize_chinese(query)
        scored: List[Dict] = []

        search_dirs = [self.summaries_dir]
        if not category or category != "summaries":
            search_dirs.extend([self.markdown_dir, self.docs_dir])

        for base in search_dirs:
            if not base.exists():
                continue
            for md in base.rglob("*.md"):
                if category and md.parent.name != category:
                    continue
                try:
                    text = read_file(md)
                except Exception:
                    continue
                hits = sum(1 for kw in keywords if kw in text.lower())
                if hits == 0:
                    continue
                title = md.stem.replace("_summary", "")
                scored.append({
                    "title": title,
                    "summary": text[:300] + "..." if len(text) > 300 else text,
                    "source": str(md.relative_to(self.data_root)),
                    "category": md.parent.name,
                    "tags": [],
                    "score": round(hits / len(keywords), 4),
                })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]


class RAGPipeline:
    def __init__(self, retriever: KnowledgeRetriever):
        self.retriever = retriever

    def query(self, question: str, top_k: int = 5) -> Dict:
        analysis = self._analyze_question(question)
        results = self.retriever.search(question, top_k=top_k)

        context = "\n\n".join([
            f"【来源: {r['source']}】\n{r['summary']}" 
            for r in results
        ])

        return {
            "question": question,
            "analysis": analysis,
            "context": context,
            "sources": [r["source"] for r in results],
            "raw_results": results
        }

    def _analyze_question(self, question: str) -> Dict:
        keywords = []
        topics = []

        topic_keywords = {
            "排序": ["sort", "排序", "快排", "归并", "冒泡", "插入排序"],
            "二分": ["binary", "二分", "查找", "搜索", "二分查找"],
            "贪心": ["greedy", "贪心"],
            "图论": ["graph", "图", "路径", "最短", "MST", "BFS", "DFS"],
            "树": ["tree", "树", "二叉", "LCA", "HLD", "树链剖分"],
            "DP": ["dp", "动态规划", "背包", "状态", "转移方程"],
            "数据结构": ["dsu", "线段树", "树状数组", "堆", "栈", "队列"],
            "数学": ["math", "数论", "FFT", "多项式", "组合"],
            "几何": ["geometry", "几何", "凸包", "半平面"]
        }

        for topic, kw_list in topic_keywords.items():
            for kw in kw_list:
                if kw in question:
                    topics.append(topic)
                    keywords.append(kw)

        return {
            "topics": topics,
            "keywords": keywords,
            "question_type": self._classify_question(question)
        }

    def _classify_question(self, question: str) -> str:
        if "如何" in question or "怎么" in question:
            return "how_to"
        elif "原理" in question or "为什么" in question:
            return "explanation"
        elif "区别" in question or "比较" in question:
            return "comparison"
        elif "实现" in question or "代码" in question:
            return "implementation"
        else:
            return "general"


def main():
    parser = argparse.ArgumentParser(description="AlgorithmTeachingAssistant 知识检索")
    parser.add_argument("--query", "-q", required=True, help="检索查询词")
    parser.add_argument("--top_k", "-k", type=int, default=5, help="返回结果数量")
    parser.add_argument("--category", "-c", help="按分类过滤")
    args = parser.parse_args()

    retriever = KnowledgeRetriever()
    results = retriever.search(args.query, args.top_k, args.category)
    print(format_results(results))


if __name__ == "__main__":
    main()