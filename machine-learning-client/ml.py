from ultralytics import YOLO
import cv2
from PIL import Image
import os
import glob
from tqdm import tqdm
import kagglehub

path = kagglehub.dataset_download("shreyapmaher/fruits-dataset-images")
print("Path to dataset files:", path)

model = YOLO("yolov8m.pt")
# model.info()

# Train the model
# results = model.train(data="coco8.yaml", epochs=100, imgsz=640, device="mps", weights="yolov8l.pt")

image_paths = glob.glob(path + "/images/*/*.jpg")
print("Number of images found:", len(image_paths))

for image_path in (pbar := tqdm(image_paths[:100])):
    fruit_cat = image_path.split('/')[-2]
    image_num = image_path.split('/')[-1]
    pbar.set_description(f'Processing {fruit_cat}')
    image = Image.open(image_path)
    
    save_path = 'labeled_images/' + fruit_cat + '/' + image_num
    os.makedirs('/'.join(save_path.split('/')[:-1]), exist_ok=True)
    
    # convert image to array
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # apply object detection
    results = model(image, verbose=False)
    
    # annotate image with bounding boxes
    annotated_image = results[0].plot()

    # convert array back to image
    img = Image.fromarray(annotated_image)
    img.save(save_path)