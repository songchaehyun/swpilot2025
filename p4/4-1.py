import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 다운로드 받은 파일 중에서 train.csv, test.csv 두 개의 파일을 읽는다.
# 두 개의 파일의 내용을 하나로 병합한다.

train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

df = pd.concat([train_data, test_data])
#진짜 그 밑에 바로 붙여 놓은 것
print(df.head(20))
print()

print(df.count())
# 전체 데이터의 수량을 파악한다.
print()

# 사람들이 다른 차원으로 전송되었는지 여부를 나타내는 Transported 항목과 가장 관련성이 높은 항목을 찾는다.
print(df['Transported'].value_counts())
print(df['Transported'].isnull().sum())  # 비어있는 값 확인용

# Transported, Age에서 값이 NaN인 행 제거
df = df[df['Transported'].notna()& df['Age'].notna()]
df['Transported'] = df['Transported'].astype(int) # True → 1, False → 0 변환

# float, int 데이터 열 추출
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
print(df[numeric_cols].corrwith(df['Transported']))

# 나이를 기준으로 10대, 20대, 30대, 40대, 50대, 60대, 70대 별로 Transported 여부를 하나의 그래프에서 출력해 본다.
# bins는 경계, labels는 표시할 이름
bins = [10, 19, 29, 39, 49, 59, 69, 79]
labels = ['10대', '20대', '30대', '40대', '50대', '60대', '70대']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

# 폰트가 깨지는 이슈 발생
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# Transported가 True인 비율을 나이대 별로 계산해서 그래프로 나타냄
sns.barplot(x='AgeGroup', y='Transported', data=df,
            estimator=lambda x: sum(x)/len(x))
            # 전송된 사람 수(true = 1 값의 총합) / 전체 사람 수 = 전송된 비율
plt.title("나이대별 Transported 비율")
plt.ylabel("Transported 비율")
plt.xlabel("나이대")
plt.ylim(0, 1)
plt.show()
