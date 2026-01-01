#!/bin/bash
# list_worktrees.sh - 현재 저장소의 모든 Worktree 목록 출력
#
# 사용법:
#   bash list_worktrees.sh

set -e

# Git 저장소인지 확인
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "오류: 현재 디렉토리는 Git 저장소가 아닙니다." >&2
    exit 1
fi

# Worktree 목록 가져오기
WORKTREES=$(git worktree list)
COUNT=$(echo "$WORKTREES" | wc -l | tr -d ' ')

echo "📂 현재 활성 Worktree: ${COUNT}개"
echo ""

# 각 worktree 정보 출력
INDEX=1
echo "$WORKTREES" | while read -r line; do
    PATH_PART=$(echo "$line" | awk '{print $1}')
    COMMIT=$(echo "$line" | awk '{print $2}')
    BRANCH=$(echo "$line" | sed 's/.*\[\(.*\)\].*/\1/' 2>/dev/null || echo "detached")

    # 디렉토리 이름 추출
    DIR_NAME=$(basename "$PATH_PART")

    echo "$INDEX. $DIR_NAME"
    echo "   경로: $PATH_PART"
    echo "   브랜치: $BRANCH"

    # 변경사항 확인 (해당 worktree에서)
    if [ -d "$PATH_PART" ]; then
        CHANGES=$(cd "$PATH_PART" && git status --short 2>/dev/null | wc -l | tr -d ' ')
        if [ "$CHANGES" -gt 0 ]; then
            echo "   상태: 📝 변경사항 ${CHANGES}개"
        else
            echo "   상태: ✅ 클린"
        fi
    fi

    echo ""
    INDEX=$((INDEX + 1))
done
