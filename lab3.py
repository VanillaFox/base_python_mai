import json
import re
import csv
# В ЭТОМ ДЗ ВЫ БУДЕТЕ АНАЛИЗИРОВАТЬ ДАННЫЕ ОБ АВИАПРОИСШЕСТВИЯХ С УЧАСТИЕМ МОДЕЛЕЙ ДРОНОВ ИЗ ВАШИХ ИСХОДНЫХ ДАННЫХ В .JSON

# =====================================
# ЗАДАНИЕ 1: Создание классов
# =====================================
# Для вас уже написаны заготовки классов Aircraft и UAV
# TODO 1-1) Добавьте в класс UAV защищенный атрибут _=_missions (тип - список списков [[], []]), куда вы будете сохранять все миссии, которые отлетал беспилотник
# TODO 1-2) При помощи декоратора @property сделайте возможность чтения и записи миссий в этот атрибут (лекция 8)
# TODO 1-3) Создайте в классе UAV публичный метод count_missions, который возвращает количество миссий (лекция 7)
# TODO 1-4) Создайте класс MultirotorUAV - наследник классов Aircraft и UAV (лекция 7)

# ВАШ КОД (дополните то, что нужно в классах):
class Aircraft:
    def __init__(self, weight):
        self._weight = weight

class UAV:
    def __init__(self):
        self._has_autopilot = True
        self._missions = []

    # напишите код для декоратора атрибута _missions
    @property
    def missions(self):
        return self._missions
    
    @missions.setter
    def missions(self, value):
        self._missions = value

    # напишите публичный метод count_missions
    def count_missions(self):
        return len(self._missions)

class MultirotorUAV(Aircraft, UAV):
    def __init__(self, weight, model, brand):
        super().__init__(weight)
        UAV.__init__(self)
        self.__weight = weight
        self.__model = model
        self.__brand = brand
        self.__incidents = []

    # напишите публичный метод get_info
    def get_info(self):
        return {"weight":self.__weight, "brand": self.__brand, "count_missions": self.count_missions()}

    # напишите публичный метод get_model
    def get_model(self):
        return self.__model
    
    # напишите код декоратора для атрибута incidents. Не забудьте сначала добавить приватный атрибут в класс
    @property
    def incidents(self):
        return self.__incidents

    # напишите публичный метод add_incident, который добавляет инцидент в список инцидентов для данной модели дрона
    def add_incident(self, incident):
        self.__incidents.append(incident)
        
    def save_data(self):
        data = {
            "model": self.get_model(),
            "weight": self.get_info()['weight'],
            "manufacturer": self.get_info()['brand'],
            "missions": self.missions,
            "incidents": self.incidents
        }
        with open(f"{self.__class__.__name__}_{self.__model}.json", 'w') as file:
            json.dump(data, file, indent=4)
        

# =====================================
# ЗАДАНИЕ 2: Работа с экземплярами классов
# =====================================
# TODO 2-1) Создайте экземпляры класса MultirotorUAV для всех моделей дронов, которые были в файле pilot_path.json
# Подсказка: созданные экземпляры класса MultirotorUAV сохраните в список для последующего использования
# TODO 2-2) При создании каждого экземпляра задайте ему как приватные атрибуты массу и производителя из справочника дронов drone_catalog в соответствии с моделью дрона
# TODO 2-3) А также добавьте ему миссии, найденные для этой модели дрона на шаге 1-3
# Напоминание: миссии находятся в атрибуте missions (с декоратором, и поэтому он публично доступен) в классе UAV

# каталог дронов уже готов для вас:
drone_catalog = {
    "DJI Mavic 2 Pro": {"weight":903, "brand":"DJI"},
    "DJI Mavic 2 Zoom": {"weight":900, "brand":"DJI"},
    "DJI Mavic 2 Enterprise Advanced": {"weight":920, "brand":"DJI"},
    "DJI Inspire 2": {"weight":1500, "brand":"DJI"},
    "DJI Mavic 3": {"weight":1000, "brand":"DJI"}
}

# ВАШ КОД:
with open("data/pilot_path.json", "r") as fp:
    file_data = json.load(fp)
    
drones_missions = dict()
for _, missions in file_data.items():
    for mission in missions["missions"]:
        drone = mission["drone"]
        if drones_missions.get(drone) is None:
            drones_missions[drone] = [mission["mission"]]
        else:
            drones_missions[drone].append(mission["mission"])

