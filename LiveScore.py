import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import random
from tkinter import *       #importeras för skapa ett grafiskt användargränssnitt till programmet
from tkinter import messagebox      #används för error meddelande
from tkinter import ttk     #Används för att skapa en scrollbar


class League:
    def __init__(self,league_name,link):
        self.league_name=league_name
        self.link=link
        self.info=[]

    def __repr__(self):
        return f"{self.league_name}"

    def get_info(self,driver):
        self.info=[]
        elem_info=[]

        driver.get(str(self.link))
        time.sleep(3)

        try:
            for x in range(35):
                try:
                    date=driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[1]/div[3]/div[2]/div/div["+str(x+1)+"]")
                    elem_info.append(date)
                except:
                    match=driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[1]/div[3]/div[2]/div/div["+str(x+1)+"]/a/div")
                    elem_info.append(match)
        except:
            pass

        for el in elem_info:
            el=el.text.split("\n")
            if el[0]=="ROUND":
                continue
            self.info.append(el)
        
        self.print_info()

    def print_info(self):
        months=["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNI","JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]

        root.destroy()    

        league_root=Tk()      
        league_root.configure(bg="black")       
        league_root.title(f"{self.league_name}")   

        w,h = league_root.winfo_screenwidth(), league_root.winfo_screenheight()
        league_root.geometry("%dx%d+0+0" % (w, h))

        window_frame=create_scrollbar(league_root)

        Button(window_frame, text="←", bg="orange", fg="white", command=lambda:[league_root.destroy(),main()]).grid(row=0,column=0,ipadx=20)

        k=1
        for info in self.info:
            for inf in info:
                Label(window_frame, text=inf, font=("Prometo",18,"bold"), bg="black", fg="orange").grid(row=0,column=k,ipady=20)
                k=3
            break

        self.info.pop(0)

        for i,info in enumerate(self.info):
            s=" "
            templist=[x.upper() for x in info]
            tempstring=s.join(templist)
            if any(month in tempstring for month in months):
                try:
                    l_name=Label(window_frame, text=info[0], font=("Prometo",18,"bold"), bg="black", fg="orange")
                    l_date=Label(window_frame, text=info[1], font=("Prometo",18,"bold"), bg="black", fg="orange")

                    l_name.grid(row=i+1,column=k-3,ipady=20)
                    l_date.grid(row=i+1,column=k,ipady=20)
                except IndexError:
                    Label(window_frame, text=info[0], font=("Prometo",18,"bold"), bg="black", fg="orange").grid(row=i+1,column=k,ipady=20)
                continue
            for j,inf in enumerate(info):
                Label(window_frame, text=inf, font=("Prometo",12,"bold"), bg="black", fg="white").grid(row=i+1,column=j)

        league_root.mainloop()


def create_league_objects(league_objects):
    fil=open("leagues_info.txt","r",encoding="utf-8")
    rader=fil.readlines()
    for rad in rader:
        rad=rad.replace("\n","").split(",")        
        league_obj=League(rad[0],rad[1])
        league_objects.append(league_obj)
    return league_objects


def create_driver():
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko; compatible; BW/1.1; bit.ly/2W6Px8S) Chrome/74.0.3729.131 Safari/537.36"

    options=webdriver.ChromeOptions()

    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("detach", True)
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')

    driver=webdriver.Chrome(executable_path="chromedriver.exe",options=options)

    return driver

def create_main_root():
    SCREEN_WIDTH=500
    SCREEN_HEIGHT=500

    global root    
    root=Tk()      
    root.configure(bg="black")       
    root.title("LiveScore")   
    root.geometry(str(SCREEN_WIDTH)+"x"+str(SCREEN_HEIGHT))       
    return root

def menu(root,league_objects,driver):
    window_frame=create_scrollbar(root)

    Label(window_frame, text="LiveScore", font=("Prometo",18,"bold"), bg="black", fg="orange").pack(padx=20)

    btns=[]
    for l in league_objects:
        btn=Button(window_frame, text=str(l), bg="orange", fg="white", command=lambda l=l: l.get_info(driver)).pack(padx=20,pady=50)
    

def create_scrollbar(root_r):     
    window_frame=Frame(root_r, bg="black")       
    window_frame.pack(fill=BOTH, expand=1)      

    canvas=Canvas(window_frame, bg="black")
    canvas.pack(side=LEFT, fill=BOTH, expand=1)

    scrollbar=ttk.Scrollbar(window_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)    

    canvas.configure(yscrollcommand=scrollbar.set)        
    
    canvas.bind("<Configure>", lambda e:canvas.configure(scrollregion=canvas.bbox("all")))      

    window_frame_2=Frame(canvas, bg="black")       

    canvas.create_window((0,0), window=window_frame_2, anchor="ne")      

    return window_frame_2    



def main():
    league_objects=[]
    league_objects=create_league_objects(league_objects)

    driver=create_driver()
    root=create_main_root()
    menu(root,league_objects,driver)
    root.mainloop()

main()