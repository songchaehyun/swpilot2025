import pandas as pd

# pd.set_option('display.max_rows', None)
# 모든 행 확인용

def read_print(file) :
    print(f"----{ file }----")
    df = pd.read_csv(file)

    print(df)
    return df

def filter_area(df):
    fil = df[ df['category'] > 0 ]
    print(fil)

map_data = read_print("3-1-area_map.csv")
# area_map.csv 파일을 읽어들이고 출력해 본다.

struct_data = read_print("3-1-area_struct.csv")
# area_struct.csv 파일을 읽어들이고 출력해 본다. 그리고 주요 시설이 어느 area에 집중적으로 설치 되어 있는지 확인한다.
filter_area(struct_data)

# 시설의 종류는 struct_category.csv 파일에 정의되어 있다. 이 내용을 area_struct.csv의 내용과 함께 출력하는데 시설의 종류를 숫자가 아닌 이름으로 출력한다.
read_print("3-1-area_category.csv")
struct_data = struct_data.replace({'category': 1}, "radder")
struct_data = struct_data.replace({'category': 2}, "weather sensors")
struct_data = struct_data.replace({'category': 3}, "Korea Mars Base")
struct_data = struct_data.replace({'category': 4}, "U.S. Mars Base Camp")
# print(struct_data)

# area_map.csv, area_struct.csv, struct_category.csv 의 내용을 모두 병합한다.
# 겹치는 내용이 있으니 임의로 편집하여 병합함
struct_data['mountain'] = map_data['mountain']
# print(struct_data)

# 확인된 데이터에는 여러지역의 정보가 들어 있지만 미국의 전진 기지는 area 1에 집중되어 있는 것을 알게 되었다. 따라서 전체 지역의 정보는 불필요하기 떄문에 area 1에대한 데이터만 필터링 해서 출력한다.
print("---area 1---")
print(struct_data.loc[struct_data['area'] == 1, : ])


# 전체 코드는 mas_map.py 파일로 저장한다.