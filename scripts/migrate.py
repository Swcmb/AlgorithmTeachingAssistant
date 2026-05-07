#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将知识库系统从 references 迁移到 db 目录
"""

import os
import shutil
from pathlib import Path

def main():
    project_root = Path("d:/TraeCode/AlgorithmTeachingAssistant")
    src_dir = project_root / "references"
    dst_dir = project_root / "db"
    
    print("=" * 60)
    print("  知识库系统迁移")
    print("=" * 60)
    print(f"源目录: {src_dir}")
    print(f"目标目录: {dst_dir}")
    print()
    
    # 创建目标目录
    if not dst_dir.exists():
        print(f"创建目标目录: {dst_dir}")
        dst_dir.mkdir(parents=True, exist_ok=True)
    
    # 核心文件列表
    core_files = [
        "INDEX.md",
        "TAGS.md",
        "SUMMARY.md",
        "build_index.py",
        "retrieval.py",
        "demo.py",
        "test_basic.py",
        "requirements.txt",
        "file_hash.json",
    ]
    
    # 核心目录列表
    core_dirs = [
        "summaries",
        "markdown",
        "metadata",
        "embeddings",
        "code",
        "datasets",
        "graph",
        "papers",
        "books",
        "raw",
    ]
    
    # 移动核心文件
    print("\n📄 移动核心文件:")
    print("-" * 40)
    for file_name in core_files:
        src_file = src_dir / file_name
        dst_file = dst_dir / file_name
        
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print(f"✅ {file_name}")
        else:
            print(f"⚠️  {file_name} (源文件不存在)")
    
    # 移动核心目录
    print("\n📁 移动核心目录:")
    print("-" * 40)
    for dir_name in core_dirs:
        src_subdir = src_dir / dir_name
        dst_subdir = dst_dir / dir_name
        
        if src_subdir.exists() and src_subdir.is_dir():
            if dst_subdir.exists():
                shutil.rmtree(dst_subdir)
            shutil.copytree(src_subdir, dst_subdir)
            print(f"✅ {dir_name}/")
    
    # 复制 docs 目录（源文档）
    print("\n📚 复制源文档:")
    print("-" * 40)
    docs_src = src_dir / "docs"
    docs_dst = dst_dir / "docs"
    if docs_src.exists():
        if docs_dst.exists():
            shutil.rmtree(docs_dst)
        shutil.copytree(docs_src, docs_dst)
        print(f"✅ docs/")
    
    # 更新路径引用
    print("\n🔧 更新路径引用:")
    print("-" * 40)
    update_path_references(dst_dir)
    
    print("\n" + "=" * 60)
    print("  迁移完成！")
    print("=" * 60)
    print(f"\n系统已迁移到: {dst_dir}")
    print("\n接下来请:")
    print(f"  cd {dst_dir}")
    print("  python demo.py")
    print("  python test_basic.py")

def update_path_references(dst_dir):
    """更新文件中的路径引用"""
    # 更新 build_index.py
    build_file = dst_dir / "build_index.py"
    if build_file.exists():
        with open(build_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        old_path = 'root_dir = Path("d:/TraeCode/AlgorithmTeachingAssistant/references")'
        new_path = 'root_dir = Path(__file__).parent'
        
        content = content.replace(old_path, new_path)
        
        with open(build_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ build_index.py (路径更新)")
    
    # 更新 retrieval.py
    retrieval_file = dst_dir / "retrieval.py"
    if retrieval_file.exists():
        with open(retrieval_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        old_path = 'root_dir = Path("d:/TraeCode/AlgorithmTeachingAssistant/references")'
        new_path = 'root_dir = Path(__file__).parent'
        
        content = content.replace(old_path, new_path)
        
        with open(retrieval_file, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ retrieval.py (路径更新)")
    
    # 更新 demo.py
    demo_file = dst_dir / "demo.py"
    if demo_file.exists():
        with open(demo_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        old_path = 'self.root_dir = Path(__file__).parent'
        # 已经是相对路径了，不需要改
        
        with open(demo_file, "w", encoding="utf-8") as f:
            f.write(content)
    
    # 更新 test_basic.py
    test_file = dst_dir / "test_basic.py"
    if test_file.exists():
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        # 已经是相对路径了，不需要改
        print("✅ test_basic.py (路径更新)")

if __name__ == "__main__":
    main()
