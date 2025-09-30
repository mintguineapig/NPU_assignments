import os
import random
import numpy as np
from PIL import Image
import tensorflow as tf

def setup_gpu_and_get_batch_size():
    try:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
        return 256
    except:
        return 256

def load_images_from_mixed_directory(directory, img_size=(128, 128), max_images=5000):
    images, labels = [], []
    if not os.path.exists(directory):
        return np.array([]), np.array([])
    
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if len(image_files) > max_images:
        image_files = random.sample(image_files, max_images)
    
    for filename in image_files:
        try:
            label = 0 if filename.lower().startswith('cat') else 1 if filename.lower().startswith('dog') else -1
            if label == -1:
                continue
            
            img = Image.open(os.path.join(directory, filename)).convert('RGB').resize(img_size)
            img_array = np.array(img, dtype=np.float32) / 255.0
            
            if img_array.shape == img_size + (3,):
                images.append(img_array)
                labels.append(label)
        except:
            continue
    
    return np.array(images, dtype=np.float32), np.array(labels, dtype=np.int32)

def create_datasets(data_dir):
    train_dir = os.path.join(data_dir, 'train', 'train')
    test_dir = os.path.join(data_dir, 'test', 'test')
    
    train_images, train_labels = load_images_from_mixed_directory(train_dir)
    
    test_images = []
    if os.path.exists(test_dir):
        image_files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        for filename in image_files[:1000]:
            try:
                img = Image.open(os.path.join(test_dir, filename)).convert('RGB').resize((128, 128))
                test_images.append(np.array(img, dtype=np.float32) / 255.0)
            except:
                continue
        test_images = np.array(test_images) if test_images else np.array([])
    
    return train_images, train_labels, test_images, None

def get_random_test_image(data_dir):
    test_dir = os.path.join(data_dir, 'test', 'test')
    if not os.path.exists(test_dir):
        return None
    
    image_files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        return None
    
    image_path = os.path.join(test_dir, random.choice(image_files))
    try:
        Image.open(image_path).convert('RGB').close()
        return image_path
    except:
        return None

def predict_image(model, image_path):
    try:
        img = Image.open(image_path).convert('RGB').resize((128, 128))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
        prediction = model.predict(img_array, verbose=0)[0][0]
        confidence = max(prediction, 1 - prediction) * 100
        return ("개", confidence) if prediction > 0.5 else ("고양이", confidence)
    except:
        return "오류", 0
