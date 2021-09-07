import cv2
import numpy as np

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 1080, 720)
cv2.moveWindow('Video', 600, 0) # For laptop screen
#cv2.moveWindow('Video', 2700, 0) # For desktop screen


def display(frame, kp):
    cv2.imshow('Video', frame)
    cv2.waitKey(1)

keypoints = []
descriptors = []
counter = 0 
def detection(frame):
    global counter
    orb = cv2.ORB_create()
    corners = cv2.goodFeaturesToTrack(frame, 2000, 0.01, 3) # N-dimensional array

    kps = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in corners] # f[row][column] to access the coordinates stored in desc array
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    corners = np.int0(corners)                          # Converts data from float32 to int64
    for pts in corners: 
        u,v = pts.ravel()                               # Convert N-dimensional array to a 1D array        cv2.circle(frame, (u,v), 5, (0,255,0), -1)      # Why draw the centers of the circle on the descriptors instead of the keypoints?
        cv2.circle(frame, (u,v), 5, (0,255,0), -1)      # Draw the detected keypoints
    kps, des = orb.compute(frame, kps)                  # Compute the descriptors                   
    
    # Store keypoint coordinates in the keypoints list 
    for p in kps:
        keypoints.append(p.pt)

    # Do the same for descriptors
    # In general, for frame (n), descriptors[n-1][x], x: 0 -> 32, will store its descriptor values. The value of x corresponds to the index of the detected keypoints   
    descriptors.append(des)
    
    # Only enter matching phase when we have info from at least 2 frames
    if (len(descriptors) >= 2):
        matching(frame)

    display(frame, kps)

    counter += 1 # Frame tracker (lags frame number by 1)

def matching(frame):
    # Define the brute force matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING) # Cross-check cannot be set to True if using knnMatch
    # Check counter value
    print('\n', "Frame number: ", counter+1)

    # Matches is a list of DMatch
    # DMatch object attributes: train descriptor index (trainIdx), query descriptor index (queryIdx), train image index (trainIdx), distance between descriptors
    matches = bf.knnMatch(descriptors[counter], descriptors[counter-1], k=2)

    # Ratio test
    for m,n in matches:
        if m.distance < 0.75 * n.distance:          
            p1 = keypoints[m.trainIdx]
            p2 = keypoints[m.queryIdx]
            u1, v1 = int(p1[0]), int(p1[1])
            u2, v2 = int(p2[0]), int(p2[1])
            cv2.line(frame, (u1,v1), (u2,v2), (255, 0, 0), 2)
                
    return frame

if __name__ == "__main__":
    path = '../test.mp4'
    cap = cv2.VideoCapture(path)

    while (True):
        ret, vid = cap.read()
        gray = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
        if (ret == True):
            detection(gray)
        else:
            cap.release() 