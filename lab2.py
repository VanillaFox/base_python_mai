# Напоминание: вам понадобится материал лекций:
# 3 - Списки и кортежи
# 4 - Словари и множества
# 5 - Функции
# 9 - Работа с файлами

# =====================================
# ЗАДАНИЕ 1: Работа с файлами
# =====================================
# TODO 1-1
#  Прочитайте данные из файла pilot_path.json (лекция 9)

# ВАШ КОД:
import json

with open("data/pilot_path.json", "r") as fp:
    file_data = json.load(fp)

# =====================================
# ЗАДАНИЕ 2: Расчет статистик
# =====================================
# TODO 2-1) Подсчитайте, сколько миссий налетал каждый пилот. Выведите результат в порядке убывания миссий
# ИНФОРМАЦИЯ:
# структура данных в файле: {"имя_пилота": "список_миссий":[миссия1, ...]]
# структура одной миссии: {"drone":"модель_дрона", "mission":[список точек миссии]}
# у пилотов неодинаковое количество миссий (и миссии могут быть разной длины). у каждой миссии - произвольная модель дрона

# РЕЗУЛЬТАТ:
# Пилоты в порядке убывания количества миссий: {'pilot1': 1, 'pilot4': 2, 'pilot9': 3, 'pilot5': 3, 'pilot7': 4, 'pilot6': 5, 'pilot2': 5, 'pilot3': 6, 'pilot8': 6}

# ВАШ КОД:
count_missions_by_pilots = {k: len(v["missions"]) for k, v in file_data.items()}
print(
    f"Пилоты в порядке убывания количества миссий: {dict(sorted(count_missions_by_pilots.items(), key=lambda item: item[1]))}"
)

# TODO 2-2) Получите и выведите список всех моделей дронов, которые были в файле pilot_path.json
# Подсказка: внутри print используйте str.join(), чтобы соединить элементы списка (множества)

# ПРИМЕР РЕЗУЛЬТАТА:
# Полеты совершались на дронах следующих моделей: DJI Mavic 2 Pro, DJI Mavic 3, DJI Inspire 2, DJI Mavic 2 Zoom, DJI Mavic 2 Enterprise Advanced

# ВАШ КОД:
drones = set()
for _, missions in file_data.items():
    for mission in missions["missions"]:
        drones.add(mission["drone"])

# вывод результата (допишите код)
print(f'Полеты совершались на дронах следующих моделей: {", ".join(drones)}')

# TODO 2-3) Получите список миссий для каждой модели дронов, которые были в файле pilot_path.json,
# и выведите на экран модель дрона и количество миссий, которые он отлетал

# ПРИМЕР РЕЗУЛЬТАТА:
# Дрон DJI Inspire 2 отлетал 6 миссий
# Дрон DJI Mavic 2 Pro отлетал 6 миссий
# Дрон DJI Mavic 2 Enterprise Advanced отлетал 10 миссий
# Дрон DJI Mavic 3 отлетал 4 миссий
# Дрон DJI Mavic 2 Zoom отлетал 9 миссий

# ВАШ КОД:
drones_missions = dict()
for _, missions in file_data.items():
    for mission in missions["missions"]:
        drone = mission["drone"]
        drones_missions[drone] = (
            drones_missions[drone] + 1 if drones_missions.get(drone) is not None else 1
        )
# вывод результата (допишите код)
for drone, count in drones_missions.items():
    print(f"Дрон {drone} отлетал {count} миссий")

# TODO 3) Оформите задания из TODO 1 и 2 в виде функций
# ВАШ КОД:


def read_json_file(filename):
    with open(filename, "r") as fp:
        file_data = json.load(fp)
    return file_data


def sorted_count_missions_by_pilots(json_data):
    count_missions_by_pilots = {k: len(v["missions"]) for k, v in json_data.items()}
    return dict(sorted(count_missions_by_pilots.items(), key=lambda item: item[1]))


def get_drones_list(json_data):
    drones = set()
    for _, missions in json_data.items():
        for mission in missions["missions"]:
            drones.add(mission["drone"])
    return list(drones)


def count_missions_by_drone(json_data):
    drones_missions = dict()
    for _, missions in file_data.items():
        for mission in missions["missions"]:
            drone = mission["drone"]
            drones_missions[drone] = (
                drones_missions[drone] + 1
                if drones_missions.get(drone) is not None
                else 1
            )
    return drones_missions


file_data = read_json_file("data/pilot_path.json")
print(
    f"Пилоты в порядке убывания количества миссий: {sorted_count_missions_by_pilots(file_data)}"
)
print(
    f'Полеты совершались на дронах следующих моделей: {", ".join(get_drones_list(file_data))}'
)
for drone, count in count_missions_by_drone(file_data).items():
    print(f"Дрон {drone} отлетал {count} миссий")