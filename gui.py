"""Draw

Usage:
  draw_ui.py [options]

Options:
  -h --help                   Show this screen

"""
import math
import random
import cairo
import docopt
import tkinter

from PIL import Image, ImageTk

class DrawUI(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width, self.height = 1024, 1024

        self.geometry("{}x{}".format(self.width, self.height))

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.label:tkinter.Label = None
        self.button = tkinter.Button(self, text="Generate", command=self.draw)
        self.button.pack()

    def draw(self):
        if self.label:
            self.label.destroy()

        self.context.set_source_rgb(random.random(), random.random(), random.random())
        self.context.arc(512, 512, 50, 0, 360)
        self.context.fill()

        self._image_ref = ImageTk.PhotoImage(Image.frombuffer("RGBA", (self.width, self.height), self.surface.get_data().tobytes(), "raw", "BGRA", 0, 1))
        self.label = tkinter.Label(self, image=self._image_ref)
        self.label.pack(expand=True, fill="both")

def main():
    arguments = docopt.docopt(__doc__, version='v0.0.0')
    window = DrawUI()
    window.mainloop()

if __name__ == '__main__':
    main()
