# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
from __future__ import print_function

import sys, os

sys.path.append(os.getcwd())
# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
from datetime import datetime
from collections import Counter
from itertools import takewhile

# from .models import Master
import push_to_db
import dlib
#import cv2
from multiprocessing import Process,Array
import requests,urllib

def detector(*param_rec):

    cctv_ip= param_rec[0]

    DATABASE = os.path.join(os.getcwd(), '..', 'db.sqlite3')

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--prototxt", required=True,
                    help="path to Caffe 'deploy' prototxt file")
    ap.add_argument("-m", "--model", required=True,
                    help="path to Caffe pre-trained model")
    ap.add_argument("-c", "--confidence", type=float, default=0.3,
                    help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())

    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

    # initialize the video stream, allow the cammera sensor to warmup,
    # and initialize the FPS counter
    print("[INFO] starting video stream...")
    vs = VideoStream(src=cctv_ip).start()
    time.sleep(2)
    #time.sleep(1)
    fps = FPS().start()

    # loop over the frames from the video stream
    while True:
        cctv_status[param_rec[1]] = 0
    #count = 0
    #while count in range(0, 10):
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        t1 = datetime.now()
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                    0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()
        # print "here are the detections"
        # print detections
        # print "here are the np.arrange"
        # print np.arange(0, detections.shape[2])
        # print "confidence"
        # for i in np.arange(0, detections.shape[2]):
        #    print detections[0, 0, i, 2]
        # time.sleep(2000)
        person_count = 0
        # loop over the detections
        for i in np.arange(0, detections.shape[2]):

            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                if CLASSES[idx] == "person":
                    cctv_status[param_rec[1]] = 1
                    person_count += 1
                else:
                    cctv_status[param_rec[1]] = 0
                # if idx != 15:
                #    break
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                                            confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                            COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
        #print "Number of people detected: ", person_count

        p_queue = push_to_db.Queue()
        p_queue.enqueue(person_count)

        if p_queue.size() == 30:
            p_queue.dequeue()
            freq = Counter(p_queue)
            mostfreq = freq.most_common()
            mode = list(takewhile(lambda _x : _x[1] == mostfreq[0][1],mostfreq))
            max_mode = mode[-1][0]

        else:
            max_mode = person_count

        #print "Pushing into database: %s" % DATABASE
        db = push_to_db.Db(DATABASE)
        room_no = 5
        #print "Updating the database: %s" % DATABASE
        db.update(room_no, max_mode)
        # db.select()
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        time.sleep(1.5)
        t2 = datetime.now()
        #print 'Frame processing time: ', (t2 - t1)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()
        #count += 1

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    vs.stop()

#---------------------------

def print_status():
	
    global cctv_status
	
    while(True):
        for i in range(len(cctv_status)):
            if(i==0):
                data=''
            print(int(cctv_status[i]),end=' ') 
            data += "[{'cam_no':"+str(i)+",'status':"+str(int(cctv_status[i]))+"}]"
            #{'cam_no':1,'status':"+str(cctv_status[1])+"}]"
            #urllib.request.urlopen().read()
            #print(int(i))
        requests.post("http://172.20.4.86/cam",data=data)
        time.sleep(4)
            
        print()
    
		
		

cctv_ip_list= [0,"rtsp://172.20.3.41:554/0"]
#"rtsp://172.20.3.13:554/av0_0","rtsp://172.20.3.11:554/1/h264major"]

#cctv_status=[0]*len(cctv_ip_list)
cctv_status=Array('i',[0]*(len(cctv_ip_list)))

counter=0
for cctv_ip in  cctv_ip_list:

    print("counter"+str(counter))
    Process(target=detector,args=(cctv_ip,counter,)).start()
    counter+=1
	
p2=Process(target=print_status)
p2.start()	
	

#---------------------------
