import os
import platform
import subprocess
from tkinter import Tk
from tkinter import filedialog as tkFileDialog
from PIL import Image
import tempfile


def raise_app(root):
    root.attributes("-topmost", True)
    if platform.system() == 'Darwin':
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'
        script = tmpl.format(os.getpid())
        output = subprocess.check_call(['/usr/bin/osascript', '-e', script])
    root.after(0, lambda: root.attributes("-topmost", False))


def set_image_dpi(image):
    image_resize = image
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    image_resize.save(temp_filename, dpi=(72, 72))
    return temp_filename


def main():
    toplevel = Tk()
    raise_app(toplevel)
    toplevel.withdraw()

    filenames = tkFileDialog.askopenfilenames()

    if len(filenames) > 0:
        for image in filenames:
            # se for pdf transformar em imagem antes de fazer a conversão
            
            path = os.path.dirname(image)
            name = os.path.basename(image).split('.')[0]

            img = Image.open(image)
            path_temp_img = set_image_dpi(img)
            img_new_dpi_size = os.path.getsize(path_temp_img) / 1024

            new_img = Image.open(path_temp_img)

            if(img_new_dpi_size > 1024):
                multplication_rate = 1024.0 / (img_new_dpi_size * 1.0)
                resized_im = new_img.resize((round(new_img.size[0] * multplication_rate), round(new_img.size[1] * multplication_rate)))
            else:
                resized_im = new_img

            path_name = path + '/' +  name + '.pdf'
            print(path_name)
            resized_im.save(path_name, save_all=True)

main()
