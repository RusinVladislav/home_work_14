import sqlite3

data_sql = 'netflix.db'


# ШАГ 0
# решил вынести подключение к базе данных и выгрузку данных из неё (по запросу) в отдельную функцию
def data_by_sql_db(query_str: str) -> tuple:
    """ Подключение к базе данных и выгрузка данных из неё (по запросу) """

    with sqlite3.connect(data_sql) as con:
        con.row_factory = sqlite3.Row
        # С помощью этой функции получаем результат запроса в виде списка кортежей
        result = con.execute(query_str).fetchall()

        return result


# ШАГ 1
def get_movie_by_title(word: str) -> dict:
    """Возвращает список с результатом поиска самого свежего фильма по слову в названии """

    find_word = word.lower()

    sqlite_query = f"""
                    SELECT title, country, release_year, description
                    FROM netflix
                    WHERE type = 'Movie' AND title LIKE '%{find_word}%'
                    ORDER BY date_added DESC
    """

    data = data_by_sql_db(sqlite_query)

    result_search = []
    for dat in data:
        record = {}
        for _ in dat.keys():
            record['title'] = f'{dat["title"]}'
            record['country'] = f'{dat["country"]}'
            record['release_year'] = f'{dat["release_year"]}'
            record['description'] = f'{dat["description"]}'
        result_search.append(record)

    return result_search


# ШАГ 2
def get_movie_by_years(start: int, stop: int) -> list[dict]:
    """ Возвращает результат поиска фильмов по годам выпуска (с - по) """

    sqlite_query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE type = 'Movie' AND release_year BETWEEN {start} AND {stop + 1}
                    ORDER BY release_year
                    LIMIT 100
    """

    data = data_by_sql_db(sqlite_query)

    result_search = []
    for dat in data:
        record = {}
        for _ in dat.keys():
            record['title'] = f'{dat["title"]}'
            record['release_year'] = f'{dat["release_year"]}'
        result_search.append(record)

    return result_search


# ШАГ 3
def get_movie_by_rating(rating: str) -> list[dict]:
    """ Возвращает результат поиска фильмов по заданному рейтингу (children, family and adult) """
    qwery_rating = ""
    if rating == 'children':
        qwery_rating = "WHERE rating = 'G'"
    elif rating == 'family':
        qwery_rating = "WHERE rating IN ('G', 'PG', 'PG-13')"
    elif rating == 'adult':
        qwery_rating = "WHERE rating IN ('R', 'NC-17')"

    sqlite_query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    {qwery_rating}
                    LIMIT 100
    """

    data = data_by_sql_db(sqlite_query)

    result_search = []
    for dat in data:
        record = {}
        for _ in dat.keys():
            record['title'] = f'{dat["title"]}'
            record['rating'] = f'{dat["rating"]}'
            record['description'] = f'{dat["description"]}'
        result_search.append(record)

    return result_search


# ШАГ 4
def get_movie_by_genre(genre: str) -> list[dict]:
    """ Возвращает результат поиска фильмов по жанру"""

    qwery_genre = f"%{genre.lower().strip()}%"

    sqlite_query = f"""
                    SELECT title, release_year, listed_in, description
                    FROM netflix
                    WHERE lower(listed_in) LIKE '{qwery_genre}'
                    ORDER BY date_added DESC
                    LIMIT 10
    """

    data = data_by_sql_db(sqlite_query)

    result_search = []
    for dat in data:
        record = {}
        for _ in dat.keys():
            record['title'] = f'{dat["title"]}'
            record['release_year'] = f'{dat["release_year"]}'
            record['listed_in'] = f'{dat["listed_in"]}'
            record['description'] = f'{dat["description"]}'
        result_search.append(record)

    return result_search


# ШАГ 5
# задание выполнено в соответствии с ответом наставника:
# https://skypro.slack.com/archives/C03C0R3GEKU/p1660230167899309?thread_ts=1660219239.347399&cid=C03C0R3GEKU
def get_movie_by_two_actors(name_actors: str) -> list[dict]:
    """ Возвращает все фильмы где снимались заданные два актера"""

    qwery_list = name_actors.split('%20')
    qwery_str = ' '.join(qwery_list)
    actor_1 = f"{qwery_str.split(' and ')[0]}"
    actor_2 = f"{qwery_str.split(' and ')[1]}"

    sqlite_query = f"""
                    SELECT *
                    FROM netflix
    """

    data = data_by_sql_db(sqlite_query)

    # получаем из базы данных все строки с актерами
    all_casts_row = []  # list[dict]
    for dat in data:
        record = {}
        for _ in dat.keys():
            record['title'] = f'{dat["title"]}'
            record['cast'] = f'{dat["cast"]}'
        all_casts_row.append(record)
    # находим те строки в которых есть искомые актеры
    two_actors_in_row = []
    for row in all_casts_row:
        if actor_1.lower() in row['cast'].lower() and actor_2.lower() in row['cast'].lower():
            two_actors_in_row.append(row)

    return two_actors_in_row


# задание выполнено дополнительно в соответствии с условием:
def get_list_actors_more_2(name_actors: str) -> list[dict]:
    """
    Поиск актеров, которые снимались 2 и более раз с указанной парой актеров
    """
    qwery_list = name_actors.split('%20')
    qwery_str = ' '.join(qwery_list)
    actor_1 = f"{qwery_str.split(' and ')[0]}"
    actor_2 = f"{qwery_str.split(' and ')[1]}"

    sqlite_query = f"""
                    SELECT *
                    FROM netflix
    """

    data = data_by_sql_db(sqlite_query)

    # получаем из базы данных все строки с актерами
    all_casts_row = []  # list[dict]
    for dat in data:
        record = {}
        for _ in dat.keys():
            record['title'] = f'{dat["title"]}'
            record['cast'] = f'{dat["cast"]}'
        all_casts_row.append(record)

    # создаем словарь с именами актеров и количеством раз съемок с указнными двумя актерами
    actors_add = {}
    for row in all_casts_row:
        if actor_1.lower() in row['cast'].lower() and actor_2.lower() in row['cast'].lower():
            for key in row['cast'].split(', '):
                actors_add[key] = actors_add.setdefault(key, 0) + 1
    # перебираем словарь actors_add и сохраняя в новом словаре только тех актеров которые играли с парой 2 и более раз
    actors_find = []
    for key, item in actors_add.items():
        if actors_add[key] >= 2:
            actors_find.append({key: item})

    return actors_find


# ШАГ 6
def get_movie_by_type_year_genre(tupe: str, year: int, genre: str) -> list[dict]:
    """ Возвращает все фильмы по заданным году и актеру"""

    find_tupe = tupe
    find_year = year
    find_genre = genre.lower()
    all_query = f"WHERE type = '{find_tupe}' AND release_year = {find_year} AND listed_in LIKE '%{find_genre}%'"

    sqlite_query = f"""
                    SELECT title, type, duration_type, release_year, listed_in
                    FROM netflix
                    {all_query}
                    ORDER BY release_year DESC
                    LIMIT 100
    """

    data = data_by_sql_db(sqlite_query)

    result_search = []
    for dat in data:
        record = {}
        for _ in dat.keys():
            record['title'] = f'{dat["title"]}'
            record['type'] = f'{dat["type"]}'
            record['release_year'] = f'{dat["release_year"]}'
            record['listed_in'] = f'{dat["listed_in"]}'
        result_search.append(record)

    return result_search
