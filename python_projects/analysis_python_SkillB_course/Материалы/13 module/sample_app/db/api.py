import pathlib
import sqlite3
import pandas as pd


DB_FILE = pathlib.Path(__file__).resolve().parent.joinpath("wind-data.db").resolve()


def get_wind_data(start, end):
    """
    Query wind data rows between two ranges

    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object 
    """

    con = sqlite3.connect(str(DB_FILE))
    statement = """SELECT Speed, SpeedError, Direction FROM Wind WHERE rowid > "{0}" AND rowid <= "{1}";""".format(start, end)
    df = pd.read_sql_query(statement, con)
    return df


def get_wind_data_by_id(id):
    """
    Query a row from the Wind Table

    :params id: a row id
    :returns: pandas dataframe object 
    """

    con = sqlite3.connect(str(DB_FILE))
    statement = """SELECT * FROM Wind WHERE rowid = "{0}";""".format(id)
    df = pd.read_sql_query(statement, con)
    return df