import pymssql
from flask import Flask, render_template
from flask import jsonify
from flask import request
import requests
from flask_cors import CORS, cross_origin
import os
from flask_swagger_ui import get_swaggerui_blueprint

ips = Flask(__name__)
CORS(ips)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API Proof"
    }
)
ips.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

##Conexão com o SQL Server

ip = 'den1.mssql8.gear.host'
username ='ipstor'
password = 'Gi0vM-!lEq88'
database = 'ipstor'



cnxn = pymssql.connect(server='den1.mssql8.gear.host', user='ipstor', password='Gi0vM-!lEq88', database='ipstor')


#Endpoint GET onde exibe toda lista de IPs

@ips.route("/main", methods=['GET'])
def main():
    iplist = []
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM dbo.ipstor")
    for row in cursor.fetchall():
        iplist.append({"IP": row[0]})
    
    
    return render_template("index.html", iplist = iplist)


@ips.route("/get", methods=['GET'])
def get():
    iplist = []
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM dbo.ipstor")
    for row in cursor.fetchall():
        iplist.append({"IP": row[0]})
    
    return jsonify({'iplist' : iplist})


#Endpoint POST onde adiciona um ou mais IPs para a tabela blacklist

@ips.route('/post', methods=['POST'])
def post():
    ipblacklist = request.get_json()
    cursor = cnxn.cursor()
    sql = "INSERT INTO ipstor.dbo.blacklist(ips) values(%s)"
    iplist = []
    num = 0
    blacklist = []
    while num <= (len(ipblacklist['iplist']) -1):
      api3 = ipblacklist["iplist"][num]
      iplist.append(str(api3))
      num = num + 1
    cursor.executemany(sql, iplist)
    cnxn.commit()
    cursor.execute("SELECT * FROM dbo.blacklist")
    for row in cursor.fetchall():
        blacklist.append({"IP": row[0]}) 
    return jsonify({'iplist' : blacklist})
   

#Endpoint GET onde exibe toda lista de IPs com exceção do que estão em blacklist

@ips.route("/ativos", methods=['GET'])
def ativos():
    iplist = []
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM dbo.ipstor WHERE IP not in (SELECT ips from dbo.blacklist)")
    for row in cursor.fetchall():
        iplist.append({"IP": row[0]})
    
    return jsonify({'iplist' : iplist})


@ips.route("/ipativos")
def ipativos():
    iplist = []
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM dbo.ipstor WHERE IP not in (SELECT ips from dbo.blacklist)")
    for row in cursor.fetchall():
        iplist.append({"IP": row[0]})
    
    return render_template("ativos.html", iplist = iplist)


if(__name__ == "__main__"):
    port = int(os.environ.get('PORT', 5000))
    ips.run(debug=True, host='0.0.0.0', port=port)

