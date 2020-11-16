import mysql.connector
import time
import datetime
import json

class classDbQueries(object):
    def __init__(self):
        db = 2
        if db == 1:
            self.mydb = mysql.connector.connect(
                    host = "localhost",
                    user = "root",
                    password = "aaaa",
                    database = "butane",
                    auth_plugin = "mysql_native_password"
                    )
        elif db == 2:
            self.mydb = mysql.connector.connect(
                    host = "klbcedmmqp7w17ik.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
                    user = "pi5ogoqbj8sq566j",
                    password = "qnkvxus0mbah43xr",
                    database = "cyf93gqg1kqnwqd1"
                    )

    def getTestRecord(self):
        self.mycursor = self.mydb.cursor(dictionary=True)
        query = "select * from props limit 555,1"
        try:
            self.mycursor.execute(query)
            x = self.mycursor.fetchone()
            if(x):
                diProps = x
            else:
                ##aaa76 tells js app that there are no records for this query
                diProps = "aaa33"
        except:
            diProps = "aaa35"
        return(diProps)

    def getPropRecords(self,filter1,searchField,operator,searchString,sort,startRecord,limit):
        ## example arguments
        # searchField = "owner_name"
        # operator = "like"
        # searchString = "frank"
        # sort = "asc"
        # startRecord = 10
        # limit = 3
        ##
        ## start the query
        ##
        filter2 = ""
        if searchString != '':
            filter2 = "and " + searchField + " " + operator + " '%" + searchString + "%'"
        if filter1 == "all":
            q1 = "select *, "
            q1 += "(select count(distinct(pid)) from props where property_address not like ''" + filter2 + ") as count "
            q1 += "from props "
            q1 += "where property_address not like '' "
            q1 += filter2
            q1 += " group by props.pid"
            q1 += " order by " + searchField + " " + sort
            q1 += " limit " + str(startRecord) + ", " + str(limit)
        elif filter1 == "mailings":
            q1 = "select *, "
            q1 += "(select count(distinct(props.pid)) from props inner join mailings on props.pid = mailings.pid where property_address not like ''" + filter2 + ") as count "
            q1 += "from props "
            q1 += "inner join mailings on props.pid = mailings.pid "
            q1 += "where property_address not like '' "
            q1 += filter2
            q1 += " group by props.pid"
            q1 += " order by " + searchField + " " + sort
            q1 += " limit " + str(startRecord) + ", " + str(limit)
        elif filter1 == "notes":
            q1 = "select props.*, "
            q1 += "(select count(distinct(props.pid)) from props inner join notes on props.pid = notes.pid where property_address not like '' and notes.active = 1 " + filter2 + ") as count "
            q1 += "from props "
            q1 += "inner join notes on props.pid = notes.pid "
            q1 += "where property_address not like '' "
            q1 += "and notes.active = 1 "
            q1 += filter2
            q1 += " group by props.pid"
            q1 += " order by " + searchField + " " + sort
            q1 += " limit " + str(startRecord) + ", " + str(limit)
        print(q1)
        self.mycursor = self.mydb.cursor(dictionary=True)
        self.mycursor.execute(q1)
        x = self.mycursor.fetchall()
        self.mycursor.close()
        return x

    def getNotesRecords(self):
        query = "select * from notes where active = 1 order by pid asc"
        self.mycursor = self.mydb.cursor(dictionary=True)
        self.mycursor.execute(query)
        listNotes = self.mycursor.fetchall()
        self.mycursor.close()
        return listNotes

    def getMailingRecords(self):
        query = "select * from mailings order by pid asc"
        self.mycursor = self.mydb.cursor(dictionary=True)
        self.mycursor.execute(query)
        listMailings = self.mycursor.fetchall()
        self.mycursor.close()
        return listMailings

    # def getMailingsforSingleProp(self,pid):
    #     query = "select * "
    #     query += " from mailings"
    #     #query += " where pid = 155238"
    #     query += " where pid = " + str(pid)
    #     query += " order by date_mailed desc"
    #     self.mycursor.execute(query)
    #     myresult = self.mycursor.fetchall()
    #     listMailings=[]
    #     for x in myresult:
    #         listMailings.append(datetime.datetime.strptime(str(x[1]), '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%y'))
    #     return(listMailings)

    # def getNotesforSingleProp(self,pid):
    #     query = "select * "
    #     query += " from props_notes"
    #     #query += " where pid = 198651"
    #     query += " where pid = " + str(pid)
    #     query += " order by time desc"
    #     self.mycursor.execute(query)
    #     myresult = self.mycursor.fetchall()
    #     listNotes=[]
    #     for x in myresult:
    #         listNotes.append(x[3])
    #     return(listNotes)

    def addNote(self,pid,note):
        query = "insert into notes (time,pid,notes,active) "
        query += "values(UNIX_TIMESTAMP(),"
        query += str(pid)
        query += ",'" + note + "',"
        query += "TRUE)"
        self.mycursor = self.mydb.cursor(dictionary=True)
        self.mycursor.execute(query)
        self.mydb.commit()
        return("hhh")

    def deleteNote(self,noteId):
        # query = "delete from notes where id = " + noteId
        query = "update notes set active = 0 where id = " + noteId
        self.mycursor = self.mydb.cursor(dictionary=True)
        self.mycursor.execute(query)
        self.mydb.commit()
        return("ddd135")

    def addMailing(self,pid):
        query = "insert into mailings (date_mailed,pid) "
        query += "values(NOW()," + pid + ")"
        self.mycursor = self.mydb.cursor(dictionary=True)
        self.mycursor.execute(query)
        self.mydb.commit()
        return("hhh")
