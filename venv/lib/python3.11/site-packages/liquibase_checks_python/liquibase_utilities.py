import polyglot
import liquibase_constants as constants
import sqlparse
import json

script_constants = constants.Constants()


def get_binding(key):
    """
    Access the binding object at the given key
    :param key: the binding to access
    :return: the binding
    """
    return polyglot.import_value(key)


def get_database():
    """
    Get the liquibase database object
    :return: the liquibase database object
    """
    return get_binding(script_constants.DATABASE_BINDING)


def get_changes():
    """
    Return a list of Liquibase Change objects
    :return: the liquibase change objects
    """
    return get_binding(script_constants.CHANGES_BINDING)


def get_changeset():
    """
    Return the Liquibase Change Set object
    :return: the liquibase change set object
    """
    return get_binding(script_constants.CHANGESET_BINDING)


def get_database_object():
    """
    Return the DatabaseObject that is being referenced in a database-scoped check
    :return: the current database object being checked
    """
    object = get_binding(script_constants.DATABASE_OBJECT_BINDING)
    if object is None:
        if get_binding(script_constants.CHECKS_SCOPE_BINDING) == "CHANGELOG":
            raise Exception("No database object available in CHANGELOG scope")
        else:
            raise Exception("No database object available in binding")
    return object


def get_database_snapshot():
    """
    Return the DatabaseSnapshot as a String
    :return: the database snapshot string
    """
    return get_binding(script_constants.DATABASE_SNAPSHOT_BINDING)


def get_snapshot():
    """
    Return the snapshot as a JSON object.
    :return: The snapshot json object or None if no snapshot is available
    """
    snapshot = get_database_snapshot()
    if snapshot is None:
        return None
    return json.loads(str(snapshot))


def get_dbutil():
    """
    Return the dbutil object used to check for object existence or to snapshot the DatabaseObject and return it
    :return: the db_util object
    """
    return get_binding(script_constants.DBUTIL_BINDING)


def _create_example_object(type, schema_name, object_name):
    """
    Create an example Liquibase object of the specified type for the schema and name
    :param type: the object type
    :param schema_name: the schema name
    :param object_name: the object name
    :return: the new example object
    """
    dbutil = get_dbutil()
    example_object = dbutil.createExampleObject(type)
    example_object.setName(object_name)
    if schema_name is None:
        example_object.setSchema(None, get_database().getDefaultCatalogName())
    else:
        example_object.setSchema(dbutil.createSchemaObject(get_database().getDefaultCatalogName(), schema_name))
    return example_object


def _create_example_relation_object(object_type, object_name, relation_object):
    """
    Create an example relation object (Table or View)
    :param object_type: the object type
    :param object_name: the object name
    :param relation_object: the object to relate to
    :return: the new example object with its relation set
    """
    dbutil = get_dbutil()
    example_object = dbutil.createExampleObject(object_type)
    example_object.setName(object_name)
    example_object.setRelation(relation_object)
    return example_object


#
#
#
# type            - The type of the object, like Table
# object_name     - The object's name
# relation_type   - A type of relation that we need to snapshot to access the object
# schema_name     - The schema for the relation object
# relation_name   - The name of the relation object
#
def snapshot_object(object_type, object_name, relation_type, schema_name, relation_name):
    """
    Return a Liquibase model object that represents a database object
    :param object_type: the type of the object, like Table
    :param object_name: the objects name
    :param relation_type: a type of relation that we need to snapshot to access the object
    :param schema_name: the schema for the relation
    :param relation_name: the name of the relation
    :return: the liquibase model for the database object
    """
    dbutil = get_dbutil()
    if relation_type is None:
        return dbutil.snapshotObject(_create_example_object(object_type, schema_name, object_name), get_database())
    else:
        relation_object = _create_example_object(relation_type, schema_name, relation_name)
        example_object = dbutil.createExampleObject(object_type)
        example_object.setName(object_name)
        example_object.setRelation(relation_object)
        return dbutil.snapshotObject(example_object, get_database())


def get_object_type_name(database_object):
    """
    Get the object type string of a given database object
    :param database_object The database_object to return the type for
    :returns the type as a string
    """
    return database_object.getObjectTypeName()


