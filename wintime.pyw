#!/usr/bin/python3
#coding: utf-8

from tkinter import *
import json
import requests
from functools import partial

import myconfig
#server = "10.6.0.22:8000/working/jsondata/"

server = myconfig.server




def get_status():

    args = {"action": "get-desk-statuses"}
    req = requests.get("http://%s" % server, params=args)

    return json.loads(req.text)








# Авторизация
class auth():

    def __init__(self):

        self.root = Tk()

        self.root.title("Регистрация")

        name_label = Label(self.root, text=u"Логин:")
        name_label.grid(row=0, column=0, sticky=(N, W))
        name = Entry(self.root)
        name.grid(row=0, column=1)

        passwd_label = Label(self.root, text=u"Пароль:")
        passwd_label.grid(row=1, column=0, sticky=(N, W))
        passwd = Entry(self.root, textvariable=StringVar(), show="*")
        passwd.grid(row=1, column=1)

        phone_label = Label(self.root, text=u"Телефон:")
        phone_label.grid(row=2, column=0, sticky=(N, W))
        phone = Entry(self.root)
        phone.grid(row=2, column=1)

        btn1 = Button(self.root, text=u"Регистрация", command=lambda: self.auth_request(name.get(), passwd.get(), phone.get()))
        btn1.grid(row=3, column=1)

        self.root.mainloop()






    # Запрос авторизации
    def auth_request(self, name, passwd, phone):

        args = {"action": "auth-desk-ip", "desktop_name":name, "desktop_passwd": passwd, "desktop_phone": phone}
        req = requests.get("http://%s" % server, params=args)

        result = json.loads(req.text)
        if result["result"] == "ok":
            self.root.destroy()
            mainwin()






class mainwin():

    def __init__(self):

        self.root = Tk()

        self.root.geometry('-0-0')
        self.root.attributes('-topmost', True)
        data = get_status()

        if data["result"] == "ok":
            self.root.title(data["user"])
            self.lbl1 = Label(self.root, text=u"")
            self.lbl1.grid(row=0,column=1)
            self.btn1 = Button(self.root, text=u"", command=self.empty)
            self.btn1.grid(row=1,column=1)
            self.btn2 = Button(self.root, text=u"", command=self.empty)
            #self.btn2.grid(row=2,column=1)

            self.buttons(data)
            self.create_evt_button(data)

        else:
            self.root.title("Error")

        self.root.mainloop()


    def buttons(self,data):

        if data["relax"] == u"no" and data["work"] == u"yes":
            self.lbl1.config(text=u"Статус: Работа", foreground='red')
            self.btn1.config(text=u'Завершить работу', foreground='blue', command=self.end_work)
            self.btn2.grid(row=2,column=1)
            self.btn2.config(text=u'Начать перерыв', foreground='green', command=self.start_relax)

        elif data["relax"] == u"yes" and data["work"] == u"yes":
            self.lbl1.config(text=u"Статус: Перерыв",  foreground='green')
            self.btn1.config(text=u'Завершить перерыв', foreground='red', command=self.end_relax)
            self.btn2.grid_forget()

        elif data["work"] == u"no":
            self.lbl1.config(text=u"Статус: Нет",  foreground='black')
            self.btn1.config(text = u'Начать работу', foreground='red', command=self.start_work)
            self.btn2.grid_forget()





    def empty(self):
        pass


    ### Нажать кнопку начало работы
    def start_work(self):
        args = {"action": "work-desk-start"}

        req = requests.get("http://%s" % server, params=args)
        if json.loads(req.text)["result"] == u"ok":
            data = get_status()
            self.buttons(data)


    ### Завершение работы
    def end_work(self):
        args = {"action": "work-desk-end"}

        req = requests.get("http://%s" % server, params=args)

        if json.loads(req.text)["result"] == u"ok":
            data = get_status()
            self.buttons(data)



    ### Начать перерыв
    def start_relax(self):
        args = {"action": "relax-desk-start"}

        req = requests.get("http://%s" % server, params=args)
        if json.loads(req.text)["result"] == u"ok":
            data = get_status()
            self.buttons(data)



    ### Закончить перерыв
    def end_relax(self):
        args = {"action": "relax-desk-end"}

        req = requests.get("http://%s" % server, params=args)
        if json.loads(req.text)["result"] == u"ok":
            data = get_status()
            self.buttons(data)




    ### Формирование кнопок отметки событий
    def create_evt_button(self, data):
        row = 3
        self.button_name = {}
        for evt in data["evt_btn"]:
            action_with_arg = partial(self.evt_button, evt["id"])
            n = eval("Button(self.root,text=u'%s', command=action_with_arg)" % evt["name"])
            n.grid(row=row, column=1)
            self.button_name[evt["id"]] = n
            row+=1


    ### Обработка нажатий кнопок отметки событий
    def evt_button(self,evtid):

        args = {"action": "evt-desk",    "evtid": evtid}

        req = requests.get("http://%s" % server, params=args)
        result = json.loads(req.text)
        if result["result"] == u"ok":
            self.button_name[evtid].config(text=u"%s (%s)" % (result["name"],result["count"]))






if __name__ == "__main__":

    auth()

