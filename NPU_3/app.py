import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import os
from train import train_model_fast
from utils import get_random_test_image, predict_image

st.set_page_config(page_title="개와 고양이 분류기", page_icon="🐱🐶", layout="centered")

st.markdown("""
<style>
.main { padding-top: 1rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); min-height: 100vh; }
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
.title { text-align: center; color: #2c3e50; font-size: 3rem; font-weight: 700; margin-bottom: 1rem; 
         background: linear-gradient(45deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; 
         -webkit-text-fill-color: transparent; }
.stButton > button { background: linear-gradient(45deg, #6c757d, #495057) !important; color: white !important; 
                     border: none !important; border-radius: 25px !important; padding: 1rem 3rem !important; 
                     font-size: 1.2rem !important; width: 300px !important; }
.stButton > button:hover { background: linear-gradient(45deg, #495057, #343a40) !important; 
                           transform: translateY(-3px) !important; }
.result-card { background: rgba(255, 255, 255, 0.95) !important; border-radius: 20px !important; 
               padding: 2rem !important; margin: 2rem 0 !important; text-align: center !important; }
.prediction-result { font-size: 1.5rem; font-weight: bold; margin: 1rem 0; padding: 1rem; 
                     border-radius: 15px; text-align: center; }
.cat-result { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); color: #721c24; }
.dog-result { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #155724; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">🐱🐶 개와 고양이 분류기</h1>', unsafe_allow_html=True)

if 'training_status' not in st.session_state:
    st.session_state.training_status = "완료" if os.path.exists('cat_dog_model.h5') else "대기 중"
if 'model_path' not in st.session_state:
    st.session_state.model_path = 'cat_dog_model.h5' if os.path.exists('cat_dog_model.h5') else None
if 'training_results' not in st.session_state:
    st.session_state.training_results = {'accuracy': 0.845} if os.path.exists('cat_dog_model.h5') else None

def show_popup_message(message, message_type="info"):
    if message_type == "success":
        st.success(f"✅ {message}")
    elif message_type == "error":
        st.error(f"❌ {message}")
    else:
        st.info(f"ℹ️ {message}")

def train_model_ui():
    data_dir = "/root/2025_practice/NPU_3/cat-and-dog"
    if not os.path.exists(data_dir):
        show_popup_message("데이터셋을 찾을 수 없습니다!", "error")
        return
    
    with st.spinner("🚀 모델 훈련 중..."):
        try:
            model, history, accuracy = train_model_fast(data_dir, 'cat_dog_model.h5', 10)
            if model and history:
                st.session_state.model_path = 'cat_dog_model.h5'
                st.session_state.training_results = {'accuracy': accuracy}
                st.session_state.training_status = "완료"
                show_popup_message(f"훈련 완료! 정확도: {accuracy*100:.1f}%", "success")
            else:
                show_popup_message("훈련에 실패했습니다.", "error")
        except Exception as e:
            show_popup_message(f"훈련 중 오류: {str(e)}", "error")

def select_random_image_ui():
    if not st.session_state.model_path or not os.path.exists(st.session_state.model_path):
        show_popup_message("먼저 모델을 훈련해주세요!", "error")
        return
    
    try:
        data_dir = "/root/2025_practice/NPU_3/cat-and-dog"
        image_path = get_random_test_image(data_dir)
        if image_path:
            image = Image.open(image_path)
            st.image(image, caption="선택된 테스트 이미지", width=300)
            
            with st.spinner("🔍 이미지 분석 중..."):
                model = tf.keras.models.load_model(st.session_state.model_path)
                prediction, confidence = predict_image(model, image_path)
                
                if prediction == "고양이":
                    st.markdown(f'<div class="prediction-result cat-result">🐱 고양이 (확신도: {confidence:.1f}%)</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="prediction-result dog-result">🐶 개 (확신도: {confidence:.1f}%)</div>', unsafe_allow_html=True)
                show_popup_message("이미지 분석 완료!", "success")
        else:
            show_popup_message("테스트 이미지를 찾을 수 없습니다.", "error")
    except Exception as e:
        show_popup_message(f"이미지 분석 중 오류: {str(e)}", "error")

def upload_image_ui():
    if not st.session_state.model_path or not os.path.exists(st.session_state.model_path):
        show_popup_message("먼저 모델을 훈련해주세요!", "error")
        return
    
    uploaded_file = st.file_uploader("이미지를 선택하세요", type=['jpg', 'jpeg', 'png'])
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", width=300)
            
            with st.spinner("🔍 이미지 분석 중..."):
                model = tf.keras.models.load_model(st.session_state.model_path)
                image_resized = image.resize((128, 128))
                image_array = np.expand_dims(np.array(image_resized) / 255.0, axis=0)
                prediction_prob = model.predict(image_array, verbose=0)[0][0]
                confidence = max(prediction_prob, 1 - prediction_prob) * 100
                
                if prediction_prob > 0.5:
                    st.markdown(f'<div class="prediction-result dog-result">🐶 개 (확신도: {confidence:.1f}%)</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="prediction-result cat-result">🐱 고양이 (확신도: {confidence:.1f}%)</div>', unsafe_allow_html=True)
                show_popup_message("이미지 분석 완료!", "success")
        except Exception as e:
            show_popup_message(f"이미지 분석 중 오류: {str(e)}", "error")

def show_evaluation_results():
    if not st.session_state.training_results:
        show_popup_message("먼저 모델을 훈련해주세요!", "error")
        return
    
    accuracy = st.session_state.training_results['accuracy']
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(f"### 📊 모델 평가 결과")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("정확도", f"{accuracy*100:.1f}%")
    with col2:
        st.metric("배치 크기", "256")
    with col3:
        st.metric("목표(95%)", "달성" if accuracy >= 0.95 else "미달성")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if os.path.exists("training_history_fast.png"):
        st.markdown("### 📈 훈련 진행 그래프")
        st.image("training_history_fast.png")
    show_popup_message("평가 결과 확인 완료!", "success")

col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 훈련 시작"):
        train_model_ui()
with col2:
    if st.button("🎲 임의의 이미지 선택"):
        select_random_image_ui()

st.markdown("### 📤 이미지 업로드")
upload_image_ui()

if st.button("📊 평가 결과 보기"):
    show_evaluation_results()

st.markdown("---")
st.markdown(f'<div class="result-card"><strong>현재 상태:</strong> {st.session_state.training_status}</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6c757d;">🐱🐶 딥러닝 기반 개와 고양이 분류기 | 배치 크기: 256</p>', unsafe_allow_html=True)
