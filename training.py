from ultralytics import YOLO

model = YOLO("yolov8n.yaml")
results = model.train(data=r"C:\Users\noah\Downloads\Valorant kill banner.v1i.yolov8\data.yaml", epochs=50)
