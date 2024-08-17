import numpy as np
dots = []
with open('naca0012.csv', 'r') as file:
    for line in file:
        stripln = line.strip()  # 줄 끝의 공백 또는 개행 문자를 제거
        lst = list(map(float, stripln.split(',')))  # 각 줄의 데이터를 쉼표로 구분하여 float 리스트로 변환
        dots.append(lst)  # 변환된 리스트를 dots 리스트에 추가

# Consider the chord as the line from (0, 0) to (50, 0)
# 코드는 코드선 (0, 0)에서 (50, 0)을 기준으로 동작

# Curve Center is assumed to be at (0, -75)
# 곡선의 중심을 (0, -75)로 설정
# 각도는 theta로 계산

r = 75  # 반지름 설정 (곡선 중심에서 코드선까지의 거리)

cdot = []  # 변환된 점들을 저장할 리스트
for dot in dots:
    x = dot[0]
    y = dot[1]

    theta = x / r  # 각도 theta 계산 (반지름에 따른 x 위치 변환)

    # 새로운 x, y 좌표 계산
    nx = (75 + y) * np.sin(theta)
    ny = (75 + y) * np.cos(theta) - 75

    cdot.append([nx, ny])  # 변환된 점을 리스트에 추가

import ezdxf
import math
import matplotlib.pyplot as plt

from ezdxf import recover
from ezdxf.addons.drawing import matplotlib
import numpy as np

def display_dxf(filename):
    # 예외 처리는 코드의 간결성을 위해 생략됨
    doc, auditor = recover.readfile(str(filename) + '.dxf')
    if not auditor.has_errors:
        matplotlib.qsave(doc.modelspace(), str(filename) + '.png')

doc = ezdxf.new()

# 모델 공간을 가져옴 (모든 도형 요소가 저장되는 곳)
msp = doc.modelspace()

# 변환된 점들을 사용하여 선을 그리기
dots = cdot
for i in range(len(dots) + 1):
    msp.add_line(dots[i - 1], dots[i % len(dots)], dxfattribs={'color': 3})  # 선을 그릴 때 색상은 초록색 사용

# DXF 문서를 파일로 저장
doc.saveas('output_1.dxf')

# 저장된 DXF 파일을 이미지로 변환하여 표시
display_dxf('output_1')
