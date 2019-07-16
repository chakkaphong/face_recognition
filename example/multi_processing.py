import os

from multiprocessing import Process, current_process
import face_recognition
import cv2 as cv2
import time




def square(number):
    """The function squares whatever number it is provided."""
    unknow_img = face_recognition.load_image_file('../IMG/iu_2.jpg')
    unkow_ing_encoding = face_recognition.face_encodings(unknow_img)[0]

    for i in range(5):
        filepath = '../IMG/thread{}.jpg'.format(number)
        load_img = face_recognition.load_image_file(filepath)
        load_img_encoding = face_recognition.face_encodings(load_img)[0]
        number+=1
        results = face_recognition.face_distance([load_img_encoding], unkow_ing_encoding)
        proc_id = os.getpid()
        process_name = current_process().name
        print(str(results) + str( proc_id) + str( process_name))
    # We can use the OS module in Python to print out the process ID
    # assigned to the call of this function assigned by the operating
    # system.
    proc_id = os.getpid()
    #print(f"Process ID: {proc_id}")

    # We can also use the "current_process" function to get the name
    # of the Process object:
    process_name = current_process().name
    #print(f"Process Name: {process_name}")

if __name__ == '__main__':
    start = time.time()
    # The processes list will store each call we make to "square" and the
    # numbers list contains the numbers we loop through and call the
    # "square" function on."
    processes = []

    # Loop through the list of numbers, call the "square" function,
    # and store and start each call to "square".
    process1 = Process(target=square, args=(0,))
    process2 = Process(target=square, args=(5,))
    process3 = Process(target=square, args=(10,))
    process4 = Process(target=square, args=(15,))

    process1.start()
    process2.start()
    process3.start()
    process4.start()

    '''
    for number in range(20):
        for j in range(4):
            process = Process(target=square, args=(number,))
            processes.append(process)
            # Processes are spawned by creating a Process object and
            # then calling its start() method.
            process.start()
            print(j)
        j = 0

    # Wait for Python process to end before starting the
    # next process.
    for process in processes:
        process.join()
    '''
process1.join()
process2.join()
#process3.join()
#process4.join()   
end = time.time()

print('time to uesed is : {}',format(end - start))