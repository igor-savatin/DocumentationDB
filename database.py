import cx_Oracle, pyodbc
from tools import decrypt

def connectOracle(user,password,connString,query):
    """
        Make connection to the database, to execute query
        input:
            user - user of database
            password - password of user
            connString - connection String (example: host/instance_name:port)
            query - query
    """
    try:
        conn = cx_Oracle.connect(user, decrypt(password), connString)
        arrColumn = []
        arrData = []
        cursor = conn.cursor()
        # documentHtml+="""<table style='width:100%'>"""
        execution = cursor.execute(query)
        for column in execution.description:
            arrColumn.append(str(column[0]))  
        for row in execution:
            arrRow=[]
            # documentHtml+="\n<tr>"
            for i in range (len(row)):
                arrRow.append(str(row[i]))
                # documentHtml+="<td>"+str(row[i])+"</td>"
            arrData.append(arrRow)
            # documentHtml+="</tr>"
        # documentHtml+="""\n</table>"""
        objJson = {
            "column": arrColumn,
            "data": arrData
        }
        
    except cx_Oracle.DatabaseError as exc:
        err, = exc.args
        print("Oracle-Error-Code:", err.code)
        print("Oracle-Error-Message:", err.message)
        # logging.error("Database connection error")
    finally:
        cursor.close()
        conn.close()
    
    return objJson


def connectMSSQL(server,database,username,password,query):
    
    arrData = []
    driver_name = ''
    driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    if driver_names:
        driver_name = driver_names[0]
    if driver_name:
        conn_str = f'DRIVER={driver_name};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={decrypt(password)}'
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                columns = [column[0] for column in cursor.description]
                # itens.append(columns)
                # for i in cursor:
                #     print(i)
                for row in cursor:
                    arrRow=[]
                    # documentHtml+="\n<tr>"
                    for i in range (len(row)):
                        arrRow.append(str(row[i]))
                        # documentHtml+="<td>"+str(row[i])+"</td>"
                    arrData.append(arrRow)
    else:
        print('(No suitable driver found. Cannot connect.)')
        # driver= '{ODBC Driver 17 for SQL Server}'
    # print(itens)
    
    objJson = {
            "column": columns,
            "data": arrData
        }
    return objJson