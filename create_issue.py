import os
import requests
import re
import argparse

# ⬇️ argparse 추가
parser = argparse.ArgumentParser()
parser.add_argument('--test', action='store_true', help='테스트 모드 (이슈를 실제로 생성하지 않음)')
args = parser.parse_args()
IS_TEST = args.test

ISSUE_QUEUE_FILE = "issue_queue.txt"
GITHUB_REPO = "PHJ2000/baekjoon-auto-organizer"
GH_TOKEN = os.environ.get("GH_PAT", "")

HEADERS = {
    "Authorization": f"token {GH_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_problem_info(problem_id):
    url = f"https://solved.ac/api/v3/problem/show?problemId={problem_id}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            title = data["titleKo"]
            level = data["level"]
            tags = [tag["key"] for tag in data["tags"]]
            return title, level, tags
    except:
        return None, None, []
    return None, None, []

def issue_exists(title):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues?state=all"
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        issues = res.json()
        return any(title in issue["title"] for issue in issues)
    return False

def create_issue(problem_id, problem_title):
    title_ko, level, tags = get_problem_info(problem_id)
    if not title_ko:
        print(f"❌ 문제 정보 가져오기 실패: {problem_id}")
        return False

    issue_title = f"[BOJ {problem_id}] {title_ko}"
    tag_str = ", ".join(tags)
    boj_link = f"https://www.acmicpc.net/problem/{problem_id}"

    body = f"""### 🔗 [문제 링크]({boj_link})
- 문제 번호: {problem_id}
- 난이도: solved.ac 레벨 {level}
- 분류: {tag_str}

---

## ✅ 체크리스트
- [ ] 문제 풀이 완료
- [ ] 커밋 연결
- [ ] Closes 연결 및 PR 반영
"""

    if issue_exists(issue_title):
        print(f"⏩ 이미 존재하는 이슈: {issue_title}")
        return True

    if IS_TEST:
        print(f"🧪 [TEST] 생성할 이슈 ↓")
        print(f"제목: {issue_title}")
        print(body)
        return True

    # 실제 이슈 생성
    payload = {
        "title": issue_title,
        "body": body,
        "labels": ["baekjoon", f"level-{level}"]
    }

    res = requests.post(
        f"https://api.github.com/repos/{GITHUB_REPO}/issues",
        json=payload,
        headers=HEADERS
    )

    if res.status_code == 201:
        print(f"✅ 이슈 생성 완료: {issue_title}")
        return True
    else:
        print(f"❌ 이슈 생성 실패: {res.status_code} | {res.text}")
        return False

def update_queue_file(lines_to_keep):
    if IS_TEST:
        print("🧪 [TEST] 큐 파일 수정 생략")
        return
    with open(ISSUE_QUEUE_FILE, "w", encoding="utf-8") as f:
        for line in lines_to_keep:
            f.write(line.strip() + "\n")

if __name__ == "__main__":
    if not os.path.exists(ISSUE_QUEUE_FILE):
        print("📂 issue_queue.txt 파일이 없습니다.")
        exit()

    with open(ISSUE_QUEUE_FILE, encoding="utf-8") as f:
        lines = f.readlines()

    lines_to_keep = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = re.match(r"(\d+)_", line)
        if not match:
            print(f"❌ 잘못된 파일명 형식: {line}")
            continue

        problem_id = match.group(1)
        problem_title = line

        success = create_issue(problem_id, problem_title)
        if not success:
            lines_to_keep.append(line)

    update_queue_file(lines_to_keep)