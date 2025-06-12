# 3-3
import pandas as pd
import collections

def read_area(file) :
    try:
        print(f"----{ file }----")
        df = pd.read_csv(file)

        return df
    except FileNotFoundError:
            print(f"ERROR: '{file}' not found")
            return pd.DataFrame() # 빈 DataFrame 반환
    except Exception as e:
        print(f"ERROR: {e}")
        return pd.DataFrame()
    # mas_map에서 import해도 되지만, 예외처리를 넣어 다시 작성.

# 화성 데이터를 기반으로 화성 기지에서 미국의 화성 전진기지까지 갈 수 있는 최단 경로를 계산한다. 즉 3 -> 4 이동 경로
# 최단 경로를 계산할 때에는 무작위로 추출해서는 안되고 알려져 있는 최단 경로 알고리듬 중 하나를 선택해서 수식을 만들고 수식을 파이썬 코드로 옮겨서 완성한다.

def bfs(df) :
    # 컴퓨터 좌표축의 이해
    #   x→
    # y↓
    rows = int(df['y'].max())
    cols = int(df['x'].max())

    start_point = None
    end_points_set = set() # 여러 도착 지점을 저장할 set
    obstacle_set = set()

    # k_base = df.loc[ df['category'] == 3 , ['x', 'y'] ]
    # us_base = df.loc[ df['category'] == 4 , ['x', 'y'] ]
    # radders = df.loc[ df['category'] == 1 , ['x', 'y'] ]

    # 데이터프레임을 한 번만 순회하여 모든 정보 추출
    for index, row in df.iterrows():
        x, y, category = int(row['x']), int(row['y']), int(row['category'])
        
        # 0-인덱스 좌표로 변환
        current = (y-1, x-1) # (row, col)

        if category == 3: # k_base
            if start_point is None: # 첫 번째 k_base를 시작점으로 설정
                start_point = current
        elif category == 4: # us_base
            end_points_set.add(current) # 모든 도착 지점을 set에 추가
        elif category == 1: # radders
            obstacle_set.add(current)
            # 최단 경로를 구할 때 암석이 가로 막으면 통과 할 수 없다.
         
    print(start_point, "\n", end_points_set, "\n", obstacle_set)

    # BFS 알고리즘 시작
    queue = collections.deque([(start_point[0], start_point[1], 0)]) #deque를 사용하면 시간복잡도 낮추기 가능
    visited = [[False for _ in range(cols)] for _ in range(rows)] #방문여부 2차원리스트 생성하며 초기화해준다
    visited[start_point[0]][start_point[1]] = True
    parent = [[None for _ in range(cols)] for _ in range(rows)] #지나온 경로 2차원리스트

    # 상하좌우 이동 방향 벡터
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        r, c, dist = queue.popleft() #꺼내기

        # 목표 지점 set에 도달했는지?
        if (r, c) in end_points_set:
            path = []
            curr_r, curr_c = r, c
            while (curr_r, curr_c) != start_point:
                path.append((curr_r + 1, curr_c + 1))
                # 1-인덱스 좌표로, !!!!x와 y 바꿔서!! 저장

                prev_r, prev_c = parent[curr_r][curr_c][0], parent[curr_r][curr_c][1]
                curr_r, curr_c = prev_r, prev_c

            path.append((start_point[0] + 1, start_point[1] + 1))
            # 1-인덱스 좌표로, !!!!x와 y 바꿔서!!!!시작 지점 추가

            path.reverse() # 경로를 시작점에서 도착점 순서로 뒤집기

            # csv로 저장하는 함수 호출
            save_path(path)
            return dist

        # 인접한 칸 탐색
        for dr, dc in directions:
            next_r, next_c = r + dr, c + dc

            if (0 <= next_r < rows and 0 <= next_c < cols and #격자 범위 안에 있는지
                not visited[next_r][next_c] and #방문한 적 없는지
                (next_r, next_c) not in obstacle_set): #radder가 있는지

                visited[next_r][next_c] = True
                queue.append((next_r, next_c, dist + 1))
                parent[next_r][next_c] = (r, c) #부모 정보 저장

    # 큐가 비었는데 목표 지점에 도달하지 못했다면 경로 없음
    return -1


# 최단 경로가 구해지면 경로를 CSV 파일로 저장하는데 파일이름은home_to_us_camp.csv 로 저장한다.
def save_path(path) :
    path_df = pd.DataFrame(path, columns=['x', 'y'])
    
    try:
        path_df.to_csv("home_to_us_camp.csv", index=False)
        print("saved file")
    except Exception as e:
        print(f"ERROR: {e}")



if __name__ == "__main__":
    data = read_area("3-1-area_struct.csv")
    if not data.empty :
        print(f"최단 경로: {bfs(data)}")

    else:
        print("data is empty")

    # 위의 코드가 완성되면 mars_map_direct_save.py 파일로 저장한다.