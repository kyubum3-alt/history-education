# AGENTS.md — 최규범의 역사교육론 연구 자료실

이 저장소에서 작업하는 AI 에이전트(Codex 등)는 **작업 전에 이 문서를 끝까지 읽고**, 아래 규칙을 반드시 지킬 것.

---

## 1. 프로젝트 개요

역사교육학 논문 번역본과 스페인어 학습 자료(RTVE 뉴스)를 모아두는 **정적 웹사이트**다.
프레임워크·빌드 과정 없음. HTML 파일을 폴더에 넣고 `posts.json`에 등록하면 끝.

| 항목 | 값 |
|---|---|
| GitHub 저장소 | `kyubum3-alt/history-education` |
| 배포 URL | https://kyubum3-alt.github.io/history-education/ |
| 기본 브랜치 | `main` |
| 로컬 폴더 | `C:\Users\user\OneDrive\문서\Claude\Projects\최규범의 역사교육학 자료 관리 홈페이지` |
| 배포 방식 | GitHub Pages (main 브랜치 루트) — push하면 자동 반영 |
| 소유자 | 최규범 (kyubum3@gmail.com) · 중학교 역사교사, 서울대 대학원생 |

> ⚠️ GitHub 계정 `kyubum3`와 `kyubum3-alt`를 혼동하지 말 것. 이 프로젝트는 **kyubum3-alt**다.

---

## 2. 파일 구조

```
/
├── index.html          # 사이트 전체 (레이아웃 + CSS + JS). 346줄. 여기만 손대면 UI가 바뀜
├── posts.json          # ★ 자료 목록 데이터. 새 자료 추가는 사실상 이 파일 수정이 전부
├── README.md
├── deploy.py           # 과거 1회성 배포 스크립트 (하드코딩된 논문 목록 포함, 그대로 실행 금지)
├── posts.json.backup   # 옛 백업. 참조용
├── posts.json.old      # 옛 백업. 참조용
└── *.html              # 논문 번역본 / RTVE 뉴스 본문 파일 (약 90개)
```

`index.html`은 `fetch('posts.json')` → `init()` 순으로 동작하는 단일 페이지다.
사이드바·목록·정렬 전부 JS가 `posts.json`을 읽어 렌더링한다. **HTML 본문 파일은 링크로만 연결된다.**

---

## 3. posts.json 스키마

최상위는 4개 섹션 배열이며, 이 키 이름은 `index.html`의 `sectionOrder` / `sectionNames`와 정확히 일치해야 한다.

```json
{
  "korean": [],
  "spanish": [],
  "english": [],
  "spanish-study-RTVE뉴스": []
}
```

| 키 | 화면 표기 | 내용 |
|---|---|---|
| `korean` | 국내 | 한국어로 쓰인 논문 |
| `spanish` | 스페인어권 | 스페인어 논문의 한국어 번역본 |
| `english` | 영어권 | 영어 논문의 한국어 번역본 |
| `spanish-study-RTVE뉴스` | RTVE 뉴스 | 스페인어 학습용 RTVE 10분뉴스 |

**논문 항목 필드**

```json
{
  "title": "스페인 학교의 역사 교과서 수용(19~20세기): 연구 현황",
  "authors": "Valls",
  "year": 1998,
  "url": "Valls_1998_스페인 학교의 역사 교과서 수용(19~20세기).html",
  "uploadDate": "2026-07-30"
}
```

**RTVE 뉴스 항목 필드**

```json
{
  "title": "2026년 5월 16일 - RTVE 10분뉴스",
  "date": "2026년 5월 16일",
  "url": "RTVE_10minutos_16052026_final.html",
  "uploadDate": "2026-05-18"
}
```

- 공통 필수 필드: `title`, `url`, `uploadDate`
- `url`은 **저장소 루트 기준 상대경로**(파일명 그대로). 한글·공백·괄호가 포함되어도 그대로 쓴다.
- `uploadDate`는 `YYYY-MM-DD`. 목록 정렬 기준이며, **같은 날짜면 배열 순서가 우선**이므로 새 항목은 배열 앞(`insert(0, ...)`)에 넣는다.
- 파일명 명명 규칙: `저자_연도_제목.html` (예: `Parkes_2024_한국어번역.html`), RTVE는 `RTVE_10minutos_DDMMYYYY_final.html`.

---

## 4. 🚨 절대 규칙 (과거 사고로 얻은 교훈)

### 규칙 1 — `posts.json`은 반드시 Python으로 수정한다

문자열 치환 도구(Edit/patch/sed)로 JSON을 고치다가 **파일 끝이 잘려 사이트 전체가 백지가 되는 사고가 여러 번** 있었다. 손상된 JSON이 push되면 GitHub Pages 캐시(5~10분) 때문에 이후 수정도 한동안 반영되지 않아 원인 파악이 더 어려워진다.

```python
import json

with open('posts.json', 'r', encoding='utf-8') as f:
    posts = json.load(f)          # 여기서 문법 검증됨

posts['english'].insert(0, {
    "title": "...", "authors": "...", "year": 2026,
    "url": "....html", "uploadDate": "2026-08-19"
})

with open('posts.json', 'w', encoding='utf-8', newline='') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
```

- `ensure_ascii=False` 필수 (한글 깨짐 방지)
- `indent=2` 필수 (diff 가독성)
- `newline=''` 필수 (기존 파일의 CRLF 개행 유지 → 불필요한 전체 diff 방지)

### 규칙 2 — 파일 크기별로 수정 도구를 바꾼다

