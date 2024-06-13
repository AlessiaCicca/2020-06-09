from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.direttore import Direttore


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def getNodi(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.*
from directors d, movies m, movies_directors md 
where d.id =md.director_id and m.id =md.movie_id and m.`year` =%s"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(Direttore(**row))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getConnessioni(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.d1 as id1,t2.d2 as id2, count(distinct a1) as peso
from (select distinct md.director_id as d1, r.actor_id as a1
from movies_directors md , movies m, roles r 
where md.movie_id =m.id and m.id =r.movie_id and m.`year` =%s) as t1,
(select distinct md.director_id as d2, r.actor_id as a2
from movies_directors md , movies m, roles r 
where md.movie_id =m.id and m.id =r.movie_id and m.`year` =%s) as t2
where t1.a1=t2.a2 and t1.d1<>t2.d2
group by t1.d1,t2.d2
"""

        cursor.execute(query,(anno,anno,))

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result
