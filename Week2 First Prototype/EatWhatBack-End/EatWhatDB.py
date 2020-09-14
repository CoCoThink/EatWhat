import datetime

import pymysql
import configparser
import os


# 读数据库连接配置文件
config = configparser.ConfigParser()
path = os.path.abspath(os.path.dirname(__file__))
config.read(path+'/EatWhatDB.ini')
host = config.get("DSDdb", "host")
port = config.get("DSDdb", "port")
user = config.get("DSDdb", "user")
pwd = config.get("DSDdb", "pwd")
db = config.get("DSDdb", "dbname")
charst = config.get("DSDdb", "charset")



class ServerDBUtils:
    """算法-数据库 工具类"""

    class UserException(Exception):
        pass

    # 需要server自己输入参数，最好写一个配置文件读取
    def __init__(self):
        self.conn = None
        self.cur = None
        self.host = host
        self.port = int(port)
        self.username = user
        self.passwd = pwd
        self.database = db
        self.charset = charst


    #Create the table food
    def createFood(self):
        #self.cur.execute("DROP TABLE IF EXISTS food")
        sql="""
        CREATE TABLE food(
            username VARCHAR(20) not null,
            time DATETIME not null,
            mapid INT not null,
            pointid INT not null,
            primary key(username,time)
        )
        """
        self.cur.execute(sql)


    def createTable(self):
        try:
            self.createHistoryposition()

        except Exception as e:
            return {"success":False,"error":str(e)}
        return {"success":True,"error":""}

    def dbconnect(self):
        # print(self.host, self.port, self.username, self.passwd, self.database, self.charset)
        # print(type(port))
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port,
                                        user=self.username,
                                        password=self.passwd,
                                        database=self.database,
                                        charset=self.charset)
            if self.conn:
                self.cur = self.conn.cursor()
        except Exception as e:
            # traceback.print_exc()
            # logger.error(str(e))
            return False

        return True

    def dbclose(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        # print("db closed")
        return True

    '''-------------------------Algorithm Utils---------------------------'''

    '''WIFI table'''

    def add_wifi(self, mapid, datadir):
        add_sql = "insert into wifi values(%s, %s)"
        try:
            self.cur.execute(add_sql, (mapid, datadir))
        except Exception as e:
            # traceback.print_exc()
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    def update_wifi(self, mapid, datadir):
        update_sql = "update wifi set datadir = %s where mapid = %s"
        try:
            rows = self.cur.execute(update_sql, (datadir, mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    def query_wifi(self, mapid):
        query_sql = "select datadir from wifi where mapid = %s"
        try:
            rows = self.cur.execute(query_sql, mapid)
            if rows == 0:
                raise self.UserException(
                    "no data which mapid is " + str(mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue), "data": ""}
        except Exception as e:
            # traceback.print_exc()
            return {"success": False, "error": str(e), "data": ""}
        rs = self.cur.fetchall()
        return {"success": True, "data": rs[0], "error": ""}

    def delete_wifi(self, mapid):
        delete_sql = "delete from wifi where mapid = %s"
        try:
            rows = self.cur.execute(delete_sql, mapid)
            if rows == 0:
                raise self.UserException(
                    "no data which mapid is " + str(mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    '''Model table'''

    def add_model(self, mapid, modeldir, wifimac, reqmac):
        add_sql = "insert into model values(%s, %s, %s, %s)"
        try:
            self.cur.execute(add_sql, (mapid, modeldir, wifimac, reqmac))
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    def update_modeldir(self, mapid, newmodeldir):

        update_sql = "update model set modeldir = %s where mapid = %s"
        try:
            rows = self.cur.execute(update_sql, (newmodeldir, mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # traceback.print_exc()
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    def update_wifimac(self, mapid, newwifimac):
        update_sql = "update model set wifimac = %s where mapid = %s"
        try:
            rows = self.cur.execute(update_sql, (newwifimac, mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # traceback.print_exc()
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    def update_reqmac(self, mapid, newreqmac):
        update_sql = "update model set reqmac = %s where mapid = %s"
        try:
            rows = self.cur.execute(update_sql, (newreqmac, mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # traceback.print_exc()
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    def query_model(self, mapid):
        query_sql = "select modeldir, wifimac, reqmac from model where mapid = %s"
        try:
            rows = self.cur.execute(query_sql, mapid)
            if rows == 0:
                raise self.UserException(
                    "no data which mapid is " + str(mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue), "data": ""}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e), "data": ""}
        rs = self.cur.fetchall()
        return {"success": True, "error": "", "data": rs[0]}
        
        
    def query_all_model(self):
        query_sql = "select * from model"
        try:
            rows = self.cur.execute(query_sql)
            if rows == 0:
                raise self.UserException("no data in table")
        except self.UserException as ue:
            return {"success": False, "error": str(ue), "data": ""}
        except Exception as e:
            return {"success": False, "error": str(e), "data": ""}
        rs = self.cur.fetchall()
        return {"success": True, "error": "", "data": rs}
    
    
    def delete_model(self, mapid):
        delete_sql = "delete from model where mapid = %s"
        try:
            rows = self.cur.execute(delete_sql, mapid)
            if rows == 0:
                raise self.UserException(
                    "no data which mapid is " + str(mapid))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # traceback.print_exc()
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    '''--------------------------Server--------------------------'''

    '''HistoryPosition table'''

    def add_history_pos(self, uname, time, mapid, pointid):
        sql = "insert into historyposition values(%s,%s, %s, %s)"
        try:
            self.cur.execute(sql, (uname, time, mapid, pointid))
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    def query_pos_within_period(self, uname, start, end):
        sql = "SELECT * FROM historyposition WHERE time > %s and time < %s and username = %s"
        try:
            data = self.cur.execute(sql, (start, end,uname))
            if data == 0:
                raise self.UserException(
                    "no data queried by the username and time")
        except self.UserException as ue:
            return dict(success=False, error=ue, data="")
        except Exception as e:
            return dict(success=False, error=e, data="")
        res = self.cur.fetchall()
        return dict(success=True, error="", data=res)

    '''Verification table'''

    # add an item to the table
    def add_new_code(self, sessionid, code, time):
        sql = "insert into verification values(%s,%s,%s)"
        try:
            self.cur.execute(sql, (sessionid, code, time))
        except Exception as e:
            # print(e)
            return dict(success=False, error=str(e))
        self.conn.commit()
        return dict(success=True, error="")

    # delete the invalid item
    def delete_invalid_code(self):
        now = datetime.datetime.now()
        sql = "delete from verification where time < %s"
        try:
            de = self.cur.execute(sql, now)
            if de == 0:
                raise self.UserException("No data which time is invalid")
        except self.UserException as ue:
            return dict(success=False, error=ue)
        except Exception as e:
            return dict(success=False, error=e)
        self.conn.commit()
        return dict(success=True, error="")

    def query_verification(self, sess):
        sql = "select code,time from verification where sessionid = %s"
        try:
            data = self.cur.execute(sql, sess)
            if data == 0:
                raise self.UserException("no data with this sessionid")
        except self.UserException as ue:
            # print(ue)
            return dict(success=False, error=ue, data="")
        except Exception as e:
            return dict(success=False, error=e, data="")
        res = self.cur.fetchall()
        return dict(success=True, error="", data=res[0])

    '''UserInfomation table'''

    # 添加新用户
    def add_new_user(self, uname, upasswd, devicename, port, email,
                     userlevel=1, onlineflag=1, phone=""):
        add_sql = "insert into userinformation values(%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            self.cur.execute(add_sql, (
                uname, upasswd, devicename, userlevel, onlineflag, port, email,
                phone))
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    # 更新用户信息
    def update_user_info(self, uname, upasswd, devicename, phone=""):
        update_sql = "update userinformation " \
                     "set password = %s, devicename = %s, phonenumber = %s " \
                     "where username = %s"
        try:
            rows = self.cur.execute(update_sql,
                                    (upasswd, devicename, phone, uname))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    # 更新用户邮箱信息
    def update_email(self, uname, email):
        update_sql = "update userinformation set email = %s where username = %s"
        try:
            rows = self.cur.execute(update_sql, (email, uname))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    # 更新用户端口信息
    def update_user_port(self, uname, port):
        update_sql = "update userinformation set communicateport = %s where username = %s"
        try:
            rows = self.cur.execute(update_sql, (port, uname))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    # 更新用户在线状态
    def update_user_onlineflag(self, uname, onlineflag):
        update_sql = "update userinformation set onlineflag = %s where username = %s"
        try:
            rows = self.cur.execute(update_sql, (onlineflag, uname))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    # 查找对应用户信息
    def query_user_info(self, uname):
        query_sql = "select * from userinformation where username = %s"
        try:
            self.cur = self.conn.cursor()
            rows = self.cur.execute(query_sql, uname)
            if rows == 0:
                raise self.UserException("no data which username is " + uname)
        except self.UserException as ue:
            return dict(success=False, error=ue, data="")
        except Exception as e:
            return dict(success=False, error=e, data="")
        res = self.cur.fetchall()
        return dict(success=True, error="", data=res[0])

    # 查找对应用户密码
    def query_passwd(self, uname):
        query_sql = "select password from userinformation where username = %s"
        try:
            rows = self.cur.execute(query_sql, uname)
            if rows == 0:
                raise self.UserException("no data which username is " + uname)
        except self.UserException as ue:
            return dict(success=False, error=ue, data="")
        except Exception as e:
            return dict(success=False, error=e, data="")
        res = self.cur.fetchall()
        return dict(success=True, error="", data=res[0][0])

    # 删除用户信息
    def delete_userinfo(self, uname):
        delete_sql = "delete from userinformation where username = %s"
        try:
            rows = self.cur.execute(delete_sql, uname)
            if rows == 0:
                raise self.UserException(
                    "no data which username is " + str(uname))
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}

        delete_sql = "delete from historyposition where username = %s"
        try:
            rows = self.cur.execute(delete_sql, uname)
        except self.UserException as ue:
            # print(ue)
            return {"success": False, "error": str(ue)}
        except Exception as e:
            # print(e)
            return {"success": False, "error": str(e)}
        self.conn.commit()
        return {"success": True, "error": ""}

    '''Coordinates table'''

    # Function that adds new coordinates to the table coordinate
    def add_coordinates(self, mapid, pointid, x, y, longitude, latitude):
        sql = "INSERT INTO coordinate (mapid, pointid, xcoordinate, ycoordinate, longitude, latitude) VALUES (%s, %s, %s, %s, %s, %s)"  # sql to insert the the new coordinates
        values = (
        int(mapid), int(pointid), float(x), float(y), float(longitude), float(
            latitude))  # variable containing the parameters, to easily insert
        try:
            self.cur.execute(sql, values)
            if self.cur.rowcount == 0:  # checks if the Insert worked or not. If it works its value is 1 else it is 0
                raise self.UserException("No data was inserted.")
        except self.UserException as ue:
            return dict(success=False, error=ue)
        except Exception as e:
            return dict(succes=False, error=e)
        self.conn.commit()  # Commits the transaction, Insert
        return dict(success=True, error="")

    # Function searches for the longitude and latitude utilizing the mapid and pointid. It returns the longitude and latitude values.
    def query_geo_pos(self, mapid, pointid):
        sql = "SELECT longitude, latitude FROM coordinate WHERE mapid=%s and pointid=%s"
        values = (int(mapid), int(
            pointid))  # variable containing the parameters, to easily insert
        try:
            self.cur.execute(sql, values)
            pos = self.cur.fetchall()  # Gets the values returned by the select, longitude and latitude
            if len(
                    pos) == 0:  # checks if the select worked or not. If it works its value should at least 1
                raise self.UserException("No data was selected.")
        except self.UserException as ue:
            return dict(success=False, error=ue)
        except Exception as e:
            return dict(success=False, error=e)
        return dict(success=True, error="", pos={"longitude": pos[0][0],
                                                 "latitude": pos[0][
                                                     1]})  # it returns the longitude and latitude values of the map

    '''Mapdata table'''

    # function that adds a new map
    def add_map_data(self, mapid, buildingname, longitude, latitude):#New Version of function add_map_data

        sqlCheck="Select * from mapdata WHERE mapid=%s"#Select to check if the id already exists
        try:
            onlyMapid=(int(mapid))
            self.cur.execute(sqlCheck,onlyMapid)
            length=self.cur.fetchall()
            if len(length)==1:#The id already exists. We just update the existig data
               sqlU="UPDATE mapdata set buildingname=%s, longitude=%s, latitude=%s WHERE mapid=%s"
               _values=(buildingname,float(longitude), float(latitude),int(mapid))
               self.cur.execute(sqlU,_values)
               if self.cur.rowcount==0:#Checks if the Update worked or not. If it works its value is 1 else it is 0
                   raise self.UserException("No data was updated.")
            else:
                sql = "INSERT INTO mapdata (mapid, buildingname, longitude, latitude) VALUES (%s, %s, %s, %s)"
                values = (int(mapid), buildingname, float(longitude), float(latitude)) 
                self.cur.execute(sql,values)
                if self.cur.rowcount==0:#Checks if the Update worked or not. If it works its value is 1 else it is 0
                    raise self.UserException("No data was inserted.")       
        except self.UserException as ue:
            return dict(success=False, error=ue)
        except Exception as e:
            return dict(success=False, error=e)   
        self.conn.commit() # Commits the transaction, Insert or Update
        return dict(success=True, error="")
               
    #function that deletes a map utilizing its id
    def delete_map(self, mapid):
        sql="DELETE from mapdata where mapid = %s"
        values=(int(mapid))
        try:
            self.cur.execute(sql,values)
            if self.cur.rowcount==0:#Checks if the delete worked or not. If it did it returns 1 else 0 
                raise self.UserException("No data was deleted.")
        except self.UserException as ue:
            return dict(success=False, error=ue)
        except self.Exception as e:
            return dict(succes=False,error=e)
        self.con.commit()#Commits the delete
        return dict(succes=True, error="")

    # function that updates the name of a building utilizing its id
    def update_building_name(self, mapid, buildingname):
        sql = "Update mapdata SET buildingname=%s WHERE mapid=%s"
        values = (buildingname, int(mapid))
        try:
            self.cur.execute(sql, values)
            self.cur.execute(sql, values)
        except self.UserException as ue:
            return dict(success=False, error=ue)
        except Exception as e:
            return dict(success=False, error=e)
        self.conn.commit()  # Commits the transaction, Insert
        return dict(success=True, error="")

    # function that searches for the center of a building utilizing its id, and returns the longitude and latitude
    def query_center(self, mapid):
        # print(type(mapid))
        sql = "SELECT longitude,latitude FROM mapdata WHERE mapid=%s"
        values = (
            int(mapid))  # variable containing the parameters, to easily insert
        try:
            self.cur.execute(sql, values)
            center = self.cur.fetchall()  # Gets the values returned by the select, center values
            if len(
                    center) == 0:  # checks if the Insert worked or not. If it works its value should be at least 1
                raise self.UserException("No data was selected.")
        except self.UserException as ue:
            return dict(success=False, error=str(ue))
        except Exception as e:
            return dict(success=False, error=e)
        return dict(success=True, error="", data={"longitude": center[0][0],
                                                  "latitude": center[0][
                                                      1]})  # it returns the longitude and latitude values

    # Function that returns all map id and building names
    def query_all(self):
        sql = "SELECT * FROM mapdata"
        try:
            self.cur.execute(sql)
            res = self.cur.fetchall()  # Gets the values returned by the select, the mapid and buildingname
            if len(
                    res) == 0:  # checks if the Insert worked or not. If it works its value should be at least 1
                raise self.UserException("No data in table \"mapdata\".")
        except self.UserException as ue:
            return dict(success=False, error=str(ue))
        except Exception as e:
            return dict(success=False, error=e)
        return dict(success=True, error="",
                    data=res)  # it returns the id and building name of the map

    # Function that searches for a building name utilizing its id and return the building name of the map
    def query_building_name(self, mapid):
        sql = "SELECT buildingname FROM mapdata where mapid=%s"
        int(mapid)
        try:
            self.cur.execute(sql, mapid)
            name = self.cur.fetchall()  # Gets the values returned by the select, building name
            if len(
                    name) == 0:  # checks if the select worked or not. If it works its value should be at least 1
                raise self.UserException("No data was selected.")
        except self.UserException as ue:
            return dict(success=False, error=str(ue))
        except Exception as e:
            return dict(success=False, error=e)
        return dict(success=True, error="",
                    data=name[0])  # it returns  the building name of the map

