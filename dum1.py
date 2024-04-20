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

# Function to display images with annotations side by side
def display_images_with_annotations(image_paths, annotation_paths, wait_time):
    images_with_annotations = []
    max_height = 0
    total_width = 0

    # Find maximum height and total width
    for i in range(3):
        image = cv2.imread(image_paths[i])
        max_height = max(max_height, image.shape[0])
        total_width += image.shape[1]

    # Resize images and annotations to have the same height
    for i in range(3):
        image = cv2.imread(image_paths[i])
        annotation_file = annotation_paths[i]
        image_height, image_width = image.shape[:2]
        annotations = parse_annotations(annotation_file, image_width, image_height)
        resized_image = cv2.resize(image, (int(image_width * max_height / image_height), max_height))
        draw_boxes(resized_image, annotations)
        images_with_annotations.append(resized_image)

    # Concatenate images horizontally
    combined_image = cv2.hconcat(images_with_annotations)

    cv2.imshow('Images with Annotations', combined_image)
    key = cv2.waitKey(wait_time)
    return key

# Main function
def main():
    images_folder = 'arch 7\\train\\images'
    annotations_folder = 'arch 7\\train\\labels'
    wait_time = 5000

    image_files = os.listdir(images_folder)
    # annotation_files = os.listdir(annotations_folder)

    # Sort image and annotation files to ensure consistency
    image_files.sort()

    # Get the first three image file names
    # # Iterate over the image file names and obtain their corresponding annotation file names
    # image_paths = [os.path.join(images_folder, image_name) for image_name in image_file_names]
    # annotation_paths = [os.path.join(annotations_folder, os.path.splitext(image_name)[0] + '.txt') for image_name in image_file_names]
    num_images = len(image_files)
    i = 0
    while i < num_images:
        image_file_names = image_files[i:i+3]
        image_paths = [os.path.join(images_folder, image_name) for image_name in image_file_names]
        annotation_paths = [os.path.join(annotations_folder, os.path.splitext(image_name)[0] + '.txt') for image_name in image_file_names]

        key = display_images_with_annotations(image_paths, annotation_paths, wait_time)
        
        # If 'p' is pressed, pause until any key is pressed again
        if key == ord('p'):
            cv2.waitKey(0)

        i += 3

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
