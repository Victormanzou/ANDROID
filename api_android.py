# Dentro de api_android.py
from fastapi import FastAPI
from control_costos import calcular_margen # Usas lo que ya hiciste

app = FastAPI()

@app.post("/escanear")
def procesar_producto(codigo: str):
    # Aquí llamas a tu lógica de "Quitar duplicados" 
    # y devuelves el resultado a la App
    return {"resultado": "Producto limpio"}