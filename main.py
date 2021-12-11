import cv2, pafy
import imutils
import sys
import numpy as np
import tkinter as tk # Tkinter
from PIL import ImageTk, Image # Pillow

class Tk_Video:
    def __init__(self):

        # 검출된 항목 저장할 리스트
        self.class_list = []
        # GUI 설계
        self.win = tk.Tk() # 인스턴스 생성

        self.win.title("AniWatch") # 제목 표시줄 추가
        self.win.geometry("1080x720+50+50") # 지오메트리: 너비x높이+x좌표+y좌표
        self.win.resizable(True, True) # x축, y축 크기 조정 비활성화
        # 프레임 추가
        frm = tk.Frame(self.win, bg="white", width=745, height=430) # 프레임 너비, 높이 설정
        frm.place(x=200,y=150)  # 격자 행, 열 배치
        # 라벨1 추가
        self.lbl1 = tk.Label(frm)
        self.lbl1.place(x=10,y=10)
        self.lbl2 = tk.Label(self.win, text="start")
        self.lbl2.place(x=800,y=50)
        self.lbl3 = tk.Label(self.win, text="percent")
        self.lbl3.place(x=800, y=80)

        url1 = 'https://www.youtube.com/watch?v=WrfLHAX82g4'  # 공지합동훈련
        url2 = 'https://www.youtube.com/watch?v=cL-D2P0UMfU'  # 해군 관함식
        url3 = 'https://www.youtube.com/watch?v=xVA8bqOIIfg' # shorts

        video = pafy.new(url1)
        best = video.getbest(preftype='mp4')  # 'webm','3gp'
        self.cap = cv2.VideoCapture(best.url)  # 클래스 생성

        self.win.bind('<Escape>', self.close_sc)
        self.video_play()
        self.win.mainloop()  # GUI 시작


    def close_sc(self,event):
        self.win.destroy()

    def video_play(self):
        ret, frame = self.cap.read()  # 두 개의 값을 반환하므로 두 변수 지정

        if not ret:  # 새로운 프레임을 못받아 왔을 때 braek
            cap.release()  # 작업 완료 후 해제
            return

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

        str = '%s' % (classNames[classId])
        str = str+'\n'
        percent = '(%4.2f%%)' % (confidence * 100)

        f1 = open('air_target.txt', 'r')
        f2 = open('ground_target.txt','r')
        f3 = open('sea_target.txt','r')

        if (confidence * 100) > 60:
            self.class_list.append(classNames[classId])
        if (confidence * 100) > 30:
            if (str in f1.readlines())==True:
                self.lbl3.configure(text="air target\nAAM")
            elif (str in f2.readlines())==True:
                self.lbl3.configure(text="ground target\nATGM")
            elif (str in f3.readlines())==True:
                self.lbl3.configure(text="sea target\nASM")
            else:
                self.lbl3.configure(text="not target")
            self.lbl2.configure(text = str)
            #self.lbl3.configure(text = percent)
        else:
            self.lbl2.configure(text = 'not sure')
            self.lbl3.configure(text="undefined")

        f.close()

        # 5ms 기다리고 다음 프레임으로 전환, Esc누르면 while 강제 종료
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=720, height=480)
        img = Image.fromarray(frame)  # Image 객체로 변환
        imgtk = ImageTk.PhotoImage(image=img)  # ImageTk 객체로 변환
        self.lbl1.imgtk = imgtk
        self.lbl1.configure(image=imgtk)
        self.lbl1.after(4, self.video_play)


if __name__ == "__main__":
    gui = Tk_Video()
