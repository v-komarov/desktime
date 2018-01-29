#coding: utf-8

from Tkinter import *
import json
import urllib


server = "127.0.0.1:8000/working/jsondata/"




def get_status():

    query_args = {"action": "get-desk-statuses"}
    encoded_args = urllib.urlencode(query_args)

    req = urllib.urlopen("http://%s?%s" % (server,encoded_args))

    return json.loads(req.read())





class mainwin:

    def __init__(self):

        self.root = Tk()

        data = get_status()

        if data["result"] == "ok":
            self.root.title(data["user"])
            self.buttons(data)
        else:
            self.root.title("Error")

        self.root.mainloop()


    def buttons(self,data):

        if data["relax"] == u"no" and data["work"] == u"yes":
            if self.button_start_work.winfo_exists() : self.button_start_work.destroy()
            if self.button_start_relax.winfo_exists() : self.button_start_relax.destroy()
            if self.button_stop_relax.winfo_exists() : self.button_stop_relax.destroy()
            self.button_stop_work = Button(self.root, text=u'Завершить работу').grid(row=1, column=1)
        elif data["relax"] == u"yes" and data["work"] == u"yes":
            self.button_stop_relax = Button(self.root, text=u'Завершить перерыв').grid(row=1, column=1)
        elif data["relax"] == u"no" and data["work"] == u"no":
            if self.button_stop_work.winfo_viewable() : self.button_stop_work.destroy()
            if self.button_stop_relax.winfo_viewable() : self.button_stop_relax.destroy()
            if self.button_start_relax.winfo_viewable() : self.button_start_relax.destroy()
            self.button_start_work = Button(self.root, text = u'Начать работу').grid(row = 1, column = 1, command=self.start_work)
        elif data["relax"] == u"yes" and data["work"] == u"no":
            self.button_start_relax = Button(self.root, text = u'Начать перерыв').grid(row = 1, column = 1)



    ### Нажать кнопку начало работы
    def start_work(self):

        query_args = {"action": "get-desk-statuses"}
        encoded_args = urllib.urlencode(query_args)

        req = urllib.urlopen("http://%s?%s" % (server, encoded_args))


if __name__ == "__main__":

    mainwin()

