from logging import raiseExceptions
import cv2
import torch
from PIL import Image
import os
from termcolor import colored
clean_path = r"F:/furniture_dataset"

yolo_folder_path = "F:/furniture_detection/furniture_detection"
yolo_weigth_path = "F:/furniture_detection/furniture_detection/runs/weights/yolov5s_coco.pt"

model_confidence = 0.7

def crop_furniture(image, yolo_folder_path, yolo_weigth_path, model_confidence):
    def get_yolov5():
        model = torch.hub.load(yolo_folder_path, 'custom', path=yolo_weigth_path, source='local')
        model.conf = model_confidence
        return model
    
    final_model = get_yolov5()
    results = final_model(image, size=640)
    crops = results.display(pprint=False, show=False, save=False, crop=True, render=False, labels=False, 
                        save_dir=False)

    
    num_muzzle = len(crops)
    return num_muzzle

path_dirs = list(os.walk(clean_path))[1:]

for dirs in path_dirs:
    dir = dirs[0]
    files = dirs[2]
    total_detected = 0
    for name in files:
        source = os.path.join(clean_path, os.path.basename(dir), name)
        image = cv2.imread(source)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        image=Image.fromarray(image)
        num_detected = crop_furniture(image, yolo_folder_path, yolo_weigth_path, model_confidence)
        total_detected += num_detected
    if total_detected >= 4:
        print (colored("furniture(s) found in this folder", "green"))
        print (colored(f" {dir}: total furnitures {total_detected} ","green"))
    else:
        print(colored(f" {dir}: not detected ","red"))
