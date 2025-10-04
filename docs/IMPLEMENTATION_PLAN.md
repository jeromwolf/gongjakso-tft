# 공작소 TFT 기능 구현 계획

**작성일**: 2025-10-04
**버전**: 1.0
**기준 문서**: 운영 정책 1.0, SWOT 분석

---

## 목차

1. [개요](#개요)
2. [회원 관리 및 프로필 시스템](#1-회원-관리-및-프로필-시스템)
3. [프로젝트 Q&A 시스템](#2-프로젝트-qa-시스템)
4. [구현 우선순위 로드맵](#3-구현-우선순위-로드맵)
5. [기술 스택 및 아키텍처](#4-기술-스택-및-아키텍처)

---

## 개요

### 목적
운영 정책과 SWOT 분석을 기반으로 데이터공작소 TFT의 핵심 기능을 체계적으로 구현하여 커뮤니티 활성화와 지속 가능성을 확보합니다.

### 핵심 목표
- ✅ **회원 등급 시스템**: 5단계 회원 등급 체계 구현 (Visitor → Core Team)
- ✅ **기여도 추적**: PR, 이슈, 스터디 참여 등 자동 집계
- ✅ **프로필 시스템**: 멤버 포트폴리오 및 활동 이력 관리
- ✅ **Q&A 기능**: 프로젝트별 질문/답변 커뮤니티
- ✅ **게이미피케이션**: 배지, 레벨, 리더보드

---

## 1. 회원 관리 및 프로필 시스템

### 1.1 데이터베이스 스키마

#### Users 테이블 확장
```python
# backend/models/user.py

from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.orm import relationship

class UserRole(str, Enum):
    VISITOR = "visitor"           # 비회원
    CONTRIBUTOR = "contributor"   # 준회원
    MEMBER = "member"            # 정회원
    MAINTAINER = "maintainer"    # 운영진
    CORE_TEAM = "core_team"      # 코어팀

class User(Base):
    __tablename__ = "users"

    # 기존 필드
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.VISITOR)

    # 새로운 필드
    member_tier = Column(Enum(UserRole), default=UserRole.VISITOR)  # 회원 등급
    github_username = Column(String(100), unique=True)  # GitHub 연동
    profile_image = Column(String(500))  # 프로필 이미지 URL
    bio = Column(Text)  # 자기소개
    skills = Column(JSON)  # 기술 스택 ["Python", "Docker", ...]
    interests = Column(JSON)  # 관심 분야
    website = Column(String(500))  # 개인 웹사이트
    twitter = Column(String(100))  # 소셜 미디어
    linkedin = Column(String(100))

    # 통계 필드
    total_prs = Column(Integer, default=0)  # 총 PR 수
    merged_prs = Column(Integer, default=0)  # 머지된 PR 수
    total_issues = Column(Integer, default=0)  # 이슈 등록 수
    total_comments = Column(Integer, default=0)  # 댓글 수
    total_qa_questions = Column(Integer, default=0)  # Q&A 질문 수
    total_qa_answers = Column(Integer, default=0)  # Q&A 답변 수
    reputation_score = Column(Integer, default=0)  # 평판 점수

    # 활동 추적
    last_active_at = Column(DateTime)  # 마지막 활동 시간
    joined_at = Column(DateTime, nullable=False)  # 가입일
    tier_upgraded_at = Column(DateTime)  # 등급 승급일

    # Relationships
    contributions = relationship("Contribution", back_populates="user")
    qa_questions = relationship("Question", back_populates="author")
    qa_answers = relationship("Answer", back_populates="author")
    badges = relationship("UserBadge", back_populates="user")
```

#### Contributions 테이블 (기여 이력)
```python
# backend/models/contribution.py

from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

class ContributionType(str, Enum):
    PR_MERGED = "pr_merged"          # PR 머지
    ISSUE_CREATED = "issue_created"  # 이슈 생성
    ISSUE_RESOLVED = "issue_resolved"  # 이슈 해결
    CODE_REVIEW = "code_review"      # 코드 리뷰
    DOCUMENTATION = "documentation"  # 문서화
    STUDY_COMPLETED = "study_completed"  # 스터디 완료
    EVENT_ATTENDED = "event_attended"  # 이벤트 참석
    MENTORING = "mentoring"          # 멘토링

class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))

    type = Column(Enum(ContributionType), nullable=False)
    title = Column(String(200), nullable=False)  # PR/이슈 제목
    description = Column(Text)
    url = Column(String(500))  # GitHub PR/이슈 URL
    points = Column(Integer, default=0)  # 획득 포인트

    created_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)  # 검증 여부

    # Relationships
    user = relationship("User", back_populates="contributions")
    project = relationship("Project")
```

#### Badges 테이블 (배지 시스템)
```python
# backend/models/badge.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)  # "첫 PR", "리뷰어"
    slug = Column(String(100), unique=True)
    description = Column(Text)
    icon = Column(String(500))  # 아이콘 URL 또는 이모지
    tier = Column(String(20))  # bronze, silver, gold, platinum
    criteria = Column(Text)  # 획득 조건 설명

    created_at = Column(DateTime)

class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)

    earned_at = Column(DateTime, nullable=False)
    displayed = Column(Boolean, default=True)  # 프로필에 표시 여부

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge")
```

### 1.2 API 엔드포인트

#### 프로필 관리 API
```python
# backend/api/profile.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

router = APIRouter(prefix="/api/profile", tags=["profile"])

# 1. 프로필 조회 (공개)
@router.get("/{username}")
async def get_user_profile(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """
    사용자 프로필 조회 (누구나 접근 가능)

    Returns:
    - 기본 정보: name, bio, skills, member_tier
    - 통계: total_prs, merged_prs, reputation_score
    - 최근 기여: 최근 5개 contributions
    - 배지: 획득한 모든 배지
    """
    pass

# 2. 내 프로필 수정
@router.put("/me")
async def update_my_profile(
    profile_data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    로그인한 사용자의 프로필 수정

    허용 필드: bio, skills, interests, website, twitter, linkedin, profile_image
    """
    pass

# 3. GitHub 연동
@router.post("/github/connect")
async def connect_github(
    github_code: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    GitHub OAuth로 계정 연동
    - GitHub username 저장
    - 자동으로 contributions 수집 (선택적)
    """
    pass

# 4. 기여 이력 조회
@router.get("/{username}/contributions")
async def get_user_contributions(
    username: str,
    page: int = 1,
    page_size: int = 20,
    type: Optional[ContributionType] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    사용자의 기여 이력 조회
    - 필터: type (pr_merged, issue_created, ...)
    - 페이지네이션
    """
    pass

# 5. 배지 조회
@router.get("/{username}/badges")
async def get_user_badges(
    username: str,
    db: AsyncSession = Depends(get_db)
):
    """
    사용자가 획득한 배지 목록
    """
    pass
```

#### 회원 등급 관리 API
```python
# backend/api/members.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/members", tags=["members"])

# 1. 멤버 리스트 (등급별 필터링)
@router.get("/")
async def list_members(
    tier: Optional[UserRole] = None,
    sort_by: str = "reputation_score",  # reputation_score, joined_at, total_prs
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    멤버 목록 조회
    - tier 필터: contributor, member, maintainer, core_team
    - 정렬: 평판 점수, 가입일, PR 수
    """
    pass

# 2. 리더보드
@router.get("/leaderboard")
async def get_leaderboard(
    period: str = "all",  # all, month, week
    metric: str = "reputation",  # reputation, prs, qa_answers
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    리더보드
    - 기간별: 전체, 이번 달, 이번 주
    - 메트릭: 평판 점수, PR 수, Q&A 답변 수
    """
    pass

# 3. 등급 승급 신청
@router.post("/tier/upgrade")
async def request_tier_upgrade(
    target_tier: UserRole,
    evidence: str,  # 승급 근거 (PR 링크, 스터디 완료 증빙 등)
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    등급 승급 신청
    - Contributor → Member: PR 3회 OR 스터디 1회
    - Member → Maintainer: 추천 필요
    """
    pass

# 4. 등급 승급 승인 (운영진 전용)
@router.post("/tier/approve/{user_id}")
async def approve_tier_upgrade(
    user_id: int,
    new_tier: UserRole,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """
    등급 승급 승인 (Maintainer 이상만 가능)
    """
    pass
```

### 1.3 프론트엔드 페이지

#### 1) 프로필 페이지 (`/profile/[username]`)
```typescript
// frontend/src/app/profile/[username]/page.tsx

interface UserProfile {
  id: number;
  name: string;
  username: string;
  email?: string;
  member_tier: 'visitor' | 'contributor' | 'member' | 'maintainer' | 'core_team';
  bio?: string;
  skills?: string[];
  profile_image?: string;
  github_username?: string;
  website?: string;

  // 통계
  stats: {
    total_prs: number;
    merged_prs: number;
    total_issues: number;
    total_qa_questions: number;
    total_qa_answers: number;
    reputation_score: number;
  };

  // 활동
  joined_at: string;
  last_active_at: string;
  tier_upgraded_at?: string;

  // 최근 기여
  recent_contributions: Contribution[];

  // 배지
  badges: Badge[];
}

export default function ProfilePage({ params }: { params: { username: string } }) {
  // 레이아웃:
  // - 왼쪽: 프로필 카드 (이미지, 이름, 등급 배지, 소셜 링크)
  // - 오른쪽: 탭
  //   - Overview: 통계 대시보드, 최근 기여, 배지
  //   - Contributions: 전체 기여 이력
  //   - Activity: 활동 타임라인
}
```

**주요 기능:**
- ✅ 등급 배지 표시 (Visitor ~ Core Team)
- ✅ 평판 점수 및 진행률 바
- ✅ 기술 스택 태그
- ✅ 최근 기여 타임라인
- ✅ 획득 배지 갤러리
- ✅ GitHub 프로필 링크

#### 2) 프로필 편집 페이지 (`/profile/edit`)
```typescript
// frontend/src/app/profile/edit/page.tsx

export default function ProfileEditPage() {
  // 폼 필드:
  // - 프로필 이미지 업로드
  // - 자기소개 (Bio)
  // - 기술 스택 (다중 선택)
  // - 관심 분야
  // - 소셜 링크 (GitHub, Twitter, LinkedIn, Website)
  // - GitHub 연동 버튼
}
```

#### 3) 멤버 디렉토리 (`/members`)
```typescript
// frontend/src/app/members/page.tsx

export default function MembersPage() {
  // 기능:
  // - 등급별 필터 (All, Contributor, Member, Maintainer, Core Team)
  // - 검색 (이름, GitHub username)
  // - 정렬 (평판 점수, 가입일, PR 수)
  // - 그리드 레이아웃 (카드형)

  // 각 카드:
  // - 프로필 이미지
  // - 이름 + 등급 배지
  // - 평판 점수
  // - 주요 배지 3개
  // - 기술 스택 태그
}
```

#### 4) 리더보드 (`/leaderboard`)
```typescript
// frontend/src/app/leaderboard/page.tsx

export default function LeaderboardPage() {
  // 탭:
  // - 평판 점수
  // - PR 기여
  // - Q&A 활동

  // 기간 필터: 전체 / 이번 달 / 이번 주

  // 순위 표시:
  // 1위: 🥇, 2위: 🥈, 3위: 🥉
  // 4위 이하: 숫자
}
```

### 1.4 자동 등급 승급 로직

```python
# backend/services/tier_service.py

from backend.models.user import User, UserRole
from backend.models.contribution import ContributionType

async def check_and_upgrade_tier(user_id: int, db: AsyncSession):
    """
    사용자의 등급 승급 조건 자동 확인 및 승급
    """
    user = await db.get(User, user_id)

    # Visitor → Contributor
    if user.member_tier == UserRole.VISITOR:
        # 조건: GitHub 계정 연동 + 행동 강령 동의
        if user.github_username and user.agreed_to_coc:
            user.member_tier = UserRole.CONTRIBUTOR
            user.tier_upgraded_at = datetime.now()
            await db.commit()
            await send_tier_upgrade_notification(user, UserRole.CONTRIBUTOR)
            return

    # Contributor → Member
    if user.member_tier == UserRole.CONTRIBUTOR:
        # 조건: PR 3회 이상 머지 OR 스터디 1회 완료
        if user.merged_prs >= 3:
            user.member_tier = UserRole.MEMBER
            user.tier_upgraded_at = datetime.now()
            await db.commit()
            await send_tier_upgrade_notification(user, UserRole.MEMBER)
            await award_badge(user_id, "member_badge", db)
            return

        # 스터디 완료 확인
        study_count = await db.scalar(
            select(func.count()).select_from(Contribution)
            .where(
                Contribution.user_id == user_id,
                Contribution.type == ContributionType.STUDY_COMPLETED,
                Contribution.verified == True
            )
        )
        if study_count >= 1:
            user.member_tier = UserRole.MEMBER
            user.tier_upgraded_at = datetime.now()
            await db.commit()
            await send_tier_upgrade_notification(user, UserRole.MEMBER)
            return

    # Member → Maintainer
    # 조건: 기여도 상위 20% OR 추천 (수동 승인 필요)
    # Maintainer → Core Team
    # 조건: 운영진 투표 (수동 승인 필요)
```

### 1.5 배지 시스템

#### 초기 배지 목록
```python
# backend/scripts/seed_badges.py

INITIAL_BADGES = [
    # 기여 배지
    {"name": "첫 PR", "slug": "first_pr", "icon": "🎉", "tier": "bronze",
     "criteria": "첫 PR 머지"},
    {"name": "PR 마스터", "slug": "pr_master", "icon": "🏆", "tier": "gold",
     "criteria": "PR 50개 머지"},
    {"name": "이슈 헌터", "slug": "issue_hunter", "icon": "🐛", "tier": "silver",
     "criteria": "이슈 20개 생성"},

    # 등급 배지
    {"name": "정회원", "slug": "member", "icon": "⭐", "tier": "silver",
     "criteria": "Member 등급 달성"},
    {"name": "운영진", "slug": "maintainer", "icon": "👑", "tier": "gold",
     "criteria": "Maintainer 등급 달성"},
    {"name": "코어팀", "slug": "core_team", "icon": "💎", "tier": "platinum",
     "criteria": "Core Team 멤버"},

    # 활동 배지
    {"name": "멘토", "slug": "mentor", "icon": "🎓", "tier": "gold",
     "criteria": "멘토링 10회 완료"},
    {"name": "리뷰어", "slug": "reviewer", "icon": "👀", "tier": "silver",
     "criteria": "코드 리뷰 50회"},
    {"name": "문서화 전문가", "slug": "doc_expert", "icon": "📝", "tier": "gold",
     "criteria": "문서화 기여 20회"},

    # Q&A 배지
    {"name": "질문왕", "slug": "questioner", "icon": "❓", "tier": "bronze",
     "criteria": "Q&A 질문 20개"},
    {"name": "해결사", "slug": "solver", "icon": "✅", "tier": "gold",
     "criteria": "Q&A 답변 50개 (채택률 70% 이상)"},

    # 특별 배지
    {"name": "얼리 어답터", "slug": "early_adopter", "icon": "🚀", "tier": "platinum",
     "criteria": "커뮤니티 초기 100명"},
    {"name": "1주년", "slug": "one_year", "icon": "🎂", "tier": "gold",
     "criteria": "1년 활동 유지"},
]
```

---

## 2. 프로젝트 Q&A 시스템

### 2.1 데이터베이스 스키마

```python
# backend/models/qa.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(JSON)  # ["docker", "python", "api"]

    views = Column(Integer, default=0)
    votes = Column(Integer, default=0)  # 추천 수

    is_answered = Column(Boolean, default=False)
    accepted_answer_id = Column(Integer, ForeignKey("answers.id"))

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    # Relationships
    project = relationship("Project")
    author = relationship("User", back_populates="qa_questions", foreign_keys=[author_id])
    answers = relationship("Answer", back_populates="question",
                          foreign_keys="Answer.question_id")
    accepted_answer = relationship("Answer", foreign_keys=[accepted_answer_id])

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(Text, nullable=False)
    votes = Column(Integer, default=0)
    is_accepted = Column(Boolean, default=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    # Relationships
    question = relationship("Question", back_populates="answers",
                           foreign_keys=[question_id])
    author = relationship("User", back_populates="qa_answers")

class QAVote(Base):
    __tablename__ = "qa_votes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer_id = Column(Integer, ForeignKey("answers.id"))

    vote_type = Column(Integer, nullable=False)  # 1: upvote, -1: downvote
    created_at = Column(DateTime, nullable=False)

    # Constraints: 한 사용자는 하나의 질문/답변에 1번만 투표
    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='unique_question_vote'),
        UniqueConstraint('user_id', 'answer_id', name='unique_answer_vote'),
    )
```

### 2.2 API 엔드포인트

```python
# backend/api/qa.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api/qa", tags=["Q&A"])

# 1. 질문 목록 조회
@router.get("/questions")
async def list_questions(
    project_id: Optional[int] = None,
    tag: Optional[str] = None,
    sort_by: str = "recent",  # recent, votes, unanswered
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """
    Q&A 질문 목록
    - 프로젝트별 필터
    - 태그별 필터
    - 정렬: 최신순, 추천순, 미해결
    """
    pass

# 2. 질문 상세 조회
@router.get("/questions/{question_id}")
async def get_question_detail(
    question_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    질문 상세 + 모든 답변
    - 조회수 증가
    - 답변은 추천순 정렬 (채택된 답변 최상단)
    """
    pass

# 3. 질문 작성
@router.post("/questions")
async def create_question(
    question_data: QuestionCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    새 질문 작성
    - 필수: title, content, project_id
    - 선택: tags
    - Contributor 이상만 가능
    """
    pass

# 4. 답변 작성
@router.post("/questions/{question_id}/answers")
async def create_answer(
    question_id: int,
    answer_data: AnswerCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    답변 작성
    - Contributor 이상만 가능
    """
    pass

# 5. 답변 채택
@router.post("/questions/{question_id}/accept/{answer_id}")
async def accept_answer(
    question_id: int,
    answer_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    답변 채택 (질문 작성자만 가능)
    - 답변자에게 평판 점수 +15
    - 질문 is_answered = True
    """
    pass

# 6. 투표 (질문/답변)
@router.post("/vote")
async def vote(
    vote_data: VoteRequest,  # question_id or answer_id, vote_type
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    질문/답변 추천/비추천
    - upvote (+1) or downvote (-1)
    - Member 이상만 가능
    """
    pass

# 7. 내 Q&A 활동
@router.get("/me/activity")
async def get_my_qa_activity(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    내가 작성한 질문/답변
    - 질문: 총 개수, 해결/미해결
    - 답변: 총 개수, 채택률
    """
    pass
```

### 2.3 프론트엔드 페이지

#### 1) Q&A 메인 페이지 (`/qa`)
```typescript
// frontend/src/app/qa/page.tsx

export default function QAPage() {
  // 레이아웃:
  // - 왼쪽: 필터 사이드바
  //   - 프로젝트 선택
  //   - 태그 필터
  //   - 상태 필터 (전체, 미해결, 해결)
  // - 오른쪽: 질문 리스트
  //   - 각 카드: 제목, 작성자, 조회수, 답변 수, 추천 수
  //   - 정렬: 최신순, 추천순, 미해결

  // 상단: "질문하기" 버튼
}
```

#### 2) 질문 상세 페이지 (`/qa/[id]`)
```typescript
// frontend/src/app/qa/[id]/page.tsx

export default function QuestionDetailPage({ params }: { params: { id: string } }) {
  // 질문 섹션:
  // - 제목
  // - 작성자 + 등급 배지
  // - 작성일, 조회수, 추천 수
  // - 내용 (마크다운 렌더링)
  // - 태그
  // - 추천/비추천 버튼

  // 답변 섹션:
  // - 채택된 답변 (최상단, 초록색 배경)
  // - 나머지 답변 (추천순)
  // - 각 답변: 작성자, 내용, 추천 수, 추천/비추천 버튼
  // - 질문 작성자라면 "채택" 버튼 표시

  // 답변 작성 폼 (하단)
  // - 마크다운 에디터
  // - "답변 작성" 버튼
}
```

#### 3) 질문 작성 페이지 (`/qa/new`)
```typescript
// frontend/src/app/qa/new/page.tsx

export default function NewQuestionPage() {
  // 폼:
  // - 프로젝트 선택 (드롭다운)
  // - 제목 (텍스트)
  // - 내용 (마크다운 에디터)
  // - 태그 (다중 선택, Autocomplete)

  // 미리보기 기능
  // "질문 게시" 버튼
}
```

### 2.4 평판 점수 시스템

```python
# backend/services/reputation_service.py

REPUTATION_POINTS = {
    # Q&A
    "question_created": 0,
    "answer_created": 0,
    "answer_accepted": 15,      # 답변 채택됨
    "question_upvote": 5,        # 질문 추천받음
    "answer_upvote": 10,         # 답변 추천받음
    "question_downvote": -2,     # 질문 비추천받음
    "answer_downvote": -5,       # 답변 비추천받음

    # 기여
    "pr_merged": 20,
    "issue_created": 5,
    "code_review": 10,
    "documentation": 15,
    "study_completed": 30,
    "event_attended": 10,
    "mentoring": 25,
}

async def add_reputation(user_id: int, action: str, db: AsyncSession):
    """
    사용자 평판 점수 증가
    """
    points = REPUTATION_POINTS.get(action, 0)

    user = await db.get(User, user_id)
    user.reputation_score += points
    await db.commit()

    # 배지 획득 조건 확인
    await check_reputation_badges(user_id, db)
```

---

## 3. 구현 우선순위 로드맵

### Phase 1: MVP (3개월) - 기본 회원 시스템

**목표**: 회원 등급 체계 구축 및 프로필 기능

**Backend (2주)**
- ✅ User 모델 확장 (member_tier, stats, profile 필드)
- ✅ Contribution 모델 생성
- ✅ Profile API 엔드포인트
- ✅ 등급 자동 승급 로직 (Visitor → Contributor → Member)
- ✅ GitHub 연동 (OAuth)

**Frontend (2주)**
- ✅ 프로필 페이지 (`/profile/[username]`)
- ✅ 프로필 편집 페이지 (`/profile/edit`)
- ✅ 멤버 디렉토리 (`/members`)
- ✅ 등급 배지 컴포넌트
- ✅ GitHub 연동 UI

**테스트 & 배포 (1주)**
- ✅ 단위 테스트
- ✅ 통합 테스트
- ✅ Production 배포

**주요 deliverable:**
- 사용자가 프로필을 생성하고 편집 가능
- GitHub 연동으로 자동 정보 수집
- Visitor/Contributor/Member 3단계 등급 시스템

---

### Phase 2: 기여 추적 & 배지 (2개월) - 게이미피케이션

**목표**: 기여 활동 자동 추적 및 배지 시스템

**Backend (3주)**
- ✅ Badge, UserBadge 모델 생성
- ✅ 배지 획득 로직 (이벤트 기반)
- ✅ 기여 이력 자동 수집 (GitHub API 연동)
- ✅ 평판 점수 계산 로직
- ✅ Leaderboard API

**Frontend (2주)**
- ✅ 배지 갤러리 컴포넌트
- ✅ 리더보드 페이지 (`/leaderboard`)
- ✅ 기여 타임라인 (프로필 페이지 내)
- ✅ 평판 점수 진행률 바

**데이터 시드 & 테스트 (1주)**
- ✅ 초기 배지 20개 생성
- ✅ 테스트 유저 데이터 생성
- ✅ E2E 테스트

**주요 deliverable:**
- 자동 배지 획득 시스템
- 실시간 리더보드
- 기여 활동 타임라인

---

### Phase 3: Q&A 시스템 (2개월) - 커뮤니티 활성화

**목표**: 프로젝트별 Q&A 커뮤니티 구축

**Backend (3주)**
- ✅ Question, Answer, QAVote 모델
- ✅ Q&A CRUD API
- ✅ 투표 시스템
- ✅ 답변 채택 기능
- ✅ 검색 및 필터링 (ElasticSearch or PostgreSQL Full-Text Search)

**Frontend (3주)**
- ✅ Q&A 메인 페이지 (`/qa`)
- ✅ 질문 상세 페이지 (`/qa/[id]`)
- ✅ 질문 작성 페이지 (`/qa/new`)
- ✅ 마크다운 에디터 통합 (예: react-markdown, @uiw/react-md-editor)
- ✅ 태그 자동완성
- ✅ 실시간 알림 (답변 작성 시)

**테스트 & 배포 (2주)**
- ✅ API 테스트
- ✅ UI 테스트
- ✅ 성능 최적화 (페이지네이션, 캐싱)

**주요 deliverable:**
- 완전한 Q&A 시스템
- 답변 채택 및 평판 점수 연동
- 프로젝트별 Q&A 필터링

---

### Phase 4: 고급 기능 (2개월) - 완성도 향상

**Backend**
- ✅ 알림 시스템 (이메일 + 인앱)
  - 답변 작성 알림
  - 답변 채택 알림
  - 등급 승급 알림
  - 배지 획득 알림
- ✅ 검색 고도화 (ElasticSearch)
- ✅ API Rate Limiting
- ✅ 관리자 대시보드 API

**Frontend**
- ✅ 알림 센터 (`/notifications`)
- ✅ 활동 피드 (`/activity`)
- ✅ 관리자 대시보드 (`/admin`)
  - 등급 승급 승인
  - 회원 관리
  - 통계 대시보드
- ✅ 다크 모드 지원 (이미 있음)
- ✅ 다국어 지원 (i18n) - 영어 추가

**성능 최적화**
- ✅ 데이터베이스 인덱싱
- ✅ Redis 캐싱 (리더보드, 통계)
- ✅ CDN 최적화
- ✅ 이미지 최적화 (프로필 이미지)

**주요 deliverable:**
- 실시간 알림 시스템
- 고성능 검색
- 관리자 도구

---

## 4. 기술 스택 및 아키텍처

### 4.1 백엔드 기술 스택

```yaml
Framework: FastAPI (Python 3.11+)
Database: PostgreSQL 15
ORM: SQLAlchemy (async)
Authentication: JWT (python-jose)
API Documentation: OpenAPI/Swagger
Validation: Pydantic v2

추가 라이브러리:
- httpx: GitHub API 연동
- python-multipart: 파일 업로드
- Pillow: 이미지 처리
- redis: 캐싱
- celery: 백그라운드 작업 (배지 계산, 통계)
- elasticsearch: 검색 (선택적)
```

### 4.2 프론트엔드 기술 스택

```yaml
Framework: Next.js 15 (App Router)
Language: TypeScript
Styling: Tailwind CSS
State Management: React Query (TanStack Query)
Form Handling: React Hook Form + Zod
Markdown: react-markdown, @uiw/react-md-editor
Charts: Recharts (통계 대시보드)
Icons: Lucide React
Date: date-fns
```

### 4.3 인프라

```yaml
Hosting: Railway (현재 사용 중)
Database: PostgreSQL (Railway)
File Storage: Cloudinary or AWS S3 (프로필 이미지)
CDN: Cloudflare
Cache: Redis (Railway Add-on)
CI/CD: GitHub Actions
Monitoring: Sentry (에러 추적)
```

### 4.4 데이터베이스 인덱스 전략

```sql
-- Users 테이블
CREATE INDEX idx_users_member_tier ON users(member_tier);
CREATE INDEX idx_users_reputation_score ON users(reputation_score DESC);
CREATE INDEX idx_users_github_username ON users(github_username);
CREATE INDEX idx_users_joined_at ON users(joined_at DESC);

-- Contributions 테이블
CREATE INDEX idx_contributions_user_id ON contributions(user_id);
CREATE INDEX idx_contributions_project_id ON contributions(project_id);
CREATE INDEX idx_contributions_type ON contributions(type);
CREATE INDEX idx_contributions_created_at ON contributions(created_at DESC);

-- Questions 테이블
CREATE INDEX idx_questions_project_id ON questions(project_id);
CREATE INDEX idx_questions_author_id ON questions(author_id);
CREATE INDEX idx_questions_is_answered ON questions(is_answered);
CREATE INDEX idx_questions_created_at ON questions(created_at DESC);
CREATE INDEX idx_questions_votes ON questions(votes DESC);
CREATE FULLTEXT INDEX idx_questions_title_content ON questions(title, content);

-- Answers 테이블
CREATE INDEX idx_answers_question_id ON answers(question_id);
CREATE INDEX idx_answers_author_id ON answers(author_id);
CREATE INDEX idx_answers_votes ON answers(votes DESC);
CREATE INDEX idx_answers_is_accepted ON answers(is_accepted);
```

---

## 5. 다음 단계

### 5.1 즉시 시작 가능한 작업

1. **Backend: User 모델 확장** (1일)
   - `backend/models/user.py` 수정
   - 마이그레이션 생성 및 실행

2. **Backend: Profile API** (2일)
   - `backend/api/profile.py` 생성
   - GET `/api/profile/{username}`
   - PUT `/api/profile/me`

3. **Frontend: 프로필 페이지** (3일)
   - `/profile/[username]/page.tsx` 생성
   - 프로필 컴포넌트 제작

### 5.2 의사결정 필요 사항

- [ ] **GitHub OAuth App 생성** → GitHub 연동 기능
- [ ] **프로필 이미지 저장소** → Cloudinary vs AWS S3?
- [ ] **검색 엔진** → PostgreSQL Full-Text vs ElasticSearch?
- [ ] **실시간 알림** → Server-Sent Events vs WebSocket?

### 5.3 정책 기반 구현 체크리스트

운영 정책 문서 기준:

- [ ] 5단계 회원 등급 (Visitor ~ Core Team)
- [ ] PR 3회 → Member 자동 승급
- [ ] 스터디 1회 → Member 자동 승급
- [ ] 기여도 상위 20% → Maintainer 후보
- [ ] 후원 등급별 혜택 (Bronze ~ Platinum)
- [ ] 행동 강령 위반 시 3단계 조치 (경고, 정지, 제명)
- [ ] 월간 MVP 투표 시스템
- [ ] 분기별 프로젝트 어워즈

---

**문서 버전**: 1.0
**다음 리뷰**: Phase 1 완료 시 (2025년 Q2)
**담당**: Core Team
