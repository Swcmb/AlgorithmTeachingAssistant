#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础功能测试脚本
"""

import json
from pathlib import Path

from .common import get_project_root

PROJECT_ROOT = get_project_root()


def test_index_structure():
    print("📋 测试 1: 检查索引结构")
    print("-" * 50)
    
    root = PROJECT_ROOT / "references" / "db"
    required_files = [
        "INDEX.md",
        "TAGS.md",
        "SUMMARY.md",
    ]
    
    all_exist = True
    for file_name in required_files:
        file_path = root / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} (缺失)")
            all_exist = False
    
    print(f"\n测试 1 结果: {'PASS' if all_exist else 'FAIL'}\n")
    return all_exist


def test_summaries():
    print("📚 测试 2: 检查模块摘要")
    print("-" * 50)
    
    root = PROJECT_ROOT / "references" / "db"
    summary_dir = root / "summaries"
    
    if not summary_dir.exists():
        print("❌ summaries目录不存在")
        return False
    
    required_summaries = [
        "basic_summary.md",
        "ds_summary.md",
        "graph_summary.md",
        "dp_summary.md",
        "math_summary.md",
        "string_summary.md",
    ]
    
    all_exist = True
    for summary_name in required_summaries:
        summary_path = summary_dir / summary_name
        if summary_path.exists():
            content = summary_path.read_text(encoding="utf-8")
            if "核心主题" in content:
                print(f"✅ {summary_name} (内容有效)")
            else:
                print(f"⚠️ {summary_name} (内容格式异常)")
        else:
            print(f"❌ {summary_name} (缺失)")
            all_exist = False
    
    print(f"\n测试 2 结果: {'PASS' if all_exist else 'FAIL'}\n")
    return all_exist


def test_file_hash():
    print("🔒 测试 3: 检查文件哈希")
    print("-" * 50)
    
    root = PROJECT_ROOT / "references" / "db"
    hash_file = root / "file_hash.json"
    
    if hash_file.exists():
        hash_data = json.loads(hash_file.read_text(encoding="utf-8"))
        print(f"✅ file_hash.json 存在")
        print(f"   包含 {len(hash_data)} 个文件记录")
        result = True
    else:
        print(f"❌ file_hash.json 不存在")
        result = False
    
    print(f"\n测试 3 结果: {'PASS' if result else 'FAIL'}\n")
    return result


def test_markdown_count():
    print("📝 测试 4: 检查Markdown文件")
    print("-" * 50)
    
    root = PROJECT_ROOT / "references" / "db"
    markdown_dir = root / "markdown"
    
    if markdown_dir.exists():
        count = len(list(markdown_dir.rglob("*.md")))
        print(f"✅ markdown目录存在")
        print(f"   包含 {count} 个Markdown文件")
        result = count > 0
    else:
        print(f"❌ markdown目录不存在")
        result = False
    
    print(f"\n测试 4 结果: {'PASS' if result else 'FAIL'}\n")
    return result


def test_code_count():
    print("💻 测试 5: 检查代码文件")
    print("-" * 50)
    
    root = PROJECT_ROOT / "references" / "db"
    code_dir = root / "code"
    
    if code_dir.exists():
        count = 0
        code_extensions = [".cpp", ".py", ".java", ".c", ".hpp", ".h"]
        for code_file in code_dir.rglob("*"):
            if code_file.suffix in code_extensions:
                count += 1
        print(f"✅ code目录存在")
        print(f"   包含 {count} 个代码文件")
        result = count > 0
    else:
        print(f"❌ code目录不存在")
        result = False
    
    print(f"\n测试 5 结果: {'PASS' if result else 'FAIL'}\n")
    return result


def main():
    print("=" * 60)
    print("  AlgorithmTeachingAssistant 知识库测试")
    print("=" * 60)
    
    results = []
    results.append(("索引结构", test_index_structure()))
    results.append(("模块摘要", test_summaries()))
    results.append(("文件哈希", test_file_hash()))
    results.append(("Markdown文件", test_markdown_count()))
    results.append(("代码文件", test_code_count()))
    
    print("=" * 60)
    print("  测试总结")
    print("=" * 60)
    
    all_pass = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:15} : {status}")
        if not passed:
            all_pass = False
    
    print("=" * 60)
    
    if all_pass:
        print("\n🎉 所有测试通过！知识库系统运行正常！")
        print("\n💡 接下来您可以:")
        print("  1. 查看 INDEX.md 了解全局索引")
        print("  2. 查看 TAGS.md 了解标签分类")
        print("  3. 安装依赖后使用 retrieve.py 体验检索功能")
    else:
        print("\n⚠️  部分测试未通过，请检查上述错误信息")
    
    return all_pass


if __name__ == "__main__":
    main()