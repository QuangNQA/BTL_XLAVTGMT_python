import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

# ---------- Utils ----------
def resize_keep_ratio(img, max_size):
    w, h = img.size
    ratio = min(max_size / w, max_size / h)
    return img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)

def show_image_on_canvas(canvas, pil_img):
    canvas.delete("all")
    img = resize_keep_ratio(pil_img, 300)
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(160, 160, image=photo)
    canvas.image = photo

# ---------- App ----------
root = tk.Tk()
root.title("Công cụ nén ảnh")
root.geometry("750x500")
root.configure(bg="#f5f6fa")

# ---------- Title ----------
tk.Label(
    root, text="Công cụ nén ảnh",
    font=("Segoe UI", 16, "bold"),
    bg="#f5f6fa"
).pack(pady=10)

# ---------- Image Area ----------
frame_img = tk.Frame(root, bg="#f5f6fa")
frame_img.pack()

canvas_orig = tk.Canvas(frame_img, width=320, height=320, bg="white")
canvas_orig.grid(row=0, column=0, padx=20)

canvas_comp = tk.Canvas(frame_img, width=320, height=320, bg="white")
canvas_comp.grid(row=0, column=1, padx=20)

tk.Label(frame_img, text="Ảnh gốc", bg="#f5f6fa").grid(row=1, column=0)
tk.Label(frame_img, text="Ảnh đã nén", bg="#f5f6fa").grid(row=1, column=1)

# ---------- Controls ----------
frame_ctrl = tk.Frame(root, bg="#f5f6fa")
frame_ctrl.pack(pady=15)

method = tk.StringVar(value="jpeg")

tk.Radiobutton(frame_ctrl, text="JPEG", variable=method, value="jpeg",
               bg="#f5f6fa").grid(row=0, column=0, padx=10)
tk.Radiobutton(frame_ctrl, text="JPEG2000", variable=method, value="jp2",
               bg="#f5f6fa").grid(row=0, column=1, padx=10)

quality = tk.IntVar(value=50)

tk.Label(frame_ctrl, text="Chất Lượng", bg="#f5f6fa")\
    .grid(row=1, column=0, columnspan=2)

slider = tk.Scale(
    frame_ctrl, from_=10, to=100, orient="horizontal",
    variable=quality, length=300, bg="#f5f6fa"
)
slider.grid(row=2, column=0, columnspan=2)
slider.config(command=lambda e: compress_image())
size_label = tk.Label(
    root,
    text="Compressed size: -- KB",
    font=("Segoe UI", 10),
    bg="#f5f6fa"
)
size_label.pack(pady=5)

# ---------- Logic ----------
original_pil = None
original_cv = None

def open_image():
    global original_pil, original_cv
    path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.png *.bmp *.jp2")]
    )
    if not path:
        return

    original_pil = Image.open(path).convert("RGB")
    original_cv = cv2.cvtColor(np.array(original_pil), cv2.COLOR_RGB2BGR)

    show_image_on_canvas(canvas_orig, original_pil)
    compress_image()

def compress_image():
    if original_cv is None:
        return

    q = quality.get()

    if method.get() == "jpeg":
        temp = "temp.jpg"
        cv2.imwrite(
            temp,
            original_cv,
            [cv2.IMWRITE_JPEG_QUALITY, q]
        )
    else:
        temp = "temp.jp2"
        rate = int((100 - q) ** 2 + 100)
        cv2.imwrite(
            temp,
            original_cv,
            [cv2.IMWRITE_JPEG2000_COMPRESSION_X1000, rate]
        )

    img = Image.open(temp)
    show_image_on_canvas(canvas_comp, img)

    size_kb = os.path.getsize(temp) / 1024
    size_label.config(text=f"Compressed size: {size_kb:.2f} KB")

# ---------- Button ----------
tk.Button(
    root, text="Chọn Ảnh",
    font=("Segoe UI", 10, "bold"),
    command=open_image,
    bg="#4a69bd", fg="white", padx=20, pady=5
).pack()

root.mainloop()
