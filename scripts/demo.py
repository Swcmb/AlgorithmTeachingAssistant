#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AlgorithmTeachingAssistant 知识库演示程序
展示系统的主要功能
"""

import json
from pathlib import Path

from .common import get_project_root

PROJECT_ROOT = get_project_root()


class KnowledgeBaseDemo:
    def __init__(self):
        self.root_dir = PROJECT_ROOT / "references" / "db"
        
        print("="*60)
        print("  AlgorithmTeachingAssistant 知识库系统")
        print("="*60)
    
    def show_structure(self):
        print("\n📁 知识库目录结构:")
        print("-"*40)
        
        dirs = [
            ("INDEX.md", "全局索引"),
            ("TAGS.md", "标签索引"),
            ("SUMMARY.md", "全局摘要"),
            ("summaries/", "模块摘要"),
            ("markdown/", "Markdown文档"),
            ("code/", "代码示例"),
            ("embeddings/", "向量索引"),
        ]
        
        for path, desc in dirs:
            full_path = self.root_dir / path
            exists = full_path.exists()
            status = "✅" if exists else "❌"
            print(f"{status} {desc:15} - {path}")
    
    def load_index(self):
        print("\n📑 全局索引信息:")
        print("-"*40)
        
        index_file = self.root_dir / "INDEX.md"
        if index_file.exists():
            content = index_file.read_text(encoding="utf-8")[:500]
            print(content)
            print("\n... (更多内容请查看完整文件)")
        
        print("\n🏷️ 标签索引:")
        tags_file = self.root_dir / "TAGS.md"
        if tags_file.exists():
            tags_content = tags_file.read_text(encoding="utf-8")
            if "基础算法" in tags_content:
                print("✅ 标签分类完整")
    
    def show_summaries(self):
        print("\n📋 模块摘要列表:")
        print("-"*40)
        
        summary_dir = self.root_dir / "summaries"
        if summary_dir.exists():
            summary_files = list(summary_dir.glob("*.md"))
            for sf in summary_files:
                print(f"✅ {sf.name}")
    
    def show_file_hash(self):
        hash_file = self.root_dir / "file_hash.json"
        if hash_file.exists():
            with open(hash_file, "r", encoding="utf-8") as f:
                file_hash = json.load(f)
                print(f"\n🔢 索引文件数量: {len(file_hash)}")
                print("   前5个文件:")
                for i, (path, _) in enumerate(list(file_hash.items())[:5]):
                    print(f"   {i+1}. {path}")
    
    def show_key_stats(self):
        print("\n📊 知识库统计:")
        print("-"*40)
        
        markdown_count = 0
        markdown_dir = self.root_dir / "markdown"
        if markdown_dir.exists():
            markdown_count = len(list(markdown_dir.rglob("*.md")))
        
        code_count = 0
        code_dir = self.root_dir / "code"
        if code_dir.exists():
            code_extensions = [".cpp", ".py", ".java", ".c", ".hpp", ".h"]
            for code_file in code_dir.rglob("*"):
                if code_file.suffix in code_extensions:
                    code_count += 1
        
        print(f"   Markdown文档: {markdown_count}")
        print(f"   代码示例: {code_count}")
    
    def demo_query_system(self):
        print("\n🔍 查询系统演示:")
        print("-"*40)
        
        sample_queries = [
            "如何实现二分查找",
            "Dijkstra算法的原理",
            "什么是动态规划"
        ]
        
        print("   示例查询:")
        for i, query in enumerate(sample_queries, 1):
            print(f"   {i}. {query}")
        
        print("\n   💡 使用 python -m scripts.retrieve --query \"你的问题\" 进行检索")


def main():
    demo = KnowledgeBaseDemo()
    demo.show_structure()
    demo.load_index()
    demo.show_summaries()
    demo.show_file_hash()
    demo.show_key_stats()
    demo.demo_query_system()
    
    print("\n" + "="*60)
    print("  使用方式:")
    print("="*60)
    print("  1. 查看 INDEX.md 了解全局索引")
    print("  2. 查看 TAGS.md 了解标签分类")
    print("  3. 查看 summaries/ 了解各模块内容")
    print("  4. 运行 python -m scripts.build_index 更新索引")
    print("  5. 安装依赖后运行 python -m scripts.retrieve 体验检索功能")
    print("="*60)


if __name__ == "__main__":
    main()