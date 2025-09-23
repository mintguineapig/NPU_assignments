#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
import re
import pytesseract

class LicensePlateDetector:
    def __init__(self, debug=False):
        self.debug = debug
    
    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.createCLAHE(clipLimit=3.0).apply(gray)
        adaptive = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        _, otsu = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        edges = cv2.Canny(enhanced, 50, 150)
        return gray, adaptive, otsu, edges
    
    def find_candidates(self, binary_images):
        candidates = []
        for binary in binary_images[1:]:
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if 30 <= w <= 200 and 10 <= h <= 60 and 1.5 <= w/h <= 8.0:
                    candidates.append((x, y, w, h))
        
        unique = []
        for x, y, w, h in candidates:
            duplicate = any(np.sqrt((x+w//2-ux-uw//2)**2 + (y+h//2-uy-uh//2)**2) < 30 
                          for ux, uy, uw, uh in unique)
            if not duplicate:
                unique.append((x, y, w, h))
        return unique
    
    def score_candidate(self, gray, x, y, w, h):
        if x < 0 or y < 0 or x+w >= gray.shape[1] or y+h >= gray.shape[0]:
            return 0
        
        region = gray[y:y+h, x:x+w]
        brightness = np.mean(region)
        aspect_ratio = w / h
        area = w * h
        
        score = 0
        if 2.0 <= aspect_ratio <= 6.0:
            score += 30
        if 140 <= brightness <= 220:
            score += 30
        if 400 <= area <= 10000:
            score += 20
        
        edges = cv2.Canny(region, 50, 150)
        if np.sum(edges > 0) > 50:
            score += 20
        
        return score
    
    def preprocess_for_ocr(self, plate_image):
        h, w = plate_image.shape[:2]
        scale = max(6, 240 // max(w, h))
        enlarged = cv2.resize(plate_image, (w*scale, h*scale), interpolation=cv2.INTER_CUBIC)
        
        gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY) if len(enlarged.shape) == 3 else enlarged
        
        denoised = cv2.bilateralFilter(gray, 9, 75, 75)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        _, otsu = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        adaptive = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        if np.mean(otsu) < 127:
            otsu = cv2.bitwise_not(otsu)
        if np.mean(adaptive) < 127:
            adaptive = cv2.bitwise_not(adaptive)
        
        kernel = np.ones((2, 2), np.uint8)
        otsu_clean = cv2.morphologyEx(otsu, cv2.MORPH_CLOSE, kernel)
        adaptive_clean = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)
        
        return otsu_clean, adaptive_clean
    
    def perform_ocr(self, processed_images):
        otsu_img, adaptive_img = processed_images
        
        configs = [
            '--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789',
            '--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789', 
            '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789',
            '--oem 3 --psm 13 -c tessedit_char_whitelist=0123456789',
            '--oem 1 --psm 8 -c tessedit_char_whitelist=0123456789',
            '--oem 1 --psm 7 -c tessedit_char_whitelist=0123456789'
        ]
        
        best_result = ""
        best_score = 0
        
        for img in [otsu_img, adaptive_img]:
            for config in configs:
                text = pytesseract.image_to_string(img, config=config, lang='eng').strip()
                digits = ''.join(re.findall(r'\d', text))
                
                if digits:
                    score = len(digits) * 10
                    if 6 <= len(digits) <= 8:
                        score += 50
                    if len(set(digits)) > 2:
                        score += 30
                    
                    if score > best_score:
                        best_result = digits
                        best_score = score
        
        return best_result
    
    def process_image(self, image_path):
        image = cv2.imread(image_path)
        binary_images = self.preprocess_image(image)
        candidates = self.find_candidates(binary_images)
        
        valid_results = []
        for i, (x, y, w, h) in enumerate(candidates):
            score = self.score_candidate(binary_images[0], x, y, w, h)
            if score >= 50:
                plate_region = image[y:y+h, x:x+w]
                cv2.imwrite(f"plate_{i+1}.jpg", plate_region)
                
                ocr_images = self.preprocess_for_ocr(plate_region)
                digits = self.perform_ocr(ocr_images)
                
                if digits and 6 <= len(digits) <= 8 and len(set(digits)) > 2:
                    valid_results.append(digits)
        
        with open("plates.txt", 'w') as f:
            for i, result in enumerate(valid_results):
                f.write(f"Plate {i+1}: {result}\n")
        
        return valid_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="carplate_hw2.jpg")
    args = parser.parse_args()
    
    detector = LicensePlateDetector()
    results = detector.process_image(args.input)
    
    print(f"Detected {len(results)} plates: {results}")
    return 0 if results else 1

if __name__ == "__main__":
    exit(main())
