import threading
from ultralytics import YOLO

class YoloModel:
    def __init__(self, model_path):
        self.segmente = YOLO(model_path)

        self.image_paths = []

        self.output_folder_SVG = "SVG Files"
        self.output_folder_JPG = "JPG Files"

        self.current_index = 0
        self.current_results = None
        self.current_img_str = None
        self.current_img = None
        self.current_img_draw = None
        self.current_svg_content = None
        self.current_img_pil_segmented = None

        self.masks = None
        self.mask_color = (255, 0, 0)

        self.transparency = 100
        self.transparency_svg = self.transparency/255
        self.mask_fill = (255, 0, 0, self.transparency)

        self.complementary_color = (0, 255, 255, self.transparency)

        self.all_processing = False

        self.mask_adding = False
        self.hole_adding = False
        self.selected_mask_index = None

        self.new_mask_points = []
        self.new_hole_points = []

        self.processing_event = threading.Event()
        

    def set_image_paths(self, paths):
        self.image_paths = paths
        self.current_index = 0

    def set_mask_color(self, color):
        self.mask_color = color 
        complementary_color = tuple(255 - component for component in color)
        self.mask_fill = color + (self.transparency,) 
        self.complementary_color = complementary_color + (self.transparency,) 

    def set_transparency(self, transparency):
        self.transparency = transparency
        self.transparency_svg = self.transparency/255
        self.set_mask_color(self.mask_color)

    def set_all_processing(self, all_processing):
        self.all_processing = all_processing

    def set_mask_adding(self, mask_adding):
        self.mask_adding = mask_adding

    def set_hole_adding(self, hole_adding):
        self.hole_adding = hole_adding


