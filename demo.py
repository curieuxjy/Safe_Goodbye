import cv2
import numpy as np
import serial
import time
   
def run_video(path):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(path)
    
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video  file")
    
    # Read until video is completed
    frame_num = 0
    # message
    
    while(cap.isOpened()):
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_num+=1
        if ret == True:
            # Display the resulting frame
            
            cv2.imshow('Frame', frame)
            print(frame_num)
            time.sleep(0.01)
            if frame_num == 400:
                break
                # send message to arduino

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
    # Break the loop
        else: 
            break
    
    # When everything done, release 
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()


if __name__=="__main__":

    arduino=serial.Serial('COM5', 9600)
    c='0'
    c=c.encode('utf-8')
    arduino.write(c)
    
    for i in range(3):
        time.sleep(5)

        # 영상을 하나로 합쳐야 하나

        path = r"C:\Users\Jungyeon\Desktop\tmp\Arrival_project\target\video\target1.mp4"

        run_video(path)

        c='1'
        c=c.encode('utf-8')
        arduino.write(c)

        time.sleep(5)

        c='2'
        c=c.encode('utf-8')
        arduino.write(c)
        path = r"C:\Users\Jungyeon\Desktop\tmp\Arrival_project\target\video\target2.mp4"
        run_video(path)

        time.sleep(10)