# 백준 2178 - 미로 탐색
# 알고리즘: BFS

from collections import deque

n, m = map(int, input().split())
graph = [list(map(int, input())) for _ in range(n)]
# ...