#!/usr/bin/env python3
"""
범용 테스트 파일 탐색 스크립트.

Usage:
    python3 find_test_files.py [directory]

Examples:
    python3 find_test_files.py
    python3 find_test_files.py ./src
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

# 테스트 디렉토리 패턴
TEST_DIRS = {"test", "tests", "__tests__", "test_output", "test-output"}

# 테스트 파일 패턴
TEST_FILE_PATTERNS = [
    "test_*.py",
    "*_test.py",
    "*.test.js",
    "*.test.ts",
    "*.test.jsx",
    "*.test.tsx",
    "*.spec.js",
    "*.spec.ts",
    "*.spec.jsx",
    "*.spec.tsx",
]

# 제외할 디렉토리
EXCLUDE_DIRS = {
    "node_modules",
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
}

# 임시 파일 패턴
TEMP_FILE_PATTERNS = [
    "*.backup",
    "*.bak",
    "*.tmp",
    "*.temp",
    ".DS_Store",
]


def get_file_description(file_path: Path) -> str:
    """파일 경로에서 용도 추론."""
    name = file_path.name.lower()
    parent = file_path.parent.name.lower()

    if parent in ("test_output", "test-output"):
        return "테스트 출력물"
    if name.startswith("test_") and name.endswith(".py"):
        return "Python 테스트 스크립트"
    if name.endswith("_test.py"):
        return "Python 테스트 스크립트"
    if ".test." in name or ".spec." in name:
        return "JavaScript/TypeScript 테스트"
    if name.endswith((".backup", ".bak")):
        return "백업 파일"
    if name.endswith((".tmp", ".temp")):
        return "임시 파일"
    if name == ".ds_store":
        return "macOS 메타데이터"
    if file_path.suffix in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
        return "이미지 파일"
    if file_path.suffix in (".mp3", ".wav", ".ogg", ".m4a"):
        return "오디오 파일"
    if file_path.suffix in (".mp4", ".mov", ".avi", ".webm"):
        return "비디오 파일"

    return "테스트 관련 파일"


def should_exclude(path: Path) -> bool:
    """제외 대상인지 확인."""
    parts = path.parts
    return any(excluded in parts for excluded in EXCLUDE_DIRS)


def find_test_files(root_dir: Path) -> List[Tuple[Path, str]]:
    """테스트 파일 및 임시 파일 탐색."""
    results = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        current = Path(dirpath)

        # 제외 디렉토리 스킵
        if should_exclude(current):
            dirnames.clear()
            continue

        # 테스트 디렉토리 내 파일
        if current.name.lower() in TEST_DIRS:
            for filename in filenames:
                file_path = current / filename
                desc = get_file_description(file_path)
                results.append((file_path, desc))
            continue

        # 테스트 파일 패턴 매칭
        for filename in filenames:
            file_path = current / filename
            name_lower = filename.lower()

            # 테스트 파일 패턴
            is_test = any(
                (pattern.startswith("*") and name_lower.endswith(pattern[1:]))
                or (pattern.endswith("*") and name_lower.startswith(pattern[:-1]))
                or (pattern.startswith("*") and pattern.endswith("*") and pattern[1:-1] in name_lower)
                for pattern in ["test_*.py", "*_test.py", "*.test.*", "*.spec.*"]
            )

            # 임시 파일 패턴
            is_temp = any(
                name_lower.endswith(ext.lstrip("*"))
                for ext in TEMP_FILE_PATTERNS
                if ext.startswith("*")
            ) or name_lower in [p for p in TEMP_FILE_PATTERNS if not p.startswith("*")]

            if is_test or is_temp:
                desc = get_file_description(file_path)
                results.append((file_path, desc))

    return results


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")

    if not root.exists():
        print(f"❌ 디렉토리가 존재하지 않습니다: {root}")
        sys.exit(1)

    files = find_test_files(root)

    if not files:
        print("테스트/임시 파일이 없습니다.")
        sys.exit(0)

    print(f"발견된 파일: {len(files)}개\n")
    for file_path, desc in sorted(files):
        relative = file_path.relative_to(root) if file_path.is_relative_to(root) else file_path
        print(f"  {relative} ({desc})")


if __name__ == "__main__":
    main()