def has(object_type, schema_name, object_name):
    """
    Returns true if there is an object of this type and name in the schema
    :param object_type: the object type
    :param schema_name: the schema name
    :param object_name: the object name
    :return: true if there is an object that matches this description, false otherwise
    """
    dbutil = get_dbutil()
    example_object = _create_example_object(object_type, schema_name, object_name)
    return dbutil.hasA(example_object, get_database())


def has_relation(object_type, object_name, relation_type, relation_schema_name, relation_name):
    """
    Returns true if there is an object of this type that has a relation object  that matches the relation type, schema,
    and name
    :param object_type: the object type
    :param object_name: the object name
    :param relation_type: the type of relation (Table or View)
    :param relation_schema_name: the schema of the relation object
    :param relation_name: the name of the relation
    :return:
    """
    relation_object = _create_example_object(relation_type, relation_schema_name, relation_name)
    example_object = _create_example_relation_object(object_type, object_name, relation_object)
    dbutil = get_dbutil()
    return dbutil.hasA(example_object, get_database())


def query_for_list(sql, sql_file, end_delimiter):
    """
    Execute a SQL statement or script
    :param sql: the sql to execute
    :param sql_file: the sql file to execute
    :param end_delimiter: the end delimiter to use
    :return: the results of the sql execution as a list
    """
    return get_dbutil().queryForList(sql, sql_file, end_delimiter, get_database())


def get_status():
    """
    Return the Status object which will be used to set the check fired status and return a message
    :return: the status object
    """
    return get_binding(script_constants.STATUS_BINDING)


def get_script_path():
    """
    Return the path of the script
    :return: the path of the script
    """
    return str(get_binding(script_constants.SCRIPT_PATH_BINDING))


def get_logger():
    """
    Get the liquibase logger
    :return: the liquibase logger
    """
    return get_binding(script_constants.LOGGER_BINDING)


def get_script_message():
    """
    Get the message for the script
    :return: the message
    """
    return get_binding(script_constants.SCRIPT_MESSAGE_BINDING)


def get_arg(name):
    """
    Return the value of script argument
    :param name: the argument to find
    :return: the value of the argument
    """
    return str(get_binding(name + script_constants.ARGS_SUFFIX))


def get_cache(key, default_value):
    """
    Return the results cache Dict object from the bindings
    if there is no current value then put the default value
    :param key            the look up key
    :param default_value  the value to put for the key if no value present
    :return:              the current value or the default
    """
    cache = get_binding(script_constants.CACHE_BINDING)
    value = cache.get(key)
    if value is None:
        cache.put(key, default_value)
        return default_value
    return value


def put_cache(key, value):
    """
    Put the value in the cache
    :param  key            The key to use
    :param  value          The value to put in the cache
    """
    cache = get_binding(script_constants.CACHE_BINDING)
    cache.put(key, value)


def generate_sql(change):
    """
    Generate the SQL for this change and database
    :param change: the change to generate sql from
    :return: the sql of the change
    """
    return get_dbutil().generateSql(change, get_database())


def strip_comments(sql_string):
    """
    Strip comments from a SQL string
    :param sql_string: the sql to strip
    :return: the sql string with comments removed
    """
    return get_dbutil().stripComments(sql_string)


def split_statements(sql_string):
    """
    Split a string of SQL into individual statements
    :param sql_string: the sql string to split
    :return: the list of sql strings
    """
    return sqlparse.split(sql_string.strip())


def split_sql(sql_string, strip_comments_flag, end_delimiter, changeset):
    """
    Returns an array of SQL lines
    :param   sql_string: the SQL to process
    :param   strip_comments_flag: true to strip out comments
    :param   end_delimiter: the end delimiter to use while processing the sql
    :param   changeset: the change set associated with the sql
    :return: the list of SQL lines
    """
    return get_dbutil().processMultiLineSQL(sql_string.strip(),
                                            strip_comments_flag,
                                            True,
                                            end_delimiter,
                                            changeset)


def tokenize(statement):
    """
    Tokenize a statement which was create by sqlparse and return a list
    :param statement: the statement to tokenize
    :return: the tokenized statement as a list
    """
    parsed = sqlparse.parse(statement)
    stmt = parsed[0]
    return stmt.tokens


