"""
 Methods to parse a JSON snapshot and return Dict objects
 Methods with names that start with '_' are private and should not be
 called external to this file
"""


def _find_column(snapshot, snapshot_id):
    """
    Private method to find a Column that matches the snapshot ID
    :param snapshot:     the snapshot to parse
    :param snapshot_id:  the snapshot ID that we are looking for
    :return:             the Column Dict or None
    """
    all_columns = snapshot["snapshot"]["objects"]["liquibase.structure.core.Column"]
    for column in all_columns:
        if column["column"]["snapshotId"] == snapshot_id:
            return column
    return None


def _find_primary_key(snapshot, snapshot_id):
    """
    Private method to find a Primary Key that matches the snapshot ID
    :param snapshot:     the snapshot to parse
    :param snapshot_id:  the snapshot ID that we are looking for
    :return:             the Primary Key Dict or None
    """
    all_primary_keys = snapshot["snapshot"]["objects"]["liquibase.structure.core.PrimaryKey"]
    for primary_key in all_primary_keys:
        if primary_key["primaryKey"]["snapshotId"] == snapshot_id:
            return primary_key
    return None


def _find_index(snapshot, snapshot_id):
    """
    Private method to find an Index that matches the snapshot ID
    :param snapshot:     the snapshot to parse
    :param snapshot_id:  the snapshot ID that we are looking for
    :return:             the Index Dict or None
    """
    all_indexes = snapshot["snapshot"]["objects"]["liquibase.structure.core.Index"]
    for index in all_indexes:
        if index["index"]["snapshotId"] == snapshot_id:
            return index
    return None


def _get_snapshot_id(snapshot_key):
    """
    Private method to get the snapshot ID from a key of the form "liquibase.structure.core.<object name>"#<snapshot id>
    :param snapshot_key:     the key to split
    :return:                 the snapshot ID portion
    """
    return snapshot_key.split("#")[1]


def _get_column_type_info(column):
    """
    Private method to get the snapshot ID from a key of the form "liquibase.structure.core.<object name>"#<snapshot id>
    :param column:     the key to split
    :return:           the snapshot ID portion
    """
    if "type" in column["column"]:
        return column["column"]["type"]
    return None


def get_tables(snapshot):
    """
    Return a list of Table Dict objects
    :param snapshot:     the snapshot to parse
    :return:             List of Table Dict objects or None
    """
    if snapshot is None:
        return None
    return snapshot["snapshot"]["objects"]["liquibase.structure.core.Table"]


def get_table(snapshot, table_name):
    """
    Return the requested table object
    :param snapshot      the snapshot to parse
    :param table_name:   the name of the table to search for
    :return:             the Table Dict object that matches the table_name or None
    """
    tables = get_tables(snapshot)
    for table in tables:
        if table["table"]["name"] == table_name:
            return table
    return None


def get_columns(snapshot, table_name):
    """
    Return a list of Column Dict objects for a table
    :param   snapshot:   the snapshot to parse
    :param   table_name: the name of the table to search for
    :return:             the Column Dict objects or None
    """
    return_list = []
    table = get_table(snapshot, table_name)
    columns = table["table"]["columns"]
    for snapshot_key in columns:
        snapshot_id = _get_snapshot_id(snapshot_key)
        column = _find_column(snapshot, snapshot_id)
        if column is not None:
            return_list.append(column)
    return return_list


def get_column(snapshot, table_name, column_name):
    """
    Return the specified Column Dict object for a table
    :param   snapshot:     the snapshot to parse
    :param   table_name:   the name of the table to search for
    :param   column_name:  the name of the column to search for
    :return:               the Column Dict object or None
    """
    table = get_table(snapshot, table_name)
    columns = table["table"]["columns"]
    for snapshot_key in columns:
        snapshot_id = _get_snapshot_id(snapshot_key)
        column = _find_column(snapshot, snapshot_id)
        if column is not None and column["column"]["name"] == column_name:
            return column
    return None


def get_column_size(column):
    """
    Return the specified Column's size
    :param   column:   the Column Dict object
    :return:           the column size as an int
    """
    type_info = _get_column_type_info(column)
    if type_info is not None and "columnSize" in type_info:
        size_string = type_info["columnSize"]
        if "!" in size_string:
            return int(size_string.split("!")[0])
    return None


def get_column_type_name(column):
    """
    Return the specified Column's type name
    :param   column:   the Column Dict object
    :return:           the column's type name
    """
    type_info = _get_column_type_info(column)
    if "typeName" in type_info:
        return type_info["typeName"]
    return None


def get_primary_key(snapshot, table_name):
    """
    Return a Primary Key Dict object for a table
    :param   snapshot:     the snapshot to parse
    :param   table_name:   the name of the table to search for
    :return:               the Primary Key Dict object or None
    """
    table = get_table(snapshot, table_name)
    if "primaryKey" in table["table"]:
        snapshot_id = table["table"]["primaryKey"]
        primary_key_id = _get_snapshot_id(snapshot_id)
        return _find_primary_key(snapshot, primary_key_id)
    return None


def get_indexes(snapshot, table_name):
    """
    Return a List of Index Dict objects for a table
    :param   snapshot:     the snapshot to parse
    :param   table_name:   the name of the table to search for
    :return:               the Index Dict objects or None
    """
    return_list = []
    table = get_table(snapshot, table_name)
    if "indexes" in table["table"]:
        indexes = table["table"]["indexes"]
        for snapshot_key in indexes:
            index_id = _get_snapshot_id(snapshot_key)
            index = _find_index(snapshot, index_id)
            return_list.append(index)
    return return_list
