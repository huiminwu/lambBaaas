#lambBaaas -- Hui Min Wu, Raunak Chowdhury, Anton Danylenko
#SoftDev1 pd8
#P02 -- The End

import sqlite3   # enable control of an sqlite database

class DB_Manager:
    '''
    HOW TO USE:
    Every method openDB by connecting to the inputted path of
    a database file. After performing all operations on the
    database, the instance of the DB_Manager must save using
    the save method.
    The operations/methods can be found below. DB_Manager
    has been custom fitted to work with
    P00 -- Da Art of Storytellin'
    '''
    def __init__(self, dbfile):
        '''
        SET UP TO READ/WRITE TO DB FILES
        '''
        self.DB_FILE = dbfile
        self.db = None
    #========================HELPER FXNS=======================
    def openDB(self):
        '''
        OPENS DB_FILE AND RETURNS A CURSOR FOR IT
        '''
        self.db = sqlite3.connect(self.DB_FILE) # open if file exists, otherwise create
        return self.db.cursor()

    def tableCreator2(self, tableName, col0, col1):
        '''
           CREATES A 2 COLUMN TABLE IF tableName NOT TAKEN
        ALL PARAMS ARE STRINGS
        '''
        c = self.openDB()
        if not self.isInDB(tableName):
            command = "CREATE TABLE '{0}'({1}, {2});".format(tableName, col0, col1)
            c.execute(command)

    def tableCreator3(self, tableName, col0, col1, col2):
        '''
           CREATES A 3 COLUMN TABLE IF tableName NOT TAKEN
        ALL PARAMS ARE STRINGS
        '''
        c = self.openDB()
        if not self.isInDB(tableName):
            command = "CREATE TABLE '{0}'({1}, {2}, {3});".format(tableName, col0, col1, col2)
            c.execute(command)

    def tableCreator4(self, tableName, col0, col1, col2, col3):
        '''
           CREATES A 4 COLUMN TABLE IF tableName NOT TAKEN
        ALL PARAMS ARE STRINGS
        '''
        c = self.openDB()
        if not self.isInDB(tableName):
            command = "CREATE TABLE '{0}'({1}, {2}, {3}, {4});".format(tableName, col0, col1, col2, col3)
            c.execute(command)


    def insertRow(self, tableName, data):
       '''
         APPENDS data INTO THE TABLE THAT CORRESPONDS WITH tableName
         @tableName is the name the table being written to
         @data is a tuple containing data to be entered
       '''
       c = self.openDB()
       command = "INSERT INTO '{0}' VALUES(?, ?)"
       c.execute(command.format(tableName), data)


    def isInDB(self, tableName):
        '''
        RETURNS True IF THE tableName IS IN THE DATABASE
        RETURNS False OTHERWISE
        '''
        c = self.openDB()
        command = "SELECT * FROM sqlite_master WHERE type = 'table'"
        c.execute(command)
        selectedVal = c.fetchall()
        # list comprehensions -- fetch all tableNames and store in a set
        tableNames = set([x[1] for x in selectedVal])

        return tableName in tableNames

    def table(self, tableName):
        '''
        PRINTS OUT ALL ROWS OF INPUT tableName
        '''
        c = self.openDB()
        command = "SELECT * FROM '{0}'".format(tableName)
        c.execute(command)
        return c.fetchall()


    def save(self):
        '''
        COMMITS CHANGES TO DATABASE AND CLOSES THE FILE
        '''
        self.db.commit()
        self.db.close()
    #========================HELPER FXNS=======================
    #===========================DB FXNS========================

    def createUsers(self):
        '''
        CREATES TABLE OF users
        '''
        self.tableCreator2('users', 'user_name text', 'passwords text')
        return True

    def createTyping(self):
        '''
        CREATES TABLE OF USERS, WPM, TIMESTAMP, AND DIFFICULTY
        '''
        self.tableCreator4('typing', 'user_name text', 'wpm int', 'timestamp int', 'difficulty int')
        return True

    def createVocab(self):
        '''
        CREATES TABLE OF VOCAB WORDS AND DEFINITIONS
        '''
        self.tableCreator3('vocab', 'user_name text', 'word text', 'definition text')
        return True
    def getUsers(self):
        '''
        RETURNS A DICTIONARY CONTAINING ALL CURRENT users AND CORRESPONDING PASSWORDS'
        '''
        c = self.openDB()
        command = "SELECT user_name, passwords FROM users"
        c.execute(command)
        selectedVal = c.fetchall()
        return dict(selectedVal)

    def get_user_ids(self, storyTitle):
        '''
        RETURNS SET OF user_ids CONTRIBUTED TO storyTitle
        '''
        c = self.openDB()
        command = "SELECT user_id FROM '{0}'".format(storyTitle)
        c.execute(command)
        ids = set(x[0] for x in c.fetchall())
        return ids

    def registerUser(self, userName, password):
        '''
        ADDS user TO DATABASE
        '''
        c = self.openDB()
        # userName is already in database -- do not continue to add
        if self.findUser(userName):
            return False
        # userName not in database -- continue to add
        else:
            row = (userName, password)
            self.insertRow('users', row)
            return True

    def findUser(self, userName):
        '''
        CHECKS IF userName IS UNIQUE
        '''
        return userName in self.getUsers()

    def verifyUser(self, userName, password):
        '''
        CHECKS IF userName AND password MATCH THOSE FOUND IN DATABASE
        '''
        c = self.openDB()
        command = "SELECT user_name, passwords FROM users WHERE user_name = {0}".format("'" + userName + "'")
        c.execute(command)
        selectedVal = c.fetchone()
        if selectedVal == None:
            return False
        if userName == selectedVal[0] and password == selectedVal[1]:
            return True
        return False

    def getID_fromUser(self, userName):
        '''
        RETURNS user_id OF userName
        '''
        c = self.openDB()
        command = "SELECT user_id FROM users WHERE user_name == '{0}'".format(userName)
        c.execute(command)
        id = c.fetchone()[0]
        return id
    
    # def saveWPM(self, userName, wpm, timestamp, difficulty):

    # def saveWord(seld, userName, word, definition):

    def getLeaderboard():
        c = self.openDB()
        command = "SELECT * FROM typing ORDER BY wpm".format(tableName)
        c.execute(command)
        return c.fetchall()

   

