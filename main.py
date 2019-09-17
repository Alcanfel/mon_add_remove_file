import os
import pickle
import logging
import datetime
import time


logging.basicConfig(filename="test.log", level=logging.INFO, filemode="a")
now = datetime.datetime.now()

file_dict="dictionary.txt"
file_resource=r"/media/attenuator/TOSHIBA EXT/Фото"

if os.path.exists(file_dict):
    pass
else:
    dict_old={}
    for d, dirs, files in os.walk(file_resource):
        try:
            dict_old[d].extend(files)
        except KeyError:
            dict_old[d] = files
#
    with open(file_dict,'wb') as out:
        pickle.dump(dict_old,out)

# with open(file_dict,'rb') as inp:
#     d_in = pickle.load(inp)
#
# print(d_in)


# print(type(d_in))
# print(d_in)
#
step = 1
while True:
    start_time = time.time()
    # Зугрузили словарь из файла
    with open(file_dict, 'rb') as inp:
        d_in = pickle.load(inp)

    # Создали новый словрь с полной иерархией каталога
    dict_new = {}
    for d, dirs, files in os.walk(file_resource):
        try:
            dict_new[d].extend(files)
        except KeyError:
            dict_new[d] = files

    # Добавдяем в лог инфу
    logging.info("Дата {} Анализируем удаление/добавление файлов".format(str(datetime.datetime.now())))
    print("Анализируем удаление/добавление файлов, шаг:{} {}".format(step, str(datetime.datetime.now())))

    list_if2 = list(set(d_in.keys()).difference(set(dict_new.keys())))
    list_if3 = list(set(dict_new.keys()).difference(set(d_in.keys())))
    # print(list(set(d_in.keys()).difference(set(dict_new.keys()))))
    # print(list(set(dict_new.keys()).difference(set(d_in.keys()))))

    # Проверяем на добавление/удаление папок,
    # Если не удалялось/не добавлялось, то проверяем добавление/удаление файлов
    if len(set(dict_new.keys()).difference(set(d_in.keys()))) == 0 and len(
            set(d_in.keys()).difference(set(dict_new.keys()))) == 0:
        # Пробегаемся по всему загруженному словарю и проверяем на перечение
        for i in d_in:
            diff_set = set(d_in[i]).difference(set(dict_new[i]))
            if len(diff_set) > 0:
                logging.critical("Из папки {} были удалены файлы: {}".format(i, diff_set))
                print("Из папки {} были удалены файлы: {}".format(i, diff_set))
                for l in list(diff_set):
                    d_in[i].remove(l)
                    with open(file_dict, 'wb') as out:
                        pickle.dump(d_in, out)
            diff_set_2 = set(dict_new[i]).difference(set(d_in[i]))
            if len(diff_set_2) > 0:
                logging.warning("В папку {} были добавлены файлы: {}".format(i, diff_set_2))
                print("В папку {} были добавлены файлы: {}".format(i, diff_set_2))
                for l in list(diff_set_2):
                    d_in[i].append(l)
                    with open(file_dict, 'wb') as out:
                        pickle.dump(d_in, out)
    elif len(set(d_in.keys()).difference(set(dict_new.keys()))) > 0:
        for i in list_if2:
            logging.critical("Дата {} - Отсутвует каталог {}".format(str(now), i))
            logging.critical("Дата {} - Из папки {} были удалены файлы: {}".format(str(datetime.datetime.now()),i, d_in[i]))
            print("Дата {} - Отсутвует каталог {}".format(str(now),i ))
            print("Дата {} - Из папки {} были удалены файлы: {}".format(str(datetime.datetime.now()), i, d_in[i]))
            d_in.pop(i, None)
            with open(file_dict, 'wb') as out:
                pickle.dump(d_in, out)

    elif len(set(dict_new.keys()).difference(set(d_in.keys()))) > 0:
        for i in list_if3:
            logging.warning("Дата {} - добавлен каталог {}".format(str(now), i))
            logging.warning("Дата {} - В папку {} были добавлены файлы: {}".format(str(datetime.datetime.now()), i, dict_new[i]))
            print("Дата {} - добавден каталог {}".format(str(now), i))
            print("Дата {} - В папку {} были добавлены файлы {}".format(str(datetime.datetime.now()), i, dict_new[i]))
            d_in.pop(i, None)
            d_in[i] = dict_new[i]
            with open(file_dict, 'wb') as out:
                    pickle.dump(d_in, out)

    time.sleep(10)
    step += 1
    print("--- %s seconds ---" % (time.time() - start_time))
    print("\n")