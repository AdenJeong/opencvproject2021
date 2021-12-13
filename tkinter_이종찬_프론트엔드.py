import cv2, pafy
import imutils
import numpy as np
import tkinter as tk # Tkinter
from PIL import ImageTk, Image # Pillow

###GUI 프로그램 이름 및 크기 정하기
###프로그램 이름 = scan_UI
scan_UI = tk.Tk()
scan_UI.title("Object Scan in Video Program")
scan_UI.geometry("1200x600+200+100")
scan_UI.resizable(True, True)
scan_UI.option_add("*Font", "맑은고딕 15")
scan_UI.configure(bg="black")

###프로그램 디자인 관련 코드
###프로그램 제목
title_label = tk.Label(text="위대한 수령 동지를 위한 대포동 미사일 인식 프로그램", font="궁서 25")
title_label.place(relx=0.05, rely=0.025)

###동영상 파일 불러오기 캔버스
canvas = tk.Canvas(scan_UI, height=500, width=500)
canvas.place(relx=0.2, rely=0.1)

###동영상 파일 불러오기 함수


###프로그램 종료 함수
def end_program():
    scan_UI.destroy()

###객체 인식 프로그램 실행 함수
#def start_recog():

###객체 인식 프로그램 종료 함수
#def stop_recog():

###동영상 불러오기 버튼
video_add_btn = tk.Button(scan_UI, text='동영상 불러오기', command=open)
video_add_btn.place(relx=0.05, rely=0.1)

###동영상 재생 및 인식 시작 버튼
end_program_btn = tk.Button(scan_UI, text='객체 인식 시작', command=end_program)
end_program_btn.place(relx=0.05, rely=0.175)

###동영상 정지 및 인식 종료 버튼
end_program_btn = tk.Button(scan_UI, text='객체 인식 종료', command=end_program)
end_program_btn.place(relx=0.05, rely=0.25)

###프로그램 종료 버튼
end_program_btn = tk.Button(scan_UI, text='프로그램 종료', command=end_program)
end_program_btn.place(relx=0.05, rely=0.325)

###추정 물체 설명
object_name = tk.Label(scan_UI, text='추정 물체')
object_name.place(relx=0.725, rely=0.25)

###정확도 표시
accuracy = tk.Label(scan_UI, text='추정 정확도')
accuracy.place(relx=0.725, rely=0.4)

###대응 무기 체계
weapon_sys = tk.Label(scan_UI, text='대응 무기체계')
weapon_sys.place(relx=0.725, rely=0.55)

scan_UI.mainloop()