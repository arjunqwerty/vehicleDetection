import cv2
import os

# Function to parse annotations from text files
def parse_annotations(annotation_file, image_width, image_height):
    with open(annotation_file, 'r') as file:
        lines = file.readlines()
    
    annotations = []
    for line in lines:
        data = line.strip().split()
        if len(data) == 5:  # Assuming format: class x_min y_min x_distance y_distance
            class_name = data[0]
            x_center, y_center, x_distance, y_distance = map(float, data[1:])
            # Convert from percentage to pixels
            # image_width = 1000 # Specify your image width here
            # image_height = 1000 # Specify your image height here
            x_min = max(0, int((x_center - (x_distance / 2)) * image_width))
            y_min = max(0, int((y_center - (y_distance / 2)) * image_height))
            x_max = min(image_width, int((x_center + (x_distance / 2)) * image_width))
            y_max = min(image_height, int((y_center + (y_distance / 2)) * image_height))
            annotations.append((class_name, (x_min, y_min, x_max, y_max)))
    
    return annotations

# Function to draw bounding boxes on an image
def draw_boxes(image, annotations):
    for class_name, (x_min, y_min, x_max, y_max) in annotations:
        color = (0, 255, 0)  # Green color for bounding boxes
        cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color, 2)
        cv2.putText(image, class_name, (int(x_min), int(y_min) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Function to display image with annotations
def display_one_image_with_annotations(image_path, annotation_path):
    image = cv2.imread(image_path)
    image_height, image_width, _ = image.shape
    annotations = parse_annotations(annotation_path, image_width, image_height)
    # print(annotations)
    cv2.imshow('Image', image)
    draw_boxes(image, annotations)
    cv2.imshow('Image with Annotations', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def display_multi_images_with_annotations(image_paths, annotation_paths, n):
    images = []
    annotations = []
    for i in range(n):
        image = cv2.imread(image_paths[i])
        annotations.append(parse_annotations(annotation_paths[i]))
        images.append(image)

    # Combine images into a single window
    combined_image = cv2.vconcat(images)
    
    # Draw annotations on the combined image
    for i in range(0):
        draw_boxes(combined_image, annotations[i])

    cv2.imshow('Images with Annotations', combined_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Main function to iterate over images and annotations
def main():
    images_folder = 'arch 7\\train\\images'
    annotations_folder = 'arch 7\\train\\labels'

    # image_files = os.listdir(images_folder)
    # annotation_files = os.listdir(annotations_folder)
    image_files = ['Highway_0_2020-07-30_jpg.rf.7d947cc31b302b22a527ecd17d3af963.jpg', 'Highway_0_2020-07-30_jpg.rf.09e9d4467f17b2b870a5d1b94a38774a.jpg', 'Highway_0_2020-07-30_jpg.rf.f2b27ff74487ea9a91b9dff189180e8d.jpg']
    annotation_files = ['Highway_0_2020-07-30_jpg.rf.7d947cc31b302b22a527ecd17d3af963.txt', 'Highway_0_2020-07-30_jpg.rf.09e9d4467f17b2b870a5d1b94a38774a.txt', 'Highway_0_2020-07-30_jpg.rf.f2b27ff74487ea9a91b9dff189180e8d.txt']
    # image_file = "Highway_0_2020-07-30_jpg.rf.f2b27ff74487ea9a91b9dff189180e8d.jpg"
    # annotation_file = "Highway_0_2020-07-30_jpg.rf.f2b27ff74487ea9a91b9dff189180e8d.txt"
    # for image_file, annotation_file in zip(image_files,annotation_files):
    #     image_path = os.path.join(images_folder, image_file)
    #     annotation_path = os.path.join(annotations_folder, annotation_file)
    #     display_image_with_annotations(image_path, annotation_path)

    # for image_file in image_files:
    #     image_name, image_ext = os.path.splitext(image_file)
    #     annotation_file = image_name + '.txt'
    #     if annotation_file in annotation_files:
    #         image_path = os.path.join(images_folder, image_file)
    #         annotation_path = os.path.join(annotations_folder, annotation_file)
    #         display_image_with_annotations(image_path, annotation_path)

if __name__ == "__main__":
    main()
