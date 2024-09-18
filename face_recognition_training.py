import recognition
import os

# Set up folder paths
authorized_folder = "authorized_faces/"
unauthorized_folder = "unauthorized_faces/"

# Load authorized face images
authorized_faces = []
for filename in os.listdir(authorized_folder):
    img = recognition.load_image_file(os.path.join(authorized_folder, filename))
    face_encoding = recognition.face_encodings(img)[0]
    authorized_faces.append((face_encoding, filename.split(".")[0]))

# Load unauthorized face images
unauthorized_faces = []
for filename in os.listdir(unauthorized_folder):
    img = recognition.load_image_file(os.path.join(unauthorized_folder, filename))
    face_encoding = recognition.face_encodings(img)[0]
    unauthorized_faces.append((face_encoding, filename.split(".")[0]))

# Save the trained face encodings
trained_data = {
    "authorized_faces": authorized_faces,
    "unauthorized_faces": unauthorized_faces
}

# Save the trained data to a file
face_recognition_model_path = "face_recognition_model.dat"
recognition.save(face_recognition_model_path, trained_data)
