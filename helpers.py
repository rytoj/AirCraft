import mysql.connector
from mysql.connector import Error
from os import environ


class Color:
    light_red = "#E82A37"
    light_blue = "#6BA2D0"


class MysqlHelper:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.cursor = None
        self.connection = None

    def connect(self):
        """
        Connect to mysql database
        :return: True only when connection is established
        """

        try:
            self.connection = mysql.connector.connect(host=self.host,
                                                      database=self.database,
                                                      user=self.user,
                                                      password=self.password)
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("Connected to MySQL database... MySQL Server version on ", db_info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("Your connected to - ", record)
                return True
        except Error as e:
            print("Error while connecting to MySQL", e)
            return False

    def query(self, sql_select_query):
        """
        Fetch all the records present under a sql_select_query.
        :param sql_select_query: sql select query
            exp: 'select * from table_1'
        :return: Return query records
        """
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql_select_query)
        records = self.cursor.fetchall()
        return records

    def disconnect(self):
        """
        Closing database connection.
        """
        try:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("MySQL connection is closed")
        except AttributeError as e:
            print(e)


def table_template(table_rows, header_data="<tr></tr>", bg_color="#00FF00"):
    """
    :param header_data: table first lines, header data
    :param table_rows: main table data
    :param bg_color: table background color
    :return: html table with background color
    """
    return """
    <table style="width:100%" bgcolor="{COLOR}">
      <tr>
        {HEADER_DATA}
      </tr>
        {TR_DATA}
    </table>""".format(COLOR=bg_color, HEADER_DATA=header_data, TR_DATA=table_rows)


def run_as_standalone():
    sql = MysqlHelper(host='localhost',
                      database='Flights',
                      user='sup',
                      password=environ['DATABASE_PASS'])
    sql.connect()
    sql = sql.query("""SELECT 
AIRCRAFT.TAIL_NUMBER, MODEL.MODEL_NUMBER, MODEL.DESCRIPTION, COMPANIES.COMPANY_NAME, COUNTRY_CODES.CODE, COUNTRY_CODES.COUNTRY_NAME, COUNTRY_CODES.SDF_COC_002
FROM COMPANIES

INNER JOIN COUNTRY_CODES
ON COMPANIES.COC_AUTO_KEY = COUNTRY_CODES.COC_AUTO_KEY

INNER JOIN AIRCRAFT
ON AIRCRAFT.CMP_OWNER = COMPANIES.CMP_AUTO_KEY

INNER JOIN MODEL
ON AIRCRAFT.MDL_AUTO_KEY = MODEL.MDL_AUTO_KEY

-- ORDER BY NOT COUNTRY_CODES.SDF_COC_002
WHERE COUNTRY_CODES.SDF_COC_003 = "T" # (T = EU country, F = nonEU country) """)
    for elements in sql:
        print(elements)


if __name__ == '__main__':
    run_as_standalone()
