from typing import Tuple
import customtkinter as ctk
from customtkinter import *
from PIL import Image
from tkinter import filedialog
import tkinter as tk
from PIL import ImageTk, Image
import cv2
import numpy as np

class app(ctk.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__()  

        self.x = 10

        self.main = CTkFrame(self,width=375,height=667,fg_color='#e4dfdf')
        self.main.place(x=0,y=0)


        self.main_app()

    def main_app(self):

        self.box = CTkFrame(self.main,height=380,width=300,fg_color='white')
        self.box.place(x=37.5,y=50)

        #box yg dipaling bawah
        self.box2 = CTkFrame(self.main,height=50,width=375,fg_color='white')
        self.box2.place(x=0,y=617)

        #box biru 
        self.box3 = CTkFrame(self.box,height=100,width=250,fg_color='#a9b7d8')
        self.box3.place(x=25,y=35)

        #gambar yang di dalam kotak putih
        image_pathh = 'opa.jpeg'  
        img = Image.open(image_pathh)
        img = img.resize((250, 250))  
        img = ImageTk.PhotoImage(img)

        self.image_label = CTkLabel(self.box, image=img,text='')
        self.image_label.image = img
        self.image_label.place(x=90, y=190)
        
        #tulisan yg di dalam koyak biru
        self.nama = CTkLabel(self.box3,text='Hello!',font=('Montserrat',24,'bold'),text_color='#5169a2')
        self.nama.place(x=10,y=10)

        self.nama = CTkLabel(self.box3,text="Don't forget to smile",font=('Montserrat',24),text_color='#5169a2')
        self.nama.place(x=10,y=50)

        #logo scan
        scan_img = CTkImage(light_image=Image.open('scann.jpeg'),size=(40,40))
        self.tombol = CTkButton(self.main,height=50,width=50,command=self.live_stream,text='',image=scan_img,fg_color='#5169a2',corner_radius=25)
        self.tombol.place(x=145,y=480)

        #logo ambil foto
        foto_img = CTkImage(light_image=Image.open('imagee.jpeg'),size=(40,40))
        self.tombol2 = CTkButton(self.main,height=40,width=40,command= self.open_image,text='',image=foto_img,fg_color='#5169a2')
        self.tombol2.place(x=50,y=550)

        #logo ambil video
        video_img = CTkImage(light_image=Image.open('videoo.jpeg'),size=(40,40))
        self.tombol3 = CTkButton(self.main,height=40,width=40,command=self.open_video,text='',image=video_img,fg_color='#5169a2')
        self.tombol3.place(x=270,y=550)

        # tulisan smilify paling bawah
        image_smilify = 'tulisan.jpeg'  # Replace with your image path
        img = Image.open(image_smilify)
        img = img.resize((60, 30))  # Resize the image to fit the box
        img = ImageTk.PhotoImage(img)

        self.image_label = CTkLabel(self.box2, image=img,text='')
        self.image_label.image = img
        self.image_label.place(x=170, y=10)
    

    def face_detect(self, image):
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=10)

        for (sx, sy, sw, sh) in faces:
            cv2.rectangle(image, (sx, sy), (sx + sw, sy + sh), (0, 255, 0), 2)

    def smile_detect(self, image):
        smile_cascade = cv2.CascadeClassifier("smile_cascade.xml")
        smiles = smile_cascade.detectMultiScale(image, scaleFactor=1.3, minNeighbors=40)

        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(image, (sx, sy), (sx + sw, sy + sh), (255, 0, 0), 2)

    #buat akses file foto
    def open_image(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select an image",
                                            filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*")))

        if filepath:
            img = Image.open(filepath)
            img = img.resize((340, 340), resample=Image.LANCZOS)

            # Convert PIL Image to numpy array
            img_array = np.array(img)

            # Detect faces and smiles
            self.face_detect(img_array)
            self.smile_detect(img_array)

            # Convert numpy array back to PIL Image (for display in GUI)
            img = Image.fromarray(img_array)
            img = ImageTk.PhotoImage(img)
            self.image_label = CTkLabel(self.box, image=img, text='')
            self.image_label.image = img
            self.image_label.place(x=40, y=145)
    #buat akses file video
    def open_video(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select a video",
                                            filetypes=(("Video files", "*.mp4;*.avi;*.mov"), ("All files", "*.*")))

        if filepath:
            cap = cv2.VideoCapture(filepath)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Resize the frame to a smaller size (e.g. 640x480)
                frame = cv2.resize(frame, (340, 340))


                # Detect faces
                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=6)

                # Draw rectangles around the detected faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Detect smiles
                smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
                smiles = smile_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=30)

                # Draw rectangles around the detected smiles
                for (x, y, w, h) in smiles:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # Convert the frame to a PIL Image object
                img = Image.fromarray(frame)

                # Convert the PIL Image object to a PhotoImage object
                img = ImageTk.PhotoImage(img)

                # Display the video frame in a CTkLabel
                self.video_label = CTkLabel(self.box, image=img, text='')
                self.video_label.image = img
                self.video_label.place(x=40, y=145)

                # Update the GUI
                self.box.update()

                # Wait for a short period of time before reading the next frame
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            cap.release()
            cv2.destroyAllWindows()

    def live_stream(self):
    
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                 break

            # Resize the frame to a smaller size (e.g. 640x480)
            frame = cv2.resize(frame, (340, 340))

            # Detect faces
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=10, minSize=(55, 55))

            # Draw rectangles around the detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Detect smiles
            smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
            smiles = smile_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=22, minSize=(30, 30))

            # Draw rectangles around the detected smiles
            for (x, y, w, h) in smiles:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Convert the frame to a PIL Image object
            img = Image.fromarray(frame)

            # Convert the PIL Image object to a PhotoImage object
            img = ImageTk.PhotoImage(img)

            # Display the video frame in a CTkLabel
            self.video_label = CTkLabel(self.box, image=img, text='')
            self.video_label.image = img
            self.video_label.place(x=40, y=145)

            # Update the GUI
            self.box.update()

            # Wait for a short period of time before reading the next frame
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
    '''
    def open_video(self):
        filepath = filedialog.askopenfilename(initialdir="/", title="Select a video",
                                          filetypes=(("Video files", "*.mp4;*.avi;*.mov"), ("All files", "*.*")))
        if filepath:
            cap = cv2.VideoCapture(filepath)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow("Video", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            cap.release()
            cv2.destroyAllWindows()
    '''

    #buat akses camera real-time
    '''
    def display_video(self):
        cap = cv2.VideoCapture(filepath)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
    '''

if __name__ == '__main__':
    root = app()
    root.title('Smilify')
    root.geometry('375x667')
    root.resizable(False,False)
    root._set_appearance_mode('light')
    root.mainloop()

    






