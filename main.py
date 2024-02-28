import cv2
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk
import pyttsx3


engine = pyttsx3.init()

def is_movement(frame1, frame2, threshold=25):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(gray1, gray2)
    _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return any(cv2.contourArea(contour) > 100 for contour in contours)

def show_popup():
    popup = tk.Tk()
    popup.wm_title("Motion Detected!")


    image_path = 'apiit_fcs_logo.png'
    img = Image.open(image_path)
    img = ImageTk.PhotoImage(img)
    label = tk.Label(popup, image=img)
    label.pack(side="top", fill="both", expand="yes")


    engine.say("Hey there! greetings from Full stack computer society!")
    engine.runAndWait()

    popup.after(3000, popup.destroy)
    popup.geometry("500x500")
    popup.mainloop()

def capture_frames():
    cap = cv2.VideoCapture(0)
    frame_width, frame_height = 640, 480
    cap.set(3, frame_width)
    cap.set(4, frame_height)

    _, frame1 = cap.read()
    _, frame2 = cap.read()

    while True:
        frame1, frame2 = frame2, cap.read()[1]
        cv2.imshow('Video', frame2)

        if is_movement(frame1, frame2):
            print("Motion Detected! Showing pop-up.")
            Thread(target=show_popup).start()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    capture_frames()

if __name__ == "__main__":
    main()

