# -*- coding:GBK -*-         # �ļ�����
import datetime
import json
import tkinter
import os.path
from random import randint


def read_class(_week):
    for widget in box.winfo_children():
        widget.destroy()
    draw_week()
    for c in js:
        name = c
        for i in js[c]['subject']:
            _week = i["week"]
            # �жϿγ��Ƿ��ǵ�˫�ܵĿγ�
            if "��" in _week:
                _week = _week.replace("��(��)", "")
                _week = _week.split("-")
                # ��ʼ��/������
                start_week, end_week = eval(_week[0]), eval(_week[-1])
                if weeks % 2 == 1:  # �ж��Ƿ��ǵ���
                    if start_week <= weeks <= end_week:  # �жϸÿγ��Ƿ��ǵ�ǰ�ܵĿγ�
                        if start_week <= weeks <= end_week:  # �жϸÿγ��Ƿ��ǵ�ǰ�ܵĿγ�
                            # ���ݽ����Ż���ʾЧ��
                            draw_box(name, i)

            elif "˫" in _week:
                _week = _week.replace("��(˫)", "")
                _week = _week.split("-")
                # ��ʼ��/������
                start_week, end_week = eval(_week[0]), eval(_week[-1])
                if weeks % 2 == 0:  # �ж��Ƿ���˫��
                    if start_week <= weeks <= end_week:  # �жϸÿγ��Ƿ��ǵ�ǰ�ܵĿγ�
                        if start_week <= weeks <= end_week:  # �жϸÿγ��Ƿ��ǵ�ǰ�ܵĿγ�
                            draw_box(name, i)

            else:
                _week = _week.replace("��", "")
                _week = _week.split("-")
                # ��ʼ��/������
                start_week, end_week = eval(_week[0]), eval(_week[-1])
                if start_week <= weeks <= end_week:  # �жϸÿγ��Ƿ��ǵ�ǰ�ܵĿγ�
                    # ���ݽ����Ż���ʾЧ��
                    print(i)
                    print(c)
                    draw_box(name, i)


def draw_box(courses, course):
    print(courses)
    scr = "{}\n��ʦ {}\n�� {}\n�ص� {}".format(
        courses, course["teacher"], course["week"], course["address"])  # Ҫ��ʾ�Ŀγ���Ϣ
    part = course["part"]
    part = part.split("-")
    start_part, end_part = eval(part[0]), eval(part[-1])

    # ȷ���ı���λ��
    x = weekday.index(course["weekday"])
    # ����һ���ı��ؼ�
    text = tkinter.Label(box, text=scr, width=20, fg="#FFFFFF", bg=js[courses]['color'],
                         height=2 * (end_part - start_part + 1))
    text.place(x=x * 150 + 40, y=start_part * 40 + 20)  # ����Ļ�Ϸ����ı��ؼ�


def draw_week():
    global weekday, now_week
    i = 0
    for we in weekday:
        if weekday.index(we) == (now_week - 1):
            label = tkinter.Label(box, text=we, background="#CCCCFF", height=2, width=20)
        else:
            label = tkinter.Label(box, text=we, background="#F8F8FF", height=2, width=20)
        label.place(x=150 * i + 40, y=10)
        i += 1
    dic = init["time"]
    for i in dic:
        label = tkinter.Label(box, text=dic[i], background="#F8F8FF")
        label.place(x=0, y=20 + 40 * int(i))


def next_week():
    global weeks
    weeks += 1
    read_class(weeks)
    week.set(weeks)


def last_week():
    global weeks
    if weeks > 1:
        weeks -= 1
        read_class(weeks)
        week.set(weeks)


# �ı�
def data_change():
    change_win = tkinter.Tk()  # ����һ������
    change_win.geometry("500x265+200+50")  # �ı䴰��Ĵ�С
    change_win.title('��������')
    change_win.resizable(0, 0)

    data_change.origin = tkinter.Text(change_win, height=20, width=30)
    data_change.origin.pack(side=tkinter.LEFT)

    frame_button = tkinter.Frame(change_win, height=300, width=100)
    frame_button.pack(side=tkinter.LEFT)

    data_change.translate = tkinter.Text(change_win, height=20, width=30)
    data_change.translate.pack(side=tkinter.LEFT)

    button_translate = tkinter.Button(frame_button, text="ת��������", command=write)
    button_translate.pack(side=tkinter.TOP)

    change_win.mainloop()


