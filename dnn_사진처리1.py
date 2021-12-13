import cv2, pafy
import sys
import numpy as np
# 입력 영상을 불러오는 파일 이름
filename = 'photo/afv.jpg'

# 명령 프롬프트에 임시파일 이름을 입력하여 파일을 불러올 수 있도록 하는 코드
if len(sys.argv) > 1:
    filename = sys.argv[1]

# 입력 영상 불러오기
img = cv2.imread(filename)

if img is None:
    print('Image load failed!')
    sys.exit()

# 네트워크 불러오기
# Caffe 설치된 파일 불러오기
net = cv2.dnn.readNet('bvlc_googlenet.caffemodel', 'deploy.prototxt')

if net.empty():
    print('Network load failed!')
    sys.exit()

# 클래스 이름 불러오기
# 이전에 다운 받아온 클래스 이름 불러오기
# classNames에 1000개의 클래스 이름 등록
classNames = None
with open('classification_classes_ILSVRC2012.txt', 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# 추론
# (1) : 0~255 픽셀값 그대로 이용, (224,224): 입력 영상 크기, (104,117,123): 평균 영상 크기
blob = cv2.dnn.blobFromImage(img, 1, (224, 224), (104, 117, 123))
net.setInput(blob)
prob = net.forward()  # 확률에 대한 ndaaray 리턴
(height, width) = img.shape[:2]
print(prob)
box = blob[0, 0, 0, 3:7] * np.array([width, height, width, height])
(startX, startY, endX, endY) = box.astype("int")
print(blob[0,0,0,2], startX, startY, endX, endY)
cv2.rectangle(img, (startX, startY), (endX, endY),(0, 255, 0), 2)

# 추론 결과 확인 & 화면 출력
out = prob.flatten()
classId = np.argmax(out)  # 가장 큰 값 저장
confidence = out[classId]  # 확률 값

# 확률 값을 보여주기 위해 text값을 제너레이션
text = f'{classNames[classId]} ({confidence * 100:4.2f}%)'
cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()