# Git Worktree 트러블슈팅

## "worktree already exists" 오류

같은 이름의 Worktree가 이미 존재할 때 발생합니다.

### 해결 방법

```bash
# 기존 Worktree 확인
git worktree list

# 사용하지 않는 Worktree 삭제
git worktree remove ~/git-worktrees/{repo}/{name}

# 또는 다른 이름으로 생성
bash ~/.claude/skills/git-worktree/scripts/create_worktree.sh feature new-name
```

## "branch already exists" 오류

같은 브랜치가 이미 존재할 때 발생합니다.

### 해결 방법

```bash
# 브랜치 확인
git branch -a | grep worktree/

# 머지되지 않은 브랜치 삭제 (주의!)
git branch -D worktree/{type}/{name}

# 또는 다른 작업 이름 사용
```

## Worktree 디렉토리 수동 삭제 후 오류

Worktree 디렉토리를 `rm -rf`로 삭제하면 Git이 여전히 참조를 유지합니다.

### 해결 방법

```bash
# Worktree 정보 정리
git worktree prune

# 상태 확인
git worktree list
```

## 머지 충돌

Squash 또는 Regular Merge 시 충돌이 발생할 수 있습니다.

### 해결 방법

```bash
# 충돌 확인
git status

# 머지 중단 (필요시)
git merge --abort

# 또는 수동 해결 후
git add .
git merge --continue
```

## Worktree에서 main 브랜치 접근 불가

Worktree에서 직접 main 브랜치를 체크아웃할 수 없습니다.

### 이유

Git은 동일 브랜치를 여러 worktree에서 동시에 체크아웃하는 것을 방지합니다.

### 해결 방법

```bash
# 메인 저장소로 이동
cd $(git worktree list | head -1 | awk '{print $1}')

# 또는 새 브랜치 생성
git checkout -b my-new-branch
```

## 권한 오류 (스크립트 실행 불가)

스크립트에 실행 권한이 없을 때 발생합니다.

### 해결 방법

```bash
chmod +x ~/.claude/skills/git-worktree/scripts/*.sh
```

## Worktree 경로에 공백 포함

경로에 공백이 있으면 스크립트가 오작동할 수 있습니다.

### 권장 사항

- 작업 이름에 공백 사용 금지
- kebab-case 사용 권장 (예: `my-feature`)

## 원격 저장소 동기화 문제

Worktree에서 푸시/풀이 안 될 때

### 해결 방법

```bash
# 원격 저장소 확인
git remote -v

# 원격 브랜치 추적 설정
git push -u origin $(git branch --show-current)
```

## Git 버전 호환성

Git Worktree는 Git 2.5 이상에서 지원됩니다.

### 확인 방법

```bash
git --version

# 업그레이드 (macOS)
brew upgrade git
```
