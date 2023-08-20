import cv2
from constant import *

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

class GenderRecognizer:

    def __init__(self,
        face1,
        face2,
        gender1,
        gender2 
    ):
        self.__face = cv2.dnn.readNet(face2, face1)
        self.__gender = cv2.dnn.readNet(gender2, gender1)

        self.__label_gender = ['Male', 'Female']
    
    def predict(self, image):
        is_valid = True
        gender_int = GENDER_MALE

        # Copy image
        fr_cv = image.copy()

        # Face detection
        fr_h = fr_cv.shape[0]
        fr_w = fr_cv.shape[1]
        blob = cv2.dnn.blobFromImage(fr_cv, 1.0, (300, 300),
                                    [104, 117, 123], True, False)

        self.__face.setInput(blob)
        detections = self.__face.forward()

        # Face bounding box creation
        faceBoxes = []
        for i in range(detections.shape[2]):
            #Bounding box creation if confidence > 0.7
            confidence = detections[0, 0, i, 2]

            if confidence > 0.9:
                
                x1 = int(detections[0, 0, i, 3]*fr_w)
                y1 = int(detections[0, 0, i, 4]*fr_h)
                x2 = int(detections[0, 0, i, 5]*fr_w)
                y2 = int(detections[0, 0, i, 6]*fr_h)
                
                faceBoxes.append([x1, y1, x2, y2])
                
                cv2.rectangle(fr_cv, (x1, y1), (x2, y2),
                            (0, 255, 0), int(round(fr_h/150)), 2)
    
        if len(faceBoxes) != 1:
            is_valid = False
            return is_valid, fr_cv, gender_int

        for faceBox in faceBoxes:
            #Extracting face as per the faceBox
            face = fr_cv[max(0, faceBox[1]-15):
                        min(faceBox[3]+15, fr_cv.shape[0]-1),
                        max(0, faceBox[0]-15):min(faceBox[2]+15,
                                    fr_cv.shape[1]-1)]
            
            #Extracting the main blob part
            blob = cv2.dnn.blobFromImage(
                face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            
            #Prediction of gender
            self.__gender.setInput(blob)
            gender_preds = self.__gender.forward()
            gender_int = gender_preds[0].argmax()
            genderLabel = self.__label_gender[gender_int]
            
            #Putting text of age and gender 
            #At the top of box
            cv2.putText(fr_cv,
                        f'{genderLabel}',
                        (faceBox[0]-150, faceBox[1]+10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.3,
                        (217, 0, 0),
                        2,
                        cv2.LINE_AA)

        return is_valid, fr_cv, gender_int