def is_table(database_object):
    """
    Check if the database object is a table
    :param database_object: the database object to check
    :return: true if the object is a table, false otherwise
    """
    return "table" == get_object_type_name(database_object)


def is_column(database_object):
    """
    Check if the database object is a column
    :param database_object: the database object to check
    :return: true if the object is a column, false otherwise
    """
    return "column" == get_object_type_name(database_object)


def is_catalog(database_object):
    """
    Check if the database object is a catalog
    :param database_object: the database object to check
    :return: true if the object is a catalog, false otherwise
    """
    return "catalog" == get_object_type_name(database_object)


def is_foreign_key(database_object):
    """
    Check if the database object is a foreign key
    :param database_object: the database object to check
    :return: true if the object is a foreign key, false otherwise
    """
    return "foreignKey" == get_object_type_name(database_object)


def is_index(database_object):
    """
    Check if the database object is a index
    :param database_object: the database object to check
    :return: true if the object is a index, false otherwise
    """
    return "index" == get_object_type_name(database_object)


def is_primary_key(database_object):
    """
    Check if the database object is a primary key
    :param database_object: the database object to check
    :return: true if the object is a primary key, false otherwise
    """
    return "primaryKey" == get_object_type_name(database_object)


def is_schema(database_object):
    """
    Check if the database object is a schema
    :param database_object: the database object to check
    :return: true if the object is a schema, false otherwise
    """
    return "schema" == get_object_type_name(database_object)


def is_sequence(database_object):
    """
    Check if the database object is a sequence
    :param database_object: the database object to check
    :return: true if the object is a sequence, false otherwise
    """
    return "sequence" == get_object_type_name(database_object)


def is_stored_database_logic(database_object):
    """
    Check if the database object is stored database logic
    :param database_object: the database object to check
    :return: true if the object is stored database logic, false otherwise
    """
    return "storedDatabaseLogic" == get_object_type_name(database_object)


def is_stored_procedure(database_object):
    """
    Check if the database object is a stored procedure
    :param database_object: the database object to check
    :return: true if the object is a stored procedure, false otherwise
    """
    return "storedProcedure" == get_object_type_name(database_object)


def is_unique_constraint(database_object):
    """
    Check if the database object is a unique constraint
    :param database_object: the database object to check
    :return: true if the object is a unique constraint, false otherwise
    """
    return "uniqueConstraint" == get_object_type_name(database_object)


def is_view(database_object):
    """
    Check if the database object is a view
    :param database_object: the database object to check
    :return: true if the object is a view, false otherwise
    """
    return "uniqueConstraint" == get_object_type_name(database_object)


def is_synonym(database_object):
    """
    Check if the database object is a synonym
    :param database_object: the database object to check
    :return: true if the object is a synonym, false otherwise
    """
    return "synonym" == get_object_type_name(database_object)


def is_check_constraint(database_object):
    """
    Check if the database object is a check constraint
    :param database_object: the database object to check
    :return: true if the object is a check constraint, false otherwise
    """
    return "checkConstraint" == get_object_type_name(database_object)


def is_database_package(database_object):
    """
    Check if the database object is a database package
    :param database_object: the database object to check
    :return: true if the object is a database package, false otherwise
    """
    return "databasePackage" == get_object_type_name(database_object)


def is_database_package_body(database_object):
    """
    Check if the database object is a database package body
    :param database_object: the database object to check
    :return: true if the object is a database package body, false otherwise
    """
    return "databasePackageBody" == get_object_type_name(database_object)


def is_function(database_object):
    """
    Check if the database object is a function
    :param database_object: the database object to check
    :return: true if the object is a function, false otherwise
    """
    return "function" == get_object_type_name(database_object)


def is_trigger(database_object):
    """
    Check if the database object is a trigger
    :param database_object: the database object to check
    :return: true if the object is a trigger, false otherwise
    """
    return "trigger" == get_object_type_name(database_object)


def get_column_type(database_object):
    """
    Get the type of the column of a database object
    :param database_object: the database object
    :return: the type of the column, or None if the database object is not a column
    """
    if is_column(database_object):
        return database_object.getType()
    else:
        return None
