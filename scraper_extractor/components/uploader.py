import mysql.connector
import os


class Uploader:
    def __init__(self, extracted_data):
        self.extracted_data = extracted_data

    def upload(self):
        self.connect()
        self.insert()
        self.close()

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

    def insert(self):

        def transform_icon(icon_url):
            if 'http' not in icon_url:
                return 'https://community.cloudflare.steamstatic.com/economy/image/' + icon_url
            else:
                return icon_url

        print('Upsert started...')
        for case in self.extracted_data:
            self.cursor.execute("INSERT INTO cases (name, icon_url) VALUES (%s, %s) ON DUPLICATE KEY UPDATE icon_url=VALUES(icon_url)", (case['name'], transform_icon(case['asset_description']['icon_url'])))
            caseId = self.cursor.lastrowid
            if caseId == 0:
                self.cursor.execute("SELECT id FROM cases WHERE name=%s", [case['name']])
                caseId = list(self.cursor)[0][0]
            self.cursor.execute("INSERT IGNORE INTO prices (caseId, sale_price, total, timestamp) VALUES (%s, %s, %s, %s)",
                                (caseId, case['sale_price'], case['total'], int(case['timestamp'])))
            if 'key' in case.keys():
                self.cursor.execute("INSERT INTO caseKeys (caseId, name, icon_url) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name), icon_url=VALUES(icon_url)", (caseId, case['key']['name'], transform_icon(case['key']['asset_description']['icon_url'])))
                self.cursor.execute("SELECT id FROM caseKeys WHERE name=%s", [case['key']['name']])
                keyId = list(self.cursor)[0][0]

            # Case description
            for i, descField in enumerate(case['asset_description']['descriptions']):
                if descField['value'] == ' ':
                    continue
                if 'color' not in descField.keys():
                    descField['color'] = 'NULL'
                ins0 = "INSERT INTO descriptionFields (caseId, ind, value, color) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE value=VALUES(value), color=VALUES(color)"
                self.cursor.execute(ins0, (caseId, i, descField['value'], descField['color']))
                if 'total' not in descField.keys():
                    continue
                descriptionFieldId = self.cursor.lastrowid
                if descriptionFieldId == 0:
                    self.cursor.execute("SELECT id FROM descriptionFields WHERE caseId=%s and ind=%s", [caseId, i])
                    descriptionFieldId = list(self.cursor)[0][0]
                ins1 = "INSERT IGNORE INTO descriptionPrices (descriptionFieldId, total, timestamp) VALUES (%s, %s, %s)"
                self.cursor.execute(ins1, (descriptionFieldId, descField['total'], int(case['timestamp'])))

            # Key description
            if 'key' in case.keys():
                for i, descField in enumerate(case['key']['asset_description']['descriptions']):
                    if descField['value'] == ' ':
                        continue
                    if 'color' not in descField.keys():
                        descField['color'] = 'NULL'
                    ins0 = "INSERT INTO keysDescriptionFields (caseKeyId, ind, value, color) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE value=VALUES(value), color=VALUES(color)"
                    self.cursor.execute(ins0, (keyId, i, descField['value'], descField['color']))

        self.cnx.commit()
        print('Upsert done.')

    def close(self):
        self.cursor.close()
        self.cnx.close()
        self.cnx = None
        print('Connection to database successfully closed.')
