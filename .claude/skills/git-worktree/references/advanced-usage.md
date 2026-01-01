# Git Worktree 고급 사용법

## Worktree 직접 관리

스크립트 없이 Git 명령어로 직접 관리하는 방법입니다.

### Worktree 추가

```bash
# 기본 사용
git worktree add <경로> -b <브랜치명>

# 예시
git worktree add ~/git-worktrees/my-repo/feature-x -b feature/x
```

### Worktree 제거

```bash
# 클린한 worktree 제거
git worktree remove <경로>

# 변경사항이 있는 worktree 강제 제거
git worktree remove <경로> --force
```

### Worktree 이동

```bash
git worktree move <현재경로> <새경로>
```

### Worktree 정리

삭제된 디렉토리 참조 제거:

```bash
git worktree prune
```

## 병렬 작업 전략

### 파일 기반 분리

```
터미널 1: frontend/ 수정
터미널 2: backend/ 수정
터미널 3: docs/ 수정
```

### 기능 기반 분리

```
worktree/feature/auth     → 인증 기능
worktree/feature/payment  → 결제 기능
worktree/bugfix/login     → 로그인 버그
```

### 충돌 최소화 팁

1. 서로 다른 디렉토리/파일 수정
2. 공통 파일 수정 전 동기화
3. 짧은 작업 주기 유지

## 머지 전략 상세

### Squash Merge (권장)

모든 커밋을 하나로 합칩니다.

**장점:**
- 깔끔한 히스토리
- 리뷰하기 쉬움
- 롤백 간편

**단점:**
- 개별 커밋 히스토리 손실

**사용 시점:**
- 실험적인 커밋이 많을 때
- WIP 커밋이 포함된 경우
- 작은 기능 구현

### Regular Merge

커밋 히스토리를 그대로 유지합니다.

**장점:**
- 전체 히스토리 보존
- git blame 정확도

**단점:**
- 복잡한 히스토리
- 불필요한 커밋 포함 가능

**사용 시점:**
- 체계적으로 커밋한 경우
- 각 커밋이 의미있는 단위인 경우

### Rebase

커밋을 main 위에 재배치합니다.

**장점:**
- 선형 히스토리
- 깔끔한 git log

**단점:**
- 충돌 해결이 복잡할 수 있음
- 이미 공유된 브랜치에는 위험

**사용 시점:**
- 개인 브랜치인 경우
- 커밋 정리가 필요한 경우

## 스크립트 커스터마이징

### 경로 변경

`create_worktree.sh`의 기본 경로 수정:

```bash
# 기본값
WORKTREE_BASE="$HOME/git-worktrees"

# 변경 예시
WORKTREE_BASE="/workspace/worktrees"
```

### 브랜치 네이밍 변경

```bash
# 기본값
BRANCH_NAME="worktree/$TYPE/$TASK_NAME"

# 변경 예시 (prefix 추가)
BRANCH_NAME="wt/$TYPE/$TASK_NAME"
```

## CI/CD 통합

### GitHub Actions에서 Worktree 사용

```yaml
- name: Setup worktree
  run: |
    git worktree add ../feature-branch feature-branch
    cd ../feature-branch
    # 작업 수행
```

## 대규모 프로젝트에서의 활용

### 모노레포 전략

```
~/git-worktrees/
└── monorepo/
    ├── frontend-auth/
    ├── backend-api/
    └── shared-utils/
```

### 팀 작업 분배

각 팀원이 별도 worktree에서 작업:

```
Team A: ~/git-worktrees/project/team-a-feature
Team B: ~/git-worktrees/project/team-b-feature
```

## 성능 최적화

### Sparse Checkout과 함께 사용

대규모 저장소에서 필요한 파일만 체크아웃:

```bash
git worktree add --no-checkout ../sparse-wt -b feature-x
cd ../sparse-wt
git sparse-checkout init --cone
git sparse-checkout set src/my-module
git checkout
```

### Shallow Clone과 함께 사용

```bash
# 메인 저장소가 shallow인 경우
git fetch --unshallow  # 먼저 전체 히스토리 가져오기
git worktree add ...
```

## 참고 자료

- [Git Worktree 공식 문서](https://git-scm.com/docs/git-worktree)
- [Pro Git Book - Worktree](https://git-scm.com/book/en/v2/Git-Tools-Working-with-Multiple-Branches)