# ����γ�
def command():
    def get_info():
        data = js[list.get(tkinter.ACTIVE)]

        subjects = data["subject"]
        data_information.delete(0.0, tkinter.END)
        data_information.insert(0.0, "{} {}\n".format(list.get(tkinter.ACTIVE), data["color"]))
        for subject in subjects:
            if len(subject["teacher"]) > 7:
                teacher = subject["teacher"][0:7] + "��"
            else:
                teacher = subject["teacher"]

            scr = "{} {} {} {} {}\n". \
                format(teacher, subject["week"], subject["weekday"], subject["address"], subject["part"])
            data_information.insert(tkinter.INSERT, scr)

    def new():
        data_information.delete(0.0, tkinter.END)
        data_information.insert(0.0, "�γ��� #999999\n��ʦ 1-20��(��) ����һ �ص� 1-12")

    def save():
        scr = data_information.get(0.0, tkinter.END)
        scr = scr.split("\n")
        name = scr[0]
        subject = []
        for i in scr[1:-1]:
            if i == "":
                pass
            else:
                i = i.split(" ")
                subject.append({"teacher": i[0], "week": i[1], "weekday": i[2], "address": i[3], "part": i[4]})
        class_key = scr[0].split(" ")
        js[class_key[0]] = {"color": class_key[1], "subject": subject}

        with open("my_class.json", "w") as f:
            json.dump(js, f)

        myself_flesh()

    def delete():
        js.pop(list.get(tkinter.ACTIVE))
        with open("my_class.json", "w") as f:
            json.dump(js, f)
            myself_flesh()

    def myself_flesh():
        list.delete(0, tkinter.END)
        n = 0
        for i in js:
            list.insert(n, i)
            n += 1
        list.pack(side=tkinter.LEFT)


    command_win = tkinter.Tk()  # ����һ������
    command_win.geometry("500x200+200+50")  # �ı䴰��Ĵ�С
    command_win.title('��������')
    command_win.resizable(0, 0)

    list = tkinter.Listbox(command_win)
    n = 0
    for i in js:
        list.insert(n, i)
        n += 1
    list.pack(side=tkinter.LEFT)

    data_frame = tkinter.LabelFrame(command_win, text="��������")
    data_frame.pack(side=tkinter.LEFT)

    button_frame = tkinter.Frame(data_frame)

    button_get = tkinter.Button(button_frame, text="��ȡ", command=get_info)
    button_get.pack(side=tkinter.LEFT)

    button_new = tkinter.Button(button_frame, text="����", command=new)
    button_new.pack(side=tkinter.LEFT)

    button_save = tkinter.Button(button_frame, text="����", command=save)
    button_save.pack(side=tkinter.LEFT)

    button_del = tkinter.Button(button_frame, text="ɾ��", command=delete)
    button_del.pack(side=tkinter.LEFT)

    button_frame.pack()

    data_information = tkinter.Text(data_frame)
    data_information.pack()


# ˢ��
def flesh():
    global js, weeks
    if os.path.isfile("my_class.json"):
        # ����γ�����
        with open("my_class.json", "rb") as f:
            class_js = f.read()
            js = json.loads(class_js)  # ת��Ϊjson
    else:
        with open("my_class.json", "w") as f:
            f.write("{}")
            js = {}
    read_class(weeks)


# ��ת
def jump():
    global weeks

    if entry.get().isnumeric():
        weeks = eval(entry.get())
        read_class(weeks)
        week.set(weeks)
    else:
        week.set(weeks)


# ����ת��
# �γ̱����ݱ���
# �����Ψһ��
#   �γ�����Ϊ����
# ������
#   ��ʦ teacher
#   �� week
#   �Ͽ�ʱ�� part
#   ���� weekday


def write():
    text = json.loads(data_change.origin.get(0.0, tkinter.END))  # ת��Ϊjson
    data = {}
    for course in text["kbList"]:
        class_data = {}
        print(course[key["name"]])
        if course[key["name"]] in data:
            subject = data[course[key["name"]]]["subject"]
            print(course[key["name"]])
        else:
            subject = []
        subject.append({"teacher": course[key["teacher"]], "week": course[key["week"]],
                        "weekday": course[key["weekday"]],
                        "address": course[key["address"]], "part": course[key["part"]]})
        # ���Ч��
        text = "56789AB"
        color = "#"
        for i in range(6):
            index = randint(0, len(text) - 1)
            color = color + text[index]

        class_data["color"] = color
        class_data["subject"] = subject
        data[course[key["name"]]] = class_data

    with open("my_class.json", "w") as f:
        json.dump(data, f)

    data_change.translate.insert(0.0, data)


# ���ⲿ�ļ��������ֵ��
with open("data.json", "r") as f:
    init = json.loads(f.read())

# ȷ�Ͽ�ʼ������ ��/��/��
init_year = init["start"][0]
init_mouth = init["start"][1]
init_day = init["start"][2]
# �����ʼ��һ�첻�����գ��򽫿�ʼ�����ڱ�Ϊ����
if not datetime.datetime(init_year, init_mouth, init_day).strftime("%w") == 0:
    init_day -= eval(datetime.datetime(init_year, init_mouth, init_day).strftime("%w"))

# ��ʼ����ʱ��
init_date = datetime.datetime(init_year, init_mouth, init_day)
# ���ڵ�ʱ��
now_date = datetime.datetime.today()
# ���������
days = (now_date - init_date).days
# �������������һ��Ϊ1
weeks = int(days / 7) + 1
# ����������ڼ�
now_week = eval(now_date.strftime("%w"))

weekday = ["����һ", "���ڶ�", "������", "������", "������", "������", "������"]
y = {}

key = init["book"]

top = tkinter.Tk()  # ����һ������
top.geometry("1100x650+200+50")  # �ı䴰��Ĵ�С
top.title('�γ̱�')
top.resizable(0, 0)

# ���
box = tkinter.LabelFrame(top, text="�γ̱�", background="#F8F8FF", height=600, width=1100)
box.pack()

set = tkinter.LabelFrame(top, text="����", height=100, width=1100)
set.pack()

week = tkinter.Variable()
week.set(weeks)

entry = tkinter.Entry(set, textvariable=week, width=10)
entry.pack(side=tkinter.LEFT)

last = tkinter.Button(set, text="��ת", command=jump)
last.pack(side=tkinter.LEFT)

# �����ܰ�ť
last = tkinter.Button(set, text="��һ��", command=last_week)
next = tkinter.Button(set, text="��һ��", command=next_week)
last.pack(side=tkinter.LEFT)
next.pack(side=tkinter.LEFT)

# ���ݿ��ư�ť
chang_button = tkinter.Button(set, text="��������", command=data_change)
chang_button.pack(side=tkinter.LEFT)

# ���ݿ��ư�ť
command_button = tkinter.Button(set, text="����γ�", command=command)
command_button.pack(side=tkinter.LEFT)

# ˢ��
flesh_button = tkinter.Button(set, text="ˢ��", command=flesh)
flesh_button.pack(side=tkinter.LEFT)

flesh()

top.mainloop()
