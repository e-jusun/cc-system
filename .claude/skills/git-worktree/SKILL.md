---
name: git-worktree
description: Git Worktree 관리 도구. 병렬 작업을 위한 Worktree 생성, 머지, 정리를 지원. 사용자가 (1) 새 worktree 생성, (2) worktree 목록 확인, (3) 작업 완료 후 머지 및 정리를 요청할 때 사용. "/git-worktree", "worktree 만들어", "병렬 작업", "깃 워크트리 생성" 등으로 트리거.
---

# Git Worktree 관리

여러 에이전트에서 병렬 작업을 위한 Git Worktree를 생성하고 관리합니다.

## 개요

Git Worktree를 사용하면 하나의 저장소에서 여러 작업 디렉토리를 동시에 사용할 수 있습니다. 각 Claude Code 세션이 독립적인 Worktree에서 작업하여 병렬 작업이 가능합니다.

## 작업 흐름

### 1. 현재 상태 확인

먼저 현재 디렉토리의 Git 상태를 확인합니다:

```bash
bash ~/.claude/skills/git-worktree/scripts/detect_context.sh
```

**결과 해석**:
- `main`: 메인 저장소 → Worktree 생성 가능
- `worktree`: Worktree 내부 → 머지/정리 가능

### 2-A. 메인 저장소: Worktree 생성

#### 정보 수집 (AskUserQuestion)

**질문 1**: "어떤 작업을 하시나요?"
- 옵션: "새 기능 개발" (feature), "버그 수정" (bugfix), "리팩토링" (refactor), "실험/테스트" (experiment)

**질문 2**: "작업 이름을 입력하세요" (자유 입력)
- 예: "image-optimization", "add-tts-engine"

#### Worktree 생성

```bash
bash ~/.claude/skills/git-worktree/scripts/create_worktree.sh <타입> <작업이름>
# 예: bash ~/.claude/skills/git-worktree/scripts/create_worktree.sh feature image-optimization
```

#### 사용자 안내

```
✅ Worktree 생성 완료!

📂 디렉토리: ~/git-worktrees/{저장소명}/{작업이름}
🌿 브랜치: worktree/{타입}/{작업이름}

⏭️ 다음 단계:
1. 새 터미널 열기
2. cd ~/git-worktrees/{저장소명}/{작업이름}
3. 새 Claude Code 세션에서 작업 시작
```

### 2-B. Worktree: 머지 및 정리

#### 변경사항 확인

```bash
git status --short
git log main..HEAD --oneline
```

#### 커밋되지 않은 변경사항 처리

변경사항이 있으면 커밋 여부 확인 (AskUserQuestion)

#### 머지 전략 선택 (AskUserQuestion)

**질문**: "어떻게 메인 브랜치에 머지하시겠습니까?"
- "Squash Merge (권장)" - 모든 커밋을 하나로 합침
- "Regular Merge" - 커밋 히스토리 유지
- "Rebase" - 커밋을 main 위에 재배치

#### 머지 및 정리 실행

```bash
bash ~/.claude/skills/git-worktree/scripts/merge_and_cleanup.sh <머지타입> [--delete-worktree] [--delete-branch]
# 예: bash ~/.claude/skills/git-worktree/scripts/merge_and_cleanup.sh squash --delete-worktree --delete-branch
```

### 3. Worktree 목록 조회

```bash
bash ~/.claude/skills/git-worktree/scripts/list_worktrees.sh
```

## 경로 규칙

### Worktree 디렉토리
```
~/git-worktrees/{저장소명}/{작업이름}
```

### 브랜치 이름
```
worktree/{타입}/{작업이름}

타입:
- feature: 새 기능
- bugfix: 버그 수정
- refactor: 리팩토링
- experiment: 실험/테스트
```

## 주의사항

### Worktree 생성 시
- 메인 저장소에서만 실행 가능
- 각 Worktree는 독립적인 브랜치 사용
- 동일한 브랜치를 여러 Worktree에서 사용 불가

### Worktree 머지 시
- 머지 전 반드시 변경사항 커밋
- Squash Merge 권장 (히스토리 정리)
- 충돌 발생 시 수동 해결 필요

### 병렬 작업 시
- 서로 다른 파일 수정 권장
- 같은 파일 수정 시 충돌 가능

## 참고

- 트러블슈팅: [references/troubleshooting.md](references/troubleshooting.md)
- 고급 사용법: [references/advanced-usage.md](references/advanced-usage.md)
