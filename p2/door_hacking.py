# 2025-05-24
# 2-1. zip 파일 속의 암호를 해독

import os, string, time, datetime
import zipfile
import itertools
from multiprocessing import Pool, cpu_count, Value, Lock
# 문제가 요구하는 스펙이 소규모이고 기본 라이브러리만 사용하므로!

zip_file = "key.zip"
CHARS = string.ascii_lowercase + string.digits #암호에 사용되는 문자들
PWD_LENGTH = 3 #디버깅용으로 설정

#멀티프로세스가 공유하는 메모리
counter = Value('i', 0)
found_flag = Value('b', False)

def try_pwd(password):
    if found_flag.value :
        return None

    with counter.get_lock() :
        counter.value += 1

    try:
        with zipfile.ZipFile(zip_file) as zf :
            with zf.open("password.txt", pwd=bytes(password, "utf-8")) as f:
                f.read(1)# 실제로 읽기를 시도해야 비번 오류가 발생함
            
        with open("password.txt", "w") as f:
            f.write(password)

        with found_flag.get_lock():
                found_flag.value = True
            
        print(f'[SUCCESS] Password found: {password}')
            # os._exit(0) # 멀티 프로세스 종료 - 프로세스가 전부 종료되지 아니함
        return password
    
    except RuntimeError:
        return None #오답
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return None
    
def generate_pwds():
    for pwd_tuple in itertools.product(CHARS, repeat=PWD_LENGTH) : #가능한 모든 경우의 수 중에서 하나를 꺼내와
        yield ''.join(pwd_tuple) #튜플을 하나로 합쳐 문자열 생성
        # yield를 사용하면 제너레이터 함수가 생성되어, 값을 하나 반환하고 다시 호출되면 그 지점부터 다시 시작

# zip 파일 열어서 암호 푸는 함수
def unlock_zip(zip_file):
    start = datetime.datetime.now()
    # 멀티 프로세싱
    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap_unordered(try_pwd, generate_pwds(), chunksize=100):
            if result:  # 비밀번호 성공 시
                pool.terminate()  # 나머지 프로세스 종료
                break
        pool.join()
        #생성된 비밀번호가 iterable하게 돌아가면서 하나씩 try_pwd에 들어가도록 map이 나눠 줌
    end = datetime.datetime.now()
    # 암호 푸는 시작 시간, 반복 횟수, 진행 시간 출력
    print(f"""시작 시간: {start} | 반복 횟수: {counter.value} | 진행 시간: {end - start} 
""")

    # 암호 푸는 데 성공하면 password.txt로 저장

if __name__ == '__main__':
    print(f"open {zip_file}")
    unlock_zip(zip_file)

#문제가 반복하여 발생. 왜???