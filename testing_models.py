import cv2
import numpy as np
import os
import sys

cap = cv2.VideoCapture(
    r"C:\Users\noah\Downloads\2160test.mp4")
cap.set(cv2.CAP_PROP_POS_MSEC, 3000)
ret, frame = cap.read()
H, W, _ = frame.shape
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_fps = int(cap.get(cv2.CAP_PROP_FPS))
print(frame_width, frame_height, frame_fps)

threshold = 0.2


def absolute_paths(specifiedpath):
    return os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), specifiedpath)


def replace_non_white_with_black(image):
    # Define the white color range
    lower_bound = np.array([217, 217, 217])  # 240 remember
    upper_bound = np.array([255, 255, 255])

    # Create a mask where pixels are within the defined range
    mask = np.all((image >= lower_bound) & (image <= upper_bound), axis=-1)

    # Replace non-white pixels with black
    image[~mask] = [0, 0, 0]

    return image


amount_frames_to_skip = 25

which_game = 'Fortnite'
detection_already_found = False
templates = []
specified_res_dir = absolute_paths(rf"template_matching_resolutions/{str(frame_height)}p")  # old_images
for filename in os.listdir(specified_res_dir):
    if which_game.replace(" ", "") in filename:
        templates.append((filename, cv2.imread(specified_res_dir + rf"/{filename}", cv2.IMREAD_COLOR)))
while ret:
    current_timestamp = cap.get(cv2.CAP_PROP_POS_MSEC)
    print(f"Time: {current_timestamp / 60000} minutes")
    for template_name, template in templates:

        if detection_already_found:
            detection_already_found = False
            break
        tH, tW, _ = template.shape

        start_y = (H // 2) + int((200 * H) / 1440)
        end_y = start_y + (H // 4) - int((100 * H) / 1440)
        start_x = W // 3
        end_x = start_x + (W // 5)
        cropped_frame = frame[start_y:end_y, start_x:end_x]
        frame_mask = replace_non_white_with_black(cropped_frame)

        res = cv2.matchTemplate(frame_mask, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):  # Switch columns and rows
            top_left = (pt[0] + start_x, pt[1] + start_y)
            bottom_right = (top_left[0] + tW, top_left[1] + tH)
            cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 4)
            cv2.putText(frame, template_name, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3,
                        (0, 255, 0), 3, cv2.LINE_AA)
            print("found detection here ", template_name)
            # cv2.imwrite("temp1.png", template)
            # cv2.imwrite("edited_frame.png", frame_mask)
            out.write(frame)
            detection_already_found = True
            break

    for _ in range(1, amount_frames_to_skip):
        ret, frame = cap.read()
        if not ret:
            break

cap.release()
out.release()
cv2.destroyAllWindows()
