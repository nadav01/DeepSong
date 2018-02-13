from SPARQLWrapper import SPARQLWrapper, JSON
from random import shuffle

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

def get_birth_place_query_answer(name):
    try:
        BIRTH_PLACE_QUERY = """
        prefix dbpedia: <http://dbpedia.org/resource/>
        prefix dbpprop: <http://dbpedia.org/property/>
        prefix dbpedia-owl:<http://dbpedia.org/ontology/>

        select ?property ?value where {
          dbpedia:""" + name + """ ?property ?value
          filter( strstarts(str(?property),str(dbpedia-owl:birthPlace)) )
        }
        """
        sparql.setQuery(BIRTH_PLACE_QUERY)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings'][0]['value']['value'][28:]
    except Exception:
        return get_hometown_place_query_answer(name)

def get_hometown_place_query_answer(name):
    try:
        HOMETOWN_QUERY = """
        prefix dbpedia: <http://dbpedia.org/resource/>
        prefix dbpprop: <http://dbpedia.org/property/>
        prefix dbpedia-owl:<http://dbpedia.org/ontology/>

        select ?property ?value where {
          dbpedia:""" + name + """ ?property ?value
          filter( strstarts(str(?property),str(dbpedia-owl:hometown)) )
        }
        """
        sparql.setQuery(HOMETOWN_QUERY)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings'][0]['value']['value'][28:]
    except Exception:
        return 0

def get_active_year_query_answer(name):
    try:
        ACTIVE_YEAR_QUERY = """
        prefix dbpedia: <http://dbpedia.org/resource/>
        prefix dbpprop: <http://dbpedia.org/property/>
        prefix dbpedia-owl:<http://dbpedia.org/ontology/>

        select ?property ?value where {
          dbpedia:""" + name + """?property ?value
          filter( strstarts(str(?property),str(dbpedia-owl:activeYearsStartYear)) )
        }
        """

        sparql.setQuery(ACTIVE_YEAR_QUERY)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings'][0]['value']['value']
    except:
        return 0


def get_genre_query_answer(name):
    try:
        GENRE_QUERY = """
        prefix dbpedia: <http://dbpedia.org/resource/>
        prefix dbpprop: <http://dbpedia.org/property/>
        prefix dbpedia-owl:<http://dbpedia.org/ontology/>

        select ?property ?value where {
          dbpedia:""" + name + """ ?property ?value
          filter( strstarts(str(?property),str(dbpedia-owl:genre)) )
        }
        """
        sparql.setQuery(GENRE_QUERY)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings'][0]['value']['value'][28:]
    except:
        return 0


def to_upper(oldList):
    newList = []
    for element in oldList:
        name = element.split(" ")
        new_name=[]
        for word in name:
            new_name.append(word.capitalize())
        element=""
        for word in new_name:
            element = element + "_" + word
        newList.append(element[1:])
    return newList


def update_list_for_dbpedia(lst):
    ret_list = []
    for name in lst:
        ret_list.append(update_name_for_dbpedia(name))
    return ret_list


def update_name_for_dbpedia(name):
    name = name.split(" ")
    ret_name = ""
    for i in range(0,len(name)-1):
        ret_name = ret_name + name[i] + "_"
    ret_name = ret_name + name[len(name)-1]
    return ret_name


def update_names_list_from_file_(filename):
    with open(filename, 'r+', encoding='utf8') as f:
        my_list = f.read()
        my_list = my_list.split("\n")
        my_list = to_upper(my_list)
        return my_list
        # f.seek(0)
        # for name in my_list:
        #     f.write(name)
        #     f.write('\n')

def extract_names(filename):
    with open(filename, 'r+', encoding='utf8') as f:
        my_list = f.read()
        my_list = my_list.split("\n")
        return my_list

def check_if_band(name):
    try:
        IS_BAND_QUERY = """
        prefix dbpedia: <http://dbpedia.org/resource/>
        prefix dbpprop: <http://dbpedia.org/property/>
        prefix dbpedia-owl:<http://dbpedia.org/ontology/>

        select ?property ?value where {
          dbpedia:""" + name + """?property ?value
          filter( strstarts(str(?property),str(dbpedia-owl:background)) )
        }
        """

        sparql.setQuery(IS_BAND_QUERY)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings'][0]['value']['value'] == 'group_or_band'
    except:
        return False


def get_random_year(list_to_work_with):
    active_year = 0
    num_taken=0
    for name in list_to_work_with:
        temp = active_year
        active_year = active_year + int(get_active_year_query_answer(name))
        if temp < active_year:
            num_taken = num_taken+1
    if num_taken == 0:
        active_year = 2018
    else:
        active_year = int(active_year / num_taken)

    return active_year

def get_genre(list_to_work_with):
    genre = 0
    range_list=list(range(len(list_to_work_with)-1))
    shuffle(range_list)
    for name in range_list:
        genre = get_genre_query_answer(list_to_work_with[name])
        if genre != 0:
            break
    if genre == 0:
        genre = "no genre found"
    return genre


def get_hometown(list_to_work_with):
    hometown = 0
    range_list = list(range(len(list_to_work_with)-1))
    shuffle(range_list)
    for name in range_list:
        hometown = get_birth_place_query_answer(list_to_work_with[name])
        if hometown != 0:
            break
    if hometown == 0:
        hometown = "no hometown found"
    return hometown

def get_info(filename):
    list_for_work = update_names_list_from_file_(filename)
    list_for_work = update_list_for_dbpedia(list_for_work)
    genre = get_genre(list_for_work)
    hometown = get_hometown(list_for_work)
    activity_year = get_random_year(list_for_work)
    print(genre)
    print(hometown)
    print(activity_year)

def get_year(filename):
    list_for_work = update_names_list_from_file_(filename)
    list_for_work = update_list_for_dbpedia(list_for_work)
    activity_year = get_random_year(list_for_work)
    return activity_year

#get_info("60s.txt")