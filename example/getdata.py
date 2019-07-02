import json

with open('face_id.json') as f:
  data = json.load(f)

#for state in data['states']:
 # del state['area_codes']

with open('face_id.json', 'w') as f:
  json.dump(data, f, indent=4)

for state in data['00000001']:
    #ex_state = state['name']
    #print(state['area_codes'])
    print(state['FaceID'])