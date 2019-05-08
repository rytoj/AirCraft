from helpers import MysqlHelper
from helpers import table_template
from helpers import Color
from mail_helper import send_mail_mock
from os import environ


def get_europe_counties(european_union=True):
    """
    Creates sql query with dynamic 'COUNTRY_CODES.SDF_COC_003' parameter
    :param european_union: True = EU country, False = nonEU country
    :return: formed sql query
    """
    if european_union:
        eu = "T"
    else:
        eu = "F"
    return """SELECT 
        AIRCRAFT.TAIL_NUMBER, MODEL.MODEL_NUMBER, MODEL.DESCRIPTION, COMPANIES.COMPANY_NAME, COUNTRY_CODES.CODE, 
        COUNTRY_CODES.COUNTRY_NAME
        FROM COMPANIES

        INNER JOIN COUNTRY_CODES
        ON COMPANIES.COC_AUTO_KEY = COUNTRY_CODES.COC_AUTO_KEY

        INNER JOIN AIRCRAFT
        ON AIRCRAFT.CMP_OWNER = COMPANIES.CMP_AUTO_KEY

        INNER JOIN MODEL
        ON AIRCRAFT.MDL_AUTO_KEY = MODEL.MDL_AUTO_KEY

        -- ORDER BY NOT COUNTRY_CODES.SDF_COC_002
        WHERE COUNTRY_CODES.SDF_COC_003 = "{EU}" """.format(EU=eu)


def create_html_table(list_of_elements, color):
    """
    Forms html table from sql query
    :return: html table
    """
    table_inner = ""
    for elements in list_of_elements:
        td = "<td>{}</td>" * 6
        table_data = td.format(*elements)
        tr = "<tr>{}<tr>".format(table_data)
        table_inner += tr
    table = table_template(table_rows=table_inner, bg_color=color,
                           header_data="<th>Tail Number</th><th>Model Number</th><th>Description</th>"
                                       "<th>Company Name</th><th>Code</th><th>Company Name</th>")
    return table


def run_as_standalone():
    # Pass database login credentials to MysqlHelper
    sql = MysqlHelper(host='localhost',
                      database='Flights',
                      user='sup',
                      password=environ['DATABASE_PASS'])
    # Connect to database
    sql.connect()

    # Query EU countries from European Union
    sql_q_ = sql.query(get_europe_counties(european_union=True))
    # Construct table from mysql query
    table_eu_counties = create_html_table(sql_q_, color=Color.light_blue)

    # Query non EU countries from European Union
    sql_q_ = sql.query(get_europe_counties(european_union=False))
    # Construct table from mysql query
    table_non_eu_counties = create_html_table(sql_q_, color=Color.light_red)

    # Send mail to to mailtrap.io for testing
    send_mail_mock(sender="my@gmail.com", receiver="rec@gmail.com",
                   html1=table_eu_counties, html2=table_non_eu_counties, subject="Aircraft's EU and nonEu")


if __name__ == '__main__':
    run_as_standalone()
