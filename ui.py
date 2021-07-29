from FaceMaskVideoDetection import DetectVideoFaceMasks
from FaceMaskImageDetect import DetectMaskImage
import time
import tkinter
from tkinter import ttk
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *
import tkinter.font as font
from tkinter.filedialog import askopenfile
from PIL import Image,ImageTk
from tkcalendar import Calendar
import os
import cv2



loadwin = tkinter.Tk()
loadwin.title("Face-Mask Detector")
    # Create an instance of tkinter frame


loadwin.config(bg='black')
windowWidth = loadwin.winfo_reqwidth()
windowHeight = loadwin.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(loadwin.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(loadwin.winfo_screenheight()/2 - windowHeight/2)

# Positions the window in the center of the page.
loadwin.geometry("500x600".format(positionRight, positionDown))
photo_image = ImageTk.PhotoImage(file="images/logo.png")
label = Label(loadwin, image=photo_image,anchor=CENTER,borderwidth=0,background='black')
label.place(relx=0.5,rely=0.3,anchor='center')
buttonFont = font.Font(family='Helvetica', size=16, weight='bold')


def StartApplication():
    loadwin.destroy()
    top = tkinter.Tk()
    top.title('Face-Mask Detector')
    top.resizable(0, 0)
    top.geometry('1780x1000')
    top.config(bg='#262837')
    buttonFont = font.Font(family='Helvetica', size=16, weight='bold')
    Labelfont = font.Font(family='Helvetica', size=20, weight='bold')
    #user_name = Label(top, font=Labelfont, text="Face-Mask Detector").place(x=750, y=100)
    my_str = tkinter.StringVar()

    #photo_image = ImageTk.PhotoImage(file="zyy.jpg")
    #label = Label(top, image=photo_image)
    #label.place(x=0, y=0, relwidth=1, relheight=1)
    Labelfont = font.Font(family='Helvetica', size=25, weight='bold')
    img = Image.open('images/logo.png')
    resized_image = img.resize((400, 350), Image.ANTIALIAS)
    logoIMG = ImageTk.PhotoImage(resized_image)
    label2 = Label(top, image=logoIMG , background="#262837").place( relx=0.5, rely=0.1, anchor='center')
    #user_name = Label(top, font=Labelfont, background="#262837", foreground="white", text="Face-Mask Detector").place(
       #     relx=0.5, rely=0.1, anchor='center')

    uploadIMG = ImageTk.PhotoImage(file="images/upload-xxl.png")
    liveIMG = ImageTk.PhotoImage(file="images/slr-camera-2-xxl.png")
    searchIMG = ImageTk.PhotoImage(file="images/search-9-xxl.png")
    A = tkinter.Button(top,image=liveIMG , font=buttonFont, activeforeground="green", height=225, width=225,
                           bg='#262837', fg='white',borderwidth=0,
                           command=LiveStreamFunction)
    A.grid(row=20, column=15, pady=400, padx=160)
    upload_photo = Label(top, font=Labelfont, background="#262837", foreground="white", text="Upload Photo").place(
        relx=0.09,rely=0.7)

    B = tkinter.Button(top, image=searchIMG, font=buttonFont, activeforeground="green", height=300, width=300,
                           bg='#262837', fg='white', borderwidth=0,
                           command=lambda: change(top, buttonFont))
    B.grid(row=20, column=14, pady=400, padx=160)
    Search_Photo = Label(top, font=Labelfont, background="#262837", foreground="white", text="Search by Date").place(
        relx=0.41, rely=0.7)
    C = tkinter.Button(top, image=uploadIMG, font=buttonFont, activeforeground="green", height=225, width=225,
                           bg='#262837', fg='white', borderwidth=0,
                           command=lambda: change2(top))
    C.grid(row=20, column=13, pady=400, padx=160)
    Live_Stream = Label(top, font=Labelfont, background="#262837", foreground="white", text="Live Stream").place(
        relx=0.76, rely=0.7)
    top.mainloop()

def change(top, buttonFont):
    top.withdraw()
    SearchDBfunction(top, buttonFont)

def change2(top):
    top.withdraw()
    uploadphotoFunction(top)

def LiveStreamFunction():
    detectvideofacemasks = DetectVideoFaceMasks()
    detectvideofacemasks.run()


def ShowItOnFram(collection):
    ShowImages = tkinter.Toplevel()
    ShowImages.title("Search in DB")
    ShowImages.geometry('820x720')
    ShowImages.config(bg='black')

    frame = Frame(ShowImages)
    frame.pack(fill=BOTH, expand=1)
    canvas = Canvas(frame)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame2 = Frame(canvas)
    canvas.create_window((0, 0), window=frame2, anchor="nw")

    for image in collection:
        lbl = Label(frame2)
        img = Image.open('SavedIMages/' + image)
        resized_image = img.resize((300, 205), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized_image)
        lbl.configure(image=img)
        lbl.image = img
        lbl.pack()

    ShowImages.mainloop()

def GetImagesandUpload(Date):
    path = 'SavedImages/'
    collection = []
    for image in os.listdir(path):
        img = image.split('.')
        img = img[0].split('(')
        img = img[0].split(' ')
        if img[0] == Date:
            collection.append(image)

    return (collection)

def SearchDBfunction(top, buttonFont):
    searchf = tkinter.Tk()
    searchf.title("Search in DB")
    searchf.geometry('1180x500')
    searchf.config(background="#262837")
    img2 = Image.open('images/home.png')
    resized_image1 = img2.resize((50, 50), Image.ANTIALIAS)
    home = ImageTk.PhotoImage(resized_image1)
    Button(searchf,text='home', command=lambda: changefromSearchToMain(top, searchf)).pack(pady=20)
    cal = Calendar(searchf, selectmode='day',
                       year=2020, month=5,
                       day=22, date_pattern='yyyy-mm-dd')
    cal.pack(pady=20)
    def grad_date():
         date.config(text="Selected Date is: " + cal.get_date())
         collection = GetImagesandUpload(cal.get_date())
         ShowItOnFram(collection)

    Button(searchf, text="Get Date",
        command=grad_date).pack(pady=20)

    date = Label(searchf, text="")
    date.pack(pady=20)

        # Button(searchf, text="Back to Home",  command=StartApplication).pack(pady=20)

        # Excecute Tkinter
    searchf.mainloop()

def uploadphotoFunction(top):
    my_str = tkinter.StringVar()
    my_str.set("")
    upload = tkinter.Toplevel()
    upload.title('upload photo')
    upload.geometry('1000x400')
    upload.config(background="#262837")
    lbl = Label(upload)
    lbl.pack()
    img2= Image.open('images/home.png')
    resized_image1 = img2.resize((50, 50), Image.ANTIALIAS)
    home = ImageTk.PhotoImage(resized_image1)
    A = tkinter.Button(upload, image=home, font=buttonFont, activeforeground="green", height=100, width=100,
                       bg='#262837', fg='white', borderwidth=0,
                       command=lambda: changefromUploadToMain(top,upload))
    A.place(relx=0.45,rely=0.77)
    file = tkinter.filedialog.askopenfilename(initialdir="/", title="Select An Image",
                                                  filetype=(("jpeg", "*.jpg"), ("png", "*.png")))
    img1 = cv2.imread(file)
    detectmaskimage = DetectMaskImage(img1)
    detectedImage = detectmaskimage.run()
    cv2.imwrite("detectedPhoto.jpg", detectedImage)
    img = Image.open('detectedPhoto.jpg') 
    resized_image = img.resize((500, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(resized_image)
    lbl.configure(image=img)
    lbl.image = img
    os.remove("detectedPhoto.jpg")

    upload.mainloop()

def changefromSearchToMain(top, searchf):
    searchf.withdraw()
    top.deiconify()

def changefromUploadToMain(top, upload):
    upload.withdraw()
    top.deiconify()

progress = Progressbar(loadwin, orient = HORIZONTAL,
            length = 300, mode = 'indeterminate')

def bar():
    progress['value'] = 20
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 40
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 50
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 60
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 80
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 100
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 80
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 60
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 50
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 40
    loadwin.update_idletasks()
    time.sleep(0.5)

    progress['value'] = 20
    loadwin.update_idletasks()
    time.sleep(0.5)
    progress['value'] = 0
    loadwin.after(1000, StartApplication)
progress.place(relx = 0.5,rely=0.5,anchor='center')
A = tkinter.Button(loadwin, text="Start Application", font=buttonFont, activeforeground="green",
                           bg='#4C4B4B', fg='white', relief=GROOVE,
                           command=bar).place(relx = 0.5, rely=0.65,anchor='center')
#Button(loadwin, text = 'Start Application' , activeforeground="green", height=4, width=20,
                          # bg='#4C4B4B', fg='white', relief=GROOVE  ,command = bar ).pack(pady = 10)

loadwin.mainloop()