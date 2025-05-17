import csv

def bubsort_all(data, column): #data는 2차원 리스트로 가정함
    #지정한 행의 값을 순서대로 정렬(bubble sort). 기본값은 역순으로 정렬. 첫 번째 행은 제외.
    columns = len(data)
    length = len(data[column])

    for i in range(length):
        for j in range(1, length - i - 1):
            if data[column][j] < data[column][j+1] :
                for k in range(columns):
                    data[k][j], data[k][j+1] = data[k][j+1], data[k][j] #python swap.

def print_array(data, index) :
    for n in range(index+1): #끝까지 나오도록! 주의!!
        print(','.join(data[m][n] for m in range(len(data))))
        #for m in range(len(data)):
        #    print(data[m][n], end=",")
        print()

try :
    with open("1-3-Mars_Base_Inventory_List.csv", "r", encoding="utf-8") as f1 :
        data = csv.reader(f1)
        data_row = list(data) #이렇게 하면 row 방식으로 컷팅

        #column 단위로 끊은 array를 여기에 넣음
        data_col = [ [] for _ in range(len(data_row[0]))] #csv 파일의 크기가 한정되어 있으므로 정적 초기화 선택
        
        for d in data_row :#d는 그 자체로 list object
            for i in range(len(d)) :
                data_col[i].append(d[i])

        #인화성이 높은 순서대로 정렬
        bubsort_all(data_col, 4)
        
        #인화성 0.7 이상 내용 출력
        index = 0
        for i in range(1, len(data_col[4])):
            if float(data_col[4][i]) >= 0.7:
                index = i
        print_array(data_col, index)
    
        #인화성 0.7 이상 내용 저장
        with open("Mars_Base_Inventory_danger.csv", "w", encoding="utf-8") as f2:
            csv_f = csv.writer(f2)
            for i in range(index+1):
                row = []
                for j in range(len(data_col)):
                    row.append(data_col[j][i])
                csv_f.writerow(row)
        
        with open("Mars_Base_Inventory_List.bin", "wb") as f3:
            for i in range(len(data_col[0])):
                row = ','.join(data_col[j][i] for j in range(len(data_col)))
                f3.write((row + "\n").encode('utf-8'))
        
        with open("Mars_Base_Inventory_List.bin", "rb") as f4:
            data_byte = f4.read()
            print(data_byte.decode('utf-8'))

except Exception as e:
    print(f"Error occur: {e}")