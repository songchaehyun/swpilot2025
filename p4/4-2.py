import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 다운로드 받은 CSV 파일을 DataFrame 객체로 읽어들인다.
df = pd.read_csv("kosis.csv", header=[0, 1, 2, 3]) # multicolumn - tuple 형태로 정리된다.

# "일반가구원" 만 포함된 열만 필터링
columns_filtered = [col for col in df.columns if col[2] == '일반가구원']
columns_filtered.insert(0, ('시점', '시점', '시점', '시점'))  # 시점도 포함해야 함
df_filtered = df[columns_filtered]

print(df_filtered.head())

# 2015년 이후로 자료가 제공되는 최대 기간의 남자 및 여자의 연도별 일반가구원 데이터 통계롤 최종적으로 출력한다.
cols = [col for col in df_filtered.columns if col[1] == '합계' and (col[3] == '남자' or col[3] == '여자') ]
cols.insert(0, ('시점', '시점', '시점', '시점'))
print(df_filtered[cols].head())

# 2015년 이후로 자료가 제공되는 최대 기간의 연령별 일반가구원 데이터 통계롤 최종적으로 출력한다.
cols = [col for col in df_filtered.columns if col[1] != '합계' and col[3] == '계']
cols.insert(0, ('시점', '시점', '시점', '시점'))
print(df_filtered[cols].head())


# 2015년 이후로 자료가 제공되는 최대 기간의 남자 및 여자의 연령별 일반가구원 데이터 통계를 꺽은선 그래프로 표현한다.
# cols = [col for col in df_filtered.columns if col[1] != '합계' and (col[3] == '남자' or col[3] == '여자') ]
# cols.insert(0, ('시점', '시점', '시점', '시점'))
# print(df_filtered[cols].head())

cols_m = [col for col in df_filtered.columns if col[1] != '합계' and col[3] == '남자']
cols_m.insert(0, ('시점', '시점', '시점', '시점'))
data_m = df_filtered[cols_m].copy()
# 컬럼 이름을 두 번째 항목 (tuple[1])으로 변경
data_m.columns = [col[1] if isinstance(col, tuple) else col for col in data_m.columns]
print(data_m.head())

cols_f = [col for col in df_filtered.columns if col[1] != '합계' and col[3] == '여자']
cols_f.insert(0, ('시점', '시점', '시점', '시점'))
data_f = df_filtered[cols_f].copy()
# 컬럼 이름을 두 번째 항목 (tuple[1])으로 변경
data_f.columns = [col[1] if isinstance(col, tuple) else col for col in data_f.columns]


# 폰트가 깨지는 이슈 발생
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지


plt.figure(figsize=(12, 10))  # 전체 그래프 크기


plt.subplot(2, 1, 1)  # 2행 1열 중 1번째
for col in data_m.columns:
    if col != '시점':
        plt.plot(data_m['시점'], data_m[col], label=col)
plt.title('남자 일반가구원')
plt.ylabel('인구 수')
plt.grid(True)
plt.legend(loc='upper right')
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format(int(x), ',')))


plt.subplot(2, 1, 2)  # 2행 1열 중 2번째
for col in data_f.columns:
    if col != '시점':
        plt.plot(data_f['시점'], data_f[col], label=col, linestyle='--')
plt.title('여자 일반가구원')
plt.xlabel('연도')
plt.ylabel('인구 수')
plt.grid(True)
plt.legend(loc='upper right')
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: format(int(x), ',')))

# 레이아웃 정리
plt.tight_layout()
plt.show()