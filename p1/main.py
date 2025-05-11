from datetime import datetime
import json

def searchDic(lists, query, case_insensitive=True) :
    if case_insensitive:
        query = query.lower()
        result = [d for d in lists if 'message' in d and query in d['message'].lower() ]
    else:
        result = [d for d in lists if 'message' in d and query in d['message'] ]

    return result if result else [{ 'message': "query not found" }, ] #return 값 형태 통일

print("Hello Mars")

try :
    try :
        with open("1-1-mission_computer_main.log", 'r') as f1, open("problem.log", "w") as f2:
            #보너스 과제 : 출력 결과를 시간의 역순으로 정렬해서 출력
            data = f1.read().splitlines() #리스트 안의 객체들을 리스트로. \n이붙지 않게 splitlines()
            print("-"*5 + f1.name +"-"*5)
            print(data[0])

            revData = list(map(lambda x: x.split(','), data[1:])) #문제2

            for item in reversed(data[1:]) : #중복 출력을 방지하기 위해 리스트 슬라이싱 사용.
                print(item.strip())
            print("\n")

            print(revData) #전환된 리스트 객체를 화면에 출력
            revData.sort(key = lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"), reverse=True)
            header = data[0].split(',')
            dataDic = [dict(zip(header, rows)) for rows in revData]

            query = input("search: ") #보너스 과제: 검색 기능
            output = searchDic(dataDic, query)
            print("-"*3 + "result" + "-"*3)
            for dict in output :
                for value in dict.values():
                    print(f"{value}", end=" ")
                print()

            with open("mission_computer_main.json", "w", encoding="utf-8") as f:
                json.dump(dataDic, f, indent=4)
            
            for item in data[-3:] : #보너스 과제 : 문제가 되는 부분만 따로 파일로 저장
                f2.write(item+"\n")
    except FileNotFoundError as e:
        print(f"Error occur: {e}")
    
    # 인코딩을 지정하지 않아 log_analysis.md 파일을 vscode로 열었을 시 UTF-8 규격과 맞지 않아 문제 발생.
    with open("log_analysis.md", "w", encoding="utf-8") as mymd :
        analysis = """# 로켓 발사의 분석

11:30:00경 미션이 성공적으로 complete되었음.
그러나 11:35:00경 산소탱크에 문제가 발생함.
이후 산소 탱크가 폭발하며 핵심 시스템이 다운됨.
"""
        mymd.write(analysis)
        mymd.close()
    
    with open("log_analysis.md", "r", encoding="utf-8") as f:
        txt = f.read()
        print("-"*5 + f.name +"-"*5)
        print(txt)
        print("\n")
        f.close()

except Exception as e:
    print(f"Error occur: {e}")