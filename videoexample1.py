import cv2, pafy, youtube_dl
import sys
import numpy as np

url = 'https://www.youtube.com/watch?v=zCx-wg-qNj8'
video = pafy.new(url)
best = video.getbest(preftype='mp4') # 'webm','3gp'
# 카메라 열기
# 0은 기본 카메라(장치관리자에 저장되어있는 순서대로), 카메라가 두 대면 1~2
cap = cv2.VideoCapture(best.url) # 클래스 생성
print('title = ', video.title)
print('author = ', video.author)
print('video.rating = ', video.rating)
print('video.duration = ', video.duration)
# cap.open(0) # 0번 카메라 열기, videoCapture(0)을 하면 안해도 됌

# 비디오 매 프레임 처리
while True:  # 무한 루프
    ret, frame = cap.read()  # 두 개의 값을 반환하므로 두 변수 지정

    if not ret:  # 새로운 프레임을 못받아 왔을 때 braek
        break

    img = frame

    net = cv2.dnn.readNet('bvlc_googlenet.caffemodel', 'deploy.prototxt')

    if net.empty():
        print('Network load failed!')
        sys.exit()

    classNames = None
    with open('classification_classes_ILSVRC2012.txt', 'rt') as f:
        classNames = f.read().rstrip('\n').split('\n')

    inputBlob = cv2.dnn.blobFromImage(img, 1, (224, 224), (104, 117, 123))
    net.setInput(inputBlob, 'data')
    prob = net.forward()

    out = prob.flatten()
    classId = np.argmax(out)
    confidence = out[classId]

    str = '%s (%4.2f%%)' % (classNames[classId], confidence * 100)
    cv2.putText(img, str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1, cv2.LINE_AA)
    # if (confidence * 100) > 50:
    #     cv2.putText(img, str, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1, cv2.LINE_AA)
    # else:
    #     cv2.putText(img,'not sure', (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9,(0, 0, 255), 1, cv2.LINE_AA)

    cv2.imshow('img', img)

    # 정지화면에서 윤곽선을 추출
    edge = cv2.Canny(frame, 50, 150)

    inversed = ~frame  # 반전

#    cv2.imshow('frame', frame)
#    cv2.imshow('inversed', inversed)
#    cv2.imshow('edge', edge)

    # 10ms 기다리고 다음 프레임으로 전환, Esc누르면 while 강제 종료
    if cv2.waitKey(10) == 27:
        break

cap.release()  # 사용한 자원 해제
cv2.destroyAllWindows()