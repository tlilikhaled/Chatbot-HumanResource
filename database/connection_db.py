import mysql.connector
import traceback
def ConnectionToDB():
    
    return mysql.connector.connect(host="localhost", user="root",  passwd="", database="ressource_humaine")
    try:
        
        print("Connexion Etablished with cursor!")
    except Exception:
        print("problem when try to connect")
        print(traceback.format_exc())

def list_known_projects_Id():
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  project_id FROM employe "
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    #print(myresult)
    list=["'","(",")",","] 
    #res="".join(i for i in myresult if i not in list) 
    res=",".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    #print(res)
    list = res
    #print(list)
    return list


def List_resources_project(num):
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  employe_number, grade_resource, start_date, end_date, resoucre_status FROM ressource WHERE project_id = {}".format(num)
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    list=["'","(",")",","] 
    res="".join(str(i) for i in myresult if i not in list) 
    #res=",".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    #list = res
    return res


def List_employees_project(num):
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  id_employee, full_name, grade, status FROM employe WHERE project_id = {}".format(num)
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    list=["'","(",")",","] 
    res="".join(str(i) for i in myresult if i not in list) 
    #res=",".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    #list = res
    return res

def active_dev():
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  id_employee, full_name, project_id  FROM employe WHERE grade='developer' "
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    list=["'","(",")",","] 
    print(myresult)
    res="".join(str(i) for i in myresult if i not in list) 
    
    #res="".join(''.join(map(str, tup)) for tup in myresult if tup not in list)
    print(res) 
    return res

def active_qa():
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT id_employee, full_name, project_id FROM employe WHERE grade='quality' "
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    list=["'","(",")",","] 
    res="".join(str(i) for i in myresult if i not in list) 
    #res="".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    return res

def active_devops():
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  id_employee, full_name, project_id  FROM employe WHERE grade='devops' "
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    list=["'","(",")",","] 
    res="".join(str(i) for i in myresult if i not in list) 

    #res="".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    return res

def active_support():
    mydb = ConnectionToDB()
    mycursor = mydb.cursor()
    sql = "SELECT  id_employee, full_name, project_id  FROM employe WHERE grade='support' "
    mycursor.execute(sql)   
    myresult = mycursor.fetchall()
    list=["'","(",")",","] 
    res="".join(str(i) for i in myresult if i not in list) 
    #res="".join(''.join(map(str, tup)) for tup in myresult if tup not in list) 
    return res