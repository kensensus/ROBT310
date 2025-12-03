import cv2

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Could not open camera. Try changing the index (0 -> 1) or check camera connection.")
        return

    print("✅ Camera opened successfully. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break

        cv2.imshow("Camera Test - Press q to quit", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Exiting, camera released.")

if __name__ == "__main__":
    main()
