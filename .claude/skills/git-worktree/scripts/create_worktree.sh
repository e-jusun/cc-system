#!/bin/bash
# create_worktree.sh - Git Worktree 생성
#
# 인자:
#   $1 - 작업 타입 (feature, bugfix, refactor, experiment)
#   $2 - 작업 이름 (kebab-case 권장)
#
# 사용법:
#   bash create_worktree.sh feature image-optimization
#   bash create_worktree.sh bugfix login-crash

set -e

# 인자 확인
if [ $# -lt 2 ]; then
    echo "사용법: $0 <타입> <작업이름>" >&2
    echo "타입: feature, bugfix, refactor, experiment" >&2
    exit 1
fi

TYPE="$1"
TASK_NAME="$2"

# 타입 유효성 검사
case "$TYPE" in
    feature|bugfix|refactor|experiment)
        ;;
    *)
        echo "오류: 유효하지 않은 타입 '$TYPE'" >&2
        echo "허용된 타입: feature, bugfix, refactor, experiment" >&2
        exit 1
        ;;
esac

# 작업 이름을 kebab-case로 변환 (공백 → 하이픈, 소문자)
TASK_NAME=$(echo "$TASK_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')

# 현재 저장소 정보
REPO_ROOT=$(git rev-parse --show-toplevel)
REPO_NAME=$(basename "$REPO_ROOT")

# 경로 설정
WORKTREE_BASE="$HOME/git-worktrees"
WORKTREE_DIR="$WORKTREE_BASE/$REPO_NAME/$TASK_NAME"
BRANCH_NAME="worktree/$TYPE/$TASK_NAME"

# 디렉토리 존재 확인
if [ -d "$WORKTREE_DIR" ]; then
    echo "오류: Worktree 디렉토리가 이미 존재합니다: $WORKTREE_DIR" >&2
    exit 1
fi

# 브랜치 존재 확인
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
    echo "오류: 브랜치가 이미 존재합니다: $BRANCH_NAME" >&2
    echo "기존 브랜치를 삭제하려면: git branch -d $BRANCH_NAME" >&2
    exit 1
fi

# 부모 디렉토리 생성
mkdir -p "$WORKTREE_BASE/$REPO_NAME"

# Worktree 생성
echo "Worktree 생성 중..." >&2
git worktree add "$WORKTREE_DIR" -b "$BRANCH_NAME"

# 결과 출력
echo ""
echo "✅ Worktree 생성 완료!"
echo ""
echo "📂 디렉토리: $WORKTREE_DIR"
echo "🌿 브랜치: $BRANCH_NAME"
echo ""
echo "⏭️ 다음 단계:"
echo "1. 새 터미널 열기"
echo "2. cd $WORKTREE_DIR"
echo "3. 새 Claude Code 세션에서 작업 시작"
echo ""
echo "💡 팁: 여러 Worktree를 만들어 병렬 작업이 가능합니다!"
