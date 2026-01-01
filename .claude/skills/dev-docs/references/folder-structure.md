# Dev Docs 폴더 구조

## 표준 구조

모든 프로젝트에서 `.claude/dev/` 폴더를 사용하여 개발 작업을 문서화합니다.

```
.claude/dev/
├── active/                     # 현재 진행 중인 작업
│   ├── feature-auth/
│   │   ├── feature-auth-plan.md
│   │   ├── feature-auth-context.md
│   │   └── feature-auth-tasks.md
│   └── bug-fix-login/
│       ├── bug-fix-login-plan.md
│       ├── bug-fix-login-context.md
│       └── bug-fix-login-tasks.md
└── completed/                  # 완료된 작업 아카이브
    └── refactor-api/
        ├── refactor-api-plan.md
        ├── refactor-api-context.md
        └── refactor-api-tasks.md
```

## 파일 명명 규칙

- **작업 이름**: kebab-case 사용 (예: `api-key-management`, `user-authentication`)
- **파일 이름**: `[task-name]-[type].md` 형식
  - `[task-name]-plan.md`
  - `[task-name]-context.md`
  - `[task-name]-tasks.md`

## 각 파일의 역할

### plan.md

구현 계획과 기술적 접근 방식 문서화.

**포함 내용:**
- 목표 및 범위
- 구현 단계
- 기술적 결정사항
- 예상 산출물
- 검증 방법

**업데이트 시점:** 계획이 변경될 때

### context.md

작업 수행 중 축적된 컨텍스트 정보 문서화.

**포함 내용:**
- 생성/수정된 핵심 파일
- 주요 아키텍처 결정사항
- 데이터 구조 및 스키마
- 내부/외부 의존성
- 알려진 이슈 및 TODO

**업데이트 시점:** 중요한 변경이 발생할 때

### tasks.md

작업 진행 상태와 태스크 추적.

**포함 내용:**
- 완료 기준 (체크리스트)
- 진행 상태 (완료/진행 중/대기 중)
- 다음 단계
- 차단 요소

**업데이트 시점:** 매 dev:docs 업데이트

## 작업 수명 주기

```
1. 새 작업 시작
   └─> .claude/dev/active/[task-name]/ 생성

2. 작업 진행
   └─> plan.md, context.md, tasks.md 지속 업데이트

3. 작업 완료
   └─> .claude/dev/completed/[task-name]/로 이관
```

## 완료 조건

tasks.md에서 다음 조건이 모두 충족되면 작업 완료로 간주:

1. "🔄 진행 중" 섹션에 항목이 0개
2. "⏳ 대기 중" 섹션에 항목이 0개 (또는 선택적 항목만)
3. "완료 기준" 섹션이 모두 ✅로 체크됨

## 이관 시 추가 정보

completed로 이관 시 tasks.md에 완료 날짜 추가:

```markdown
---

## 완료 날짜

**YYYY-MM-DD**

작업이 완료되어 `.claude/dev/completed/`로 이관되었습니다.
```
