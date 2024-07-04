import tkinter as tk
from app.views.main_view import MainView
from app.controllers.main_controller import MainController
from app.models.yolo_model import YoloModel

def start_application():
    root = tk.Tk()
    model = YoloModel("best-yolov9.pt")
    view = MainView(master=root)
    controller = MainController(view, model)
    root.mainloop()
