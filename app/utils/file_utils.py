import gdown

def download_model_from_drive(drive_url, output_path):
    gdown.download(drive_url, output_path, quiet=False)