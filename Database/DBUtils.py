#import mysql
import sqlite3
"""This program uses the Table and Query classes to generate the SQL
to create the groceries database described in the Facade chapter."""
class Database():
    def __init__(self, *args):
        #self._db = MySQLdb.connect(args[0], args[1], args[2])
        self.host=args[0]
        self.userid=args[1]
        self.pwd = args[2]
        self._cursor = self._db.cursor()

    def commit(self):
        self._db.commit()

    def create(self, dbname):
        self.cursor.execute("drop database if exists "+dbname)
        self._cursor.execute("Create database "+ dbname)
        self._dbname = dbname
        #self._db=MySQLdb.connect(self.host, self.userid, self.pwd, dbname)
        self.cursor.execute("use "+dbname)
        self._cursor= self._db.cursor()

    def getName(self):
        return self._dbname

    @property
    def cursor(self):
        return self._cursor

    def getTables(self):
        self._cursor.execute("show tables")

        # create array of table objects
        self.tables = []
        rows = self._cursor.fetchall()
        for r in rows:
            self.tables.append(Table(self._cursor, r))
        return self.tables

class ColumnNames():
    def __init__(self, query):
        self.query = query

    def getColumnNames(self):
        # make list of tokens
        qlist = self.query.lower().split(' ')
        # remove trailing commas and stop at first SQL keyword
        newq = []
        i = 0
        quit = False
        while i < len(qlist) and not quit:
            ql = qlist[i].strip().removesuffix(',') #remove trailing commas
            if ql in {'from', 'join', 'where', 'inner'}: #stop on SQL keyword
                quit = True
            else:
                if ql not in { 'distinct', 'select'}:
                    newq.append(ql)     #insert name in column list
            i += 1
        # now remove leading table names
        # and split where there was a comma but no space
        newq2 = []
        for ql in newq:
            if '.' in ql:
                qa = ql.split('.')  # remove table name
                ql = qa[1]
            if ',' in ql:
                qa = ql.split(',')  # split at comma
                newq2.append(qa[0])  # when there is no space
                newq2.append(qa[1])  # between column names
            else:
                newq2.append(ql)
        return newq2            # return the column name array


# Query object makes queries and returns Results
class Query():
    def __init__(self, cursor, *qstring):
        self.qstring = qstring[0]
        self.multiple=False
        if len(qstring) >1:
            self.vals = qstring[1]
            self.multiple = True
        self.cursor = cursor



    def setMultiple(self, mult):
        self.multiple = mult

        # executes the query and returns all the results
    def execute(self):
        #print (self.qstring)
        self.getCols = ColumnNames(self.qstring)
        self.colNames = self.getCols.getColumnNames()
        if not self.multiple:
            self.cursor.execute(self.qstring)
            rows = self.cursor.fetchall()
            return Results(rows,  self.colNames)
        else:
            self.cursor.executemany(self.qstring, self.vals)

    def executeMultiple(self, vals):
        #print (self.qstring, vals)
        self.cursor.executemany(self.qstring, vals)

#  Mediator used by columns and Table class to keep
# the primary key string used in creating the SQL
class Mediator() :
    def __init__(self, db):
        self.db = db
        self.filename = ""
    def setPrimaryString(self, prims):
        self.pstring = prims
    def getPrimaryString(self):
        return self.pstring

# base class Column
class Column():
    def __init__(self, name):
        self._name=name
        self._primary = False

    def isPrimary(self):
       return self._primary

    @property
    def name(self):
        return self._name



# Integer column- may be a primary key
class Intcol(Column)  :
    def __init__(self, name, med:Mediator):
        super().__init__(name)
        self.med = med

    def getName(self):
        idname = self.name+" INT NOT NULL "
        return idname

class PrimaryCol(Intcol):
    def __init__(self, name, autoInc, med: Mediator):
        super().__init__(name, med)
        self.med = med
        self.autoInc = autoInc

    def getName(self):
        idname = self.name + " INT NOT NULL "
        if self.autoInc:
            idname += "AUTO_INCREMENT "

        self.med.setPrimaryString("PRIMARY KEY (" + self.name + ")")
        return idname

# Float col
class Floatcol(Column):
    def __init__(self, name):
        super().__init__(name)

    def getName(self):
        idname =  self.name + " FLOAT NOT NULL "
        return idname
# character column - length is  the 2nd argument
class Charcol(Column):
    def __init__(self, name, width:int):
        super().__init__(name)
        self.width=width
    def getName(self):
        idname =  self.name + " VARCHAR("+str(self.width)+") NULL "
        return idname
