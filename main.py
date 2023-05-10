import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
    # products - список продуктов
    # id - номер товара
    # name - наименование
    # provider - поставщик
    # price - цена
    # date - дата производства
    # expiration - годен до
    # weight - вес
    # count - число единиц товара
products = [{
    "id": 0,
    "name": "Яблоки",
    "provider": "Яблочное село",
    "price": 78.90,
    "date": "17062022",
    "expiration": "18062022",
    "weight": 0.789,
    "count": 7
}, {
    "id": 1,
    "name": "Груша",
    "provider": "Грушевое село",
    "price": 40.00,
    "date": "15062022",
    "expiration": "25062022",
    "weight": 1.1,
    "count": 14
}, {
    "id": 2,
    "name": "Лапша",
    "provider": "Лапшинино",
    "price": 103.34,
    "date": "10062022",
    "expiration": "11082022",
    "weight": 0.62,
    "count": 5
}, {
    "id": 3,
    "name": "Рис",
    "provider": "Рисово",
    "price": 61.90,
    "date": "06062022",
    "expiration": "17112022",
    "weight": 1.0,
    "count": 11
}, {
    "id": 4,
    "name": "Масло",
    "provider": "Маслово",
    "price": 150.62,
    "date": "27052022",
    "expiration": "03082022",
    "weight": 1.5,
    "count": 6
}, {
    "id": 5,
    "name": "Яблоко",
    "provider": "Айдаред",
    "price": 130.00,
    "date": "01062022",
    "expiration": "25062022",
    "weight": 2.4,
    "count": 10
}, {
    "id": 6,
    "name": "Чипсы",
    "provider": "Лэйс",
    "price": 64.50,
    "date": "10052022",
    "expiration": "11082022",
    "weight": 0.60,
    "count": 4
}]


# перенос веб-приложения flask, использующего веб-сервер uWSGI, на веб-сервер ASGI (uvicorn)
app = FastAPI()
@app.post("/docs", status_code=200, description="Описание интерфейса")
def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url=app.openapi_url,title="Swagger UI")


# Добавление пользовательского интерфейса Swagger в app
@app.get("/find_name", status_code=200, description="Поиск по названию")
def find_name_(name: str = None):
    if name:
        for i in range(len(products)):
            if name == products[i]["name"]:
                return ">>>", products[i]
    return "не найдено"


@app.get("/api/status", status_code=200, description="Поиск минимального, максимального или среднего для числовых полей. Укажите min/max/average")

async def min_max_average(weight: str = None, count: str = None, price: str = None):
    empty_list = [] # Создаем пустой список, куда будем сохранять значения
    # Каждое поле заполнять не обязательно, поэтому проверяем на наличие значений
    if price:
        _are = []
        for i in range(len(products)):
            _are.append(products[i]["price"]) # Заполняем пустой списо _are значениями цены из products

        if price == "min":
            empty_list.append({"price": min(_are)})
        if price == "max":
            empty_list.append({"price": max(_are)})
        if price == "average":
            empty_list.append({"price": sum(_are) / len(_are)})

    if count:
        _are = []
        for i in range(len(products)):
            _are.append(products[i]["count"])

        if count == "min":
            empty_list.append({"count": min(_are)})
        if count == "max":
            empty_list.append({"count": max(_are)})
        if count == "average":
            empty_list.append({"count": sum(_are) / len(_are)})

    if weight:
        _are = []
        for i in range(len(products)):
            _are.append(products[i]["weight"])

        if weight == "min":
            empty_list.append({"weight": min(_are)})
        if weight == "max":
            empty_list.append({"weight": max(_are)})
        if weight == "average":
            empty_list.append({"weight": sum(_are) / len(_are)})

    return empty_list

@app.put("/api/change", status_code=200, description="Изменить данные о товаре")
async def changing(id: int, name: str = None, provider: str = None,
price: float = None, date: int = None, expiration: int = None, weight: float = None, count: float = None):
    global products
    # Ввод id обязателен
    for i in range(len(products)):
        if products[i]["id"] == id:
            # Проверяем каждый параметр товара на наличие значения, если оно имеется, то изменяем
            if name:
                products[i]['name'] = name
            if provider:
                products[i]['provider'] = provider
            if price:
                products[i]['price'] = price
            if date:
                products[i]['date'] = date
            if expiration:
                products[i]['expiration'] = expiration
            if weight:
                products[i]['weight'] = weight
            if count:
                products[i]['count'] = count
            return {">>>": "Данные изменены"}
    return {">>>": "Товар не найден"}


@app.put("/api/add", status_code=200, description="Добавить товар. Необходимо ввести все параметры товара")
async def adding(id: int, name: str, provider: str, price: float, date: int, expiration: int, weight: float,
count: float): # Получаем на вход все параметры товара
    global products # Объявляем products глобально, чтобы ее обновления вступали в силу и вне функции
    products.append({"id": id,
            "name": name,
            "provider": provider,
            "price": price,
            "date": date,
            "expiration": expiration,
            "weight": weight,
            "count": count})
    return {">>>": "Товар добавлен"}


@app.delete("/api/delete", status_code=200, description="Удалить товар по id")
async def del_id(id: int):
    global products
    for i in range(len(products)):
        if products[i]["id"] == id:
            products.pop(i) # Функция, которая удаляет из списка значение по заданному индексу
            return {">>>": "Товар удален"}
    return {">>>": "Товар не найден"}


@app.get("/api/find", status_code=200, description="Найти товар по id. Введите all чтобы показать все товары")
async def find_id(id: str): # Получим на вход id в виде строки
    if id == "all": # Если пользователь хочет вывести все товары
        _are = {" ": []} # Создаем еще один список, чтобы вывести все единицы товара
        for i in range(len(products)):
            _are[" "].append(products[i])
        return _are
    else:
        for i in range(len(products)):
            if products[i]["id"] == int(id): # Ищем товар, с id, которое было указано и выводим его
                return {">>>": products[int(id)]}
    return {">>>": "Товар не найден"}

    if __name__ == "__main__":
        uvicorn.run(app, host="127.0.0.1", port=5000) # port 8000 нужен, чтобы не было пересечений ссылок
# Запуск приложения, как веб-сервер ASG