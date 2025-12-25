# 🍞 Breadtopia (빵토피아)

**"빵지순례의 새로운 시작, 빵토피아에서 당신만의 빵 여행을 시작하세요"**

Breadtopia는 흩어진 빵집 정보를 통합하고, 게이미피케이션 요소를 결합하여 즐거운 빵지순례 경험을 제공하는 웹 플랫폼입니다. 사용자의 취향을 분석하는 AI 알고리즘과 귀여운 펫(웰시코기) 컨셉을 도입하여 단순한 정보 검색을 넘어선 '탐험'의 재미를 선사합니다.

---

📌 목차

프로젝트 개요

핵심 기능

기술 스택

시스템 아키텍처 & ERD

주요 알고리즘 및 로직

설치 및 실행 가이드

팀원 소개

---

## 📖 프로젝트 개요

### 📅 개발 기간

2025.12.13 ~ 2025.12.24 (총 12일)

---

### 🎯 기획 의도

MZ세대의 트렌드인 **'빵지순례'**와 '로컬 탐방' 문화를 겨냥했습니다. 기존의 블로그나 지도 앱에 파편화된 정보를 통합하고, 단순히 빵집을 찾는 것을 넘어 레벨업과 뱃지 수집을 통해 사용자가 지속적으로 참여할 수 있는 동기를 부여합니다.

### 💡 해결하고자 하는 문제

정보 파편화: 여러 플랫폼에 흩어진 빵집 정보와 리뷰의 통합

취향 미스매치: AI 및 키워드 분석을 통한 개인화된 빵집 추천

기록의 부재: '빵 여권' 시스템을 통한 체계적인 탐방 기록

### ✨ 핵심 기능

1. 🤖 AI 기반 3대 서비스

오늘의 빵집 추천: 사용자가 설정한 선호 키워드(달달함, 고소함 등)를 분석하여 매일 자정, 새로운 빵집을 추천합니다.

웰시코기 챗봇: 우측 하단에 플로팅되는 AI 챗봇이 빵집 위치, 영업시간, 메뉴 등을 실시간으로 안내합니다.

AI 리뷰 요약: 수많은 리뷰 데이터를 LLM이 분석하여 3~5줄의 핵심 요약(장단점, 추천 메뉴)을 제공합니다.

2. 🗺️ 지도 기반 탐색 & 기분 필터

Kakao Map API를 활용하여 내 주변 빵집을 직관적으로 탐색합니다.

기분 필터: "☁️ 우울할 땐", "🎉 즐거울 땐" 등 현재 기분을 선택하면 그에 어울리는 맛(달달함, 화려함 등)을 가진 빵집을 추천합니다.

3. 🎮 게이미피케이션 (빵 여권)

레벨 시스템: 리뷰 작성, 방문 인증 시 경험치(EXP)를 획득하여 '아기빵쥐(Lv.1)'에서 '황금밀 유니콘(Lv.10)'까지 성장합니다.

뱃지 수집: 특정 조건(크루아상 리뷰 10개 등) 달성 시 유니크한 뱃지를 획득하여 핀보드에 장식할 수 있습니다.

4. 🤝 커뮤니티

빵덕후들을 위한 자유 게시판, 질문, 정보 공유 공간을 제공하며 좋아요 및 댓글 기능을 지원합니다.

---

### 🛠 기술 스택

#### Backend

Django

RESTful API 서버 구축

SQLite

Python

---

#### Frontend

VUE

Vite

Pinia

vue-router

AXIOS

Java Script

CSS

HTML


---

#### Infrastructure & Tools

API: Kakao Map API, OpenAI API (Chatbot/Summary)

Git

Gitflow Workflow

VS Code

---

### System Architecture & ERD

#### User

사용자 정보, 레벨, 경험치, 칭호 관리

#### Store

빵집 정보, 위경도 좌표, 평균 평점

#### Review

평점, 내용, taste_tags(맛 태그 JSON), 이미지

#### Badge

획득 조건 및 뱃지 메타데이터

#### Note

User와 Badge는 N:M 관계이며, Store와 Review는 1:N 관계를 가집니다.

---
비동기 서버 통신

Infrastructure & Tools

API: Kakao Map API, OpenAI API (Chatbot/Summary)

VCS: Git, Gitflow Workflow

IDE: VS Code

---

## 🧩 주요 알고리즘 및 로직

1. 오늘의 빵집 추천 (Determinetic Random)

매번 랜덤하게 바뀌는 것이 아니라, 하루 동안은 동일한 추천을 유지하기 위해 날짜와 사용자 ID를 시드(Seed)로 사용합니다.


2. 자동 레벨업 시스템 (Django Signals)

리뷰 작성과 동시에 비즈니스 로직이 트리거되도록 Django Signal을 활용했습니다.

경험치 획득 메서드 내부에서 check_level_up()이 자동 수행되어 등급과 칭호를 즉시 업데이트

3. 기분 기반 필터링

사용자의 감정 상태를 빵의 맛(Taste Tags)과 매핑하여 추천합니다.

Input: "☁️ 우울할 땐"

Mapping: ['달달함', '부드러움', '따뜻함']

Output: 해당 태그를 포함한 리뷰가 많은 빵집 목록 (평점순 정렬)

---

## 💻 설치 및 실행 가이드

이 프로젝트는 로컬 환경에서 실행하기 위해 .env 설정이 필요합니다.

---
### 1. backend setup

```bash
가상환경 생성 및 실행
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

패키지 설치
pip install -r requirements.txt

환경 변수 설정 (.env 파일 생성)
SECRET_KEY, KAKAO_API_KEY 등 입력

DB 마이그레이션 및 실행
python manage.py migrate
python manage.py loaddata fixtures/*.json  # 초기 데이터 로드
python manage.py runserver
```

---

### 2. Frontend Setup (Vue 3)

```bash
패키지 설치
npm install

환경 변수 설정 (.env.local 파일 생성)
VITE_KAKAO_MAP_API_KEY 입력

개발 서버 실행
npm run dev
```
---

## 👥 팀원 소개


| 이름      | 역할            | 담당 기능                                                    |
| ------- | ------------- | -------------------------------------------------------- |
| **조하원** | 팀장 (Backend)  | Back-End, DB, User / Store / Review 모델 설계, 레벨 시스템, 인증·인가 |
| **손효지** | 팀원 (Frontend) | Front-End, UX, 지도 API 연동, 컴포넌트 구현, 마이페이지 / 커뮤니티          |

---

### 📬 Contact

프로젝트에 대한 문의사항이나 제안은 Issues 탭을 이용해 주세요.

Copyright © 2025 Breadtopia Team. All rights reserved.