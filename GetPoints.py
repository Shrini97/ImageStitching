from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np
import time
import sys

# placeholders for the 4 corresponding points coordinated in the two images respectively
# and their indexe variables i,j
A,B = np.zeros((4,2)), np.zeros((4,2))
i, j = 0, 0

Left = True


def process_images(img1, img2):
    '''
    Given 2 images return process the images and concat them to maintain
    the same height and maintain the aspect ratio of the secong image.
    Args:
        img1 : 3 channel cv2 image corresponding to the image from the first source
        img2 : 3 channel cv2 image corresponding to the image from the second source
    Returns:
        A single 3 channel cv2 image 

    '''
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    h1, w1, _ = img1.shape
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    h2, w2, _ = img2.shape
    img2 = cv2.resize(img2, (int(w2*h1/h2), h1))
    
    combined_img = cv2.hconcat([img1, img2])
    return combined_img

def select_keypts(img1, img2):
    '''
    Given 2 images select the corresponding points in both the images and return a matrix
    corresponding to the coordinates
    Args:
        img1 : 3 channel cv2 image corresponding to the image from the first source
        img2 : 3 channel cv2 image corresponding to the image from the second source
    Returns:
        A matrix(numpy) A and B of shape (4,2) corresponding to the pixel coordinates 
        of related elements tagged in both the images.
    '''
    root = Tk()

    #setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)
    
    #adding the image
    combined_img = process_images(img1, img2)
    
    img_pil = ImageTk.PhotoImage(Image.fromarray(combined_img))
    # we will need h to bound the click region from below and to restrict the 
    # click in the left region and right region alternatively when selecting 
    # corresponding points in the images.
    h, w, _ = img1.shape

    canvas.create_image(0,0,image=img_pil,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    def _create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
    Canvas.create_circle = _create_circle

    #function to be called when mouse is clicked
    def printcoords(event):
        global Left, A, B, i, j
        if event.y < h:
            if event.x < w and Left:
                canvas.create_circle(event.x,event.y, 5, fill="blue", outline="#DDD", width=4)
                A[i,0], A[i,1] = event.x, event.y
                i+=1
                Left = False
            if event.x > w and not Left:
                canvas.create_circle(event.x,event.y, 5, fill="blue", outline="#DDD", width=4)
                B[j,0], B[j,1] = event.x - w, event.y
                j+=1
                Left = True
        if i == 4 and j == 4:
            np.save("Left.npy",A)
            np.save("Right.npy",B)
            sys.exit()

    #mouseclick event
    canvas.bind("<Button 1>",printcoords, Left)
    root.mainloop()
