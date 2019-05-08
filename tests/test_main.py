import unittest
from helpers import MysqlHelper
from helpers import table_template
from os import environ


class SqlConnect(unittest.TestCase):
    def setUp(self):
        self.sql = MysqlHelper(host='localhost',
                               database='Flights',
                               user='sup',
                               password=environ['DATABASE_PASS'])

    def test_connect(self):
        """
        Tests connection to database with correct credentials
        """
        self.assertEqual(self.sql.connect(), True)

    def test_sql_query(self):
        """
        Tests if sql.query returns non empty table
        """
        self.sql.connect()
        sql = self.sql.query("""SELECT variable, value, set_time, set_by FROM sys.sys_config;""")
        self.assertTrue(len(sql) > 0)


class CrateTable(unittest.TestCase):
    def test_create_table(self):
        table = table_template(table_rows="<tr>data</tr>")
        result = '<table style="width:100%" bgcolor="#00FF00">      <tr>        <tr></tr>      </tr>        ' \
                 '<tr>data</tr>    </table> '
        self.assertTrue(table.strip().replace("\n", ""), result)
