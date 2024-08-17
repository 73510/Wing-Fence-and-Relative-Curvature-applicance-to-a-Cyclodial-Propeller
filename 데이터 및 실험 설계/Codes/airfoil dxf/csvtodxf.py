# 'read' 모드로 파일을 열어 점 데이터를 읽어옴
dots = []
with open('naca0012.csv', 'r') as file:
    for line in file:
        stripln = line.strip()  # strip() 함수는 줄 끝의 공백이나 개행 문자를 제거함
        lst = list(map(float, stripln.split(',')))  # 각 줄의 데이터를 쉼표로 분리하여 float 리스트로 변환
        dots.append(lst)  # 변환된 리스트를 dots 리스트에 추가

import ezdxf
import math
import matplotlib.pyplot as plt

from ezdxf import recover
from ezdxf.addons.drawing import matplotlib
import numpy as np

# DXF 파일을 열고 이미지를 저장하는 함수
def display_dxf(filename):
    # 예외 처리는 코드의 간결성을 위해 생략되었습니다.
    doc, auditor = recover.readfile(str(filename) + '.dxf')
    if not auditor.has_errors:
        matplotlib.qsave(doc.modelspace(), str(filename) + '.png')

# 새로운 DXF 파일 생성
doc = ezdxf.new()

# 모델 공간을 가져옴 (모든 도형 요소가 저장되는 곳)
msp = doc.modelspace()

# dots 리스트에 있는 점들을 연결하여 선을 그림
for i in range(len(dots) + 1):
    msp.add_line(dots[i - 1], dots[i % len(dots)], dxfattribs={'color': 3})  # 선의 색상은 초록색

# DXF 문서를 파일로 저장
doc.saveas('output_1.dxf')

# 저장된 DXF 파일을 이미지로 변환하여 표시
display_dxf('output_1')
