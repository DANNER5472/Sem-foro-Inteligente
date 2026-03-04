# 🚦 Semaforo Inteligente con IA

Sistema de control de semáforo inteligente usando YOLOv8 y OpenCV.

## 📋 Requisitos
- Python 3.11
- pip

## 📦 Instalación

1. Clona o descarga el proyecto

2. Instala las dependencias:
pip install ultralytics==8.4.14 opencv-python==4.13.0.90 numpy==2.4.2

3. Descarga un video de tráfico desde:
https://www.pexels.com/search/videos/traffic/

4. Renómbralo a trafico.mp4 y ponlo en la carpeta video/

## 🚀 Ejecutar
python main.py

## ⌨️ Controles
- Presiona Q para salir

## 📁 Estructura del proyecto
semaforo_ia/
├── main.py
├── detector.py  
├── controlador.py
├── requirements.txt
└── video/
    └── trafico.mp4
```

Y también crea el `requirements.txt`:
```
ultralytics==8.4.14
opencv-python==4.13.0.90
numpy==2.4.2