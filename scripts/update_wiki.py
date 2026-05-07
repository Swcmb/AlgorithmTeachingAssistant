#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AlgorithmTeachingAssistant - 知识库更新脚本
从 OI-wiki GitHub 仓库同步文档并重新构建索引
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from .common import get_project_root, ensure_dir, save_json, load_json

PROJECT_ROOT = get_project_root()
DB_ROOT = PROJECT_ROOT / "references" / "db"
DOC_DIR = DB_ROOT / "doc"
DOCS_DIR = DOC_DIR / "docs"
MARKDOWN_DIR = DB_ROOT / "markdown"


class WikiUpdater:
    def __init__(self):
        self.db_root = DB_ROOT
        self.doc_dir = DOC_DIR
        self.docs_dir = DOCS_DIR
        self.markdown_dir = MARKDOWN_DIR
        self.last_update_file = DB_ROOT / "last_update.json"
        
    def _get_last_update(self) -> dict:
        """获取上次更新记录"""
        return load_json(self.last_update_file)
    
    def _save_last_update(self, data: dict):
        """保存更新记录"""
        save_json(self.last_update_file, data)
    
    def check_git_repo(self) -> bool:
        """检查 doc 目录是否为 git 仓库"""
        if not self.doc_dir.exists():
            return False
        git_dir = self.doc_dir / ".git"
        return git_dir.exists()
    
    def init_git_repo(self):
        """初始化 git 仓库并拉取 OI-wiki"""
        print(f"📥 初始化 OI-wiki 仓库...")
        
        if self.doc_dir.exists():
            shutil.rmtree(self.doc_dir)
        
        ensure_dir(self.doc_dir.parent)
        
        repo_url = "https://github.com/OI-wiki/OI-wiki.git"
        cmd = ["git", "clone", "--depth=1", repo_url, str(self.doc_dir)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ 仓库克隆成功")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 仓库克隆失败: {e.stderr}")
            return False
    
    def pull_latest(self) -> bool:
        """拉取最新代码"""
        print(f"🔄 拉取最新更新...")
        
        cmd = ["git", "pull", "origin", "master"]
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                check=True,
                cwd=str(self.doc_dir)
            )
            if "Already up to date" in result.stdout:
                print("✅ 已是最新版本")
                return False
            print(f"✅ 成功拉取更新")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 拉取失败: {e.stderr}")
            return False
    
    def sync_markdown(self):
        """同步 Markdown 文档到知识库"""
        print(f"📝 同步 Markdown 文档...")
        
        ensure_dir(self.markdown_dir)
        
        source_dir = self.docs_dir
        if not source_dir.exists():
            print(f"⚠️ 源目录不存在: {source_dir}")
            return
        
        copied_count = 0
        for md_file in source_dir.rglob("*.md"):
            rel_path = md_file.relative_to(source_dir)
            dest_file = self.markdown_dir / rel_path
            
            ensure_dir(dest_file.parent)
            
            try:
                shutil.copy2(md_file, dest_file)
                copied_count += 1
            except Exception as e:
                print(f"⚠️ 复制失败 {md_file}: {e}")
        
        print(f"✅ 同步完成，共复制 {copied_count} 个文件")
    
    def build_index(self, rebuild: bool = False):
        """构建知识库索引"""
        print(f"🏗️ 构建知识库索引...")
        
        from .build_index import IndexBuilder
        
        builder = IndexBuilder(rebuild=rebuild)
        builder.run()
    
    def run(self, force: bool = False, rebuild: bool = False):
        """执行完整更新流程"""
        print("=" * 60)
        print("  AlgorithmTeachingAssistant 知识库更新")
        print("=" * 60)
        print()
        
        # 检查或初始化 git 仓库
        if not self.check_git_repo():
            print(f"⚠️ 未检测到 git 仓库，开始初始化...")
            if not self.init_git_repo():
                print("❌ 初始化失败，退出")
                return
        
        # 拉取最新更新
        has_update = self.pull_latest()
        
        if not has_update and not force:
            print("\nℹ️ 没有新更新，使用 --force 强制同步")
            return
        
        # 同步 Markdown 文档
        self.sync_markdown()
        
        # 构建索引
        self.build_index(rebuild=rebuild)
        
        # 保存更新记录
        import datetime
        self._save_last_update({
            "last_update": datetime.datetime.now().isoformat(),
            "has_update": has_update
        })
        
        print("\n🎉 更新完成！")


def main():
    parser = argparse.ArgumentParser(description="更新 OI-wiki 知识库")
    parser.add_argument("--force", "-f", action="store_true", help="强制同步（即使没有更新）")
    parser.add_argument("--rebuild", "-r", action="store_true", help="全量重建索引")
    args = parser.parse_args()
    
    updater = WikiUpdater()
    updater.run(force=args.force, rebuild=args.rebuild)


if __name__ == "__main__":
    main()