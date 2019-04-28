#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:11:38 2019

@author: erkamozturk
"""

from Tkinter import *
import ttk
from bs4 import BeautifulSoup
import urllib2
import io
from PIL import Image, ImageTk
from urllib2 import urlopen
import tkMessageBox
from PIL import Image


class ProjectAnalyzer(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        self.widgets()
        self.geometricDesign()

    def widgets(self):
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.frame3 = Frame(self.root)
        self.title = Label(self.frame1, text="SEHIR Research Projects Analyzer - CS Edition", font="times 11 bold ",
                           bg="darkblue", fg="white", width=50)
        self.provide = Label(self.frame1, text="Please provide an URL:")
        self.url = Entry(self.frame1, bg="yellow", width=60) # we will insert after the line which one is close now.

        self.fetch = Button(self.frame1, text="Fetch Research Projects", font="Verdana 7", command=self.fetch)
        self.period = Label(self.frame1, text="." * 350)
        self.filter = Label(self.frame2, text="Filter Research Projects By:", font="Verdana 8 bold")
        self.year = Label(self.frame2, text="Year:", fg="navy")
        self.principal = Label(self.frame2, text="Principal Investigator:", fg="navy")
        self.funding = Label(self.frame2, text="Funding Institution:", fg="navy")
        self.display = Button(self.frame2, text="Display Project Titles", font="Verdana 7", command=self.showing)
        self.box1_value = StringVar()  # combobox works with string values
        self.box1 = ttk.Combobox(self.frame2, textvariable=self.box1_value, width=25)
        self.box1.set("All Years")
        self.box2_value = StringVar()  # combobox works with string values
        self.box2 = ttk.Combobox(self.frame2, textvariable=self.box2_value, width=25)
        self.box2.set("All Investigators")
        self.box3_value = StringVar()  # combobox works with string values
        self.box3 = ttk.Combobox(self.frame2, textvariable=self.box3_value, width=25)
        self.box3.set("All Institutions")
        self.scrollbar = Scrollbar(self.frame2)
        self.mylist = Listbox(self.frame2, yscrollcommand=self.scrollbar.set, height=5, width=60)
        self.scrollbar.config(command=self.mylist.yview)
        self.show = Button(self.frame2, text="Show Description", font="Verdana 7", command=self.displayText)
        self.period1 = Label(self.frame2, text="." * 350)
        self.des = Label(self.frame3, text="Project Description:")
        self.bar = Scrollbar(self.frame3)
        self.text = Text(self.frame3, height=10, width=60, yscrollcommand=self.bar.set)
        self.bar.config(command=self.text.yview)

    def fetch(self):
        try:
            url = self.url.get()  # get string from entry
            response = urllib2.urlopen(url)  # type instance; when we print, <addinfourl at 50382568 whose fp = <socket._fileobject object at 0x0300ACB0>>
            html = response.read()  # type str, all page in str
            soup = BeautifulSoup(html, 'html.parser')
            all_data = soup.findAll("li", {"class": "list-group-item"})  # our data holds in class:list-group-item

    #       this are containers for saving data from geting HTML
            self.titles = []
            self.dates = []
            self.instutions = []
            self.name_of_lecturers = []
            self.pics = []
            self.informations = []

    #       two dict one for name to pic's url, one for saving all data in one structure
            self.images = {}
            self.myData = {}
            for prj in all_data:
                title = prj.find("h4").text.strip()  # strip = it cleans the spaces start and end
                if title not in self.titles:  # if not in, append it. If in, not append.
                    self.titles.append(title)

                all_p = prj.find_all("p")
                p1 = all_p[0]
                date = p1.text.strip().split()[2], p1.text.strip().split()[-1] # strip = it cleans the spaces start and end split = it separetes content. and appent it in list.
                if date not in self.dates:  # if not in, append it. If in, not append.
                    self.dates.append(date)

                p2 = all_p[1]
                instution = p2.text.split("\n")[2].strip()  # split and split if needed for all process
                if instution not in self.instutions:    # if not in, append it. If in, not append.
                    self.instutions.append(instution)

                p3 = all_p[2]
                name_of_lecturer = p3.text.strip().split("\n")[-1].strip()  # split and sprit if needed for all process
                # name_of_lecturer = name_of_lecturer.decode('utf-8') for Ali Cakmak not C with dotted
                if name_of_lecturer not in self.name_of_lecturers:  # if not in, appent it. If in, not append.
                    self.name_of_lecturers.append(name_of_lecturer)

                pic = prj.find("img").get("src")
                pic_url = "http://cs.sehir.edu.tr" + pic  # we need to insert main url before our url
                if pic not in self.pics:    # if not in, append it. If in, not append.
                    self.pics.append(pic)
                information = all_p[4].text.strip()  # split and sprit if needed for all process
                if information not in self.informations:    # if not in, appent it. If in, not append.
                    self.informations.append(information)
                self.images[title] = pic_url    # one dict for saves images url. we will use it for calling images when display on canvas
                self.myData[title] = [date, name_of_lecturer, instution, pic_url, information]  # one dict for save all data

            self.dates.sort()   # sorted cus when we insert in combobox, it will insert respectively increasing
            self.instutions.sort()
            self.name_of_lecturers.sort(key=lambda n: n.split()[1])  # this process for sort names by surnames
            self.adding_boxes()

        except:
            tkMessageBox.showerror("Error",
                                   "This area should be filled.\nPlease give valid url.")

    def adding_boxes(self):
        t = []  # container to years.
        for i in range(int(self.dates[0][0]), int(self.dates[-1][1])+1):  # this process, get he from our sorted list the lowest and highest year
            t.append(i)
        t.sort()
        t.insert(0, "All Years")  # the first one should be all years
        self.box1['values'] = t  # then our values should be years sorted.

        self.name_of_lecturers.insert(0, "All Investigators")  # the first one should be all Investigators
        self.box2['values'] = self.name_of_lecturers  # then our values should be investigatos sorted by surname.

        self.instutions.insert(0, "All Institutions")       # the first one should be all Institutions
        self.box3['values'] = self.instutions       # then our values should be Institutions

    def showing(self):
        try:  # let first try, if something wrong, try except
            self.mylist.delete(0, END)  # clean the area
            for key, val in self.myData.items():

                if val[0][0] <= self.box1.get() <= val[0][1]:   # filtering by years
                    if self.box2.get() == val[1]:   # filtering by lecturer
                        if self.box3.get() == val[2]:   # filtering by institution
                            self.mylist.insert(END, key)    # displaying chosen titles on listbox
                        if self.box3.get() == "All Institutions":   # no filter by institutions
                            self.mylist.insert(END, key)

                    if self.box2.get() == "All Investigators":  # no filter by investigators
                        if self.box3.get() == val[2]:   # filtering by institution
                            self.mylist.insert(END, key)    # displaying chosen titles on listbox
                        if self.box3.get() == "All Institutions":   # no filter by institutions
                            self.mylist.insert(END, key)    # displaying chosen titles on listbox
                elif self.box1.get() == "All Years":    # no filter by years

                    if self.box2.get() == val[1]:  # filtering by lecturer
                        if self.box3.get() == val[2]:  # filtering by institution
                            self.mylist.insert(END, key)  # displaying chosen titles on listbox
                        elif self.box3.get() == "All Institutions":  # no filter by institutions
                            self.mylist.insert(END, key)  # displaying chosen titles on listbox

                    elif self.box2.get() == "All Investigators":  # no filter by investigators
                        if self.box3.get() == val[2]:  # filtering by institution
                            self.mylist.insert(END, key)  # displaying chosen titles on listbox
                        elif self.box3.get() == "All Institutions":  # no filter by institutions
                            self.mylist.insert(END, key)  # displaying chosen titles on listbox
        except:
            tkMessageBox.showerror("Error",
                                   "Please before click Fetch Research Projects button.")

    def displayText(self):
        try:
            #   self.root.geometry("1050x570+150+100")
            self.text.delete('1.0', END)  # from start, to end
            which_one = self.mylist.get(ACTIVE)  # get the which one is selected
            document = self.myData[which_one][4]  # get the text for which one is selected
            self.text.insert(END, document)  # insert the text

            url = self.images[which_one]  # get the url from dict
            image_bytes = urlopen(url).read()  # read the pic
            # internal data file
            data_stream = io.BytesIO(image_bytes)
            # open as a PIL image object
            pil_image = Image.open(data_stream)
            img = pil_image.resize((500, 250), Image.ANTIALIAS)  # same size with canvas
            self.tk_image = ImageTk.PhotoImage(img)

            # create a white canvas
            cv = Canvas(self.frame3, bg='brown', width=500, height=250)
            cv.grid(row=1, column=1)

            # put the image on the canvas with
            # create_image(xpos, ypos, image, anchor)
            cv.create_image(2, 2, image=self.tk_image, anchor='nw')

        except:
            tkMessageBox.showerror("Error",
                                   "Please before click Dislay Project Titles button.")

    def geometricDesign(self):
        self.title.grid(row=0, column=0, columnspan=5, sticky=N)
        self.provide.grid(row=1, column=0, sticky=W)
        self.url.grid(row=2, column=0, sticky=W, columnspan=2)
        self.fetch.grid(row=1, column=2, sticky=W, pady=10)
        self.period.grid(row=3, column=0, columnspan=4)
        self.filter.grid(row=0, column=0, sticky=W)
        self.year.grid(row=1, column=0, sticky=W)
        self.principal.grid(row=2, column=0, sticky=W)
        self.funding.grid(row=3, column=0, sticky=W)
        self.display.grid(row=6, column=0, sticky=W)
        self.box1.grid(row=1, column=1)
        self.box2.grid(row=2, column=1)
        self.box3.grid(row=3, column=1)
        self.mylist.grid(row=1, column=2, rowspan=4, padx=(20, 0), sticky=E)
        self.scrollbar.grid(row=1, column=3, rowspan=4, sticky=N + W + S)
        self.show.grid(row=6, column=2, pady=10)
        self.period1.grid(row=7, column=0, columnspan=4)
        self.des.grid(row=0, column=2, padx=200)
        self.text.grid(row=1,column=2,rowspan=10, padx=(20, 0), sticky=E)
        self.bar.grid(row=1,column=3, rowspan=10, sticky=N+W+S)

        self.frame1.grid()
        self.frame2.grid(sticky=W)
        self.frame3.grid()


def main():
    root = Tk()
    root.title("SEHIR Research Projects Analyzer")
    #   root.geometry("1050x500+150+100")
    app = ProjectAnalyzer(root)
    root.mainloop()


if __name__ == '__main__':
    main()

