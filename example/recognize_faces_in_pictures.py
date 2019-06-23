import face_recognition
import cv2 as cv2




form_class = uic.loadUiType("MyWindowClass.ui")[0]


# Load the jpg files into numpy arrays
pam_image = face_recognition.load_image_file("IMG/pam_1.jpg")
obama_image = face_recognition.load_image_file("IMG/obama_1.jpg")
na_kom_image = face_recognition.load_image_file("IMG/kom_1.jpg")



unknown_image = face_recognition.load_image_file("IMG/obama_test.jpg")



# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    pam_face_encoding = face_recognition.face_encodings(pam_image)[0]
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    na_kom_encoding = face_recognition.face_encodings(na_kom_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

known_faces = [
    pam_face_encoding,
    obama_face_encoding,
    na_kom_encoding
]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

cv2.imshow('this is obama', obama_image)
print("Is the unknown face a picture of ป๋อมแป๋ม? {}".format(results[0]))
print("Is the unknown face a picture of โอบาม่า? {}".format(results[1]))
print("Is the unknown face a picture of น้าค่อม? {}".format(results[2]))
print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
cv2.waitKey(0)
cv2.destroyAllWindows()
