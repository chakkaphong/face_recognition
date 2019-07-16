import threading
import time
import face_recognition
import cv2 as cv2

unknow_img = face_recognition.load_image_file('../IMG/iu_2.jpg')
unkow_ing_encoding = face_recognition.face_encodings(unknow_img)[0]

def sleeper(number):
    for i in range(10):
        filepath = '../IMG/thread{}.jpg'.format(number)
        load_img = face_recognition.load_image_file(filepath)
        load_img_encoding = face_recognition.face_encodings(load_img)[0]

        results = face_recognition.face_distance([load_img_encoding], unkow_ing_encoding)
        world = 'id: ' + str(i) + 'result of matching image is ' + str(results)
        print(world)
        number+=1
    #print('this is lenght arra of training. {}'.format(len(load_img_encoding)))
    #print('this is lenght array of unknow. {}'.format(len(unkow_ing_encoding)))
    #print('Hi, I am {}. Going to sleep for 5 seconds \n'.format(name))
    #print("is the unknow face a picture {}",format(results))    
    
 
start = time.time()
threads = []


t1 = threading.Thread(target = sleeper , args = (0,))
t2 = threading.Thread(target = sleeper , args = (10,))
#t3 = threading.Thread(target = sleeper , args = (10,))
#t4 = threading.Thread(target = sleeper , args = (15,))

t1.start()
t2.start()
#t3.start()
#t4.start()

t1.join()
t2.join()
#t3.join()
#t4.join()



'''

for i in range(1):
    t = threading.Thread(target = sleeper, name = 'thread{}'.format(i), args =(i,'thread{}'.format(i) ) )
    threads.append(t)
    t.start()
    #print('{} has started \n'.format(t.name))
 
 
 
    
for i in threads:

    i.join()
'''
end = time.time()



print('time is {}'.format(end - start))