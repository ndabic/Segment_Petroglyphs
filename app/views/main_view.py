import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
import webbrowser

class MainView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.master = master
        self.master.title("PetroVision")

        # Récupérer la résolution de l'écran
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        
        # Définir la géométrie de la fenêtre
        self.master.geometry(f"{screen_width}x{screen_height}")
        
        self.display_size = int(screen_height*0.625)
        self.pady = int(screen_height*0.004)

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
        self.folder_button_frame.pack(pady=2*self.pady)

        # Create a button to display credits
        self.credits_button = ttk.Button(self.master, text="Credits", command=self.show_credits)
        self.credits_button.place(x=2*self.pady, y=2*self.pady)  # Place the button at coordinates (0, 0)

        # Create a button to load images
        self.load_button = ttk.Button(self.folder_button_frame, text="Load Images")
        self.load_button.pack(pady=self.pady)

        # Create a frame for the color selection button and segmentation display settings
        self.display_frame = tk.Frame(self.master, bg="#1b384a")
        self.display_frame.pack(pady=self.pady)

        # Create a to choose color
        self.color_button = ttk.Button(self.display_frame, text="Choose Color")
        self.color_button.pack(side=tk.LEFT, padx=self.pady)
        
        # Create a scale for transparency of masks
        self.transparency_scale = ttk.Scale(self.display_frame, from_=0, to=255, value=100, orient=tk.HORIZONTAL, style='TScale')
        self.transparency_scale.pack(side=tk.LEFT, padx=self.pady)
        
        # Create a button to update display parameters
        self.button_update_parameters = ttk.Button(self.display_frame, text="Update display parameters")
        self.button_update_parameters.pack(side=tk.LEFT, padx=self.pady)
        
        # Create a frame for other action buttons
        self.action_button_frame = tk.Frame(self.master, bg="#1b384a")
        self.action_button_frame.pack(pady=4*self.pady)

        # Create a checkbox
        self.all_var = tk.IntVar()
        self.all_checkbox = ttk.Checkbutton(self.action_button_frame, text="For all", variable=self.all_var)
        self.all_checkbox.pack(side=tk.LEFT, padx=self.pady)

        # Create a button to export SVG file for the current image
        self.button_create_svg = ttk.Button(self.action_button_frame, text="Export SVG")
        self.button_create_svg.pack(side=tk.LEFT, padx=self.pady)

        # Create a button to export JPG file for the current image
        self.button_create_jpg = ttk.Button(self.action_button_frame, text="Export JPG")
        self.button_create_jpg.pack(side=tk.LEFT, padx=self.pady)

        # Create a button to export both SVG and JPG files for the current image
        self.button_create_both = ttk.Button(self.action_button_frame, text="Export SVG and JPG")
        self.button_create_both.pack(side=tk.LEFT, padx=self.pady)

        # Create a button to skip the current image and process the next
        self.button_skip = ttk.Button(self.action_button_frame, text="Skip")
        self.button_skip.pack(side=tk.LEFT, padx=self.pady)

        # Create a frame for the text
        self.text_frame = tk.Frame(self.master, bg="#1b384a")
        self.text_frame.pack(pady=4*self.pady)

        # Create a label to display image processing status
        self.label_text = ttk.Label(self.text_frame, text="No images being processed")
        self.label_text.pack(pady=self.pady)

        # Create a label to display image processing status
        self.label_text_number = ttk.Label(self.text_frame)
        self.label_text_number.pack(pady=self.pady)

        # Create a label to display instructions for splitting masks
        self.label_text_separating = ttk.Label(self.text_frame, foreground='#990000', text="Place two points to form a line and then click again on the Split Mask button")
        self.label_text_separating.pack(pady=self.pady)
        self.label_text_separating.pack_forget()

        # Create a frame for images
        self.image_frame = tk.Frame(self.master, bg="#1b384a")
        self.image_frame.pack(pady=4*self.pady)

        # Create a label to display the original image
        self.label_image = ttk.Label(self.image_frame)
        self.label_image.pack(side=tk.LEFT, padx=self.pady)

        # Create a label to display the segmented image
        self.label_image_segmented = ttk.Label(self.image_frame)
        self.label_image_segmented.pack(side=tk.LEFT, padx=self.pady)

        # Create a frame for mask editing
        self.mask_frame = tk.Frame(self.image_frame, bg="#1b384a")
        self.mask_frame.pack(pady=4*self.pady)

        # Create a button to delete the selected mask
        self.delete_button = ttk.Button(self.mask_frame, text="Delete Selected Mask")
        self.delete_button.pack(side="top", pady=self.pady, expand=True)
        self.delete_button.pack_forget()  # Hide the button initially

        # Create a checkbox to set the mask adding mode
        self.add_mask_var = tk.IntVar()
        self.add_mask_checkbox = ttk.Checkbutton(self.mask_frame, text="Add Mask", variable=self.add_mask_var)
        self.add_mask_checkbox.pack(side="top", pady=self.pady, expand=True)
        self.add_mask_checkbox.pack_forget() # Hide the checkbox initially

        # Create a button to complete the polygon
        self.complete_mask_button = ttk.Button(self.mask_frame, text="Complete Mask")
        self.complete_mask_button.pack(side="top", pady=self.pady, expand=True)
        self.complete_mask_button.pack_forget()  # Hide the button initially

        # Create a checkbox to set the hole adding mode
        self.add_hole_var = tk.IntVar()
        self.add_hole_checkbox = ttk.Checkbutton(self.mask_frame, text="Add Hole", variable=self.add_hole_var)
        self.add_hole_checkbox.pack(side="top", pady=self.pady, expand=True)
        self.add_hole_checkbox.pack_forget() # Hide the checkbox initially

        # Create a button to complete the polygon
        self.complete_hole_button = ttk.Button(self.mask_frame, text="Complete Hole")
        self.complete_hole_button.pack(side="top", pady=self.pady, expand=True)
        self.complete_hole_button.pack_forget()  # Hide the button initially

        # Create a button to complete the polygon
        self.separate_mask_button = ttk.Button(self.mask_frame, text="Split Mask")
        self.separate_mask_button.pack(side="top", pady=self.pady, expand=True)
        self.separate_mask_button.pack_forget()  # Hide the button initially

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.text_frame, mode='indeterminate')
    
    def update_image(self, current_draw):
        # Convert image to Tkinter format
        img_tk = ImageTk.PhotoImage(current_draw)

        # Display the image in the label
        self.label_image_segmented.config(image=img_tk)
        self.label_image_segmented.image = img_tk

    def show_credits(self):
        # Create a new window for the credits
        credits_window = tk.Toplevel(self.master)
        credits_window.title("Credits")
        
        # Set the size of the window
        credits_window.geometry("600x400")
        
        # Add a label for the credits
        credits_text = (
            "Tkinter Application\n"
            "Developed by Nikola Dabic\n"
            "Year: 2024\n"
            "\n"
            "Thanks to:\n"
            "- Jean-Denis Durou\n"
            "- Antoine Laurent\n"
            "- Fabien Castan\n"
            "- Jean Mélou\n"
            "- Ani Danielyan\n"
            "\n"
            "GitHub Repository: https://github.com/ndabic/Segment_Petroglyphs \n"
        )
        
        credits_label = ttk.Label(credits_window, text=credits_text, justify='left')
        credits_label.pack(padx=10, pady=10, expand=True)

        # Add a button to open the GitHub link
        github_button = ttk.Button(credits_window, text="Open GitHub Repository", command=self.open_github_link)
        github_button.pack(pady=10)

        # Add a button to close the credits window
        close_button = ttk.Button(credits_window, text="Close", command=credits_window.destroy)
        close_button.pack(pady=10)

    def open_github_link(self):
        webbrowser.open("https://github.com/ndabic/Segment_Petroglyphs")

