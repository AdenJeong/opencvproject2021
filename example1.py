# -*- coding: utf-8 -*-
import cv2

CAM_ID = 0


def capture(camid=CAM_ID):
    for i in range(10):
        # 윈도우 사용자는 마지막에 cv2.CAP_DSHOW 추가
        cam = cv2.VideoCapture(camid, cv2.CAP_DSHOW)
        # 리눅스 사용자는 아래와 같이 사용
        # cam = cv2.VideoCapture(camid)
        if cam.isOpened() == False:
            print('cant open the cam (%d)' % camid)
            return None

        ret, frame = cam.read()
        if frame is None:
            print('frame is not exist')
            return None

        # png로 압축 없이 영상 저장
        photonum = 'messigray' + str(i) + '.jpg'
        cv2.imwrite(photonum, frame, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
        cam.release()

if __name__ == '__main__':
    capture()