| 파일 | 권장 도구 | 이유 |
|---|---|---|
| `posts.json` (모든 크기) | **Python `json` 모듈만** | 문법 자동 검증 |
| HTML 500줄 이상 | `sed` / `awk` | 문자열 치환 도구가 파일 끝을 자름 |
| HTML 500줄 미만 (`index.html` 346줄) | 일반 편집 가능 | 단, 수정 후 검증 필수 |

### 규칙 3 — push 전에 반드시 검증한다

```bash
python3 -m json.tool posts.json > /dev/null && echo "JSON OK"
tail -c 20 posts.json          # 반드시 } 로 끝나야 함
wc -l posts.json index.html    # 라인 수가 급감했으면 손상 의심
tail -3 index.html             # </html> 로 끝나야 함
```

### 규칙 4 — 한 번에 한 가지만 고친다

CSS·HTML·JS를 한꺼번에 바꾸면 어디서 깨졌는지 특정할 수 없다. 수정 → 검증 → 커밋을 한 단위로 반복한다.

### 규칙 5 — 새 HTML 파일을 `git add` 했는지 확인한다

`posts.json`에는 등록했는데 본문 HTML 파일을 커밋하지 않아 **링크가 404 나는 사고가 실제로 있었다.**
자료를 추가한 뒤 반드시 확인:

```bash
git status --short          # ?? 로 남은 파일이 없어야 함
```

---

## 5. 새 자료 추가 표준 절차

1. 번역본 HTML 파일을 저장소 루트에 저장한다 (명명 규칙 준수).
2. Python으로 `posts.json`의 해당 섹션 배열 **맨 앞에** 항목을 추가한다 (규칙 1).
3. 검증한다 (규칙 3).
4. 무결성 교차 확인 — `posts.json`의 모든 `url`이 실제로 존재하는지:

```bash
python3 -c "
import json, os
d = json.load(open('posts.json', encoding='utf-8'))
urls = {p['url'] for v in d.values() for p in v}
missing = [u for u in urls if not u.startswith('http') and not os.path.exists(u)]
orphan = [f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html' and f not in urls]
print('파일 없음:', missing)
print('미등록 파일:', orphan)
"
```

5. 로컬에서 `index.html`을 브라우저로 열어 사이드바 개수와 새 항목이 보이는지 확인한다 (F12 콘솔 에러 없어야 함).
6. 커밋 & push (아래 6장).
7. 배포 확인: 브라우저에서 `Ctrl+Shift+R`로 캐시 무시 새로고침. 즉시 반영 안 되면 5~10분 기다린다.

**커밋 메시지 관례**: 한국어, 무엇을 추가/변경했는지 구체적으로.
예) `논문 7편 추가: Harris·Foreman-Peck 2004, Mir 2001, Bain 2026, ...`

---

## 6. Git 워크플로우

```bash
git add <추가한 HTML 파일들> posts.json
git commit -m "자료 추가: ..."
git push origin main
```

### 인증

`origin` 리모트 URL에 토큰이 비어 있어(`https://kyubum3-alt:@github.com/...`) 그대로 push하면 인증에 실패할 수 있다.
Personal Access Token은 `C:\Users\user\Documents\github_config.json`에 있다. 실패하면:

```bash
git push "https://kyubum3-alt:<TOKEN>@github.com/kyubum3-alt/history-education.git" main
```

> 🔒 토큰을 커밋·로그·리모트 URL에 평문으로 남기지 말 것. 가능하면 `gh auth login` 또는 Git Credential Manager로 한 번 인증해두는 편이 안전하다.

### 초기 설정 (최초 1회)

```bash
git config --global user.email "kyubum3@gmail.com"
git config --global user.name "Kyubum Choi"
```

### 자주 겪은 문제

| 증상 | 원인 | 대응 |
|---|---|---|
| 사이트가 헤더만 뜨고 목록이 비어 있음 | `posts.json` 손상 | `python3 -m json.tool posts.json` 로 확인 → `git show <정상커밋>:posts.json > posts.json` 복구 |
| 수정했는데 반영 안 됨 | GitHub Pages / 브라우저 캐시 | `Ctrl+Shift+R`, 5~10분 대기 |
| `index.lock` 오류로 git 명령 실패 | 이전 git 프로세스 잔여물 | `rm -f .git/index.lock` 후 재시도 |
| `.git/index` 손상 | 로컬 인덱스 문제 (원격에는 영향 없음) | `git read-tree HEAD` 또는 fresh clone |
| 링크 클릭 시 404 | HTML 파일 미커밋 | `git status`로 `??` 확인 후 add |

---

## 7. 손대지 말아야 할 것

- **`deploy.py`를 그대로 실행하지 말 것.** 2026-05-13 시점의 논문 목록이 하드코딩돼 있어 실행하면 중복 항목이 추가된다. 참고용으로만 읽는다.
- `posts.json.backup`, `posts.json.old`는 과거 백업이다. 수정하거나 참조 대상으로 삼지 않는다.
- 섹션 키 이름(`korean`/`spanish`/`english`/`spanish-study-RTVE뉴스`)을 바꾸려면 `index.html`의 `sectionOrder`·`sectionNames`도 함께 바꿔야 한다. 한쪽만 바꾸면 목록이 사라진다.
- 기존 HTML 본문 파일의 내용은 번역 결과물이다. 요청 없이 문구를 고치지 않는다.

---

## 8. 소통 규칙

- 답변은 **한국어로, 간결하게 핵심만**.
- 대학원 연구 관련 내용에는 근거(논문·기고문 출처)를 반드시 표시한다.
- 파괴적 작업(파일 삭제, force push, 대량 치환) 전에는 반드시 확인을 받는다.
