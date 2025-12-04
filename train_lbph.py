import os
import cv2
import numpy as np
import json

def augment_image(img):
    """Enhanced augmentation for better accuracy"""
    augmented = [img]
    
    # Horizontal flip
    augmented.append(cv2.flip(img, 1))
    
    # Brightness variations
    augmented.append(cv2.convertScaleAbs(img, alpha=1.2, beta=10))
    augmented.append(cv2.convertScaleAbs(img, alpha=0.8, beta=-10))
    
    # Slight rotations
    rows, cols = img.shape
    for angle in [-5, 5]:
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        augmented.append(cv2.warpAffine(img, M, (cols, rows)))
    
    return augmented

def get_images_and_labels(dataset_dir="dataset"):
    image_paths = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir)
                   if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    face_samples = []
    ids = []
    label_to_id = {}
    next_id = 0

    for path in image_paths:
        # Example filename: name_1.jpg
        filename = os.path.basename(path)
        if "_" not in filename:
            continue
        label = filename.split("_")[0]

        if label not in label_to_id:
            label_to_id[label] = next_id
            next_id += 1

        id_ = label_to_id[label]

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue

        img = cv2.resize(img, (150, 150))  # Larger size

        # Add original + minimal augmentation
        for aug_img in augment_image(img):
            face_samples.append(aug_img)
            ids.append(id_)

    return face_samples, np.array(ids), label_to_id

def main():
    dataset_dir = "dataset"
    if not os.path.exists(dataset_dir):
        print("Dataset folder not found. Run collect_faces.py first.")
        return

    faces, ids, label_to_id = get_images_and_labels(dataset_dir)
    if len(faces) == 0:
        print("No faces found in dataset. Collect some first.")
        return

    print(f"Found {len(faces)} face images belonging to {len(label_to_id)} people.")
    
    # Optimized LBPH for Raspberry Pi
    recognizer = cv2.face.LBPHFaceRecognizer_create(
        radius=2,        # Better accuracy
        neighbors=8,     # Standard LBP
        grid_x=8,
        grid_y=8
    )
    
    print("Training... (this may take 1-2 minutes)")
    recognizer.train(faces, ids)

    # Save model
    recognizer.write("trainer.yml")
    print("Saved trained model to trainer.yml")

    # Save label mapping (id -> name)
    id_to_label = {str(v): k for k, v in label_to_id.items()}
    with open("labels.json", "w") as f:
        json.dump(id_to_label, f)

    print("Saved labels to labels.json")
    print("Training complete.")

if __name__ == "__main__":
    main()
