import sqlite3, datetime, string, getpass

#gets name of the user that is currently logged onto machine
username = getpass.getuser()

#the four files that will have data inside when program is ran
chromeHistoryFile = open('ChromeHistory.txt', 'a')
chromeLoginDataFile = open('ChromeLoginData.txt', 'a')
chromeDownloadsFile = open('ChromeDownloads.txt', 'a')
chromeCookiesFile = open('ChromeCookies.txt', 'a')

#Method which tells user about the program and how to access their data after running.
def toolPrompt():
    print("Success! \n")
    print("Now that you have run the program, the program has export your Chrome History, Login Data, etc into respective .txt files inside your current working directory. \nIf everything was succesful, you will receieve a message that the respective artifacts have been gathered below.")
    print("To access the data after completion, 'ls' to see the file names and 'cat' with the respective .txt file that you wish to access. Ex: cat ChromeHistory.txt \nThis is the quickest way, but it is not the only way to access your acquired data.\n\n\n")
    print("GATHERING DATA..\n\n")

#Parses the Chrome History Database File and gets useful data exported to .txt file
def ChromeHistory():
    #path of database file we will parse
    database_file = (r"C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History" %(username))
    db = sqlite3.connect(database_file)
    cursor = db.cursor()
    #querying all from urls table
    cursor.execute("SELECT * from urls")
    getdata = (cursor.fetchall())
    for row in getdata:
        #time is given in unix time so this is to convert it to something humans can understand
        history_time = str(datetime.datetime(1601,1,1) + datetime.timedelta(microseconds=row[5]))
        if history_time[:4] == "1601":
            pass
        else:
            history_time = str(datetime.datetime.strptime(history_time, "%Y-%m-%d %H:%M:%S.%f"))
            history_time = history_time[:-7]
            setstring = set(string.printable)
            history_title = "".join(filter(lambda x: x in setstring, row[2]))
            history_url = row[1]
        history_value = "Website visited: \" %s \" \" \nURL visited:  %s \nUsername: %s \nTime Visited: %s\n\n" %(history_title, history_url, username, history_time)   
        #exports data to file in a neat format
        chromeHistoryFile.write(history_value)

#Parses the Chrome Login Data Database File and gets useful data exported to .txt file
def ChromeLoginData():
    #path of database file we will parse
    database_file = (r"C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data" %(username))
    db = sqlite3.connect(database_file)
    cursor = db.cursor()
    #querying all from logins table
    cursor.execute("SELECT * from logins")
    getdata = (cursor.fetchall())
    for row in getdata:
        origin_url = row[0]
        username_element = row[2]
        username_value = row[3]
        loginData_value = "Website logged into: %s \nType of Element: %s \nUsername Used: %s \n\n" %(origin_url, username_element, username_value)
        #exports data to file in a neat format
        chromeLoginDataFile.write(loginData_value)

#Parses the Chrome History Database File and gets useful data exported to .txt file
def ChromeDownloads():
    #path of database file we will parse
    database_file = (r"C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History" %(username))
    db = sqlite3.connect(database_file)
    cursor = db.cursor()
    #querying all from downloads table
    cursor.execute("SELECT * from downloads")
    getdata = (cursor.fetchall())
    for row in getdata:
        target_path = row[3]
        size_in_bytes = row[6]
        tab_url = row[17]
        last_modified = row[23]
        mime_type = row[24]
        downloads_value = "Target Path: %s \nSize of Download in Bytes: %s \nURL downloaded from: %s \nLast Modified: %s \nFile Type: %s\n\n" %(target_path, size_in_bytes, tab_url, last_modified, mime_type)
        #exports data to file in a neat format
        chromeDownloadsFile.write(downloads_value)

#Parses the Chrome Cookies Database File and gets useful data exported to .txt file
def ChromeCookies():
    #path of database file we will parse
    database_file = (r"C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies" %(username))
    db = sqlite3.connect(database_file)
    cursor = db.cursor()
    #querying creation_utc, host_key, expires_utc, last_access_utc from cookies table
    cursor.execute("SELECT creation_utc, host_key, expires_utc, last_access_utc from cookies")
    getdata = (cursor.fetchall())
    for row in getdata:
        creation_utc = (row[0])
        expires_utc = (row[2])
        last_access_utc = (row[3])
        host_key = row[1]
        cookies_value = "Creation Time: %s \nHost Key: %s \nExpiration Time: %s \nLast Accessed: %s\n\n" %(creation_utc, host_key, expires_utc, last_access_utc)
        #exports data to file in a neat format
        chromeCookiesFile.write(cookies_value)

if __name__ == "__main__":
    toolPrompt()
    ChromeHistory()
    print("Google Chrome browsing history gathered.")
    ChromeLoginData()
    print("Google Chrome login data gathered.")
    ChromeDownloads()
    print("Google Chrome downloads data gathered.")
    ChromeCookies()
    print("Google Chrome cookies data gathered.")