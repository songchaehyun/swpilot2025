# 2025-05-21
# 1-4. 완전한 반구 형태의 돔 전체 면적 구하기! >> 두께 및 안쪽 면적까지 포함하도록 코드를 작성
import math
from enum import Enum

class Weight(Enum) : # 고유 값 저장하기 위해 enum 사용. g/cm3
    GLASS = 2.4
    ALUMINIUM = 2.7
    CARBON_STEEL = 7.85

def sphere_area():
    # 전역변수를 가지고 계산할 예정
    global area
    global weight

    # 외부 곡면 + 내부 곡면 + 바닥 단면(링 형태)
    rad_out = diameter / 2
    rad_in = rad_out - thickness

    a_out = 2 * rad_out ** 2 # * pi
    a_in = 2 * rad_in ** 2 # * pi
    a_bottom = rad_out ** 2 - rad_in ** 2 # * pi
    
    # 무게를 구하려면 부피를 구해야 함
    volume = 2 / 3 * (rad_out ** 3 - rad_in ** 3) * math.pi

    # Weight enum 기준은 g/cm3 > kg/m3으로 바꾸어 줘야 함 - *1000
    # 무게에 화성의 중력 반영할 것
    g_mars = 3.721 # m/s^2
    mass = volume * (material.value * 1000)

    # 전역변수에 저장
    area = math.pi * (a_out + a_in + a_bottom)
    weight = mass * g_mars # kg * m/s^2 = N

def print_global() :
    # 전역변수를 읽어내기만 할 거니까 global 호출은 필요 X
    # 전역변수를 소수점 아래 세 자리까지 출력
    print(f"재질 ⇒ {material.value}, 지름 ⇒ {diameter:.3f}, 두께 ⇒ {thickness}, 면적 ⇒ {area:.3f}, 무게⇒ {weight:.3f} kg")

def verify_input(x, name) :
    # 보너스 과제: 전역변수에 숫자가 아닌 문자가 들어왔을 때 어떻게 처리할 것인가?
    try:
        x = float(x)

        if x == 0:
            print(f"error: {name} must not be 0")
            return -1
        else :
            return float(x)
    except ValueError:
        print(f"error: input of {name} must be digit")
        return -1

diameter, material, thickness, area, weight = 0, Weight.GLASS, 1, 0, 0

while(1) :

    # 재질, 지름, 두께를 사용자로부터 입력받기
    print("choose mode. i : input, e : exit")
    op = input(">> ")

    if op == "i" :
        print("""
            input diameter(m), material(glass/aluminium/carbon_steel) and thickness(m)
            default: material = glass, thickness = 1(m)""")

        diameter = input(">> diameter: ")
        diameter = verify_input(diameter, "diameter")
        if diameter == -1 :
            continue

        # 기본값 세팅한 두 변수가 비어 있어도 제대로 작동하는지 확인하자
        
        try:
            material = (lambda value: getattr(Weight, value.upper()) if value else Weight.GLASS)(input(">> material: "))
        except AttributeError:
            print("error: wrong material")
            continue

        thickness = input(">> thickness: ")
        if thickness == "": #default setting
            thickness = 1
        else :
            thickness = verify_input(thickness, "thickness")
            if thickness == -1:
                continue
        

        # 계산
        sphere_area()

        # 출력
        print_global()
    
    elif op == "e":
        break 

# 내용을 출력 - 전역변수를 이용해 저장되어 있는 마지막 내용