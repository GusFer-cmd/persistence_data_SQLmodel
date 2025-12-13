from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.routers import owners, manufacturers, cars, series, collections, carsLink, seriesLink

app = FastAPI(
    title="HotWheels API",
    description="API para gestão de coleções HotWheels",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(owners.router)
app.include_router(manufacturers.router)
app.include_router(series.router)
app.include_router(cars.router)
app.include_router(collections.router)
app.include_router(carsLink.router)
app.include_router(seriesLink.router)