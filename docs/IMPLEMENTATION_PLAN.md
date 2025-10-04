# 공작소 TFT 기능 구현 계획

**작성일**: 2025-10-04
**버전**: 2.0 (확장판)
**기준 문서**: 운영 정책 1.0, SWOT 분석
**총 구현 기간**: 약 20개월 (Phase 1-8)

---

## 목차

1. [개요](#개요)
2. [회원 관리 및 프로필 시스템](#1-회원-관리-및-프로필-시스템)
3. [프로젝트 Q&A 시스템](#2-프로젝트-qa-시스템)
4. [구현 우선순위 로드맵](#3-구현-우선순위-로드맵)
   - Phase 1: MVP - 기본 회원 시스템
   - Phase 2: 기여 추적 & 배지
   - Phase 3: Q&A 시스템
   - Phase 4: 고급 기능 (알림, 관리자 도구)
   - **Phase 5: 커뮤니티 게시판** ⭐ NEW
   - **Phase 6: 스터디 관리 시스템** ⭐ NEW
   - **Phase 7: 프로젝트 협업 기능 강화** ⭐ NEW
   - **Phase 8: 행사/세미나 관리** ⭐ NEW
5. [기술 스택 및 아키텍처](#4-기술-스택-및-아키텍처)

---

## 개요

### 목적
운영 정책과 SWOT 분석을 기반으로 데이터공작소 TFT의 핵심 기능을 체계적으로 구현하여 커뮤니티 활성화와 지속 가능성을 확보합니다.

### 핵심 목표

**Phase 1-4: 핵심 기능 (9개월)**
- ✅ **회원 등급 시스템**: 5단계 회원 등급 체계 구현 (Visitor → Core Team)
- ✅ **기여도 추적**: PR, 이슈, 스터디 참여 등 자동 집계
- ✅ **프로필 시스템**: 멤버 포트폴리오 및 활동 이력 관리
- ✅ **Q&A 기능**: 프로젝트별 질문/답변 커뮤니티
- ✅ **게이미피케이션**: 배지, 레벨, 리더보드

**Phase 5-8: 커뮤니티 확장 (11개월)** ⭐ NEW
- 📢 **게시판**: 공지사항, 자유게시판, 건의사항
- 📚 **스터디**: 스터디 그룹 생성, 일정 관리, 자료 공유
- 👥 **프로젝트 협업**: Kanban 보드, 작업 관리, 토론
- 🎉 **행사 관리**: 세미나/밋업 생성, 참가 신청, QR 출석

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

### Phase 5: 커뮤니티 게시판 (2개월) - 소통 활성화

**목표**: 공지사항, 자유게시판, 건의사항 등 커뮤니티 게시판 구축

**Backend (3주)**

데이터베이스 스키마:
```python
# backend/models/board.py

from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class BoardType(str, Enum):
    NOTICE = "notice"           # 공지사항 (운영진만 작성)
    FREE = "free"               # 자유게시판
    FEEDBACK = "feedback"       # 건의사항
    QNA = "qna"                 # 질문/답변 (간단한 Q&A)

class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True)
    type = Column(Enum(BoardType), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 메타데이터
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)  # 상단 고정
    is_notice = Column(Boolean, default=False)  # 중요 공지

    # 파일 첨부
    attachments = Column(JSON)  # [{"name": "file.pdf", "url": "..."}]

    # 타임스탬프
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    # Relationships
    author = relationship("User", back_populates="board_posts")
    comments = relationship("BoardComment", back_populates="post", cascade="all, delete-orphan")

class BoardComment(Base):
    __tablename__ = "board_comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("boards.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("board_comments.id"))  # 대댓글

    likes = Column(Integer, default=0)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    # Relationships
    post = relationship("Board", back_populates="comments")
    author = relationship("User")
    replies = relationship("BoardComment", backref="parent", remote_side=[id])
```

API 엔드포인트:
```python
# backend/api/board.py

# 게시글 목록
GET /api/boards?type=notice&page=1&limit=20

# 게시글 상세
GET /api/boards/{post_id}

# 게시글 작성 (인증 필요)
POST /api/boards
{
    "type": "free",
    "title": "제목",
    "content": "내용",
    "attachments": []
}

# 게시글 수정
PUT /api/boards/{post_id}

# 게시글 삭제
DELETE /api/boards/{post_id}

# 댓글 작성
POST /api/boards/{post_id}/comments
{
    "content": "댓글 내용",
    "parent_id": null  # 대댓글이면 부모 댓글 ID
}

# 좋아요
POST /api/boards/{post_id}/like
DELETE /api/boards/{post_id}/like
```

**Frontend (3주)**

페이지 구조:
```typescript
// /app/board/page.tsx - 게시판 홈
// - 공지사항, 자유게시판, 건의사항 탭

// /app/board/[type]/page.tsx - 게시판 목록
// - type: notice, free, feedback

// /app/board/[type]/[id]/page.tsx - 게시글 상세

// /app/board/[type]/new/page.tsx - 게시글 작성
```

주요 컴포넌트:
- `<BoardList>` - 게시글 목록 (페이지네이션)
- `<BoardPost>` - 게시글 상세 + 댓글
- `<BoardEditor>` - 게시글 작성/수정 (마크다운)
- `<CommentSection>` - 댓글/대댓글

**테스트 & 배포 (1주)**

**주요 deliverable:**
- 공지사항, 자유게시판, 건의사항 완성
- 댓글/대댓글 시스템
- 파일 첨부 기능

---

### Phase 6: 스터디 관리 시스템 (3개월) - 학습 커뮤니티

**목표**: 스터디 그룹 생성 및 관리, 학습 활동 추적

**Backend (4주)**

데이터베이스 스키마:
```python
# backend/models/study.py

from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

class StudyStatus(str, Enum):
    RECRUITING = "recruiting"   # 모집 중
    IN_PROGRESS = "in_progress" # 진행 중
    COMPLETED = "completed"     # 완료
    CANCELLED = "cancelled"     # 취소

class Study(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    # 스터디 정보
    category = Column(String(50))  # Python, JavaScript, AI, etc.
    max_members = Column(Integer, default=10)
    status = Column(Enum(StudyStatus), default=StudyStatus.RECRUITING)

    # 일정
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    meeting_schedule = Column(String(200))  # "매주 토요일 오후 2시"

    # 요구사항
    required_level = Column(String(50))  # Beginner, Intermediate, Advanced
    prerequisites = Column(Text)  # 사전 요구사항

    # 메타데이터
    tags = Column(JSON)  # ["Python", "Django", "웹개발"]
    study_materials = Column(JSON)  # [{"name": "자료.pdf", "url": "..."}]

    # 리더
    leader_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    # Relationships
    leader = relationship("User", foreign_keys=[leader_id])
    members = relationship("StudyMember", back_populates="study")
    sessions = relationship("StudySession", back_populates="study")

class StudyMember(Base):
    __tablename__ = "study_members"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey("studies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    role = Column(String(50), default="member")  # leader, mentor, member
    status = Column(String(50), default="active")  # active, pending, left

    # 참여 통계
    attendance_count = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)

    joined_at = Column(DateTime, nullable=False)

    # Relationships
    study = relationship("Study", back_populates="members")
    user = relationship("User")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True)
    study_id = Column(Integer, ForeignKey("studies.id"), nullable=False)

    title = Column(String(200), nullable=False)
    description = Column(Text)
    session_date = Column(DateTime, nullable=False)

    # 세션 자료
    materials = Column(JSON)  # [{"name": "발표자료.pdf", "url": "..."}]
    recording_url = Column(String(500))  # 녹화 영상 링크

    # 출석
    attendees = Column(JSON)  # [user_id1, user_id2, ...]

    created_at = Column(DateTime, nullable=False)

    # Relationships
    study = relationship("Study", back_populates="sessions")
```

API 엔드포인트:
```python
# 스터디 목록
GET /api/studies?status=recruiting&category=Python

# 스터디 상세
GET /api/studies/{study_id}

# 스터디 생성 (인증 필요, Member 이상)
POST /api/studies

# 스터디 가입 신청
POST /api/studies/{study_id}/join

# 스터디 멤버 관리
GET /api/studies/{study_id}/members
PUT /api/studies/{study_id}/members/{user_id}  # 승인/역할 변경

# 세션 관리
GET /api/studies/{study_id}/sessions
POST /api/studies/{study_id}/sessions
PUT /api/studies/{study_id}/sessions/{session_id}

# 출석 체크
POST /api/studies/{study_id}/sessions/{session_id}/attendance
```

**Frontend (4주)**

페이지 구조:
```typescript
// /app/studies/page.tsx - 스터디 목록
// /app/studies/[id]/page.tsx - 스터디 상세
// /app/studies/[id]/sessions/page.tsx - 세션 목록
// /app/studies/[id]/members/page.tsx - 멤버 관리
// /app/studies/new/page.tsx - 스터디 생성
```

**테스트 & 배포 (1주)**

**주요 deliverable:**
- 스터디 그룹 생성 및 모집
- 멤버 관리 및 출석 체크
- 세션 자료 공유
- 스터디 완료 시 자동 등급 승급

---

### Phase 7: 프로젝트 협업 기능 강화 (2개월) - 팀워크

**목표**: 기존 Project 모델 확장, 실시간 협업 기능 추가

**Backend (3주)**

데이터베이스 스키마 확장:
```python
# backend/models/project.py 확장

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    role = Column(String(50))  # owner, maintainer, contributor
    permissions = Column(JSON)  # ["write", "admin", "deploy"]

    joined_at = Column(DateTime)

    # Relationships
    project = relationship("Project")
    user = relationship("User")

class ProjectTask(Base):
    __tablename__ = "project_tasks"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))

    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50))  # todo, in_progress, review, done
    priority = Column(String(50))  # low, medium, high, urgent

    assignee_id = Column(Integer, ForeignKey("users.id"))
    created_by = Column(Integer, ForeignKey("users.id"))

    due_date = Column(DateTime)
    created_at = Column(DateTime)
    completed_at = Column(DateTime)

    # Relationships
    project = relationship("Project")
    assignee = relationship("User", foreign_keys=[assignee_id])
    creator = relationship("User", foreign_keys=[created_by])

class ProjectDiscussion(Base):
    __tablename__ = "project_discussions"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))

    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"))

    is_pinned = Column(Boolean, default=False)

    created_at = Column(DateTime)

    # Relationships
    project = relationship("Project")
    author = relationship("User")
    comments = relationship("DiscussionComment", back_populates="discussion")
```

API 엔드포인트:
```python
# 프로젝트 멤버
GET /api/projects/{project_id}/members
POST /api/projects/{project_id}/members  # 멤버 초대
PUT /api/projects/{project_id}/members/{user_id}  # 역할 변경
DELETE /api/projects/{project_id}/members/{user_id}

# 작업 관리
GET /api/projects/{project_id}/tasks
POST /api/projects/{project_id}/tasks
PUT /api/projects/{project_id}/tasks/{task_id}
DELETE /api/projects/{project_id}/tasks/{task_id}

# 토론
GET /api/projects/{project_id}/discussions
POST /api/projects/{project_id}/discussions
```

**Frontend (3주)**

페이지 구조:
```typescript
// /app/projects/[id]/board/page.tsx - 작업 칸반 보드
// /app/projects/[id]/discussions/page.tsx - 프로젝트 토론
// /app/projects/[id]/members/page.tsx - 멤버 관리
// /app/projects/[id]/settings/page.tsx - 프로젝트 설정
```

주요 컴포넌트:
- `<KanbanBoard>` - 드래그앤드롭 작업 보드
- `<TaskCard>` - 작업 카드
- `<MemberList>` - 멤버 목록 및 권한 관리

**주요 deliverable:**
- Kanban 스타일 작업 보드
- 멤버별 역할 및 권한 관리
- 프로젝트 토론 기능

---

### Phase 8: 행사/세미나 관리 (2개월) - 오프라인 연결

**목표**: 온라인/오프라인 행사 관리 및 아카이브

**Backend (3주)**

데이터베이스 스키마:
```python
# backend/models/event.py

from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

class EventType(str, Enum):
    SEMINAR = "seminar"         # 세미나
    WORKSHOP = "workshop"       # 워크샵
    MEETUP = "meetup"           # 밋업
    HACKATHON = "hackathon"     # 해커톤
    CONFERENCE = "conference"   # 컨퍼런스

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    # 행사 정보
    type = Column(Enum(EventType), nullable=False)
    category = Column(String(50))  # AI, Web, Mobile, Data, etc.

    # 일정
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)

    # 장소
    is_online = Column(Boolean, default=False)
    location = Column(String(200))  # 오프라인 주소
    online_link = Column(String(500))  # Zoom, Google Meet 링크

    # 등록 정보
    max_participants = Column(Integer)
    registration_deadline = Column(DateTime)
    requires_approval = Column(Boolean, default=False)

    # 메타데이터
    tags = Column(JSON)
    speakers = Column(JSON)  # [{"name": "홍길동", "bio": "..."}]
    agenda = Column(JSON)  # [{"time": "14:00", "title": "세션1"}]

    # 자료
    materials = Column(JSON)  # 행사 자료
    recording_url = Column(String(500))  # 녹화 영상
    photos = Column(JSON)  # 행사 사진

    # 주최자
    organizer_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime)

    # Relationships
    organizer = relationship("User")
    registrations = relationship("EventRegistration", back_populates="event")

class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    status = Column(String(50))  # pending, approved, attended, cancelled

    # 참가 정보
    questions_answers = Column(JSON)  # 참가 신청 시 질문 응답
    attended = Column(Boolean, default=False)
    attended_at = Column(DateTime)

    registered_at = Column(DateTime)

    # Relationships
    event = relationship("Event", back_populates="registrations")
    user = relationship("User")
```

API 엔드포인트:
```python
# 행사 목록
GET /api/events?type=seminar&upcoming=true

# 행사 상세
GET /api/events/{event_id}

# 행사 생성 (Member 이상)
POST /api/events

# 참가 신청
POST /api/events/{event_id}/register
{
    "questions_answers": {"질문1": "답변1"}
}

# 참가 신청 관리 (주최자)
GET /api/events/{event_id}/registrations
PUT /api/events/{event_id}/registrations/{registration_id}  # 승인/거절

# 출석 체크
POST /api/events/{event_id}/attendance/{user_id}

# 행사 아카이브
GET /api/events/archive?year=2024
```

**Frontend (3주)**

페이지 구조:
```typescript
// /app/events/page.tsx - 행사 목록 (예정/지난)
// /app/events/[id]/page.tsx - 행사 상세 및 참가 신청
// /app/events/[id]/registrations/page.tsx - 참가자 관리 (주최자)
// /app/events/archive/page.tsx - 행사 아카이브
// /app/events/new/page.tsx - 행사 생성
```

주요 컴포넌트:
- `<EventCard>` - 행사 카드
- `<EventRegistrationForm>` - 참가 신청 폼
- `<EventAttendanceCheck>` - QR 출석 체크
- `<EventGallery>` - 행사 사진 갤러리

**테스트 & 배포 (1주)**

**주요 deliverable:**
- 온라인/오프라인 행사 생성 및 관리
- 참가 신청 및 승인 시스템
- 출석 체크 (QR 코드)
- 행사 아카이브 및 영상 공유

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
