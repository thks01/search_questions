from tkinter import *
import os
import cv2
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
import shutil

win = Tk()
win.title("Searcher")
win.geometry("1200x700")
win.option_add("*Font", "맑은고딕 15")

# 기출 문항 입력창

# Label
lab1 = Label(win, bg="aqua")
lab1.config(text="기출 문항")
lab1.place(relx=0.1, rely=0.1)

# 연도
lab2 = Label(win)
lab2.config(text="연도")
lab2.place(relx=0.4, rely=0.01)

ent2 = Entry(win, width=15)
ent2.place(relx=0.35, rely=0.1)

# 월
lab3 = Label(win)
lab3.config(text="월")
lab3.place(relx=0.6, rely=0.01)

ent3 = Entry(win, width=15)
ent3.place(relx=0.55, rely=0.1)

# 문제 번호
lab4 = Label(win)
lab4.config(text="번")
lab4.place(relx=0.8, rely=0.01)

ent4 = Entry(win, width=15)
ent4.place(relx=0.75, rely=0.1)


# 유효 무효 함수 - 문제
def exist():
    global whether_valid
    lab5 = Label(win)
    try:
        if f"{ent2.get()}_{ent3.get()}_{ent4.get()}.jpg" in os.listdir(f"문제/{ent2.get()}년/{ent2.get()}년 {ent3.get()}월"):
            whether_valid = "유효"
        else:
            whether_valid = "무효"
    except FileNotFoundError:
        whether_valid = "무효"
    finally:
        lab5.config(text=whether_valid)
        lab5.place(relx=0.3, rely=0.5)

frm = LabelFrame(win)
frm.place(relx=0.7, rely=0.6)

# 풀이 개수 함수
def number():
    if whether_valid=='유효':
        for wg in frm.grid_slaves():
            wg.destroy()

    lab6 = Label(win)
    sol_list = os.listdir(f"풀이")  # 모든 풀이 이미지 파일을 리스트로 생성
    try:
        if f"{ent2.get()}_{ent3.get()}_{ent4.get()}_sol.jpg" in sol_list:  # 1번 풀이가 있다면 1번 세기
            count = 1
            for i in range(2, 6):  # 풀이가 여러개 있다면 개수 세기
                if f"{ent2.get()}_{ent3.get()}_{ent4.get()}_sol ({i}).jpg" in sol_list:
                    count += 1
                else:
                    break
        else:
            count = 0
    except FileNotFoundError:
        count = 0

    lab6.config(text=str(count) + '개')  # (!) 단위 '개' 추가하였음.
    lab6.place(relx=0.72, rely=0.5)

    # 풀이 1, 2, 3... 버튼 생성
    if count>0:
        btn_sol_1=Button(frm)
        btn_sol_1.config(text=f"풀이 1")
        btn_sol_1.config(command=lambda: search(2, 1))
        btn_sol_1.grid(column=0, row=0)
        count-=1
        if count>0:
            btn_sol_2 = Button(frm)
            btn_sol_2.config(text=f"풀이 2")
            btn_sol_2.config(command=lambda: search(2, 2))
            btn_sol_2.grid(column=0, row=1)
            count -= 1
            if count > 0:
                btn_sol_3 = Button(frm)
                btn_sol_3.config(text=f"풀이 3")
                btn_sol_3.config(command=lambda: search(2, 3))
                btn_sol_3.grid(column=0, row=2)
                count -= 1
                if count > 0:
                    btn_sol_4 = Button(frm)
                    btn_sol_4.config(text=f"풀이 4")
                    btn_sol_4.config(command=lambda: search(2, 4))
                    btn_sol_4.grid(column=0, row=3)
                    count -= 1
                    if count > 0:
                        btn_sol_5 = Button(frm)
                        btn_sol_5.config(text=f"풀이 5")
                        btn_sol_5.config(command=lambda: search(2, 5))
                        btn_sol_5.grid(column=0, row=4)
                        count -= 1


# '문제' 버튼
btn1 = Button(win)
btn1.config(text="문제")
btn1.config(command=exist)
btn1.place(relx=0.3, rely=0.4)

