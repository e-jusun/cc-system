#!/usr/bin/env python3
"""
새 개발 작업 폴더 및 문서 파일 초기화 스크립트.

Usage:
    python3 init_task.py <task-name> [output-dir]

Examples:
    python3 init_task.py api-refactoring
    python3 init_task.py user-auth .claude/dev/active/
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path


def to_kebab_case(name: str) -> str:
    """문자열을 kebab-case로 변환."""
    # 공백, 언더스코어를 하이픈으로
    name = re.sub(r'[\s_]+', '-', name)
    # 연속 하이픈 제거
    name = re.sub(r'-+', '-', name)
    # 앞뒤 하이픈 제거
    name = name.strip('-')
    # 소문자로
    return name.lower()


def get_timestamp() -> str:
    """현재 타임스탬프 반환."""
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def get_skill_dir() -> Path:
    """skill 디렉토리 경로 반환."""
    return Path(__file__).parent.parent


def create_task_folder(task_name: str, output_dir: str = ".claude/dev/active") -> None:
    """새 작업 폴더와 템플릿 파일 생성."""

    task_name = to_kebab_case(task_name)
    skill_dir = get_skill_dir()
    assets_dir = skill_dir / "assets"

    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    task_dir = output_path / task_name

    if task_dir.exists():
        print(f"❌ 작업 폴더가 이미 존재합니다: {task_dir}")
        sys.exit(1)

    # 폴더 구조 생성
    task_dir.mkdir(parents=True, exist_ok=True)

    # completed 폴더도 함께 생성
    completed_dir = output_path.parent / "completed"
    completed_dir.mkdir(parents=True, exist_ok=True)

    timestamp = get_timestamp()

    # 템플릿 파일들 복사 및 변환
    templates = [
        ("plan-template.md", f"{task_name}-plan.md"),
        ("context-template.md", f"{task_name}-context.md"),
        ("tasks-template.md", f"{task_name}-tasks.md"),
    ]

    for template_name, output_name in templates:
        template_path = assets_dir / template_name
        output_file = task_dir / output_name

        if template_path.exists():
            content = template_path.read_text(encoding="utf-8")
            # 플레이스홀더 치환
            content = content.replace("{{TASK_NAME}}", task_name)
            content = content.replace("{{TIMESTAMP}}", timestamp)
            output_file.write_text(content, encoding="utf-8")
            print(f"✅ Created: {output_file}")
        else:
            print(f"⚠️  Template not found: {template_path}")

    print(f"\n🎉 작업 '{task_name}' 초기화 완료!")
    print(f"   위치: {task_dir}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 init_task.py <task-name> [output-dir]")
        print("\nExamples:")
        print("  python3 init_task.py api-refactoring")
        print("  python3 init_task.py user-auth .claude/dev/active/")
        sys.exit(1)

    task_name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else ".claude/dev/active"

    create_task_folder(task_name, output_dir)


if __name__ == "__main__":
    main()
