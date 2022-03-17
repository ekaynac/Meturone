#@title Run object detection and show the detection results
from modelclass import *
from PIL import Image
import numpy as np
import os

INPUT_IMAGE_URL = "https://cdn.protoolreviews.com/wp-content/uploads/2018/05/Best-Portable-Generator-Buying-Guide-01.jpg" 
DETECTION_THRESHOLD = 0.18 
TFLITE_MODEL_PATH = r"D:\Github\Meturone\UORG\Object Detection\Model\efficientdet_lite0-portablegenerator-augmented.tflite" 

IMG_PATH = r'D:\Github\Meturone\UORG\Object Detection\portable_generator\test\portable_generator5.jpg'

image = Image.open(IMG_PATH).convert('RGB')
image.thumbnail((512, 512), Image.ANTIALIAS)
image_np = np.asarray(image)

# Load the TFLite model
options = ObjectDetectorOptions(
      num_threads=5,
      score_threshold=DETECTION_THRESHOLD
      
)
detector = ObjectDetector(model_path=TFLITE_MODEL_PATH, options=options)

PATH = r"D:\Github\Meturone\UORG\Object Detection\data06\data06"

for i in os.listdir(PATH):
    img_path = os.path.join(PATH,i)
    img = cv2.imread(img_path)
    image_np = np.asarray(img)
    #image_np = cv2.resize(img,(512,512))
    # Run object detection estimation using the model.
    detections = detector.detect(image_np)
    # Draw keypoints and edges on input image
    image_np = visualize(image_np, detections)

    # Show the detection result
    img = Image.fromarray(image_np)
            
    cv2.imshow("detection",image_np)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
