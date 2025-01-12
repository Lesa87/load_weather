# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import pyodbc
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime, timedelta

# Конфигурация
API_KEY = 'b356018cc648fdb86d4b9ba38a1fc450' #leska.pak@gmail.com
#API_KEY = '8e121adcbc9d5a617aef3447528d7286' #leska_pak@mail.ru
CITIES = ['Almaty', 'Astana', 'Kokshetau', 'Kostanay', 'Kyzylorda', 'Pavlodar', 'Semey', 'Taldykorgan', 'Taraz', 'Ekibastuz']
SQL_SERVER = 'ANPCBOOK\SQLEXPRESS'
DATABASE = 'testDB'
USERNAME = 'userLena'
PASSWORD = 'Ok123456'

# Функция для получения данных по погоде
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    weather = {
        'city': city,
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'datetime': datetime.utcfromtimestamp(data['dt'])
    }
    return weather

# Подключение к MS SQL Server
def connect_to_db():
    conn_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}"
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_str}")
    return engine

# Сохранение данных в базу данных
def save_to_db(engine, data):
    df = pd.DataFrame([data])
    df.to_sql('weather', con=engine, if_exists='append', index=False)

def main():
    engine = connect_to_db()
    #print(engine)
    for city in CITIES:
        weather_data = get_weather_data(city)
        ##print(weather_data)
        save_to_db(engine, weather_data)
        print(f"Data for {city} saved to database")

if __name__ == "__main__":
    main()


