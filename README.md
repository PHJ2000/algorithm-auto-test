# 🧠 Baekjoon Algorithm Auto Organizer

> Baekjoon 문제를 자동으로 정리해주는 GitHub Actions 기반 저장소입니다.  
> 문제 번호만 입력해주면, solved.ac를 통해 난이도 및 알고리즘 태그를 불러와  
> **자동 디렉토리 분류 + 커밋 & 푸시까지 전부 자동화**됩니다.

---

## 🚀 사용법

### 1️⃣ 문제 파일 저장

아래 형식으로 문제를 풀고 `.py` 파일을 `백준_임시/` 폴더에 저장하세요:

```
백준_임시/문제번호_문제이름.py

예)
백준_임시/2178_미로_탐색.py
백준_임시/1920_수_찾기.py
```

---

### 2️⃣ 커밋 & 푸시

```bash
git add 백준_임시
git commit -m "✨ 2178 미로 탐색 추가"
git push origin main
```

---

### 3️⃣ 자동 분류 결과 확인

GitHub Actions가 실행되어 `.py` 파일이 아래처럼 정리됩니다:

```
백준/
└─ 실버/
   └─ bfs/
      └─ 실버1/
         └─ 2178_미로_탐색.py
```

---

## 📁 디렉토리 구조 예시

```
📂 백준/
 ┣ 📂 실버/
 ┃ ┣ 📂 bfs/
 ┃ ┃ ┗ 📂 실버1/
 ┃ ┃   ┗ 📜 2178_미로_탐색.py
 ┗ 📂 정렬/
   ┗ 📂 실버3/
     ┗ 📜 10989_수_정렬하기_3.py

📂 백준_임시/
 ┗ 📜 .gitkeep ← 정리 후 비워지며 유지됨
```

---

## 🛠 작동 방식

- `백준_임시/`에 `.py` 파일 추가 → Push
- GitHub Actions 워크플로우 자동 실행
- `organize_problems.py` 스크립트가 실행됨
- `solved.ac` API를 통해 문제의 티어 및 태그 수집
- 자동으로 디렉토리 구조 생성 및 이동
- 이동 결과는 bot 계정으로 자동 커밋되어 푸시됨

---

## 🔐 보안

- 워크플로우는 GitHub Secrets에 등록된 `GH_PAT` Personal Access Token으로 안전하게 푸시됩니다.
- 코드에는 토큰이 직접 노출되지 않으며, Fine-grained 권한으로 최소화됨.

---

## 🧩 의존 기술

| 도구 | 설명 |
|------|------|
| GitHub Actions | 자동화 트리거 및 푸시 실행 |
| Python | 분류 스크립트 실행 (`organize_problems.py`) |
| solved.ac API | 문제 난이도 및 알고리즘 태그 수집 |

---

## 📦 포크해서 사용하는 방법 (선택 사항)

> 🙋‍♀️ 나도 자동 정리 시스템을 쓰고 싶다면?

1. **이 저장소를 Fork**합니다.
2. 본인 GitHub 저장소에서 `Settings > Secrets > Actions`로 이동
3. **`GH_PAT`라는 이름으로 Personal Access Token을 등록**합니다.
4. `백준_임시/`에 문제 파일을 추가하고 push하면 자동 정리됩니다!

🔐 **주의**: 생성된 토큰은 반드시 `repo > contents: read & write`,`repo > workflows: read & write`  권한을 포함해야 합니다.

---

## 🙌 기여

- 문제 정리, 태그 맵핑 확장, 사용법 문서화 등 환영합니다!
- PR 환영합니다 ✨

---

## 📚 참고 자료

- [solved.ac Unofficial API 문서](https://solvedac.github.io/unofficial-documentation/)
- [Baekjoon Online Judge](https://www.acmicpc.net/)
