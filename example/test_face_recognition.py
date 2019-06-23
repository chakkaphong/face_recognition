import cv2 as cv2
import face_recognition

know_image = face_recognition.load_image_file("IMG/obama_1.jpg")
unknow_image = face_recognition.load_image_file("IMG/obama_2.jpg")

obama_encoding = face_recognition.face_encodings(know_image)[0]
unknow_encoding = face_recognition.face_encodings(unknow_image)[0]

result = face_recognition.compare_faces([obama_encoding], unknow_encoding)


print("obama_face_id: ", obama_encoding[1])
print("obama_face_id: ", obama_encoding)
#print("unknow_face_id: ", unknow_encoding)
print("result of face is",result)