import cv2
import face_recognition
import numpy as np

class FaceAuthorization:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

    def add_face(self, image_path, name):
        """Add a new face to the known faces database."""
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)

        if face_encoding:
            self.known_face_encodings.append(face_encoding[0])
            self.known_face_names.append(name)
        else:
            print(f"No face found in the image: {image_path}")

    def authorize_face(self, image_path):
        """Authorize a face based on the known faces."""
        image = face_recognition.load_image_file(image_path)
        unknown_face_encoding = face_recognition.face_encodings(image)

        if not unknown_face_encoding:
            print("No face found in the image for authorization.")
            return None

        matches = face_recognition.compare_faces(self.known_face_encodings, unknown_face_encoding[0])

        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_names[first_match_index]

        return name

    def capture_face(self):
        """Capture a face from webcam and return its encoding."""
        cap = cv2.VideoCapture(0)  # Start video capture

        while True:
            ret, frame = cap.read()
            rgb_frame = frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if face_encodings:
            return face_encodings[0]
        return None

if __name__ == "__main__":
    face_auth = FaceAuthorization()

    face_auth.add_face("path_to_face_image_1.jpg", "Alice")
    face_auth.add_face("path_to_face_image_2.jpg", "Bob")

    authorized_name = face_auth.authorize_face("path_to_face_image_to_authorize.jpg")
    print(f"Authorized Name: {authorized_name}")
