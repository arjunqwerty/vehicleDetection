import os
import cv2
import pandas as pd
import shutil

# Directory where the images are stored
image_dir = 'arch 7\\train\\images'

# Directory where the annotations are stored
annotation_dir = 'arch 7\\train\\labels'

# Directory to store the images with bounding boxes
output_dir = 'arch 7\\train\\working'
if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

# Iterate over each file in the annotation directory
for filename in os.listdir(annotation_dir):
    if filename.endswith('.txt'):  # this is an annotation file
        # Read the annotation file
        annotation_file = os.path.join(annotation_dir, filename)
        with open(annotation_file, 'r') as file:
            lines = file.readlines()

        # df = pd.read_csv(os.path.join(annotation_dir, filename), header=None, sep="\s+")
        # df.columns = ['class_name', 'xmin', 'ymin', 'xdistance', 'ydistance']
        # print(lines)
        lines = [line.split() for line in lines]
        df = pd.DataFrame(lines, columns=['class_name', 'xmin', 'ymin', 'xdistance', 'ydistance'])

        # Load the corresponding image
        img_filename = filename.replace('.txt', '.jpg')  # replace with your image file extension
        img = cv2.imread(os.path.join(image_dir, img_filename))

        # Convert the annotations from percentages to pixels and draw the bounding boxes on the image
        for index, row in df.iterrows():
            xmin = int((float(row['xmin']) - float(row['xdistance']) / 2) * img.shape[1])
            ymin = int((float(row['ymin']) - float(row['ydistance']) / 2) * img.shape[0])
            xmax = int((float(row['xmin']) + float(row['xdistance']) / 2) * img.shape[1])
            ymax = int((float(row['ymin']) + float(row['ydistance']) / 2) * img.shape[0])
            cropped_img = img[ymin:ymax, xmin:xmax]

        # Create a separate folder for each class and save the corresponding images in their respective folders
        class_dir = os.path.join(output_dir, row['class_name'])
        os.makedirs(class_dir, exist_ok=True)
        cv2.imwrite(os.path.join(class_dir, img_filename), cropped_img)