multirotoruavs = []
for model, data in drone_catalog.items():
    multirotoruav = MultirotorUAV(model=model, **data)
    multirotoruav.missions = drones_missions[model]
    multirotoruavs.append(multirotoruav)


# TODO 2-4
# Напишите код, который выводит информацию по заданной модели дрона. Состав информации: масса, производитель, количество отлетанных миссий
# (название модели пользователь вводит с клавиатуры в любом регистре, но без опечаток)
# Подсказка: для этого вам необходимо добавить в класс два публичных метода: get_info(), который выводит нужную информацию,
# и get_model(), который позволит получить название модели дрона

# РЕЗУЛЬТАТ:
# Информация о дроне DJI Mavic 2 Pro: масса 903, производитель DJI, количество миссий 6

# ВАШ КОД:
user_input = input("Введите модель дрона (полностью) в любом регистре\n")
for multirotoruav in multirotoruavs:
    model = multirotoruav.get_model()
    if model.lower() == user_input.lower():
        info = multirotoruav.get_info()
        print(f"Информация о дроне {model}: масса {info['weight']}, производитель {info['brand']}, количество миссий {info['count_missions']}")

# =====================================
# ЗАДАНИЕ 3: Классы - декораторы
# =====================================
# TODO 3-1 - Добавить атрибут incidents типа список
# Добавьте в класс MultirotorUAV атрибут incidents и внесите туда информацию обо всех найденных происшествиях для этой модели
# Не забудьте, что атрибут добавляется при помощи декоратора


with open ("data/faa_incidents.csv") as filename_csv:
    incidents_csv = csv.reader(filename_csv)
    for row in incidents_csv:
        column_split = str(row).split("', ")
        for drone in multirotoruavs:
            drone_name = drone.get_model().replace("DJI ","")
            for cell in column_split:
                incident = re.search(drone_name, cell, re.I)
                if incident is not None:
                    drone.add_incident(incident.string)


# TODO 4-2 - Добавьте в класс MultirotorUAV публичный метод save_data, который сохраняет статистику по дрону в файл
# Внимание! Метод save_data не принимает параметры. Название файла сформируйте как: название класса + название модели + расширение .json
# например: "MultirotorUAV_DJI Mavic 2 Pro.json"
# Подсказка: название класса вы можете получить вот так: self.__class__.__name__
# используйте ключи: "model", "weight", "brand", "missions", "incidents"
# например: {"model":"DJI Inspire 2", "weight": 1500, "info": "...", "manufacturer": "DJI", "missions": [], "incidents": []}

# ВАШ КОД - допишите код в объявлении класса

# =====================================
# ЗАДАНИЕ 5: Регулярные выражения
# =====================================
# TODO 5-1 - Выведите на экран собранную информацию по инцидентам по каждому дрону в таком виде:
# модель: инцидентов - количество
# порядковый_номер_инцидента - краткий текст инцидента*
# полный текст инцидента

# * - краткий текст инцидента получайте следующим образом: в исходном тексте инцидента найдите модель, например, INSPIRE 2,
# и выведите все предложения, в которых встречается упоминание этой модели

# Подсказка 1: Полностью готовый код есть в лекции про регулярные выражения (пример про перелетных птиц).
# Ваши изменения: а) вставить вместо "зим" название модели дрона, б) поменять язык поиска на английский
# Подсказка 2: не забывайте использовать флаг re.I для игнорирования регистра символов
# Подсказка 3: перед тем, как искать, уберите из названия модели название производителя
# Подсказка 4: лучше не используйте re.compile. Для этого случая работает не очень

