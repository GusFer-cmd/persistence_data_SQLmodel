from sqlmodel import Session
from datetime import datetime
from app.core.database import engine
from app.models.models import Owner, Manufacturer, Serie, Car, Collection, CarSerieLink, CollectionCarLink

def run_seed():
    with Session(engine) as session:

        # ======================
        # OWNERS
        # ======================
        owners = [
            Owner(name="Gustavo Fernandes", email="gustavo@email.com"),
            Owner(name="Lucas Silva", email="lucas@email.com"),
            Owner(name="Mariana Costa", email="mariana@email.com"),
        ]
        session.add_all(owners)
        session.commit()

        o = {owner.name: owner for owner in owners}

        # ======================
        # MANUFACTURERS
        # ======================
        manufacturers = [
            Manufacturer(name="Ferrari", country="Italy"),
            Manufacturer(name="Volkswagen", country="Germany"),
            Manufacturer(name="Audi", country="Germany"),
            Manufacturer(name="Nissan", country="Japan"),
            Manufacturer(name="Toyota", country="Japan"),
            Manufacturer(name="Porsche", country="Germany"),
            Manufacturer(name="BMW", country="Germany"),
            Manufacturer(name="Lamborghini", country="Italy"),
            Manufacturer(name="McLaren", country="UK"),
            Manufacturer(name="Ford", country="USA"),
        ]
        session.add_all(manufacturers)
        session.commit()

        m = {m.name: m for m in manufacturers}

        # ======================
        # SERIES
        # ======================
        series = [
            Serie(name="HW Exotics", year=2023),
            Serie(name="HW Exotics", year=2024),
            Serie(name="Art Cars", year=2023),
            Serie(name="Art Cars", year=2024),
            Serie(name="HW J-Imports", year=2023),
            Serie(name="HW J-Imports", year=2024),
            Serie(name="HW Speed Graphics", year=2024),
            Serie(name="HW Factory Fresh", year=2023),
            Serie(name="HW Factory Fresh", year=2024),
        ]
        session.add_all(series)
        session.commit()

        s = {(x.name, x.year): x for x in series}

        # ======================
        # CARS
        # ======================
        cars = [
            Car(name="Ferrari 488 GTB", scale="1:64", color="Red", manufacturer_id=m["Ferrari"].id),
            Car(name="Ferrari SF90 Stradale", scale="1:64", color="Yellow", manufacturer_id=m["Ferrari"].id),
            Car(name="Lamborghini Huracán", scale="1:64", color="Green", manufacturer_id=m["Lamborghini"].id),
            Car(name="Lamborghini Aventador", scale="1:64", color="Orange", manufacturer_id=m["Lamborghini"].id),
            Car(name="Porsche 911 GT3", scale="1:64", color="White", manufacturer_id=m["Porsche"].id),
            Car(name="Porsche Taycan", scale="1:64", color="Silver", manufacturer_id=m["Porsche"].id),
            Car(name="Nissan Skyline R34", scale="1:64", color="Blue", manufacturer_id=m["Nissan"].id),
            Car(name="Nissan Silvia S15", scale="1:64", color="Purple", manufacturer_id=m["Nissan"].id),
            Car(name="Toyota Supra MK4", scale="1:64", color="Orange", manufacturer_id=m["Toyota"].id),
            Car(name="Toyota GR86", scale="1:64", color="Black", manufacturer_id=m["Toyota"].id),
            Car(name="Audi R8 LMS", scale="1:64", color="Black", manufacturer_id=m["Audi"].id),
            Car(name="Audi RS6 Avant", scale="1:64", color="Gray", manufacturer_id=m["Audi"].id),
            Car(name="BMW M3 E46", scale="1:64", color="Blue", manufacturer_id=m["BMW"].id),
            Car(name="BMW M4 G82", scale="1:64", color="Green", manufacturer_id=m["BMW"].id),
            Car(name="Ford Mustang GT", scale="1:64", color="Red", manufacturer_id=m["Ford"].id),
            Car(name="McLaren 720S", scale="1:64", color="Orange", manufacturer_id=m["McLaren"].id),
        ]
        session.add_all(cars)
        session.commit()

        c = {car.name: car for car in cars}

        # ======================
        # CAR ↔ SERIE
        # ======================
        links = [
            (c["Ferrari 488 GTB"], s[("HW Exotics", 2023)], 1, 10),
            (c["Ferrari SF90 Stradale"], s[("HW Exotics", 2024)], 2, 10),
            (c["Lamborghini Huracán"], s[("HW Exotics", 2023)], 3, 10),
            (c["Lamborghini Aventador"], s[("HW Exotics", 2024)], 4, 10),
            (c["Porsche 911 GT3"], s[("HW Factory Fresh", 2023)], 5, 12),
            (c["Porsche Taycan"], s[("HW Factory Fresh", 2024)], 6, 12),
            (c["Nissan Skyline R34"], s[("HW J-Imports", 2024)], 1, 8),
            (c["Nissan Silvia S15"], s[("HW J-Imports", 2023)], 2, 8),
            (c["Toyota Supra MK4"], s[("Art Cars", 2023)], 7, 12),
            (c["Toyota GR86"], s[("Art Cars", 2024)], 3, 12),
        ]

        session.add_all([
            CarSerieLink(
                car_id=car.id,
                serie_id=serie.id,
                number=num,
                max_number=maxn
            )
            for car, serie, num, maxn in links
        ])
        session.commit()

        # ======================
        # COLLECTIONS (1 por owner)
        # ======================
        collections = [
            Collection(name="Coleção do Gustavo", title="Premium Exotics", owner_id=o["Gustavo Fernandes"].id),
            Collection(name="Coleção do Lucas", title="JDM Lovers", owner_id=o["Lucas Silva"].id),
            Collection(name="Coleção da Mariana", title="Factory Fresh", owner_id=o["Mariana Costa"].id),
        ]
        session.add_all(collections)
        session.commit()

        col = {c.name: c for c in collections}

        # ======================
        # COLLECTION ↔ CAR
        # ======================
        session.add_all([
            # Gustavo
            CollectionCarLink(collection_item_id=col["Coleção do Gustavo"].id, car_id=c["Ferrari 488 GTB"].id, added_date=datetime.now()),
            CollectionCarLink(collection_item_id=col["Coleção do Gustavo"].id, car_id=c["Lamborghini Aventador"].id, added_date=datetime.now()),
            CollectionCarLink(collection_item_id=col["Coleção do Gustavo"].id, car_id=c["Porsche 911 GT3"].id, added_date=datetime.now()),

            # Lucas
            CollectionCarLink(collection_item_id=col["Coleção do Lucas"].id, car_id=c["Nissan Skyline R34"].id, added_date=datetime.now()),
            CollectionCarLink(collection_item_id=col["Coleção do Lucas"].id, car_id=c["Toyota Supra MK4"].id, added_date=datetime.now()),
            CollectionCarLink(collection_item_id=col["Coleção do Lucas"].id, car_id=c["Nissan Silvia S15"].id, added_date=datetime.now()),

            # Mariana
            CollectionCarLink(collection_item_id=col["Coleção da Mariana"].id, car_id=c["Audi RS6 Avant"].id, added_date=datetime.now()),
            CollectionCarLink(collection_item_id=col["Coleção da Mariana"].id, car_id=c["BMW M4 G82"].id, added_date=datetime.now()),
            CollectionCarLink(collection_item_id=col["Coleção da Mariana"].id, car_id=c["Porsche Taycan"].id, added_date=datetime.now()),
        ])
        session.commit()

        print("Banco populado com sucesso!")

if __name__ == "__main__":
    run_seed()
