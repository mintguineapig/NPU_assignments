#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
import glob
import os
import sys

class PanoramaStitcher:
    def __init__(self):
        self.stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    
    def load_images(self, input_dir, pattern="*.jpg"):
        image_paths = sorted(glob.glob(os.path.join(input_dir, pattern)))
        if len(image_paths) < 2:
            raise ValueError(f"Need at least 2 images, found {len(image_paths)}")
        
        images = []
        for path in image_paths:
            image = cv2.imread(path)
            if image is not None:
                images.append(image)
        
        if len(images) < 2:
            raise ValueError(f"Need at least 2 valid images, found {len(images)}")
        
        return images
    
    def preprocess_images(self, images, max_dimension=1200):
        processed = []
        for image in images:
            h, w = image.shape[:2]
            if h > max_dimension or w > max_dimension:
                scale = max_dimension / max(h, w)
                new_h, new_w = int(h * scale), int(w * scale)
                image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            processed.append(image)
        return processed
    
    def stitch_images(self, images):
        status, panorama = self.stitcher.stitch(images)
        return status == cv2.Stitcher_OK, panorama
    
    def create_panorama(self, input_dir, pattern="*.jpg", output_path="panorama.jpg"):
        images = self.load_images(input_dir, pattern)
        processed_images = self.preprocess_images(images)
        success, panorama = self.stitch_images(processed_images)
        
        if success:
            cv2.imwrite(output_path, panorama)
            return True
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--pattern", default="*.jpg")
    parser.add_argument("--output", default="panorama.jpg")
    args = parser.parse_args()
    
    stitcher = PanoramaStitcher()
    success = stitcher.create_panorama(args.input_dir, args.pattern, args.output)
    
    print(f"Panorama creation {'succeeded' if success else 'failed'}")
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
