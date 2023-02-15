import tensorflow as tf
import os
import json
from flask import current_app
from catalog_client import products_per_category

saved_model_dir = os.environ["MODEL_DIR"]
saved_model = tf.saved_model.load(saved_model_dir)
detector = saved_model.signatures["default"]

def find_objects_and_query_catalog(img_bytes):

    detected_objects = detect_objects(img_bytes)
    filtered = filter_detections(detected_objects)

    categories = []
    for i in filtered:
        categories.append(i["class"])
    current_app.logger.info('categories: ' + json.dumps(categories))

    products = products_per_category(categories)

    return {'detected objects': categories, 'products': products}

def detect_objects(img):
    """
    finds the objects in a given image
    using our pretrained CV model
    """
    image = tf.image.decode_jpeg(img, channels=3)
    converted_img = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]
    result = detector(converted_img)
    num_detections = len(result["detection_scores"])

    output_dict = {key: value.numpy().tolist() for key, value in result.items()}
    output_dict["num_detections"] = num_detections

    return output_dict

def filter_detections(detections):
    # only keep predictions with confidence > 0.30, max 10 predictions

    filtered = []
    max_boxes = 10
    num_detections = min(detections['num_detections'], max_boxes)

    for i in range(0, num_detections):
        d = {
            'box': {
                'yMin': detections['detection_boxes'][i][0],
                'xMin': detections['detection_boxes'][i][1],
                'yMax': detections['detection_boxes'][i][2],
                'xMax': detections['detection_boxes'][i][3]
            },
            'class': detections['detection_class_entities'][i].decode('utf-8'),
            'label': detections['detection_class_entities'][i].decode('utf-8'),
            'score': detections['detection_scores'][i],
        }
        if d.get("score") >= 0.30:
            filtered.append(d)
    
    return filtered

