"""
Methods to return attributes of the Database object
"""


def get_database_product_name(database):
    """
    Returns the database product name
    :param    database:  the database instance
    :return:  string     the database product name
    """
    return database.getDatabaseProductName()


def get_database_product_version(database):
    """
    Returns the database product version
    :param    database:    the database instance
    :return:  string       the database product version
    """
    return database.getDatabaseProductVersion()


def get_short_name(database):
    """
    Returns the database short name

    :param    database:   the database instance
    :return:  string      the database short name lower-cased, i.e oracle, mssql
    """
    return database.getShortName()


def get_default_schema_name(database):
    """
    Returns the default schema for this database
    :param    database:   the database instance
    :return:  string      the default schema name, None if the database has no default schema
    """
    return database.getDefaultSchemaName()
