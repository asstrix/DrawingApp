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

		self.last_x, self.last_y = None, None
		self.pen_color = 'black'
		self.last_color = ''
		self.control_frame = tk.Frame(self.root)

		self.rubber_button = tk.Button(self.control_frame, command=self.rubber)

		self.setup_ui()

		self.canvas.bind('<B1-Motion>', self.paint)
		self.canvas.bind('<ButtonRelease-1>', self.reset)
		self.canvas.bind('<Button-3>', self.pipette)

	def setup_ui(self):
		"""
        Sets up the control panel UI, including buttons for clearing, choosing color,
        saving, selecting brush size, and switching between brush and rubber modes.

		"""
		self.control_frame.pack(fill=tk.X)

		clear_icon = tk.PhotoImage(file="images/clear.png")
		clear_button = tk.Button(self.control_frame, image=clear_icon, command=self.clear_canvas)
		clear_button.image = clear_icon
		clear_button.pack(side=tk.LEFT)
		self.add_tooltip(clear_button, "Очистить")

		color_icon = tk.PhotoImage(file="images/colour.png")
		color_button = tk.Button(self.control_frame, image=color_icon, command=self.choose_color)
		color_button.image = color_icon
		color_button.pack(side=tk.LEFT)
		self.add_tooltip(color_button, "Цвет кисти")

		save_icon = tk.PhotoImage(file="images/save.png")
		save_button = tk.Button(self.control_frame, image=save_icon, command=self.save_image)
		save_button.image = save_icon
		save_button.pack(side=tk.LEFT)
		self.add_tooltip(save_button, "Сохранить изоюражение")

		brush_sizes = ['1', '2', '5', '10']
		self.selected_brush_size.set(brush_sizes[0])
		brush_size = tk.OptionMenu(self.control_frame, self.selected_brush_size, *brush_sizes)
		brush_size.pack(side=tk.LEFT)
		self.add_tooltip(brush_size, "Размер кисти")

		rubber_icon = tk.PhotoImage(file="images/rubber.png")
		self.rubber_button.config(image=rubber_icon, state="disabled")
		self.rubber_button.image = rubber_icon
		self.rubber_button.pack(side=tk.LEFT)
		self.add_tooltip(self.rubber_button, "Ластик")

	@staticmethod
	def add_tooltip(widget, text):
		tooltip = None

		def show_tooltip(event):
			nonlocal tooltip
			if tooltip is not None:
				return
			x = widget.winfo_rootx() + 20
			y = widget.winfo_rooty() + widget.winfo_height() + 5
			tooltip = tk.Toplevel(widget)
			tooltip.wm_overrideredirect(True)
			tooltip.wm_geometry(f"+{x}+{y}")
			label = tk.Label(tooltip, text=text, background="white", relief="solid", borderwidth=1, padx=5, pady=3)
			label.pack()

		def hide_tooltip(event):
			nonlocal tooltip
			if isinstance(tooltip, tk.Toplevel):
				tooltip.destroy()
				tooltip = None
		widget.bind("<Enter>", show_tooltip)
		widget.bind("<Leave>", hide_tooltip)

	def paint(self, event):
		"""
        Draws a line on the canvas and image from the last known mouse position to
        the current mouse position. This function is bound to mouse movement events.

        Args:
            event (tk.Event): The event object containing the current mouse position.
		"""
		self.rubber_button.config(state="normal")
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

	def rubber(self):
		"""
        Activates the rubber tool by setting the pen color to white (background color)
        and storing the last used pen color in case the user switches back to brush.
		"""
		self.last_color = self.pen_color
		self.pen_color = 'white'

	def pipette(self, event):
		rgb = self.image.getpixel((event.x, event.y))
		self.pen_color = '#{:02x}{:02x}{:02x}'.format(*rgb)

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
