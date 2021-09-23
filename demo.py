import cv2
import numpy as np
import serial

   
def run_video(path, arduino=None):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(path)
    
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video  file")
    
    # Read until video is completed
    frame_num = 0
    while(cap.isOpened()):
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame_num+=1
        if ret == True:
            # Display the resulting frame
            
            cv2.imshow('Frame', frame)
            print(frame_num)
            if frame_num == 35:
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
    # arduino=serial.Serial('COM4', 57600)

    # c='0'
    # c=c.encode('utf-8')
    # arduino.write(c)
    for i in range(10):
        path = r"C:\Users\Jungyeon\Desktop\Arrival_project\target\video\target1.mp4"

        run_video(path)

        path = r"C:\Users\Jungyeon\Desktop\Arrival_project\target\video\target2.mp4"
        run_video(path)