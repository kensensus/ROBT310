import cv2
import os
import sys
import time

def main():
    # Check if name passed as argument
    name = None
    if len(sys.argv) > 2 and sys.argv[1] == "--name":
        name = sys.argv[2].strip()
    
    if not name:
        name = input("Enter students's name (no spaces NameSurname format): ").strip()
    
    if not name:
        print("Name cannot be empty.")
        return

    # Make sure dataset folder exists
    dataset_dir = "dataset"
    os.makedirs(dataset_dir, exist_ok=True)

    # Load Haar cascade
    cascade_path = "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Open camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera.")
        return
    
    # Optimize camera settings
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    # Give user time to setup
    print(f"Collecting faces for: {name}")
    print("Position yourself in front of the camera.")
    print("Tips: Good lighting, face the camera directly, vary expressions slightly")
    print("Starting in 5 seconds...")
    
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    
    print("Starting collection now!")

    count = 0
    target_count = 100
    frame_skip = 0
    skipped_blurry = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Use CLAHE for better preprocessing
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray_eq = clahe.apply(gray)
        gray_eq = cv2.GaussianBlur(gray_eq, (5, 5), 0)

        # Multi-scale detection
        faces = face_cascade.detectMultiScale(
            gray_eq,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(100, 100)
        )
        
        if len(faces) == 0:
            faces = face_cascade.detectMultiScale(
                gray_eq,
                scaleFactor=1.1,
                minNeighbors=4,
                minSize=(80, 80)
            )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            frame_skip += 1
            if frame_skip % 3 != 0:
                continue

            face_roi = gray_eq[y:y+h, x:x+w]
            
            # Check face quality before saving
            laplacian_var = cv2.Laplacian(face_roi, cv2.CV_64F).var()
            
            if laplacian_var < 50:
                skipped_blurry += 1
                cv2.putText(frame, "Too blurry - hold still", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                continue
            
            face_roi = cv2.resize(face_roi, (150, 150))

            count += 1
            filename = os.path.join(dataset_dir, f"{name}_{count}.jpg")
            cv2.imwrite(filename, face_roi)

        # Progress bar
        progress = int((count / target_count) * 100)
        cv2.putText(frame, f"Progress: {progress}% ({count}/{target_count})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.putText(frame, f"Skipped blurry: {skipped_blurry}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        
        cv2.putText(frame, "Press 'q' to stop early", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow("Collecting faces", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or count >= target_count:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. Collected {count} images for {name} (skipped {skipped_blurry} blurry images).")
    print("Please run 'Train System' to update the model.")
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()