# '풀이' 버튼
btn2 = Button(win)
btn2.config(text="풀이")
btn2.config(command=number)
btn2.place(relx=0.7, rely=0.4)


# 보기 함수 정의
def search(i, j=1):
    year_list = [str(year) for year in range(2012, 2022)]
    month_list = ['3', '4', '6', '7', '9', '10', '11']
    problem_list = [str(number) for number in range(1, 21)]

    year = str(ent2.get())
    month = str(ent3.get())
    problem = str(ent4.get())

    to_proceed = True
    # tkinter.messagebox.showwarning(title=None, message=None, **options)¶
    # tkinter.messagebox.showerror(title=None, message=None, **options)
    if year not in year_list:
        messagebox.showwarning("Unavailable year", "The year entered is not vaild now")
        to_proceed = False
    if month not in month_list:
        messagebox.showwarning("Unavailable month", "The month entered is not vaild now")
        to_proceed = False
    if problem not in problem_list:
        messagebox.showwarning("Unavailable problem number", "The problem number entered is not vaild now")
        to_proceed = False

    #     assert year in year_list, "Unavailable year"
    #     assert month in month_list, "Unavailable month"
    #     assert problem in problem_list, "Unavailable problem number"
    if to_proceed:
        if i == 1:  # '문제'의 '보기' 버튼을 눌렀을 때 구현
            path = f'문제/{year}년/{year}년 {month}월'
            img_name = f'{year}_{month}_{problem}.jpg'
        else:  # '풀이'의 '풀이 1, 2, 3....' 버튼을 눌렀을 때 구현
            path = '풀이'
            if j == 1:  # 풀이가 1개일 때
                img_name = f'{year}_{month}_{problem}_sol.jpg'
            else:  # 풀이가 2개 이상일 때
                img_name = f'{year}_{month}_{problem}_sol ({j}).jpg'
        full_path = path + '/' + img_name

        img_array = np.fromfile(full_path, np.uint8)  # 파일의 데이터로 배열을 구성
        problem_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # 1차원 배열인 img_array를 3차원 배열로 만들어줌.
        problem_img = cv2.resize(problem_img, dsize=(520,640))

        cv2.imshow(f'{year}_{month}_{problem}', problem_img)
        cv2.waitKey()
        cv2.destroyAllWindows()


# 문제 '보기' 버튼
btn3 = Button(win)
btn3.config(text="보기")
btn3.config(command=lambda: search(1))
btn3.place(relx=0.3, rely=0.6)


# '풀이 추가' 함수 구현
def add_solution():
    year = str(ent2.get())
    month = str(ent3.get())
    problem = str(ent4.get())

    path_filename = filedialog.askopenfilename(initialdir="/", title="Select the solution file")

    filename = path_filename.split('/')[-1]  # (기존)파일이름.(기존)확장자
    extension = path_filename.split('.')[-1]  # (기존)확장자
    path = '/'.join(path_filename.split('/')[:-1]) + '/'  # (기존)경로/
    nowpath = os.getcwd()  # (현재)경로
    newpath = nowpath + '/풀이/'  # 새로 지정할 경로 -> (현재)경로+/풀이/
    newname = f"{year}_{month}_{problem}_sol." + extension  # 새로 지정할 이름+확장자(확장자유지)
    if newname in os.listdir("풀이"):
        newname = f"{year}_{month}_{problem}_sol (2)." + extension
        if newname in os.listdir("풀이"):
            newname = f"{year}_{month}_{problem}_sol (3)." + extension
            if newname in os.listdir("풀이"):
                newname = f"{year}_{month}_{problem}_sol (4)." + extension
                if newname in os.listdir("풀이"):
                    newname = f"{year}_{month}_{problem}_sol (5)." + extension
    shutil.move(path + filename, newpath + newname)
    lab_add_solution = Label(win)
    messagebox.showinfo("Success notification",
                        f'''The file has been successfully moved. \n(The file name is "{newname}")''')


# '풀이 추가' 버튼

btn_add_solution = Button(win)
btn_add_solution.config(text="풀이추가")
btn_add_solution.config(command=add_solution)
btn_add_solution.place(relx=0.9, rely=0.85)

win.mainloop()