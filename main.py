from app.gui import start_application
from app.utils.file_utils import download_model_from_drive
import os


def download_model():
    drive_url = 'https://drive.google.com/uc?id=1E8Qk5bfdl_eI02y0TvSVKMQht2pao7ka'
    model_path = 'best-yolov9.pt'
    if not os.path.exists(model_path):
        download_model_from_drive(drive_url, model_path)

if __name__ == "__main__":
    download_model()
    start_application()
