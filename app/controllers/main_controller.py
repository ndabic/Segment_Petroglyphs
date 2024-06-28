import os
import cv2
import base64
import threading
from PIL import Image, ImageTk, ImageDraw
import torch
import tkinter as tk
from tkinter import colorchooser, filedialog
from app.utils.image_utils import create_svg_content

class MainController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.configure_view()

    def configure_view(self):
        self.view.load_button.config(command=self.select_image_folder)
        self.view.color_button.config(command=self.choose_color)
        self.view.transparency_scale.config(command=self.update_transparency)
        self.view.button_update_parameters.config(command=self.on_click_display_update)
        self.view.button_create_svg.config(command=self.OnClick_SVG)
        self.view.button_create_jpg.config(command=self.OnClick_JPG)
        self.view.button_create_both.config(command=self.OnClick_Both)
        self.view.all_checkbox.config(command=self.toggle_all)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose a color")
        if color[0] and color[1]:
            self.model.set_mask_color(color[0])

    def update_transparency(self, val):
        self.model.set_transparency(int(val))

    def toggle_all(self):
        self.model.set_all_processing(self.view.all_var.get())

    def select_image_folder(self):
        image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.png;*.bmp;*.jpeg;*.tif;*.tiff;*.pfm")])
        if image_paths:
            self.model.set_image_paths(image_paths)
            self.display_segmentation()

    def on_click_display_update(self):
        # Create SVG and display it
        results = self.model.current_results
        img_str = self.model.current_img_str
        transparency_svg = self.model.transparency_svg
        current_img = self.model.current_img
        mask_color = self.model.mask_color
        self.model.current_svg_content = create_svg_content(results, img_str, transparency_svg, current_img, mask_color)     
        self.display_svg_in_label()

    def OnClick_SVG(self):
        if self.model.all_processing:
            self.process_all_images(self.create_svg)
        else:
            self.create_svg()

    def OnClick_JPG(self):
        if self.model.all_processing:
            self.process_all_images(lambda: self.create_jpg(True))
        else:
            self.create_jpg(True)

    def OnClick_Both(self):
        if self.model.all_processing:
            self.process_all_images(lambda: self.create_jpg(False) or self.create_svg())
        else:
            self.create_jpg(False)
            self.create_svg()

    # Function to create SVG file
    def create_svg(self):

        if not os.path.exists(self.model.output_folder_SVG):
            os.makedirs(self.model.output_folder_SVG)
        
        # Build SVG file path
        image_name = os.path.basename(self.model.image_paths[self.model.current_index]).split('.')[0]
        svg_file = os.path.join(self.model.output_folder_SVG, image_name + '.svg')
        
        # Save segmented image to disk in SVG format
        with open(svg_file, 'w') as f:
            f.write(self.model.current_svg_content)
        
        # Move to the next image
        self.model.current_index += 1
        
        # Display segmentation of the next image if it exists
        if self.model.current_index < len(self.model.image_paths):
            self.display_segmentation()
        else:
            # Display completion message when all images are processed
            tk.messagebox.showinfo("Processing complete", "All images have been processed.")
            self.view.label_image.image = None  # Effacer l'image affichée
            self.view.label_image_segmented.image = None
            self.view.label_text.config( text= "No images being processed")

    # Function to create JPG file
    def create_jpg(self, bool):

        if not os.path.exists(self.model.output_folder_JPG):
            os.makedirs(self.model.output_folder_JPG)

        # Build JPG file path
        image_name = os.path.basename(self.model.image_paths[self.model.current_index]).split('.')[0]
        jpg_file = os.path.join(self.model.output_folder_JPG, image_name + '.jpg')

        # Save segmented image to disk in JPG format
        self.model.current_img_pil_segmented.save(jpg_file)

        if bool:
            # Move to the next image
            self.model.current_index += 1
            
            # Display segmentation of the next image if it exists
            if self.model.current_index < len(self.model.image_paths):
                self.display_segmentation()
            else:
                # Display completion message when all images are processed
                tk.messagebox.showinfo("Processing complete", "All images have been processed.")
                self.view.label_image.image = None  # Effacer l'image affichée
                self.view.label_image_segmented.image = None
                self.view.label_text.config( text= "No images being processed")

    # Function to display segmentation of the current image
    def display_segmentation(self):    
        if self.model.current_index < len(self.model.image_paths):
            def run_segmentation():
                image_path = self.model.image_paths[self.model.current_index]
                img_cv = cv2.imread(image_path)

                # Convert the image to base64
                _, buffer = cv2.imencode('.jpg', img_cv)
                img_str = base64.b64encode(buffer).decode('utf-8')

                # Perform inference
                # Check if GPU is available
                if torch.cuda.is_available():
                    device = 'cuda:0'
                else:
                    device = 'cpu'

                results = self.model.segmente(image_path, retina_masks=True, device = device, iou = 0.2)

                img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_pil = img_pil.resize((640, 640), Image.Resampling.LANCZOS)

                # Convert the image to Tkinter format
                img_tk = ImageTk.PhotoImage(img_pil)

                # Display the image
                self.view.label_image.config(image=img_tk)
                self.view.label_image.image = img_tk
                self.view.label_text.config( text= "Image number " +  str(self.model.current_index + 1) + " of " + str(len(self.model.image_paths)))

                # Update model variables for SVG conversion
                self.model.current_results = results
                self.model.current_img_str = img_str
                self.model.current_img = img_cv
                
                self.display_svg_in_label()

                # Create and display SVG content
                self.model.current_svg_content = create_svg_content(results, img_str, self.model.transparency_svg, img_cv, self.model.mask_color)            

                # Hide the progress bar
                self.view.progress_bar.stop()
                self.view.progress_bar.pack_forget()
                self.view.master.config(cursor="")

                # Signal the end of processing for the current image
                self.model.processing_event.set()

            # Display the progress bar
            self.view.progress_bar.pack(pady=20)
            self.view.progress_bar.start()
            self.view.master.config(cursor="wait")

            # Reset the event before starting a new thread
            self.model.processing_event.clear()

            # Execute inference in a separate thread
            threading.Thread(target=run_segmentation).start()
        else:
            # Display completion message when all images are processed
            tk.messagebox.showinfo("Processing complete", "All images have been processed.")
            self.view.label_image.image = None  # Effacer l'image affichée
            self.view.label_image_segmented.image = None
            self.view.label_text.config( text= "No images being processed")

    def process_all_images(self, process_function):
        def process_next_image():
            while self.model.current_index < len(self.model.image_paths):
                process_function()
                self.view.master.update_idletasks()
                # Attendre la fin du traitement de l'image actuelle
                self.model.processing_event.wait()

        threading.Thread(target=process_next_image).start()

    # Function to display SVG in the label
    def display_svg_in_label(self):

        # Convert current image to RGB format
        img_rgb = cv2.cvtColor(self.model.current_img, cv2.COLOR_BGR2RGB)

        if self.model.current_results[0].masks != None:
            # Convert RGB image to PIL Image and add an alpha channel
            img_pil = Image.fromarray(img_rgb).convert("RGBA")
            
            # Create a new image for masks with transparency
            mask_img = Image.new("RGBA", img_pil.size, (255, 255, 255, 0))

            draw = ImageDraw.Draw(mask_img)

            for mask in self.model.current_results[0].masks.xy:
                points = [(int(point[0]), int(point[1])) for point in mask]
                draw.polygon(points, outline=self.model.mask_fill, fill=self.model.mask_fill)  

            # Combine base image with masks
            img_pil = Image.alpha_composite(img_pil, mask_img)

            # Create a white background
            background = Image.new("RGB", img_pil.size, (255, 255, 255))
            # Combine image with white background using alpha channel as mask
            img_pil = Image.alpha_composite(background.convert("RGBA"), img_pil).convert("RGB")
        else:
            # Convert RGB image to PIL Image
            img_pil = Image.fromarray(img_rgb)

        # Save current segmented PIL image
        self.model.current_img_pil_segmented = img_pil

        # Resize the image
        img_pil = img_pil.resize((640, 640), Image.Resampling.LANCZOS)
        
        # Convert image to Tkinter format
        img_tk = ImageTk.PhotoImage(img_pil)

        # Display the image in the label
        self.view.label_image_segmented.config(image=img_tk)
        self.view.label_image_segmented.image = img_tk