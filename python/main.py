from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import pickle
import pandas as pd
import numpy as np
import joblib
from IPython.display import display, clear_output
import ipywidgets as widgets
import warnings
warnings.filterwarnings('ignore')

app = FastAPI()

# Загрузка модели
print("Загрузка модели...")

try:
    model = joblib.load('python/url_model.pkl')
    vectorizer = joblib.load('python/vectorizer.pkl')

    print(f"Модель загружена: {type(model).__name__}")
    print(f"Векторизатор загружен: {type(vectorizer).__name__}")
    print("="*70)

except FileNotFoundError as e:
    print(f"Файл не найден: {e}")
    print("Убедитесь, что файлы 'url_model.pkl' и 'vectorizer.pkl' находятся в текущей директории")
    raise
except Exception as e:
    print(f"Ошибка загрузки: {e}")
    raise

# Функция предсказания
def predict_url(url):
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

class StringRequest(BaseModel):
    url_to_test: str

@app.post("/example")
async def double_string(request: StringRequest):

    url = request.url_to_test
    prediction, probabilities, error = predict_url(url)
    print("returning", prediction)
    return JSONResponse(
        content={
            "prediction": prediction,
            "probability": probabilities['safe']
        }
    )