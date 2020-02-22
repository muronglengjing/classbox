# -*- coding:GBK -*-         # 文件编码
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
            # 判断课程是否是单双周的课程
            if "单" in _week:
                _week = _week.replace("周(单)", "")
                _week = _week.split("-")
                # 开始周/结束周
                start_week, end_week = eval(_week[0]), eval(_week[-1])
                if weeks % 2 == 1:  # 判断是否是单周
                    if start_week <= weeks <= end_week:  # 判断该课程是否是当前周的课程
                        if start_week <= weeks <= end_week:  # 判断该课程是否是当前周的课程
                            # 根据节来优化显示效果
                            draw_box(name, i)

            elif "双" in _week:
                _week = _week.replace("周(双)", "")
                _week = _week.split("-")
                # 开始周/结束周
                start_week, end_week = eval(_week[0]), eval(_week[-1])
                if weeks % 2 == 0:  # 判断是否是双周
                    if start_week <= weeks <= end_week:  # 判断该课程是否是当前周的课程
                        if start_week <= weeks <= end_week:  # 判断该课程是否是当前周的课程
                            draw_box(name, i)

            else:
                _week = _week.replace("周", "")
                _week = _week.split("-")
                # 开始周/结束周
                start_week, end_week = eval(_week[0]), eval(_week[-1])
                if start_week <= weeks <= end_week:  # 判断该课程是否是当前周的课程
                    # 根据节来优化显示效果
                    print(i)
                    print(c)
                    draw_box(name, i)


def draw_box(courses, course):
    print(courses)
    scr = "{}\n讲师 {}\n周 {}\n地点 {}".format(
        courses, course["teacher"], course["week"], course["address"])  # 要显示的课程信息
    part = course["part"]
    part = part.split("-")
    start_part, end_part = eval(part[0]), eval(part[-1])

    # 确认文本的位置
    x = weekday.index(course["weekday"])
    # 创建一个文本控件
    text = tkinter.Label(box, text=scr, width=20, fg="#FFFFFF", bg=js[courses]['color'],
                         height=2 * (end_part - start_part + 1))
    text.place(x=x * 150 + 40, y=start_part * 40 + 20)  # 在屏幕上放置文本控件


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


# 改变
def data_change():
    change_win = tkinter.Tk()  # 创建一个窗体
    change_win.geometry("500x265+200+50")  # 改变窗体的大小
    change_win.title('导入数据')
    change_win.resizable(0, 0)

    data_change.origin = tkinter.Text(change_win, height=20, width=30)
    data_change.origin.pack(side=tkinter.LEFT)

    frame_button = tkinter.Frame(change_win, height=300, width=100)
    frame_button.pack(side=tkinter.LEFT)

    data_change.translate = tkinter.Text(change_win, height=20, width=30)
    data_change.translate.pack(side=tkinter.LEFT)

    button_translate = tkinter.Button(frame_button, text="转换并保存", command=write)
    button_translate.pack(side=tkinter.TOP)

    change_win.mainloop()


# 管理课程
def command():
    def get_info():
        data = js[list.get(tkinter.ACTIVE)]

        subjects = data["subject"]
        data_information.delete(0.0, tkinter.END)
        data_information.insert(0.0, "{} {}\n".format(list.get(tkinter.ACTIVE), data["color"]))
        for subject in subjects:
            if len(subject["teacher"]) > 7:
                teacher = subject["teacher"][0:7] + "等"
            else:
                teacher = subject["teacher"]

            scr = "{} {} {} {} {}\n". \
                format(teacher, subject["week"], subject["weekday"], subject["address"], subject["part"])
            data_information.insert(tkinter.INSERT, scr)

    def new():
        data_information.delete(0.0, tkinter.END)
        data_information.insert(0.0, "课程名 #999999\n教师 1-20周(单) 星期一 地点 1-12")

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


    command_win = tkinter.Tk()  # 创建一个窗体
    command_win.geometry("500x200+200+50")  # 改变窗体的大小
    command_win.title('管理数据')
    command_win.resizable(0, 0)

    list = tkinter.Listbox(command_win)
    n = 0
    for i in js:
        list.insert(n, i)
        n += 1
    list.pack(side=tkinter.LEFT)

    data_frame = tkinter.LabelFrame(command_win, text="数据详情")
    data_frame.pack(side=tkinter.LEFT)

    button_frame = tkinter.Frame(data_frame)

    button_get = tkinter.Button(button_frame, text="获取", command=get_info)
    button_get.pack(side=tkinter.LEFT)

    button_new = tkinter.Button(button_frame, text="新增", command=new)
    button_new.pack(side=tkinter.LEFT)

    button_save = tkinter.Button(button_frame, text="保存", command=save)
    button_save.pack(side=tkinter.LEFT)

    button_del = tkinter.Button(button_frame, text="删除", command=delete)
    button_del.pack(side=tkinter.LEFT)

    button_frame.pack()

    data_information = tkinter.Text(data_frame)
    data_information.pack()


