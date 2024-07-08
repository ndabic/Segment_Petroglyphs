from ultralytics import YOLO


# Load a model
model = YOLO("yolov9e-seg.pt")  # load a pretrained model (recommended for training)

# Use the model
model.train(data="datav9.yaml", epochs=1000, batch =-1, device = 1)  # train the model

path = model.export(format="onnx")  # export the model to ONNX format