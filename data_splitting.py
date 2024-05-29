import os
import random
import shutil

# Define paths
dataset_path = 'bilateral_filtering/'
train_path = 'bilateral_filtering/train'
val_path = 'bilateral_filtering/validation'
test_path = 'bilateral_filtering/test'

# Get list of fruit classes
disease_classes = [disease_class for disease_class in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, disease_class))]
print(disease_classes)

# Create train, validation, and test folders
os.makedirs(train_path, exist_ok=True)
os.makedirs(val_path, exist_ok=True)
os.makedirs(test_path, exist_ok=True)

# Define split percentages
train_split = 0.8  # 80% for training
val_split = 0.1    # 10% for validation
test_split = 0.1   # 10% for testing

def rename_images(dataset_path):
    """
    Renames images in each class folder of the dataset path according to the format <class_name>_1, <class_name>_2, ...
    
    Parameters:
    - dataset_path (str): Path to the dataset directory containing class folders.
    """
    for disease_class in disease_classes:
        class_path = os.path.join(dataset_path, disease_class)
        if os.path.isdir(class_path):
            images = os.listdir(class_path)
            for i, image in enumerate(images, start=1):
                image_ext = os.path.splitext(image)[1]
                new_image_name = f"{disease_class}_{i:03d}{image_ext}"
                old_image_path = os.path.join(class_path, image)
                new_image_path = os.path.join(class_path, new_image_name)
                os.rename(old_image_path, new_image_path)

# Rename images before splitting
rename_images(dataset_path)

# Create train, validation, and test sets for each fruit class
for disease_class in disease_classes:
    disease_class_path = os.path.join(dataset_path, disease_class)
    disease_images = os.listdir(disease_class_path)
    random.shuffle(disease_images)
    
    print("\n")
    print("Disease Class: " + str(disease_class))
    # Calculate split sizes
    num_images = len(disease_images)
    print("Number of images: " + str(num_images))
    train_size = int(train_split * num_images)
    print("Training images: " + str(train_size))
    val_size = int(val_split * num_images)
    print("Validation images: " + str(val_size))
    test_size = num_images - train_size - val_size
    print("Testing images: " + str(test_size))

    # Create folders for each fruit class in train, validation, and test sets
    train_disease_path = os.path.join(train_path, disease_class)
    print(train_disease_path)
    val_disease_path = os.path.join(val_path, disease_class)
    print(val_disease_path)
    test_disease_path = os.path.join(test_path, disease_class)
    print(test_disease_path)
    os.makedirs(train_disease_path, exist_ok=True)
    os.makedirs(val_disease_path, exist_ok=True)
    os.makedirs(test_disease_path, exist_ok=True)

    # Move images to respective folders based on splits
    for i, img in enumerate(disease_images):
        img_path = os.path.join(disease_class_path, img)
        if i < train_size:
            shutil.copy(img_path, os.path.join(train_disease_path, img))
        elif i < train_size + val_size:
            shutil.copy(img_path, os.path.join(val_disease_path, img))
        else:
            shutil.copy(img_path, os.path.join(test_disease_path, img))

print("Train, validation, and test sets created successfully.")
