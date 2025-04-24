import cv2
from utils.simple_facerec import SimpleFacerec  # Updated import path
import csv
from datetime import datetime

# Initialize SimpleFacerec
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")  # Updated path for images folder

# Open CSV file to log attendance
attendance_file = "data/attendance.csv"  # Updated path for attendance file
with open(attendance_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Time"])

# Start video capture
cap = cv2.VideoCapture(0)
present_names = set()  # To avoid duplicate entries

while True:
    ret, frame = cap.read()
    face_locations, face_names = sfr.detect_known_faces(frame)

    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        # Get text size
        (w, h), _ = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, 1, 2)

        # Draw filled white rectangle as background
        cv2.rectangle(frame, (x1, y1 - h - 10), (x1 + w, y1), (255, 255, 255), -1)

        # Draw name text on top
        cv2.putText(frame, name, (x1, y1 - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

        # Draw face rectangle
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)

        # Log attendance if the person is not already marked
        if name not in present_names:
            present_names.add(name)
            with open(attendance_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
