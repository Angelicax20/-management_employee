import pymysql.cursors

# Connect to the database
try:
    connection = pymysql.connect(host='grupo9.mysql.pythonanywhere-services.com',
                                user='grupo9',
                                password='empleados',
                                db='grupo9$grupo_9',
                                cursorclass=pymysql.cursors.DictCursor)
except:
    pass


def seleccion2(sql) -> list:
    """ Ejecuta una consulta de selección sobre la base de datos """
    with connection:
        try:
            with connection.cursor() as cursor:
            # Read a single record
                cursor.execute(sql)
                res = cursor.fetchone()
            
        except Exception:
            res = None
        return res

def accion2(sql, datos) -> int:
    """ Ejecuta una consulta de acción sobre la base de datos """
    try:
       with connection:
            with connection.cursor() as cursor:
        # Create a new record
                
                res=cursor.execute(sql, datos).rowcount
                if res!=0:
                    connection.commit()

    # connection is not autocommit by default. So you must commit to save
    # your changes.
            
    except Exception:
        res = 0
    return res
