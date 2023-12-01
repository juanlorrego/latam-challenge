import fastapi
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from pydantic import BaseModel
from model import DelayModel

app = fastapi.FastAPI()
model = DelayModel()

class InputData(BaseModel):
    # Define la estructura de los datos de entrada si es necesario
    pass

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }    

@app.post("/predict", status_code=200)
async def post_predict(data: dict) -> dict:
    # Validar la estructura del cuerpo de la solicitud
    if "flights" not in data or not isinstance(data["flights"], list):
        raise HTTPException(status_code=400, detail="Invalid request format")

    for flight in data["flights"]:
        # Validar los valores permitidos para TIPOVUELO
        if "TIPOVUELO" in flight and flight["TIPOVUELO"] not in ["N", "I"]:
            raise HTTPException(status_code=400, detail="Invalid TIPOVUELO value")

        # Validar los valores permitidos para MES
        if "MES" in flight and not 1 <= flight["MES"] <= 12:
            raise HTTPException(status_code=400, detail="Invalid MES value")

    try:
        features = model.preprocess(data)  # Asegúrate de que esta función coincida con tu lógica de preprocesamiento
        prediction = model.predict(features)
        return {"predict": prediction}
    except Exception as e:
        print(f"Error in post_predict: {e}")
        raise e