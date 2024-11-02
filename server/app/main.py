from fastapi import FastAPI
import app.api.endpoints as endpoints

app = FastAPI()

# Подключаем роуты
app.include_router(endpoints.router)
