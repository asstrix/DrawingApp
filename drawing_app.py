import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk, ImageFont


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
		Initializes the DrawingApp with a Tkinter root, canvas, image, and UI controls.

		This constructor method sets up the main components of the drawing application, including:
		- An RGBA image for storing drawings, which allows transparency.
		- A drawing canvas for user interactions.
		- Controls and tools, such as color selection, brush, rubber, and text buttons.
		- Event bindings for interactive functionality, like drawing and erasing.

		Args:
			root (tk.Tk): The main Tkinter window in which the application is displayed.

		Attributes:
			selected_brush_size (tk.StringVar): Tracks the size of the selected brush.
			root (tk.Tk): Reference to the main application window.
			width (int): Width of the drawing canvas.
			height (int): Height of the drawing canvas.
			bg_colour (str): Default background color of the canvas.
			image (PIL.Image.Image): The RGBA image where drawings are stored.
			draw (PIL.ImageDraw.ImageDraw): Object for drawing on `self.image`.
			last_x, last_y (int, int): Last known coordinates for drawing actions.
			pen_color (str): Current color of the drawing tool.
			last_color (str): Stores the previous pen color, used for switching tools.
			control_frame (tk.Frame): Frame containing UI controls.
			mode (str): Current mode of the application, e.g., 'draw'.
			color_button (tk.Button): Button to choose drawing color.
			brush_button (tk.Button): Button to activate the brush tool.
			rubber_button (tk.Button): Button to activate the eraser tool.
			text_button (tk.Button): Button to add text to the canvas.
			label (tk.Label): Label displaying the current pen color.
			canvas (tk.Canvas): Canvas widget for displaying and interacting with the image.

		Methods called:
			- `setup_ui()`: Sets up the user interface components in the control frame.
			- `binds()`: Configures event bindings for user interactions on the canvas.

		"""
		self.selected_brush_size = tk.StringVar()
		self.root = root
		self.root.title('Рисовалка с сохранением в PNG')

		self.width = 600
		self.height = 400
		self.bg_colour = 'white'
		self.image = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 255))
		self.draw = ImageDraw.Draw(self.image)

		self.last_x, self.last_y = None, None
		self.pen_color, self.last_color = 'black', 'black'
		self.control_frame = tk.Frame(self.root)
		self.mode = 'draw'

		self.color_button = tk.Button(self.control_frame, command=lambda: self.choose_color(None))
		self.brush_button = tk.Button(self.control_frame, command=self.brush)
		self.rubber_button = tk.Button(self.control_frame, command=self.rubber)
		self.text_button = tk.Button(self.control_frame, command=self.add_text)
		self.label = tk.Label(self.control_frame, bg=self.pen_color)

		self.setup_ui()

		self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
		self.canvas.pack()

		self.binds()

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
		self.color_button.config(image=color_icon)
		self.color_button.image = color_icon
		self.color_button.pack(side=tk.LEFT)
		self.add_tooltip(self.color_button, 'Цвет кисти')

		save_icon = tk.PhotoImage(file='images/save.png')
		save_button = tk.Button(self.control_frame, image=save_icon, command=lambda: self.save_image(None))
		save_button.image = save_icon
		save_button.pack(side=tk.LEFT)
		self.add_tooltip(save_button, 'Сохранить')

		brush_icon = tk.PhotoImage(file='images/brush.png')
		self.brush_button.config(image=brush_icon, relief='sunken')
		self.brush_button.image = brush_icon
		self.brush_button.pack(side=tk.LEFT)

		# Brush sizes menu
		brush_menu = tk.Menu(self.root, tearoff=0)
		brush_sizes = ['1', '2', '5', '10']
		self.selected_brush_size.set(brush_sizes[0])
		for size in brush_sizes:
			brush_menu.add_radiobutton(label=size, variable=self.selected_brush_size, command=self.brush)
		self.brush_button.bind('<Button-1>', lambda event: brush_menu.post(event.x_root, event.y_root))
		self.add_tooltip(self.brush_button, 'Выбор размера кисти')

		rubber_icon = tk.PhotoImage(file='images/rubber.png')
		self.rubber_button.config(image=rubber_icon, state='disabled')
		self.rubber_button.image = rubber_icon
		self.rubber_button.pack(side=tk.LEFT)
		self.add_tooltip(self.rubber_button, 'Ластик')

		resize_icon = tk.PhotoImage(file='images/resize.png')
		resize_button = tk.Button(self.control_frame, image=resize_icon, command=self.choose_size)
		resize_button.image = resize_icon
		resize_button.pack(side=tk.LEFT)
		self.add_tooltip(resize_button, 'Размер холста')

		text_icon = tk.PhotoImage(file='images/text.png')
		self.text_button.config(image=text_icon)
		self.text_button.image = text_icon
		self.text_button.pack(side=tk.LEFT)
		self.add_tooltip(self.text_button, 'Текст')

		background_icon = tk.PhotoImage(file='images/background.png')
		background_button = tk.Button(self.control_frame, image=background_icon, command=self.background)
		background_button.image = background_icon
		background_button.pack(side=tk.LEFT)
		self.add_tooltip(background_button, 'Фон')

		self.label.pack()
		self.label.place(relx=0.98, rely=0.2, anchor='ne', width=20, height=20)
		self.add_tooltip(self.label, 'Текущий цвет')

	def binds(self):
		# Binds
		self.canvas.bind('<B1-Motion>', self.paint)
		self.canvas.bind('<ButtonRelease-1>', self.reset)
		self.canvas.bind('<Button-3>', self.pipette)
		self.root.bind('<Control-s>', self.save_image)
		self.root.bind('<Control-c>', self.choose_color)

	@staticmethod
	def add_tooltip(widget, text):
		"""
		    This method creates a `Toplevel` window that appears near the widget when
		    the mouse cursor enters the widget's area, displaying the specified tooltip text.
		    The tooltip window closes automatically when the mouse cursor leaves the widget area.

		    Args:
		        widget (tk.Widget): The widget to which the tooltip will be attached.
		        text (str): The text to display within the tooltip window.

		    Inside the method:
		        - `show_tooltip(event)`: A function to create and display the tooltip near the widget.
		        - `hide_tooltip(event)`: A function to destroy the tooltip when the mouse leaves the widget area.
		"""
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
			label = tk.Label(tooltip, text=text, background='white', relief='solid', borderwidth=1, padx=5, pady=3)
			label.pack()

		def hide_tooltip(event):
			nonlocal tooltip
			if isinstance(tooltip, tk.Toplevel):
				tooltip.destroy()
				tooltip = None
		widget.bind('<Enter>', show_tooltip)
		widget.bind('<Leave>', hide_tooltip)

	def paint(self, event):
		"""
			Draws a line on the canvas and image from the last known mouse position to
			the current mouse position. This function is bound to mouse movement events.

			Args:
				event (tk.Event): The event object containing the current mouse position.
		"""
		self.rubber_button.config(state='normal')
		if self.mode == 'draw':
			self.canvas.config(cursor='@cursor.cur')
		else:
			self.canvas.config(cursor='@eraser.cur')
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
		self.label.config(bg=self.pen_color)

	def brush(self):
		"""
		    This method sets the app's drawing mode, enabling the brush tool
		    with the color stored in `self.last_color`. It updates the canvas cursor
		    to indicate active brush tool and visually resets other tools' states.
		"""
		self.color_button.config(state='normal')
		self.pen_color = self.last_color
		self.canvas.config(cursor='@cursor.cur')
		self.mode = 'draw'
		self.rubber_button.config(relief='raised')

	def rubber(self):
		"""
			Activates the rubber tool by setting the pen color to white (background color)
			and storing the last used pen color in case the user switches back to brush.
		"""

		self.last_color = self.pen_color
		self.pen_color = self.bg_colour
		self.canvas.config(cursor='@eraser.cur')
		self.mode = 'rubber'
		self.brush_button.config(relief='raised')
		self.rubber_button.config(relief='sunken')
		self.color_button.config(state='disabled')

	def pipette(self, event):
		"""
		   This method captures the color of a pixel located at the given coordinates (`event.x`, `event.y`)
		   on the canvas image and sets it as active drawing color (`self.pen_color`).
		   Additionally, it updates the cursor to indicate the pipette tool and adjusts the
		   button states to reflect the selected tool.
		"""
		rgb = self.image.getpixel((event.x, event.y))
		self.pen_color = '#{:02x}{:02x}{:02x}'.format(*rgb)
		self.canvas.config(cursor='@pipette.cur')
		self.mode = 'draw'
		self.brush_button.config(relief='sunken')
		self.rubber_button.config(relief='raised')

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
		self.canvas.delete('all')
		self.canvas.config(background='white')
		self.image = Image.new('RGB', (self.width, self.height), 'white')
		self.draw = ImageDraw.Draw(self.image)
		self.bg_colour = 'white'
		self.brush()

	def choose_color(self, event):
		"""
			Opens a color chooser dialog to let the user pick a new color for the pen.
			Updates the pen color with the selected color.
		"""
		self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
		self.last_color = self.pen_color

	def choose_size(self):
		"""
			Asks the user to set custom sizes of plot and creates a new canvas and image with the specified size.
		"""
		self.width = tk.simpledialog.askinteger('','Ширина', parent=self.root)
		self.height = tk.simpledialog.askinteger('' ,'Высота', parent=self.root)
		if self.width is not None and self.height is not None:
			self.image = self.image = Image.new('RGB', (self.width, self.height), 'white')
			self.draw = ImageDraw.Draw(self.image)
			self.canvas.destroy()
			self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white')
			self.canvas.pack()
			self.binds()

	def background(self):
		"""
		    Opens a color chooser dialog to set a new background color for the canvas and image.

		    Attributes updated:
		        - `self.bg_colour`: Stores the selected background color in hex format.
		        - `self.image`: Recreates the image with the new background color.
		        - `self.draw`: Updates the drawing object to use the new image.
		        - `self.canvas`: Configures the canvas background and updates its image.

		    """
		self.bg_colour = colorchooser.askcolor(color=self.pen_color)[1]
		if self.bg_colour:
			bg_rgb = Image.new("RGB", (1, 1), self.bg_colour).getpixel((0, 0))
			self.image = Image.new("RGBA", self.image.size, (*bg_rgb, 255))
			self.draw = ImageDraw.Draw(self.image)
			self.canvas.config(background=self.bg_colour)
			self.tk_image = ImageTk.PhotoImage(self.image.convert("RGB"))
			self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

	def add_text(self):
		"""
		    Asks the user to enter text and its size, then places the text on the canvas at a specified location.

		    Attributes updated:
		        - `self.image`: Updates with the composited text layer to display on the canvas.
		        - `self.tk_image`: Contains the updated image for display on the canvas.
		        - `self.canvas`: Displays the modified image with the newly added text.

		    """
		text_str = simpledialog.askstring('Введите текст', '', parent=self.root)
		text_size = simpledialog.askinteger('Размер текста', '', parent=self.root)
		if text_str and text_size:
			font = ImageFont.truetype('arial.ttf', text_size)

			def on_click(event):
				text_layer = Image.new("RGBA", self.image.size, (255, 255, 255, 0))
				text_img = ImageDraw.Draw(text_layer)
				text_img.text((event.x, event.y), text_str, fill=self.pen_color, font=font)
				self.image = Image.alpha_composite(self.image, text_layer)
				self.tk_image = ImageTk.PhotoImage(self.image.convert("RGB"))
				self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
				self.canvas.unbind("<Button-1>")
			self.canvas.bind("<Button-1>", on_click)

	def save_image(self, event):
		"""
		Opens a file dialog to save the current drawing as a PNG file. If a file
		path is chosen, the image is saved, and a success message is displayed.
		"""
		file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
		if file_path:
			if not file_path.endswith('.png'):
				file_path += '.png'
			self.image.save(file_path)
			messagebox.showinfo('Информация', 'Изображение успешно сохранено!')


def main():
	"""
	Main function to initialize and run the drawing application.
	"""
	root = tk.Tk()
	app = DrawingApp(root)
	root.mainloop()


if __name__ == '__main__':
	main()
