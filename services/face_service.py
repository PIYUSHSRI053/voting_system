import face_recognition
import cv2
import numpy as np
from config.settings import Settings
from datetime import datetime

class FaceService:
    @staticmethod
    def capture_and_encode():
        cap = cv2.VideoCapture(0)
        
        print("📸 Press SPACE to capture face")
        while True:
            ret, frame = cap.read()
            cv2.imshow("Capture Face", frame)
            
            if cv2.waitKey(1) == 32:  # SPACE
                locations = face_recognition.face_locations(frame)
                if locations:
                    encoding = face_recognition.face_encodings(frame, locations)[0]
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    path = f"{Settings.PROOF_IMAGES_DIR}/reg_{timestamp}.jpg"
                    cv2.imwrite(path, frame)
                    
                    cap.release()
                    cv2.destroyAllWindows()
                    return encoding.tobytes(), path
                
                print("No face detected!")
            
            if cv2.waitKey(1) == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        return None, None