# Table class used to create all the table
class Table():
    def __init__(self, db, name, med:Mediator):
        self.cursor = db.cursor
        self.db = db
        self.tname = name   # first of tuple
        self.colList=[]     # list of column names generated
        self._primarystring = ""
        self.med = med

    @property
    def name(self):     # gets table name
        return self.tname

    # add a column
    def addColumn(self, column):
        self.colList.append(column)

        # creates the sql to make the columns
    def addRow(self, varnames):
            qry = "insert into " + self.tname + "("
            i = 0
            for i in range(1, len(self.colList) - 1):
                c = self.colList[i]
                # if type(c)==PrimaryCol:
                qry += c.name + ","
            qry += self.colList[-1].name + ") VALUES "
            #for i in range(1, len(self.colList) - 1):
            #    qry += "\'%s\',"
           # qry += "\'%s\') "
            #qry += " , "
            qry += varnames
            query = Query(self.cursor, qry, "")
            query.setMultiple(False)
            query.execute()
            self.db.commit()

    # creates the sql to make the columns
    def addRows(self, varnames):
        qry = "insert into "+self.tname +"("
        i = 0
        for i in range(1, len(self.colList)-1):
            c = self.colList[i]
            #if type(c)==PrimaryCol:
            qry += c.name + ","
        qry += self.colList[-1].name+") VALUES ("
        for i in range(1, len(self.colList) - 1):
            qry += "\'%s\',"
        qry +="\'%s\') "
        query = Query(self.cursor, qry, varnames)
        query.execute()
        self.db.commit()

    #deletes a row
    def deleteRow(self, colname, key):
        querytxt= "delete from "+self.tname+" where "+colname+ "="+key
        #print(querytxt)
        query = Query(querytxt)
       # query.execute()
       # self.db.commit()

    # creates the table and columns
    def create(self):
        sql = "create table "+self.db.getName()+"."+ self.name+" ("
        for col in self.colList:
            sql += col.getName()+","

        sql += self.med.getPrimaryString()
        sql +=")"
        #print (sql)
        self.cursor.execute(sql)

    # returns a list of columns
    def getColumns(self):
        self.cursor.execute("show columns from " + self.tname)
        self.columns = self.cursor.fetchall()
        return self.columns

# contains the result of a query
class Results():
    def __init__(self, rows, colNames):
        self.rows = rows
        self.cnames = colNames
        self.makeDict()

    def makeDict(self):
        self.dictRows = []
        #print(self.rows, self.cnames)

        for r in self.rows:
            self.makeDictRow(r)
        #print(self.dictRows)

    def makeDictRow(self, row):
        niter = iter(self.cnames)
        dict = {}
        for r in row:
            dict[next(niter)] = r
        self.dictRows.append(dict)

    def getRows(self):
        return self.rows

    def getDictRows(self):
        return self.dictRows

# holds primary key string as table is created
class Primary() :
    primaryString = ""

# Table class used to create all the table
class SqltTable(Table):
    def __init__(self, db, name):
        self.cursor = db.cursor()
        self.db = db
        self.tname = name   # first of tuple
        self.colList=[]     # list of column names generated
        self._primarystring = ""


    # creates the sql to make the columns--Sqlite differs slightly
    def addRows(self, varnames):
        qry = "insert into "+self.tname +"("
        i = 0
        for i in range(0, len(self.colList)-1):
            c = self.colList[i]
            qry += c.name + ","

        qry += self.colList[-1].name+") values ("
        for i in range(0, len(self.colList) - 1):
            qry += "?,"
        qry +="?);"

        query = Query(self.cursor, qry, varnames)
        #print(qry+"\n", varnames)
        query.execute()
        self.db.commit()

    # creates the table and columns
    def create(self):
        sql = "create table " +  self.name + " ("
        for col in self.colList:
            sql += col.getName()+","

        sql += Primary.primaryString
        sql +=");"
        #print (sql)
        self.cursor.execute(sql)

    def getColumns(self):
        tn = self.tname[0]
        #print(self.tname)
        sql="select name from pragma_table_info('"+tn+"')"
        #print(sql)
        self.cursor.execute(sql)
        self.columns = self.cursor.fetchall()
        return self.columns


class SqltDatabase(Database):
    def __init__(self, *args):
        self._db = sqlite3.connect(args[0])
        self._dbname = args[0]
        self._cursor = self._db.cursor()

    def create(self, dbname):
        pass
    def getTables(self):
        self._cursor.execute("select name from sqlite_master where type='table'")
        # create array of table objects
        self.tables = []
        rows = self._cursor.fetchall()
        for r in rows:
            self.tables.append(SqltTable(self._db, r))
        return self.tables


