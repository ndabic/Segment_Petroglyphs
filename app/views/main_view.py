import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Petroglyph Segmentation Application")
        self.master.geometry("1536x1024")
        self.display_size = 640

        self.photo = None
        # Configure styles

        # Change the background color of the main window
        self.master.config(bg="#1b384a")

        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), foreground='#1a842e', background='seagreen')
        self.style.map('TButton', background=[('active', 'teal')])
        self.style.configure('TLabel', font=('Helvetica', 12, 'bold'), foreground='#1a842e', background='#1b384a')
        self.style.configure('TScale', background='#1b384a', troughcolor='darkgray', foreground='black', font=('Helvetica', 12, 'bold'))
        self.style.configure('TCheckbutton', background='#1b384a', foreground='white', font=('Helvetica', 12, 'bold'))


        self.create_widgets()
        self.pack()

    def create_widgets(self):

        # Create a frame for the folder selection button
        self.folder_button_frame = tk.Frame(self.master, bg="#1b384a")
        self.folder_button_frame.pack(pady=10)

        # Create a button to load images
        self.load_button = ttk.Button(self.folder_button_frame, text="Load Images")
        self.load_button.pack(pady=10)

        # Create a frame for the color selection button and segmentation display settings
        self.display_frame = tk.Frame(self.master, bg="#1b384a")
        self.display_frame.pack(pady=10)

        # Create a to choose color
        self.color_button = ttk.Button(self.display_frame, text="Choose Color")
        self.color_button.pack(side=tk.LEFT, padx=10)
        
        # Create a scale for transparency of masks
        self.transparency_scale = ttk.Scale(self.display_frame, from_=0, to=255, value=100, orient=tk.HORIZONTAL, style='TScale')
        self.transparency_scale.pack(side=tk.LEFT, padx=10)
        
        # Create a button to update display parameters
        self.button_update_parameters = ttk.Button(self.display_frame, text="Update display parameters")
        self.button_update_parameters.pack(side=tk.LEFT, padx=10)
        
        # Create a frame for other action buttons
        self.action_button_frame = tk.Frame(self.master, bg="#1b384a")
        self.action_button_frame.pack(pady=20)

        # Create a checkbox
        self.all_var = tk.IntVar()
        self.all_checkbox = ttk.Checkbutton(self.action_button_frame, text="All", variable=self.all_var)
        self.all_checkbox.pack(side=tk.LEFT, padx=10)

        # Create a button to export SVG file for the current image
        self.button_create_svg = ttk.Button(self.action_button_frame, text="Export SVG")
        self.button_create_svg.pack(side=tk.LEFT, padx=10)

        # Create a button to export JPG file for the current image
        self.button_create_jpg = ttk.Button(self.action_button_frame, text="Export JPG")
        self.button_create_jpg.pack(side=tk.LEFT, padx=10)

        # Create a button to export both SVG and JPG files for the current image
        self.button_create_both = ttk.Button(self.action_button_frame, text="Export SVG and JPG")
        self.button_create_both.pack(side=tk.LEFT, padx=10)

        self.delete_button = ttk.Button(self.action_button_frame, text="Delete Selected Mask")
        self.delete_button.pack(side=tk.LEFT, padx=10)
        self.delete_button.pack_forget()  # Hide the button initially

        # Create a frame for the text
        self.text_frame = tk.Frame(self.master, bg="#1b384a")
        self.text_frame.pack(pady=20)

        # Create a label to display image processing status
        self.label_text = ttk.Label(self.text_frame, text="No images being processed")
        self.label_text.pack(pady=10)

        # Create a frame for images
        self.image_frame = tk.Frame(self.master, bg="#1b384a")
        self.image_frame.pack(pady=20)

        # Create a label to display the original image
        self.label_image = ttk.Label(self.image_frame)
        self.label_image.pack(side=tk.LEFT, padx=10)

        # Create a label to display the segmented image
        self.label_image_segmented = ttk.Label(self.image_frame)
        self.label_image_segmented.pack(side=tk.LEFT, padx=10)

        # Create a frame for images
        self.mask_frame = tk.Frame(self.image_frame, bg="#1b384a")
        self.mask_frame.pack(pady=20)

        # Create a checkbox
        self.add_mask_var = tk.IntVar()
        self.add_mask_checkbox = ttk.Checkbutton(self.mask_frame, text="Add Mask", variable=self.add_mask_var)
        self.add_mask_checkbox.pack(pady=10)
        self.add_mask_checkbox.pack_forget() # Hide the checkbox initially

        # Create a button to complete the polygon
        self.complete_mask_button = ttk.Button(self.mask_frame, text="Complete Mask")
        self.complete_mask_button.pack(pady=10)
        self.complete_mask_button.pack_forget()  # Hide the button initially

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.text_frame, mode='indeterminate')
    
    def update_image(self, current_draw):
        # Convert image to Tkinter format
        img_tk = ImageTk.PhotoImage(current_draw)

        # Display the image in the label
        self.label_image_segmented.config(image=img_tk)
        self.label_image_segmented.image = img_tk


