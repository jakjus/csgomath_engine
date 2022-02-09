from flask import Flask
from flask_cors import CORS
import os
import mysql.connector

app = Flask(__name__)
CORS(app)


class Db:
    def connect(self):
        root_pass = os.environ.get('MARIADB_ROOT_PASSWORD')
        # root_pass is defined, if process run from docker-compose
        if root_pass:
            host = 'db'
            root_pass = root_pass
        else:
            host = 'localhost'
            root_pass = 'example'
        self.cnx = mysql.connector.connect(user='root',
                                           password=root_pass,
                                           host=host,
                                           database='extracted')
        self.cursor = self.cnx.cursor()
        print('Connected to database.')

    def select_cases_keys(self):
        full = []
        self.cursor.execute("SELECT id, name, icon_url FROM cases")
        for (caseId, name, icon_url) in list(self.cursor):
            # Case
            self.cursor.execute("SELECT caseId, sale_price, total, timestamp FROM prices WHERE caseId = %s", [caseId])
            prices = []
            for (caseId, sale_price, total, timestamp) in self.cursor:
                prices.append({'sale_price': sale_price,
                              'total': total, 'timestamp': timestamp})
            case = {'id': caseId, 'name': name,
                    'icon_url': icon_url, 'prices': prices}
            # Key
            self.cursor.execute("SELECT id, caseId, name, icon_url FROM caseKeys WHERE caseId = %s", [caseId])
            key = None
            for (keyId, caseId, name, icon_url) in self.cursor:
                key = {'id': keyId, 'name': name, 'icon_url': icon_url}
            full.append({'case': case, 'key': key})
        return full

    def select_case_description(self, caseId):
        full = []
        self.cursor.execute(
            "SELECT id, caseId, ind, value, color FROM descriptionFields WHERE caseId = %s", [caseId])
        for (descId, caseId, ind, value, color) in list(self.cursor):
            self.cursor.execute("SELECT descriptionFieldId, total, timestamp FROM descriptionPrices WHERE descriptionFieldId = %s", [descId])
            prices = []
            for (descriptionFieldId, total, timestamp) in self.cursor:
                prices.append({'total': total, 'timestamp': timestamp})
            full.append({'ind': ind, 'value': value, 'color': color, 'prices': prices})
        return full

    def select_key_description(self, keyId):
        full = []
        self.cursor.execute(
            "SELECT caseKeyId, ind, value, color FROM keysDescriptionFields WHERE caseKeyId = %s", [keyId])
        for (caseKeyId, ind, value, color) in self.cursor:
            full.append({'ind': ind, 'value': value, 'color': color})
        return full

    def close(self):
        self.cursor.close()
        self.cnx.close()
        self.cnx = None
        print('Connection to database successfully closed.')


db = Db()


@app.route("/api/cases")
def get_cases():
    db.connect()
    full = db.select_cases_keys()
    db.close()
    return {'data': full}


@app.route("/api/case_description/<caseId>")
def get_case_description(caseId):
    db.connect()
    full = db.select_case_description(caseId)
    db.close()
    return {'data': full}


@app.route("/api/key_description/<keyId>")
def get_key_description(keyId):
    db.connect()
    full = db.select_key_description(keyId)
    db.close()
    return {'data': full}
