import random
import threading
import time
import datetime

class FarmSensor:
    def __init__(self, name):
        self.name = name
        self.temperature = None
        self.illuminance = None
        self.humidity = None

    def SetData(self):
        self.temperature = random.randint(20, 30)        # 온도: 20 ~ 30
        self.illuminance = random.randint(5000, 10000)     # 조도: 5000 ~ 10000
        self.humidity = random.randint(40, 70)             # 습도: 40 ~ 70

    def GetData(self):
        # dictionary 형태로 반환
        return {
            'Temperature': self.temperature,
            'Illuminance': self.illuminance,
            'Humidity': self.humidity
        }

print_lock = threading.Lock()  # 전역 락 객체 생성

def sensor_thread(sensor: FarmSensor):
    while True:
        sensor.SetData()
        data = sensor.GetData()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output = (f"{now} {sensor.name} — temp {data['Temperature']:02d}, "
                  f"light {data['Illuminance']:05d}, humi {data['Humidity']:02d}")
        with print_lock:  # 락을 사용하여 출력이 겹치지 않도록 함
            print(output)
        time.sleep(10)  # 10초 대기

def main():
    # FarmSensor 인스턴스를 Farm-1 부터 Farm-5 까지 생성
    sensors = [FarmSensor(f"Farm-{i}") for i in range(1, 6)]
    threads = []

    # 각 센서에 대해 별도의 스레드 생성 및 시작
    for sensor in sensors:
        t = threading.Thread(target=sensor_thread, args=(sensor,), daemon=True)
        threads.append(t)
        t.start()

    # 메인 스레드는 무한 대기하여 프로그램 종료를 방지
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("프로그램 종료")


if __name__ == "__main__":
    main()
