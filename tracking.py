# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import threading
# import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cameras", type=int,
                help="number of cameras")
args = ap.parse_args()

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (24, 33, 166)
greenUpper = (45, 131, 255)
# used for tracked points
# pts = deque(maxlen=args["buffer"])

broker_address="192.168.1.206" 
#broker_address="iot.eclipse.org" #use external broker
client = mqtt.Client("P1") #create new instance
client.connect(broker_address) #connect to broker



def track_obj(cam):

    vs = VideoStream(src=cam).start()

    # allow the camera or video file to warm up
    time.sleep(2.0)
    areaArray = []
    # keep looping
    while True:
        # grab the current frame
        frame = vs.read()
        frame = cv2.flip(frame,1)

        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if frame is None:
            break

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        for c in cnts:
            area = cv2.contourArea(c)
            areaArray.append(area)
        # only proceed if at least one contour was found
        if len(areaArray) > 0:
            sorteddata = sorted(zip(areaArray, cnts), key=lambda x: x[0], reverse=True)
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            # c = max(cnts, key=cv2.contourArea)
            centers = []
            if areaArray and len(areaArray) >= 2:
                for i in sorteddata:
                    c = i[1]
                    ((x, y), radius) = cv2.minEnclosingCircle(c)
                    M = cv2.moments(c)
                    # print(M)
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    centers.append(center)
                    if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    # cv2.circle(frame, (int(x), int(y)), int(radius),
                    # 	(0, 255, 255), 2)
                        cv2.circle(frame, center, 5, (0, 0, 255), -1)
                        rect = cv2.minAreaRect(c)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(frame,[box],0,(0,0,255),2)

                centerX, centerY = 0,0
                for center in centers:
                    centerX += center[0]
                    centerY += center[1]
                absCenter = (int(centerX / (len(centers) if len(centers)>0 else 1)), int(centerY / (len(centers) if len(centers)>0 else 1)))
                cv2.circle(frame, absCenter, 5, (0, 255, 0), -1)

                # c1 = sorteddata[0][1]
                # ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
                # M1 = cv2.moments(c1)
                # # print(M)
                # center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
                # c2 = sorteddata[1][1]
                # ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
                # M2 = cv2.moments(c2)
                # # print(M)
                # center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
                # # client.publish("test",str(center))#publish
                # # print(center)
                # # only proceed if the radius meets a minimum size
                # if radius1 > 10:
                #     # draw the circle and centroid on the frame,
                #     # then update the list of tracked points
                #     # cv2.circle(frame, (int(x), int(y)), int(radius),
                #     # 	(0, 255, 255), 2)
                #     cv2.circle(frame, center1, 5, (0, 0, 255), -1)
                # if radius2 > 10:
                #     # draw the circle and centroid on the frame,
                #     # then update the list of tracked points
                #     # cv2.circle(frame, (int(x), int(y)), int(radius),
                #     # 	(0, 255, 255), 2)
                #     cv2.circle(frame, center2, 5, (0, 0, 255), -1)
        # cv2.circle(frame, (600,450), 5, (0, 255, 0), -1)


        # update the points queue
        # pts.appendleft(center)

        # loop over the set of tracked points
        # for i in range(1, len(pts)):
        # 	# if either of the tracked points are None, ignore
        # 	# them
        # 	if pts[i - 1] is None or pts[i] is None:
        # 		continue

        # 	# otherwise, compute the thickness of the line and
        # 	# draw the connecting lines
        # 	thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        # 	cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        # show the frame to our screen
        # cv2.imshow("Mask"+str(cam), mask)

        cv2.imshow("Frame"+str(cam), frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break

    vs.stop()

    # close all windows
    cv2.destroyAllWindows()
    exit()

# if args.cameras is None:
# 	print(args.cameras)
# 	track_obj(0)
# 	# t1 = threading.Thread(target=track_obj, args=(0,))
# 	# t1.start()
# 	# t1.join()
# else:
# 	threads=[]
# 	print("multiple cameras")
# 	print(args.cameras)
# 	for x in range(0,args.cameras):
# 		threads.append(threading.Thread(target=track_obj, args=(x,)))
# 		threads[x].start()

# if args.cameras is not None:
# 	for x in threads:
# 		x.join()


t1 = threading.Thread(target=track_obj, args=(0,))
# t2 = threading.Thread(target=track_obj, args=(2,))
t1.start()
# t2.start()

t1.join()
# t2.join()
