import os
import cv2
import base64
import threading
from PIL import Image, ImageTk, ImageDraw
import torch
import tkinter as tk
from tkinter import colorchooser, filedialog
from app.utils.image_utils import create_svg_content, point_in_polygon, merge_polygons, mask2polygon
from shapely.geometry import Polygon

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
        self.view.delete_button.config(command=self.delete_selected_mask)
        self.view.all_checkbox.config(command=self.toggle_all)
        self.view.add_mask_checkbox.config(command=self.toggle_add_mask)
        self.view.complete_mask_button.config(command=self.OnClick_Complete)
        self.view.label_image_segmented.bind("<Button-1>", self.OnClick_Mask)
        

    def OnClick_Mask(self, event):
        x, y = event.x, event.y
        
        height, width, _ = self.model.current_img.shape

        # Adjust the coordinates according to the scale of the image
        x_scaled = x * width / self.view.display_size
        y_scaled = y * height / self.view.display_size

        if self.model.mask_adding:
            self.model.new_mask_points.append([x_scaled, y_scaled])
            # Draw point on the image
            draw = ImageDraw.Draw(self.model.current_img_draw)
            draw.ellipse((x-3, y-3, x+3, y+3), fill=self.model.mask_fill, outline=self.model.mask_fill)
            
            self.view.update_image(self.model.current_img_draw)

        else: 
            self.model.selected_mask_index = self.get_mask_at_position(x_scaled, y_scaled)
            if self.model.selected_mask_index is not None:
                self.view.delete_button.pack(side=tk.LEFT, padx=10) 
                self.display_svg_in_label()

    def OnClick_Complete(self):
        if len(self.model.new_mask_points) > 2:

            points = [(int(point[0]), int(point[1])) for point in self.model.new_mask_points]
            self.model.masks.append(Polygon(points))

            self.model.masks = merge_polygons(self.model.masks)

            # Create SVG and display it
            image_path = self.model.image_paths[self.model.current_index]
            masks = self.model.masks
            img_str = self.model.current_img_str
            transparency_svg = self.model.transparency_svg
            current_img = self.model.current_img
            mask_color = self.model.mask_color
            self.model.current_svg_content = create_svg_content(masks, img_str, transparency_svg, current_img, mask_color, image_path)   
            self.display_svg_in_label()
            
            self.model.new_mask_points.clear()  # Clear points after drawing 

    def get_mask_at_position(self, x, y):
        # Check if the coordinates (x, y) are inside one of the masks
        if self.model.current_results[0].masks != None:
            for i, mask in enumerate(self.model.masks):
                if point_in_polygon(x, y, mask):
                    return i
        return None

    def delete_selected_mask(self):
        # Delete selected mask
        if self.model.selected_mask_index is not None:
            del self.model.masks[self.model.selected_mask_index]

            self.model.selected_mask_index = None
            
            # Create SVG and display it
            image_path = self.model.image_paths[self.model.current_index]
            masks = self.model.masks
            img_str = self.model.current_img_str
            transparency_svg = self.model.transparency_svg
            current_img = self.model.current_img
            mask_color = self.model.mask_color
            self.model.current_svg_content = create_svg_content(masks, img_str, transparency_svg, current_img, mask_color, image_path)     
            self.display_svg_in_label()

            self.view.delete_button.pack_forget()  # Hide the button after deletion

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose a color")
        if color[0] and color[1]:
            self.model.set_mask_color(color[0])

    def update_transparency(self, val):
        transparency = int(float(val))
        self.model.set_transparency(int(transparency))

    def toggle_all(self):
        self.model.set_all_processing(self.view.all_var.get())
    
    def toggle_add_mask(self):
        self.model.set_mask_adding(self.view.add_mask_var.get())
        if self.model.mask_adding: 
            self.view.complete_mask_button.pack(pady=10)
        else:
            self.view.complete_mask_button.pack_forget()

    def select_image_folder(self):
        image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.png;*.bmp;*.jpeg;*.tif;*.tiff;*.pfm")])
        if image_paths:
            self.model.set_image_paths(image_paths)
            self.display_segmentation()

    def on_click_display_update(self):
        # Create SVG and display it
        image_path = self.model.image_paths[self.model.current_index]
        masks = self.model.masks
        img_str = self.model.current_img_str
        transparency_svg = self.model.transparency_svg
        current_img = self.model.current_img
        mask_color = self.model.mask_color
        self.model.current_svg_content = create_svg_content(masks, img_str, transparency_svg, current_img, mask_color, image_path)     
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
            self.end()

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
                self.end()

    # Function to display segmentation of the current image
    def display_segmentation(self):   

        # Uncheck the Checkbutton before hiding it
        self.view.add_mask_var.set(0)
        self.toggle_add_mask()
        self.view.add_mask_checkbox.pack_forget()
        
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

                polygons = mask2polygon(results)
                masks = merge_polygons(polygons)

                img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img_rgb)
                img_pil = img_pil.resize((self.view.display_size, self.view.display_size), Image.Resampling.LANCZOS)

                # Convert image to Tkinter format
                img_tk = ImageTk.PhotoImage(img_pil)

                # Display the image in the label
                self.view.label_image.config(image=img_tk)
                self.view.label_image.image = img_tk

                self.view.label_text.config( text= "Image number " +  str(self.model.current_index + 1) + " of " + str(len(self.model.image_paths)))

                # Update model variables for SVG conversion
                self.model.masks = masks
                self.model.current_results = results
                self.model.current_img_str = img_str
                self.model.current_img = img_cv
                
                self.display_svg_in_label()

                # Create and display SVG content
                self.model.current_svg_content = create_svg_content(masks, img_str, self.model.transparency_svg, img_cv, self.model.mask_color, image_path)            

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
            self.end()

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

            for i, polygon  in enumerate(self.model.masks):
                points = [(int(point[0]), int(point[1])) for point in polygon.exterior.coords]
                outline_color = (0, 0, 255, 255) if i == self.model.selected_mask_index else self.model.mask_fill
                width = 4 if i == self.model.selected_mask_index else 2
                draw.polygon(points, outline=outline_color, fill=self.model.mask_fill, width=width)  

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
        img_pil = img_pil.resize((self.view.display_size, self.view.display_size), Image.Resampling.LANCZOS)
        
        self.model.current_img_draw = img_pil

        self.view.update_image(img_pil)

        self.view.add_mask_checkbox.pack(pady=10)

    def end(self):
        # Display completion message when all images are processed
        tk.messagebox.showinfo("Processing complete", "All images have been processed.")
        
        # Uncheck the Checkbutton before hiding it
        self.view.add_mask_var.set(0)
        self.toggle_add_mask()
        self.view.add_mask_checkbox.pack_forget()

        self.view.label_image.image = None  # Erase the displayed image
        self.view.label_image_segmented.image = None
        self.view.label_text.config( text= "No images being processed")