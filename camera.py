import cv2
import imutils
import datetime
import numpy as np

def get_frame(camera_port):
    import cv2
    import numpy as np
    import datetime
    import imutils
    import time

    vs = cv2.VideoCapture(camera_port)
    time.sleep(2)

    firstFrame = None

    while True:
        ret, frame = vs.read()
        text = 'baseline'

        if frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9, 9), 0)


        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        #cv2.imshow('frame', firstFrame)
        # find diff
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
        #dilate
        thresh = cv2.dilate(thresh, None, iterations=2)
        #countour
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "countour found"

        # draw the text and timestamp on the frame
        cv2.putText(frame, "Tampering: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


        # show the frame and record if the user presses a key
        #cv2.imshow("Camera", frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Difference", frameDelta)
        imgencode=cv2.imencode('.jpg',frame)[1]
        stringData=imgencode.tostring()
        yield (b'--frame\r\n'
            b'Content-Type: text/plain\r\n\r\n'+stringData+b'\r\n')

        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

    # cleanup the camera and close any open windows
    #del(vs)
    vs.release()
    cv2.destroyAllWindows()
