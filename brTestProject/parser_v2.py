import asyncio
import aiohttp
from lxml import html
from loader import uload_to_spreadsheet
from settings import URL, HEADERS, CARS
from sheetapi import SheetAPI

def check_miliage(miliage):
    if miliage.strip() == "без пробега":
        return "0"
    else:
        for digit in miliage.split(" "):
            if digit.isdigit():
                return "".join(digit)

def filter_year(years):
    return [year for year in years if year != ' ']

def parse_page(dom_tree):
    mark = dom_tree.xpath('//span[contains(@class, "blue bold")]/text()')
    year = filter_year(dom_tree.xpath('//a[contains(@class, "address")]/text()'))
    date = dom_tree.xpath('//div[contains(@class, "footer_ticket")]/span/@title')
    link = dom_tree.xpath('//a[contains(@class, "m-link-ticket")]/@href')
    price = dom_tree.xpath('//span[contains(@data-currency, "USD")]/text()')
    miliage = dom_tree.xpath('//li[contains(@class, "item-char js-race")]/text()')
    cars = []
    for car in range(len(mark)):
        cars.append([
            mark[car].split(" ")[0],
            " ".join(mark[car].split(" ")[1:3]) if "Land" in mark[car].split(" ")[1] or "Passat" in
                                                   mark[car].split(" ")[1] else mark[car].split(" ")[1].strip(),
            date[car].split(" ")[-1].strip(),
            check_miliage(miliage[car]),
            link[car],
            year[car].strip(),
            price[car].replace(" ","")
        ])

    print(len(CARS))
    return cars

async def parser(url):

    async with aiohttp.ClientSession() as session:
        page_count = 0
        content = ['s']
        while content:
            async with session.get(url + '&page=' + str(page_count), headers=HEADERS) as response:
                html_code = await response.text()
            if response.status == 200:
                dom_tree = html.fromstring(html_code)
                content = parse_page(dom_tree)
                CARS.extend(content)
                page_count += 1
            else:
                break

async def main():
    tasks = []
    for url in URL:
        task = asyncio.Task(parser(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    sheet = SheetAPI(CARS)
    data_to_upload, mark_density = sheet.get_avg_values()
    print("Загрузка в гугл таблицы")
    CARS.append(['Марка', 'Модель', 'Дата публикации', 'Пробег тыс. км.', 'Ссылка', 'Год выпуска', 'Цена в $'])
    CARS.reverse()
    uload_to_spreadsheet("Лист1!A", CARS)

    data_to_upload.sort()
    data_to_upload.reverse()
    data_to_upload.append(["Марка", "Модель", "Кол-во объявлений по данной модели", "Средняя цена в $", "Средний возраст","Удельный вес по данной модели"])
    data_to_upload.reverse()
    uload_to_spreadsheet("Лист2!A", data_to_upload)

    mark_density.append(['Удельный вес по марке'])
    mark_density.reverse()
    uload_to_spreadsheet("Лист2!G", mark_density, end_sheet=0)