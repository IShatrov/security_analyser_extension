import pickle
import pandas as pd
import numpy as np
import joblib
from IPython.display import display, clear_output
import ipywidgets as widgets
import warnings
warnings.filterwarnings('ignore')

# ========== ЗАГРУЗКА МОДЕЛИ ==========
print("🔄 Загрузка модели...")

try:
    # Загружаем модель и векторизатор
    model = joblib.load('url_model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')

    print(f"✓ Модель загружена: {type(model).__name__}")
    print(f"✓ Векторизатор загружен: {type(vectorizer).__name__}")
    print("="*70)

except FileNotFoundError as e:
    print(f"❌ Файл не найден: {e}")
    print("Убедитесь, что файлы 'url_model.pkl' и 'vectorizer.pkl' находятся в текущей директории")
    raise
except Exception as e:
    print(f"❌ Ошибка загрузки: {e}")
    raise

# ========== ФУНКЦИЯ ПРЕДСКАЗАНИЯ ==========
def predict_url(url):
    """Предсказывает безопасность URL"""
    try:
        # Векторизация URL
        url_vector = vectorizer.transform([url])

        # Предсказание
        prediction = model.predict(url_vector)[0]

        # Вероятности (если доступны)
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(url_vector)[0]
            classes = model.classes_
            prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        else:
            prob_dict = {prediction: 1.0}

        return prediction, prob_dict, None

    except Exception as e:
        return None, None, f"Ошибка предсказания: {str(e)}"

url = "https://inoriginal.net/series/486-avatar-last-airbender-2004.html"
prediction, probabilities, error = predict_url(url)
print(prediction, "/", probabilities['safe'],"/", error)