import os
from ultralytics import YOLO
import cv2

cap = cv2.VideoCapture(r'path\to\your\clip.mp4')  # path to a video for the model to watch through
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

model_path = os.path.join('.', 'runs', 'detect', 'train', 'weights', 'last.pt')  # relative path to YOLO model
model = YOLO(model_path)

threshold = 0.5

while ret:
    current_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
    print(f"Time: {current_timestamp}")
    results = model(frame)[0]

    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        print(f"Confidence/score: {score}")
        if score > threshold:
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
    out.write(frame)
    ret, frame = cap.read()
cap.release()
out.release()
cv2.destroyAllWindows()
