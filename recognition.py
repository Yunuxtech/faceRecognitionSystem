import face_recognition
import cv2

# Load the trained data
face_recognition_model_path = "face_recognition_model.dat"
trained_data = face_recognition.load_image_file(face_recognition_model_path)
authorized_faces = trained_data["authorized_faces"]
unauthorized_faces = trained_data["unauthorized_faces"]

# Initialize the video capture object
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Convert the frame to RGB format
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and their encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Initialize the list of names and images for recognized faces
    face_names = []
    face_images = []

    for face_encoding in face_encodings:
        # Compare the captured face encoding with the authorized face encodings
        matches = face_recognition.compare_faces([face_data[0] for face_data in authorized_faces], face_encoding)

        # Find the matched face index
        matched_index = [i for i, match in enumerate(matches) if match]

        if matched_index:
            # Get the matched face name and image
            matched_face_data = authorized_faces[matched_index[0]]
            face_names.append("Access Granted: " + matched_face_data[1])
            face_images.append(frame)

        else:
            face_names.append("Access not granted")
            face_images.append(None)

    # Draw rectangles and display the names on the frame
    for (top, right, bottom, left), name, image in zip(face_locations, face_names, face_images):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Exit loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the windows
video_capture.release()
cv2.destroyAllWindows()