# 刷新
def flesh():
    global js, weeks
    if os.path.isfile("my_class.json"):
        # 保存课程数据
        with open("my_class.json", "rb") as f:
            class_js = f.read()
            js = json.loads(class_js)  # 转化为json
    else:
        with open("my_class.json", "w") as f:
            f.write("{}")
            js = {}
    read_class(weeks)


# 跳转
def jump():
    global weeks

    if entry.get().isnumeric():
        weeks = eval(entry.get())
        read_class(weeks)
        week.set(weeks)
    else:
        week.set(weeks)


# 数据转换
# 课程表数据保存
# 共有项（唯一）
#   课程名作为索引
# 单独项
#   教师 teacher
#   周 week
#   上课时间 part
#   星期 weekday


def write():
    text = json.loads(data_change.origin.get(0.0, tkinter.END))  # 转化为json
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
        # 多彩效果
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


# 用外部文件来保存键值对
with open("data.json", "r") as f:
    init = json.loads(f.read())

# 确认开始的日期 年/月/日
init_year = init["start"][0]
init_mouth = init["start"][1]
init_day = init["start"][2]
# 如果开始的一天不是周日，则将开始的日期变为周日
if not datetime.datetime(init_year, init_mouth, init_day).strftime("%w") == 0:
    init_day -= eval(datetime.datetime(init_year, init_mouth, init_day).strftime("%w"))

# 初始化的时间
init_date = datetime.datetime(init_year, init_mouth, init_day)
# 现在的时间
now_date = datetime.datetime.today()
# 间隔的天数
days = (now_date - init_date).days
# 间隔的周数，第一周为1
weeks = int(days / 7) + 1
# 框出今天星期几
now_week = eval(now_date.strftime("%w"))

weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
y = {}

key = init["book"]

top = tkinter.Tk()  # 创建一个窗体
top.geometry("1100x650+200+50")  # 改变窗体的大小
top.title('课程表')
top.resizable(0, 0)

# 框架
box = tkinter.LabelFrame(top, text="课程表", background="#F8F8FF", height=600, width=1100)
box.pack()

set = tkinter.LabelFrame(top, text="操作", height=100, width=1100)
set.pack()

week = tkinter.Variable()
week.set(weeks)

entry = tkinter.Entry(set, textvariable=week, width=10)
entry.pack(side=tkinter.LEFT)

last = tkinter.Button(set, text="跳转", command=jump)
last.pack(side=tkinter.LEFT)

# 上下周按钮
last = tkinter.Button(set, text="上一周", command=last_week)
next = tkinter.Button(set, text="下一周", command=next_week)
last.pack(side=tkinter.LEFT)
next.pack(side=tkinter.LEFT)

# 数据控制按钮
chang_button = tkinter.Button(set, text="导入数据", command=data_change)
chang_button.pack(side=tkinter.LEFT)

# 数据控制按钮
command_button = tkinter.Button(set, text="管理课程", command=command)
command_button.pack(side=tkinter.LEFT)

# 刷新
flesh_button = tkinter.Button(set, text="刷新", command=flesh)
flesh_button.pack(side=tkinter.LEFT)

flesh()

top.mainloop()
