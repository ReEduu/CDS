import tkinter as tk
from PIL import Image, ImageTk
import time

def show_image(image_path, window, label):
    if window is None:
        window = tk.Tk()
        window.title("Image Viewer")
        window.geometry("800x600")

    new_img = Image.open(image_path)
    new_img_tk = ImageTk.PhotoImage(new_img)

    if label is not None:
        label.config(image=new_img_tk)
        label.image = new_img_tk
    else:
        label = tk.Label(window, image=new_img_tk)
        label.image = new_img_tk
        label.pack()

    return window, label

def main():
    image_paths = ["clock_fear.png", "clock_happiness.png", "clock_neutral.png"]
    current_index = 0
    window = None
    label = None

    while True:
        window, label = show_image(image_paths[current_index], window, label)
        current_index = (current_index + 1) % len(image_paths)
        window.update()
        time.sleep(3)

if __name__ == "__main__":
    main()
