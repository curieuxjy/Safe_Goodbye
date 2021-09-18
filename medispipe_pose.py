import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
# from google.colab.patches import cv2_imshow
import math
import numpy as np

DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480

def resize_and_show(image):
  h, w = image.shape[:2]
  if h < w:
    img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
  else:
    img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
  plt.imshow(img)

# Read images with OpenCV.
path = r"C:\Users\Jungyeon\Desktop\Arrival_project\test2.png"
# img = cv2.imread(path)
img = cv2.imread(path)

plt.imshow(img)
images = {path: cv2.imread(path)}
# Preview the images.
for name, image in images.items():
  print(name)   
  resize_and_show(image)
  
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils 
mp_drawing_styles = mp.solutions.drawing_styles

# help(mp_pose.Pose)

# Run MediaPipe Pose and draw pose landmarks.
with mp_pose.Pose(
    static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
  for name, image in images.items():
    # Convert the BGR image to RGB and process it with MediaPipe Pose.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Print nose landmark.
    image_hight, image_width, _ = image.shape
    if not results.pose_landmarks:
      continue
    # print(
    #   f'Nose coordinates: ('
    #   f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
    #   f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_hight})'
    # )

    # Draw pose landmarks.
    print(f'Pose landmarks of {name}:')
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    resize_and_show(annotated_image)


# # Run MediaPipe Pose and plot 3d pose world landmarks.
# with mp_pose.Pose(
#     static_image_mode=True, min_detection_confidence=0.5, model_complexity=2) as pose:
#   for name, image in images.items():
#     results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Print the real-world 3D coordinates of nose in meters with the origin at
#     # the center between hips.
#     # print('Nose world landmark:'),
#     # print(results.pose_world_landmarks.landmark[mp_pose.PoseLandmark.NOSE])
    
#     # Plot pose world landmarks.
#     mp_drawing.plot_landmarks(
#         results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)


# # Run MediaPipe Pose with `enable_segmentation=True` to get pose segmentation.
# with mp_pose.Pose(
#     static_image_mode=True, min_detection_confidence=0.5, 
#     model_complexity=2, enable_segmentation=True) as pose:
#   for name, image in images.items():
#     results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # Draw pose segmentation.
#     print(f'Pose segmentation of {name}:')
#     annotated_image = image.copy()
#     red_img = np.zeros_like(annotated_image, dtype=np.uint8)
#     red_img[:, :] = (255,255,255)
#     segm_2class = 0.2 + 0.8 * results.segmentation_mask
#     segm_2class = np.repeat(segm_2class[..., np.newaxis], 3, axis=2)
#     annotated_image = annotated_image * segm_2class + red_img * (1 - segm_2class)
#     resize_and_show(annotated_image)