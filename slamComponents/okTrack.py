import cv2
import numpy as np

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 1080, 720)
cv2.moveWindow('Video', 600, 0) # For laptop screen
# cv2.moveWindow('Video', 2700, 0) # For desktop screen


def display(frame, kp):
    cv2.imshow('Video', frame)
    cv2.waitKey(1)

# Meant to track the frames (counter = 0 ==> frame = 1)
counter = 0

# Define the things that we need for matching
ref_kps = []    
cur_kps = []   
ref_des = 0
cur_des = 0

def detection(frame):
    global counter, ref_des, cur_des

    orb = cv2.ORB_create()

    # Good features to track: Shi-Tomasi method
    corners = cv2.goodFeaturesToTrack(frame, 2000, 0.01, 3) # N-dimensional array
    kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in corners] # f[row][column] to access the coordinates stored in corners array
    
    # Convert the frame back to RGB so that you can see the color of the keypoints
    # Should I move this bloke somewhere that makes more sense? 
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    # Draw the detected keypoints
    corners = np.int0(corners)                          # Converts data from float32 to int64
    for pts in corners: 
        u,v = pts.ravel()                               # Convert N-dimensional array to a 1D array        cv2.circle(frame, (u,v), 5, (0,255,0), -1)      # Why draw the centers of the circle on the descriptors instead of the keypoints?
        cv2.circle(frame, (u,v), 3, (0,255,0), -1)      # Draw the detected keypoints 
    kps, des = orb.compute(frame, kps)                  # Compute the descriptors               

    # Update ref_des so we can compare every frame
    # Is there a better location to put this? 
    if (counter > 1):
        ref_des = cur_des

    # First frame append new values, subsequently replace with the previous keypoints
    if (counter == 0):
        for p in kps: 
            ref_kps.append(p.pt)
            ref_des = des
    else:
        for p in kps:
            cur_kps.append(p.pt)
            cur_des = des
    
    # Matching is only performed when cur_kps list is not empty
    if (len(cur_kps)):
        matching(frame, ref_des, cur_des)

    display(frame, kps)

    # Track the frames
    counter += 1

def matching(frame, ref_des, cur_des):
    # Define brute force matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
  
    # knnMatch(queryDes, trainDes, k value)
    # What does the k value represent?
    matches = bf.knnMatch(cur_des, ref_des, k=2)

    # Ratio test
    for m,n in matches:
        if m.distance < 0.7 * n.distance:
            train_kps = ref_kps[m.trainIdx] # reference points
            query_kps = cur_kps[m.queryIdx] # query points

            # Convert the points to integers
            u_train, v_train = int(train_kps[0]), int(train_kps[1])
            u_query, v_query = int(query_kps[0]), int(query_kps[1])

            # Draw the trails for the matched points
            cv2.line(frame, (u_train, v_train), (u_query, v_query), (255, 0, 0), 2)
            '''
            # Print the points for reference 
            print('\n')
            print("Reference points: ", (u_train,v_train))
            print("Matched points: ", (u_query,v_query))
            '''
  
    # Clear the lists to update with new points
    ref_kps.clear()
    for element in cur_kps:
        ref_kps.append(element)
    cur_kps.clear()

if __name__ == '__main__':
    path = '../test.mp4'
    cap = cv2.VideoCapture(path)

    while (True):
        ret, vid = cap.read()
        gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        if (ret == True):
            detection(gray)
        else:
            cap.release() 