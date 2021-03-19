from typing import NamedTuple

class Old_tuple(NamedTuple):
    mark: str
    model: str
    date: str
    miliage: int
    link: str
    year: int
    price: int


class SheetAPI:
    def __init__(self, values: list):
        self.__data_from_sheet = values
        self.__current_data = {}
        self.__data_to_upload = []
        self.__mark_density = []
        self.i_ = 0
        for items in self.__data_from_sheet:
            self.__current_data[self.i_]= Old_tuple(
                mark=items[0],
                model=items[1],
                date=items[2],
                miliage=items[3],
                link=items[4],
                year=items[5],
                price=items[6],
            )
            self.i_ +=1


    def get_unique_model(self) -> list:
        for value in self.__current_data.values():
            self.__data_to_upload.append([
                value.mark,
                value.model,
            ])
        self.__temp_list = []
        for item in self.__data_to_upload:
            if item not in self.__temp_list:
                self.__temp_list.append(item)
        self.__data_to_upload = self.__temp_list


    def get_avg_values(self):
        SheetAPI.get_unique_model(self)

        for car in self.__data_to_upload:
            car_count = 0
            model_count = 0
            car_price = 0
            car_year = 0
            model_density = 0
            for value in self.__current_data.values():
                if car[0] == value.mark:
                    car_count += 1
                    if car[1] == value.model:
                        model_count += 1
                        car_price += int(value.price)
                        car_year += int(value.year)
            car_price /= model_count
            car_year /= model_count
            model_density = str(round((model_count * 100) / len(self.__current_data), 2)) + "%"
            car_count = str(round(car_count * 100 / len(self.__current_data), 2)) + "%"
            car.append(model_count)
            car.append(int(car_price))
            car.append(int(car_year))
            car.append(model_density)
            mark_density = [car[0], car_count]
            if mark_density not in self.__mark_density:
                self.__mark_density.append(mark_density)
        return self.__data_to_upload, self.__mark_density


