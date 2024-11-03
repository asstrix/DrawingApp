import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.selected_brush_size = tk.StringVar()
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_image = tk.PhotoImage(file="images/clear2.png")
        clear_button = tk.Button(control_frame, image=clear_image, command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)
        clear_button.image = clear_image

        color_image = tk.PhotoImage(file="images/colour2.png")
        color_button = tk.Button(control_frame, image=color_image, command=self.choose_color)
        color_button.pack(side=tk.LEFT)
        color_button.image = color_image

        save_image = tk.PhotoImage(file="images/save2.png")
        save_button = tk.Button(control_frame, image=save_image, command=self.save_image)
        save_button.pack(side=tk.LEFT)
        save_button.image = save_image

        label = tk.Label(control_frame, text='Размер кисти')
        label.pack(side=tk.LEFT)
        brush_sizes = ['1', '2', '5', '10']

        self.selected_brush_size.set(brush_sizes[0])
        brush_size = tk.OptionMenu(control_frame, self.selected_brush_size, *brush_sizes)
        brush_size.pack(side=tk.LEFT)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=int(self.selected_brush_size.get()), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=int(self.selected_brush_size.get()))

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
