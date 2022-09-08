import pyodbc
import requests
import json

##Conexão com o SQL Server

ip = 'den1.mssql8.gear.host'
username ='ipstor'
password = 'Gi0vM-!lEq88'
database = 'ipstor'
num = 0
num2 = 0

cnxn = pyodbc.connect(
       'DRIVER={ODBC Driver 17 for SQL Server}' + 
       ';SERVER=' + ip + ';UID=' + username + 
       ';PWD=' + password +
       ';database='+ database)

sql = "INSERT INTO ipstor.dbo.ipstor(IP) values(?)"
sqldelete = "DELETE FROM ipstor.dbo.ipstor"
cursor = cnxn.cursor()
iplist = []

api = requests.get("https://www.dan.me.uk/torlist/").text
substring = "Umm..."
if substring not in api: 
    cursor.execute(sqldelete)
    cnxn.commit()
    
    ##Primeira lista de IPs
    ip = requests.get("https://onionoo.torproject.org/summary?limit=5000").json()
    while num <= (len(ip['relays']) -1):
        api3 = ip['relays'][num]['a'][0]
        iplist.append([str(api3)])
        num = num + 1
    cursor.fast_executemany = True
    cursor.executemany(sql, iplist)
    print('Primeira lista salva no banco de dados com sucesso!')
    cnxn.commit() 

    ##Segunda lista de IPs
    api2 = api.split("\n")
    iplist2 = []
    while num2 <= (len(api2) -1): 
        if api2[num2] != "":
            iplist2.append([api2[num2]])
        num2 = num2 + 1
    cursor.executemany(sql, iplist2)
    print('Segunda lista salva no banco de dados com sucesso!')
    cnxn.commit()
else:
    print('Esperar 30 minutos para request de lista de IPs!')
cnxn.close()
