import cv2, pafy
import imutils
import numpy as np
import tkinter as tk # Tkinter
from PIL import ImageTk, Image # Pillow


class Tk_Video:
    def __init__(self):

        # GUI 설계
        ###GUI 프로그램 이름 및 크기 정하기
        ###프로그램 이름 = win

        ###프로그램 디자인 관련 코드
        ###프로그램 제목


        self.win = tk.Tk() # 인스턴스 생성
        self.win.title("Object Scan in Video Program") # 제목 표시줄 추가
        self.win.geometry("1200x600+200+100") # 지오메트리: 너비x높이+x좌표+y좌표
        self.win.resizable(True, True) # x축, y축 크기 조정 비활성화
        self.win.option_add("*Font", "맑은고딕 15")
        self.win.configure(bg="black")
        # 프레임 추가
        frm = tk.Frame(self.win, bg="black", width=725, height=480) # 프레임 너비, 높이 설정
        frm.place(relx=0.2,rely=0.1)  # 격자 행, 열 배치
        # 라벨1 추가
        title_label = tk.Label(self.win,text="위대한 수령 동지를 위한 대포동 미사일 인식 프로그램", font="궁서 25")
        title_label.place(relx=0.05, rely=0.025)
        self.lbl1 = tk.Label(frm, height=480, width=720)
        self.lbl1.place(relx=0, rely=0)
        ###동영상 파일 불러오기 캔버스
        # canvas = tk.Canvas(self.win, height=500, width=500)
        # canvas.place(relx=0.2, rely=0.1)
        self.lbl2 = tk.Label(self.win, text="start")
        self.lbl2.place(relx=0.82,rely=0.3)
        self.lbl3 = tk.Label(self.win, text="percent")
        self.lbl3.place(relx=0.82, rely=0.45)
        self.weapon = tk.Label(self.win, text = '대응 무기체계')
        self.weapon.place(relx=0.82, rely=0.6)
        ###추정 물체 설명
        object_name = tk.Label(self.win, text='추정 물체')
        object_name.place(relx=0.82, rely=0.25)

        ###정확도 표시
        accuracy = tk.Label(self.win, text='추정 정확도')
        accuracy.place(relx=0.82, rely=0.4)

        ###대응 무기 체계
        weapon_sys = tk.Label(self.win, text='대응 무기체계')
        weapon_sys.place(relx=0.82, rely=0.55)


        ###객체 인식 프로그램 실행 함수
        # def start_recog():

        ###객체 인식 프로그램 종료 함수
        # def stop_recog():

        ###동영상 불러오기 버튼
        video_add_btn = tk.Button(self.win, text='동영상 불러오기', command=self.video_open)
        video_add_btn.place(relx=0.05, rely=0.1)

        ###동영상 재생 및 인식 시작 버튼
        end_program_btn = tk.Button(self.win, text='객체 인식 시작', command=self.end_program)
        end_program_btn.place(relx=0.05, rely=0.175)

        ###동영상 정지 및 인식 종료 버튼
        end_program_btn = tk.Button(self.win, text='객체 인식 종료', command=self.end_program)
        end_program_btn.place(relx=0.05, rely=0.25)

        ###프로그램 종료 버튼
        end_program_btn = tk.Button(self.win, text='프로그램 종료', command=self.end_program)
        end_program_btn.place(relx=0.05, rely=0.325)

        self.win.mainloop()

    def video_open(self):        ###동영상 파일 불러오기 함수

        url1 = 'https://www.youtube.com/watch?v=WrfLHAX82g4'  # 공지합동훈련
        url2 = 'https://www.youtube.com/watch?v=cL-D2P0UMfU'  # 해군 관함식
        url3 = 'https://www.youtube.com/watch?v=xVA8bqOIIfg' # shorts
        url4 = 'https://www.youtube.com/watch?v=tMiXvno2Zw4'

        video = pafy.new(url4)
        best = video.getbest(preftype='mp4')  # 'webm','3gp'
        self.cap = cv2.VideoCapture(best.url)  # 클래스 생성

        self.video_play()
        self.win.mainloop()  # GUI 시작

    def end_program(self):        ###프로그램 종료 함수
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
        str = str
        percent = '(%4.2f%%)' % (confidence * 100)

        air_target = ['military air vehicle','glider','multirole aircraft','projectile','aircraft','missile','decoy, deployment']
        ground_target = ['machine','amphibious vehicle','tank, armored combat vehicle','unicycle, monocycle']
        sea_target = ['maritime structure','pirate, pirate ship','electric ray, torpedo','vessel','naval ship','warship','speedboat','naval vessel']

        if (confidence * 100) > 30:
            if (str in air_target)==True:
                self.weapon.configure(text="air target : AAM")
            elif (str in ground_target)==True:
                self.weapon.configure(text="ground target : ATGM")
            elif (str in sea_target)==True:
                self.weapon.configure(text="sea target : ASM")
            else:
                self.lbl3.configure(text="not target")
            self.lbl2.configure(text = str)
            self.lbl3.configure(text = percent)
        else:
            self.lbl2.configure(text = 'not sure')
            self.lbl3.configure(text="undefined")
            self.weapon.configure(text='no target')

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
