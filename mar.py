def mouth_aspect_ratio(mouth):
    # compute the euclidean distances between the two sets of
    # vertical mouth landmarks (x, y)-coordinates
    A = np.linalg.norm(mouth[2] - mouth[10])  # 51, 59
    B = np.linalg.norm(mouth[4] - mouth[8])   # 53, 57
 
    # compute the euclidean distance between the horizontal
    # mouth landmark (x, y)-coordinates
    C = np.linalg.norm(mouth[0] - mouth[6])   # 49, 55
 
    # compute the mouth aspect ratio
    mar = (A + B) / (2.0 * C)
 
    # return the mouth aspect ratio
    return mar

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    # detected face in faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = frame.copy()
        cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        landmarks = predictor(gray, face)
        landmarks = face_utils.shape_to_np(landmarks)

        # The numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36], landmarks[37],
                             landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42], landmarks[43],
                              landmarks[44], landmarks[47], landmarks[46], landmarks[45])

        # Calculate Mouth Aspect Ratio (MAR)
        mouth_mar = mouth_aspect_ratio(landmarks[48:68])

        # Now judge what to do for the eye blinks and mouth aspect ratio
        if (left_blink == 0 or right_blink == 0) and mouth_mar > 0.6:
            sleep += 1
            drowsy = 0
            active = 0
            if sleep > 6:
                status = "SLEEPING!!!"
                color = (255, 0, 0)

        elif (left_blink == 1 or right_blink == 1) and mouth_mar > 0.6:
            sleep = 0
            active = 0
            drowsy += 1
            if drowsy > 6:
                status = "DROWSY!"
                color = (0, 0, 255)

        elif mouth_mar < 0.35:
            drowsy = 0
            sleep = 0
            active += 1
            if active > 6:
                status = "ACTIVE :)"
                color = (0, 255, 0)

        cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        for n in range(0, 68):
            (x, y) = landmarks[n]
            cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
