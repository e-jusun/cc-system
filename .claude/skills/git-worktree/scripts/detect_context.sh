#!/bin/bash
# detect_context.sh - 현재 디렉토리가 메인 저장소인지 Worktree인지 판단
#
# 출력:
#   main     - 메인 저장소 (.git 디렉토리)
#   worktree - Worktree (.git 파일)
#   error    - Git 저장소가 아님
#
# 사용법:
#   bash detect_context.sh

set -e

# Git 저장소인지 확인
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "error"
    echo "현재 디렉토리는 Git 저장소가 아닙니다." >&2
    exit 1
fi

# .git이 디렉토리인지 파일인지 확인
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)

if [ -d "$GIT_DIR" ] && [ "$GIT_DIR" = ".git" ]; then
    echo "main"

    # 추가 정보 출력
    REPO_NAME=$(basename "$(git rev-parse --show-toplevel)")
    BRANCH=$(git branch --show-current)
    echo "저장소: $REPO_NAME" >&2
    echo "브랜치: $BRANCH" >&2

elif [ -f ".git" ]; then
    echo "worktree"

    # 추가 정보 출력
    BRANCH=$(git branch --show-current)
    MAIN_DIR=$(git worktree list | head -1 | awk '{print $1}')
    echo "브랜치: $BRANCH" >&2
    echo "메인 저장소: $MAIN_DIR" >&2

else
    # 다른 경우 (예: bare repository 내부)
    echo "main"
fi
