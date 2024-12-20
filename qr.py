import tkinter as tk
from tkinter import ttk

import qrcode

import PIL
from PIL import Image, ImageTk

def gen_qr_code(qr_text):
    if len(qr_text) == 0:
        pass
    else:
        qr_code_window = tk.Toplevel()
        qr_code_window.wm_title("QR Code Generator")
        qr_code_window.attributes("-topmost", True)
        qr_code_window.lift()
        qr_image = qrcode.make(qr_text)
        qr_image.save('QR_CODE.png')
        
        qr_img = Image.open('QR_CODE.png').resize((600, 600))
        
        qr_img = ImageTk.PhotoImage(qr_img)

        qr_code_image = ttk.Label(qr_code_window, image=qr_img)
        qr_code_image.image = qr_img 
        qr_code_image.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        qr_code_window.mainloop()