# ✅ 디렉토리 템플릿 생성 + 자동 분류 스크립트 (solved.ac 연동 - 알고리즘 태그 + 세부 티어)
# 사용법:
# - "백준_임시/" 폴더에 문제 파일이 있어야 함
# - 파일명은 "문제번호_문제이름.py" 형식
# - solved.ac API를 통해 난이도(세부 등급) + 알고리즘 태그 자동 추출

import os
import shutil
import requests
import time



# solved.ac API 사용: 문제번호 → 난이도 + 태그 정보
def get_problem_info(problem_id):
    url = f"https://solved.ac/api/v3/problem/show?problemId={problem_id}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            level = data['level']
            tags = [tag['key'] for tag in data['tags']]
            return level, tags
        else:
            print(f"[오류] solved.ac 응답 실패: {res.status_code}")
            return None, []
    except Exception as e:
        print(f"[예외] solved.ac 요청 실패: {e}")
        return None, []

# 티어 숫자 → 세부 등급 문자열
solvedac_level_detail = {
    1: "브론즈5", 2: "브론즈4", 3: "브론즈3", 4: "브론즈2", 5: "브론즈1",
    6: "실버5", 7: "실버4", 8: "실버3", 9: "실버2", 10: "실버1",
    11: "골드5", 12: "골드4", 13: "골드3", 14: "골드2", 15: "골드1",
    16: "플래5", 17: "플래4", 18: "플래3", 19: "플래2", 20: "플래1",
    21: "다이아5", 22: "다이아4", 23: "다이아3", 24: "다이아2", 25: "다이아1",
    26: "루비5", 27: "루비4", 28: "루비3", 29: "루비2", 30: "루비1"
}

# 주요 알고리즘 태그만 필터링 (디렉토리 이름으로 쓸만한 것들)
tag_map = {
    "implementation": "구현",
    "bruteforcing": "브루트포스",
    "graph_traversal": "bfs",
    "dfs": "dfs",
    "bfs": "bfs",
    "dp": "dp",
    "greedy": "greedy",
    "binary_search": "이분탐색",
    "sorting": "정렬",
    "string": "문자열"
}

# 디렉토리 설정
root = "백준"
temp_dir = "백준_임시"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

for filename in os.listdir(temp_dir):
    if filename.endswith(".py"):
        try:
            problem_num, title = filename[:-3].split("_", 1)

            level_num, tags = get_problem_info(problem_num)
            time.sleep(0.2)  # API 요청 간격 제한
            if level_num is None:
                print(f"[스킵] solved.ac 요청 실패: {filename}")
                continue

            level_name = solvedac_level_detail.get(level_num, "기타")
            level_dir = level_name[:2]  # 예: "실버3" → "실버"

            # 첫 번째 매핑 가능한 알고리즘 태그 추출
            algo_dir = "기타"
            for tag in tags:
                if tag in tag_map:
                    algo_dir = tag_map[tag]
                    break

            target_dir = os.path.join(root, level_dir, algo_dir, level_name)
            ensure_dir(target_dir)

            src_path = os.path.join(temp_dir, filename)
            dst_path = os.path.join(target_dir, filename)

            shutil.move(src_path, dst_path)
            print(f"[이동 완료] {filename} → {target_dir}")

        except ValueError:
            print(f"[스킵] 파일명 형식 오류: {filename}")

print("\n✅ solved.ac 기반 문제 정리 완료 (세부 티어 + 태그)")
