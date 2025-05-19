"""
Constants classes
An immutable set of well-known constants that are used to access the script bindings
"""


class ScriptConstants:
    DATABASE_BINDING = "database_binding"
    DATABASE_OBJECT_BINDING = 'databaseObject_binding'
    DATABASE_SNAPSHOT_BINDING = 'databaseSnapshot_binding'
    CHANGES_BINDING = 'changes_binding'
    CHANGESET_BINDING = 'changeSet_binding'
    DBUTIL_BINDING = "dbutil_binding"
    SCRIPT_MESSAGE_BINDING = "scriptMessage_binding"
    CHECKS_SCOPE_BINDING = "checksScope_binding"
    CACHE_BINDING = "cache_binding"
    STATUS_BINDING = "status_binding"
    SCRIPT_PATH_BINDING = "script_path_binding"
    LOGGER_BINDING = "logger_binding"
    ARGS_SUFFIX = "_arg_binding"


#
# ConstantsManagement class
# This class makes the constants immutable
#
class Constants:
    def __init__(self):
        # Set constants from separate classes as attributes
        for cls in [ScriptConstants]:
            for key, value in cls.__dict__.items():
                if not key.startswith("__"):
                    self.__dict__.update(**{key: value})

    def __setattr__(self, name, value):
        raise TypeError("Constants are immutable")
