from ultralytics import YOLO

model = YOLO("yolov8n.yaml")  # path to your YAML config file
results = model.train(data=r"path\to\your\dataset.yolov8\data.yaml", epochs=50)  # path to your dataset YAML file
