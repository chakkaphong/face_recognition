import json
import face_recognition

known_face_encoding = []
count = 0

image_to_test = face_recognition.load_image_file("../IMG/captureimg.jpg")
image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
ex_img = image_to_test_encoding[0]
print(len(face_recognition.face_encodings(image_to_test)))
#print(len(ex_img))

with open('face_id.json') as f:
  data = json.load(f)

with open('face_id.json', 'w') as f:
  json.dump(data, f, indent=4)

print(len(data)) 
num = 10000001

for state in data[str(num)]:
    #print(state['FaceID'])
    known_face_encoding = state['FaceID']
    #face_distances = face_recognition.face_distance(ex_know_img, image_to_test_encoding)
  
print([known_face_encoding])
print(image_to_test_encoding)
print(len(known_face_encoding))
face_distances = face_recognition.face_distance([known_face_encoding[1]], image_to_test_encoding)

for i, face_distance in enumerate(face_distances):
    print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
    print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
    print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.4))
    print()