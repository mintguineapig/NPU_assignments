import os
import time
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from model import create_and_compile_model
from utils import create_datasets, setup_gpu_and_get_batch_size

def create_training_plots(history, save_path='training_history_fast.png'):
    if not history:
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    epochs = range(1, len(history.history['accuracy']) + 1)
    
    ax1.plot(epochs, history.history['accuracy'], 'bo-', label='Training accuracy')
    ax1.plot(epochs, history.history['val_accuracy'], 'ro-', label='Validation accuracy')
    ax1.axhline(y=0.95, color='g', linestyle='--', label='Target 95%')
    ax1.set_title('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(epochs, history.history['loss'], 'bo-', label='Training loss')
    ax2.plot(epochs, history.history['val_loss'], 'ro-', label='Validation loss')
    ax2.set_title('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')

def train_model_fast(data_dir, model_save_path='cat_dog_model.h5', max_epochs=10):
    start_time = time.time()
    batch_size = setup_gpu_and_get_batch_size()
    
    train_images, train_labels, test_images, _ = create_datasets(data_dir)
    
    np.random.seed(42)
    indices = np.arange(len(train_images))
    np.random.shuffle(indices)
    
    split_idx = int(0.8 * len(train_images))
    train_idx = indices[:split_idx]
    val_idx = indices[split_idx:]
    
    x_train = train_images[train_idx]
    y_train = train_labels[train_idx]
    x_val = train_images[val_idx]
    y_val = train_labels[val_idx]
    
    model = create_and_compile_model((128, 128, 3))
    
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', factor=0.5, patience=2, min_lr=1e-6)
    ]
    
    try:
        history = model.fit(x_train, y_train, batch_size=batch_size, epochs=max_epochs,
                          validation_data=(x_val, y_val), callbacks=callbacks, verbose=1)
        
        model.save(model_save_path)
        test_loss, test_accuracy = model.evaluate(x_val, y_val, verbose=0)
        
        create_training_plots(history)
        
        return model, history, test_accuracy
    except Exception as e:
        return None, None, 0

def main():
    data_dir = "/root/2025_practice/NPU_3/cat-and-dog"
    if os.path.exists(data_dir):
        train_model_fast(data_dir)

if __name__ == "__main__":
    main()