# РЕЗУЛЬТАТ:
# mavic 2 enterprise advanced: инцидентов - 0
# mavic 2 pro: инцидентов - 0
# mavic 3: инцидентов - 0
# mavic 2 zoom: инцидентов - 1
# 1 - ON JULY 15, 2020 AT 1050 EDT, A DJI, MAVIC 2 ZOOM L1Z UAS, SERIAL # 0M6TG85R0A04ZP, UA FA REGISTRATION # FA3RE7RNWP, REGISTERED TO ^PRIVACY DATA OMITTED^ (PIC), REMOTE PILOT CERTIFICATE ^PRIVACY DATA OMITTED^, LOST CONTROLLED FLIGHT IN THE AREA OF ^PRIVACY DATA OMITTED^ AND HIT A BLACK NISSAN PICKUP TRUCK BEARING ^PRIVACY DATA OMITTED^ TRAVELING ALONG TAMIAMI TRAIL IN NORTH PORT CAUSING PROPERTY DAMAGE.
# ON JULY 15, 2020 AT 1050 EDT, A DJI, MAVIC 2 ZOOM L1Z UAS, SERIAL # 0M6TG85R0A04ZP, UA FA REGISTRATION # FA3RE7RNWP, REGISTERED TO ^PRIVACY DATA OMITTED^ (PIC), REMOTE PILOT CERTIFICATE ^PRIVACY DATA OMITTED^, LOST CONTROLLED FLIGHT IN THE AREA OF ^PRIVACY DATA OMITTED^ AND HIT A BLACK NISSAN PICKUP TRUCK BEARING ^PRIVACY DATA OMITTED^ TRAVELING ALONG TAMIAMI TRAIL IN NORTH PORT CAUSING PROPERTY DAMAGE. THE UAS WAS FLOWN ON A RECREATIONAL FLIGHT OVER A CONSTRUCTION SITE AT ^PRIVACY DATA OMITTED^, USING AN AUTOMATIC FREQUENCY SELECTION FEATURE THAT RANGED FROM 2.400 - 2.4835 GHZ; 5.725 - 5.850 GHZ. WEATHER CONDITIONS WERE CLEAR AND ARE NOT CONSIDERED A FACTOR. THE UAS WAS DESTROYED AND THE PROPERTY DAMAGE WAS GREATER THAN $500. THERE WERE NO PERSONAL INJURIES. THE FLIGHT ORIGINATED FROM ^PRIVACY DATA OMITTED^, EARLIER THAT DAY. WHILE THIS INCIDENT MEETS FAA UAS ACCIDENT CRITERIA, IT DOES NOT MEET THE NTSB?S UAS ACCIDENT CRITERIA. THE NTSB WOULD NOT ISSUE A NTSB ACCIDENT NUMBER FOR THIS EVENT. THEREFORE, THIS EVENT WILL BE CLASSIFIED AN INCIDENT.
# inspire 2: инцидентов - 3
# 1 - RPIC WAS OPERATING A DJI INSPIRE 2 WITH A CAMERA/GIMBLE COMBINATION SET UP. DJI INSPIRE 2 (SN 09YDDCQL040384) CURRENT FAA SUAS REGISTRATION NUMBER FA343FTPWM.
# ON MAY 25, 2020, MOJAVE AIR AND SPACE PORT (KMHV) AIR TRAFFIC CONTROL TOWER (ATCT) PROVIDED VERBAL AUTHORIZATION TO ^PRIVACY DATA OMITTED^ TO PERFORM SUAS OPERATIONS IN KMHV CLASS D AIRSPACE. WIND SPEED WAS 7 KNOTS WITH GUSTS AT 14 KNOTS. WIND DIRECTION 060. ^PRIVACY DATA OMITTED^. AND KMHV HAVE A LETTER OF AGREEMENT (LOA) EFFECTIVE JANUARY 28, 2020 FOR SUAS OPERATIONS IN KMHV CLASS D AIRSPACE. ^PRIVACY DATA OMITTED^ HOLDS A CURRENT CERTIFICATE OF WAIVER OR AUTHORIZATION EFFECTIVE FROM JANUARY 31, 2019 TO SEPTEMBER 30, 2020 TO PERFORM SMALL UNMANNED AIRCRAFT SYTEM (SUAS) OPERATIONS IN CLASS D AIRSPACE AT KMHV. ^PRIVACY DATA OMITTED^ HOLDS A CURRENT REMOTE PILOT CERTIFICATE WITH A SUAS RATING ^PRIVACY DATA OMITTED^. REMOTE PILOT IN COMMAND (RPIC), ^PRIVACY DATA OMITTED^ WAS OPERATING UNDER PART 107 AT KMHV COVERING SURVEILLANCE OF THE VIRGIN ORBIT LAUNCHER ONE MISSION. RPIC WAS OPERATING A DJI INSPIRE 2 WITH A CAMERA/GIMBLE COMBINATION SET UP. DJI INSPIRE 2 (SN 09YDDCQL040384) CURRENT FAA SUAS REGISTRATION NUMBER FA343FTPWM. REGISTERED TO ^PRIVACY DATA OMITTED^. RPIC WAS OPERATING WITH ONE INEXPERIENCED VISUAL OBSERVER (VO). RPIC WAS NOT ACCUSTOMED TO OPERATING THE SMALL UNMANNED AIRCRAFT CONTROLS, MANIPULATING THE CAMERA/GIMBLE COMBINATION SET UP, AND COMMUNICATING TO ATCT VIA RADIO SIMULTANEOUSLY. RPIC WAS ALSO WORKING WITH AN INEXPERIENCED VO. RPIC BECAME TASK SATURATED AND LOST SIGHT OF THE SMALL UNMANNED AIRCRAFT. AT 1208 LOCAL TIME, THE SMALL UNMANNED AIRCRAFT STRUCK THE WEST SIDE OF KMHV ATCT. ^PRIVACY DATA OMITTED^ SUSTAINED A SUPERFICIAL HORIZONTAL LACERATION TO HIS RIGHT LOWER, INSIDE FOREARM. HE WAS TREATED ON-SCENE WITH BANDAGE AND GAUZE WRAP.
# 2 - USED RENTED DJI INSPIRE 2 DRONE.
# UAS PILOT ^PRIVACY DATA OMITTED^ REMOTE CERTIFICATE #^PRIVACY DATA OMITTED^ WAS HIRED BY PRODUCER ^PRIVACY DATA OMITTED^ TO DO SOME AERIAL SHOTS OF EL MORRO FOR A DOCUMENTARY ABOUT THE 500 YEARS OF THE CITY OF SAN JUAN ON SEPTEMBER 3RD. USED RENTED DJI INSPIRE 2 DRONE. LOST CONTROL LINK WITH DRONE ON WAY BACK CRASHED INTO EL MORRO FORT IN OLD SAN JUAN.
# 3 - AIRCRAFT IS A DJI T650A INSPIRE 2 SUAS, SERIAL # 0A0LG2J107005, REGISTRATION # FA3FTYCLFE.
# AIRCRAFT IS A DJI T650A INSPIRE 2 SUAS, SERIAL # 0A0LG2J107005, REGISTRATION # FA3FTYCLFE. FREQUENCY USED IS UNKNOWN. THE AIRCRAFT HAS TWO FREQUENCIES AVAILABLE, 2.4 AND 5.8 GHZ, BUT THE PIC DOESN'T REMEMBER WHICH ONE WAS IN USE DURING THE FLIGHT. PIC IS ^PRIVACY DATA OMITTED^, CERTIFICATE ^PRIVACY DATA OMITTED^. ^PRIVACY DATA OMITTED^ SAID THAT THE UAS EXPERIENCED AN ERROR ON ITS FIRST CALIBRATION ATTEMPT PRIOR TO LAUNCH BUT CALIBRATED CORRECTLY ON THE SECOND ATTEMPT AND THE FLIGHT CONTINUED AFTER RECORDING THE HOME POINT AT THE LAUNCH POSITION. HE SAID THE UAS WAS IN POSITIONING MODE (P-MODE) FOR THE ENTIRE FLIGHT. THE LANDING SEQUENCE WAS INITIATED MANUALLY (I.E. THE AUTOLAND FEATURE WAS NOT USED). ^PRIVACY DATA OMITTED^ SAID THAT THE UAS "TOOK OFF" WHEN IT GOT DOWN TO ABOUT 5' AGL AND FLEW INSIDE THE CPD HANGAR WHERE IT STRUCK A CPD HELICOPTER. HE SAID THAT THE UAS ACTED AS IF IT WAS "PRE-PROGRAMMED" TO FLY INTO THE HANGAR ONCE IT GOT AWAY FROM HIM.

# ВАШ КОД:
for multirotoruav in multirotoruavs:
    print(f"{multirotoruav.get_model()} инцидентов - {len(multirotoruav.incidents)}")
    for i, incident in enumerate(multirotoruav.incidents):
        model = multirotoruav.get_model().replace('DJI ', '')
        short_inc = ' '.join(re.findall(f"[A-Z][^.!?]*(?:{model})[^.!?]*[.!?]", incident, flags=re.I))
        print(i, '-', short_inc)
        print(incident)

# TODO 5-2 - После вывода информации об инциденте сохраните всю информацию о дроне в файл .json при помощи метода save_data() класса
# ВАШ КОД:
for multirotoruav in multirotoruavs:
    multirotoruav.save_data()

# РЕЗУЛЬТАТ:
# см. приложенные файлы в папке samples