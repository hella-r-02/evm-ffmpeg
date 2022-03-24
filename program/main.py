import os
import ffmpeg

from tkinter import *
from tkvideo import tkvideo


def change_logo_position(video_ffmpeg, logo, result_name):
    master = Tk()
    master.title("change")
    Label(master,
          text="Координаты высоты").grid(row=0)
    Label(master,
          text="Координата длины").grid(row=1)

    height_entry = Entry(master)
    weight_entry = Entry(master)

    height_entry.grid(row=0, column=1)
    weight_entry.grid(row=1, column=1)

    Button(master,
           text='Ok',
           command=master.quit).grid(row=3,
                                     column=0,
                                     sticky=W,
                                     pady=4)
    master.mainloop()
    height = height_entry.get()
    weight = weight_entry.get()
    try:
        master.destroy()
        (
            ffmpeg
                .filter([video_ffmpeg, logo], 'overlay', int(height), int(weight))
                .output(result_name)
                .overwrite_output()
                .run()
        )
    except ValueError:
        print("Попробуйте еще раз")
        change_logo_position(video_ffmpeg, logo, result_name)


def create_video_player(video_ffmpeg, logo, result_name):
    root = Tk()
    root.title("preview")
    video_label = Label(root)

    def change_position():
        change_logo_position(video_ffmpeg, logo, result_name)
        root.update()

    Button(root, text="Поменять позицию", command=change_position).pack()
    Button(root, text="Ok", command=quit).pack()
    video_label.pack()
    player = tkvideo(result_name, video_label, loop=1, size={700, 500})
    player.play()
    root.mainloop()


def main():
    video_name = input("Введите путь до видео: ")
    logo_name = input("Введите путь до логотипа: ")
    result_name = input("Ввведите название файла, в который будет записан результат: ")
    if os.path.isfile(video_name) == True and os.path.isfile(logo_name) == True:
        video_ffmpeg = ffmpeg.input(video_name)
        logo = ffmpeg.input(logo_name)
        (
            ffmpeg
                .filter([video_ffmpeg, logo], 'overlay', 20, 20)
                .output(result_name)
                .run()
        )
        create_video_player(video_ffmpeg, logo, result_name)

    else:
        print("Проверьте пути до файлов")


if __name__ == "__main__":
    main()
