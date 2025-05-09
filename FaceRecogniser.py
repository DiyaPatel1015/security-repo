import cv2
import face_recognition
import os

class FaceRecogniser:
    def __init__(self, known_faces_dir='./encoding_images', tolerance=0.6):
        self.known_face_encodings = []
        self.known_face_names = []
        self.tolerance = tolerance
        self.load_known_faces(known_faces_dir)
        
    def load_known_faces(self, known_faces_dir):
        """Load and encode known faces from the specified directory."""
        for filename in os.listdir(known_faces_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # Load image and get the encoding
                img_path = os.path.join(known_faces_dir, filename)
                image = face_recognition.load_image_file(img_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    encoding = encodings[0]
                    self.known_face_encodings.append(encoding)
                    # Use filename (without extension) as the person's name
                    self.known_face_names.append(os.path.splitext(filename)[0])
        print("Loaded known faces:", self.known_face_names)

    def identify_faces(self, frame):
        """Detect and identify faces in a given frame."""
        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Detect face locations and encodings in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        face_labels = []  # List to store labels (friendly or unknown)

        for face_encoding in face_encodings:
            # Check if this face matches any known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)
            label = "Unknown"  # Default label
            
            # If a match is found, use the name of the matched known face
            if True in matches:
                match_index = matches.index(True)
                label = f"Friendly: {self.known_face_names[match_index]}"
            
            face_labels.append(label)

        return face_locations, face_labels
        

    def identify_face_only(self, frame):
		# Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Detect face locations and encodings in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        face_labels = []  # List to store labels (friendly or unknown)
        
        for face_encoding in face_encodings:
            # Check if this face matches any known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, self.tolerance)
            label = "Unknown"  # Default label
            
            # If a match is found, use the name of the matched known face
            if True in matches:
                match_index = matches.index(True)
                label = f"Friendly: {self.known_face_names[match_index]}"
            
            face_labels.append(label)
        if label:
            print(f"{label} found")
        return face_labels
        
        
    def process_frame(self, frame, face_locations, face_labels):
        # Display results
        for (top, right, bottom, left), label in zip(face_locations, face_labels):
            # Draw rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            # Display label below the face
            cv2.putText(frame, label, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
		