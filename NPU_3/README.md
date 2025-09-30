# 🐱🐶 개와 고양이 분류기

딥러닝을 이용한 개와 고양이 이미지 분류 프로젝트입니다.

## 📁 파일 구조

- `app.py` - Streamlit 웹 애플리케이션
- `model.py` - CNN 모델 정의
- `train.py` - 모델 훈련 스크립트
- `utils.py` - 유틸리티 함수들

## 🚀 실행 방법

1. 필요한 패키지 설치:
```bash
pip install tensorflow streamlit matplotlib numpy pillow
```

2. 웹 앱 실행:
```bash
streamlit run app.py
```

## 📊 모델 정보

- **아키텍처**: 4층 CNN (Conv2D + BatchNormalization + MaxPooling2D)
- **입력 크기**: 128x128x3
- **배치 크기**: 256
- **목표 정확도**: 95%

## 🎯 주요 기능

- 🚀 모델 훈련 (10 에포크)
- 🎲 랜덤 이미지 테스트
- 📤 사용자 이미지 업로드
- 📊 훈련 결과 시각화
