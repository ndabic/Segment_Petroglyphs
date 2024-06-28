import tkinter as tk
from tkinter import ttk

class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Petroglyph Segmentation Application")
        self.master.geometry("1360x920")
        self.create_widgets()
        self.pack()

    def create_widgets(self):

        # Create a frame for the folder selection button
        self.folder_button_frame = tk.Frame(self)
        self.folder_button_frame.pack(pady=10)

        # Create a button to load images
        self.load_button = tk.Button(self.folder_button_frame, text="Load Images")
        self.load_button.pack(pady=10)

        # Create a frame for the color selection button and segmentation display settings
        self.display_frame = tk.Frame(self)
        self.display_frame.pack(pady=10)

        # Create a to choose color
        self.color_button = tk.Button(self.display_frame, text="Choose Color")
        self.color_button.pack(side=tk.LEFT, padx=10)
        
        # Create a scale for transparency of masks
        self.transparency_scale = tk.Scale(self.display_frame, from_=0, to=255, orient=tk.HORIZONTAL)
        self.transparency_scale.pack(side=tk.LEFT, padx=10)
        
        # Create a button to update display parameters
        self.button_update_parameters = tk.Button(self.display_frame, text="Update display parameters")
        self.button_update_parameters.pack(side=tk.LEFT, padx=10)
        
        # Create a frame for other action buttons
        self.action_button_frame = tk.Frame(self)
        self.action_button_frame.pack(pady=20)

        # Create a checkbox
        self.all_var = tk.IntVar()
        self.all_checkbox = tk.Checkbutton(self.action_button_frame, text="All", variable=self.all_var)
        self.all_checkbox.pack(side=tk.LEFT, padx=10)

        # Create a button to export SVG file for the current image
        self.button_create_svg = tk.Button(self.action_button_frame, text="Export SVG")
        self.button_create_svg.pack(side=tk.LEFT, padx=10)

        # Create a button to export JPG file for the current image
        self.button_create_jpg = tk.Button(self.action_button_frame, text="Export JPG")
        self.button_create_jpg.pack(side=tk.LEFT, padx=10)

        # Create a button to export both SVG and JPG files for the current image
        self.button_create_both = tk.Button(self.action_button_frame, text="Export SVG and JPG")
        self.button_create_both.pack(side=tk.LEFT, padx=10)

        # Create a frame for the text
        self.text_frame = tk.Frame(self)
        self.text_frame.pack(pady=20)

        # Create a label to display image processing status
        self.label_text = tk.Label(self.text_frame, text="No images being processed")
        self.label_text.pack(pady=10)

        # Create a frame for images
        self.image_frame = tk.Frame(self)
        self.image_frame.pack(pady=20)

        # Create a label to display the original image
        self.label_image = tk.Label(self.image_frame)
        self.label_image.pack(side=tk.LEFT, padx=10)

        # Create a label to display the segmented image
        self.label_image_segmented = tk.Label(self.image_frame)
        self.label_image_segmented.pack(side=tk.LEFT, padx=10)

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.text_frame, mode='indeterminate')


