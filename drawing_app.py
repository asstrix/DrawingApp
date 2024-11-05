import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
	"""
    A GUI application for drawing on the 600x400 plot and saving the image as a PNG file.

    Attributes:
        selected_brush_size (tk.StringVar): Variable to store selected brush size.
        root (tk.Tk): Root window of the tkinter application.
        image (PIL.Image): Image object for drawing and saving as a PNG.
        draw (PIL.ImageDraw.Draw): Draw object for drawing on the image.
        canvas (tk.Canvas): Canvas widget for drawing shapes.
        last_x, last_y (int or None): Coordinates of the last mouse position for drawing lines.
        pen_color (str): Current color of the pen/brush.
        last_color (str): Last used color of the pen, stored when switching to rubber.
	"""

	def __init__(self, root):
		"""
        Initializes the DrawingApp with the main tkinter root, canvas, image, and UI controls.

        Args:
            root (tk.Tk): Root window of the tkinter application.
		"""
		self.selected_brush_size = tk.StringVar()
		self.root = root
		self.root.title("Рисовалка с сохранением в PNG")

		self.image = Image.new("RGB", (600, 400), "white")
		self.draw = ImageDraw.Draw(self.image)

		self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
		self.canvas.pack()

		self.setup_ui()

		self.last_x, self.last_y = None, None
		self.pen_color = ''
		self.last_color = ''

		self.brush()

	def setup_ui(self):
		"""
        Sets up the control panel UI, including buttons for clearing, choosing color,
        saving, selecting brush size, and switching between brush and rubber modes.

		"""

		control_frame = tk.Frame(self.root)
		control_frame.pack(fill=tk.X)

		clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
		clear_button.pack(side=tk.LEFT)

		color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
		color_button.pack(side=tk.LEFT)

		save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
		save_button.pack(side=tk.LEFT)

		label = tk.Label(control_frame, text="Размер кисти:")
		label.pack(side=tk.LEFT)
		brush_sizes = ['1', '2', '5', '40']
		self.selected_brush_size.set(brush_sizes[0])
		brush_size = tk.OptionMenu(control_frame, self.selected_brush_size, *brush_sizes)
		brush_size.pack(side=tk.LEFT)

		brush_button = tk.Button(control_frame, text="Кисть", command=self.brush)
		brush_button.pack(side=tk.LEFT)

		rubber_button = tk.Button(control_frame, text="Ластик", command=self.rubber)
		rubber_button.pack(side=tk.LEFT)

	def paint(self, event):
		"""
        Draws a line on the canvas and image from the last known mouse position to
        the current mouse position. This function is bound to mouse movement events.

        Args:
            event (tk.Event): The event object containing the current mouse position.
		"""
		if self.last_x and self.last_y:
			self.canvas.create_line(
				self.last_x, self.last_y, event.x, event.y,
				width=int(self.selected_brush_size.get()), fill=self.pen_color,
				capstyle=tk.ROUND, smooth=tk.TRUE
			)
			self.draw.line(
				[self.last_x, self.last_y, event.x, event.y],
				fill=self.pen_color, width=int(self.selected_brush_size.get())
				)
		self.last_x = event.x
		self.last_y = event.y

	def brush(self):
		"""
        Activates the brush tool by setting the pen color to the last used color
        or black if no previous color exists, and binds the paint method to mouse
        motion events.
		"""
		self.pen_color = self.last_color if self.last_color != '' else 'black'
		self.canvas.bind('<B1-Motion>', self.paint)
		self.canvas.bind('<ButtonRelease-1>', self.reset)

	def rubber(self):
		"""
        Activates the rubber tool by setting the pen color to white (background color)
        and storing the last used pen color in case the user switches back to brush.
		"""
		self.last_color = self.pen_color
		self.pen_color = 'white'

	def reset(self, event):
		"""
		Resets the last known mouse position, ending the current line. This function
        is called on mouse release events.

        Args:
            event (tk.Event): The event object indicating the mouse release.
		"""
		self.last_x, self.last_y = None, None

	def clear_canvas(self):
		"""
		Clears the canvas and resets the image to a blank white background.
		"""
		self.canvas.delete("all")
		self.image = Image.new("RGB", (600, 400), "white")
		self.draw = ImageDraw.Draw(self.image)

	def choose_color(self):
		"""
		Opens a color chooser dialog to let the user pick a new color for the pen.
        Updates the pen color with the selected color.
		"""
		self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

	def save_image(self):
		"""
		Opens a file dialog to save the current drawing as a PNG file. If a file
        path is chosen, the image is saved, and a success message is displayed.
		"""
		file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
		if file_path:
			if not file_path.endswith('.png'):
				file_path += '.png'
			self.image.save(file_path)
			messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
	"""
	Main function to initialize and run the drawing application.
	"""
	root = tk.Tk()
	app = DrawingApp(root)
	root.mainloop()


if __name__ == "__main__":
	main()
