"""
Methods to return Liquibase changeset attributes
"""


def get_id(changeset):
    """
    Returns the changeset ID
    :param   changeset:    the changeset instance
    :return: string        the changeset ID
    """
    return changeset.getId()


def get_author(changeset):
    """
    Returns the changeset author
    :param   changeset:    the changeset instance
    :return: string        the changeset author
    """
    return changeset.getAuthor()


def get_changes(changeset):
    """
    Returns the list of changes for this changeset
    :param   changeset:    the changeset instance
    :return: list          the list of changes
    """
    return changeset.getChanges()


def get_comments(changeset):
    """
    Return the comments associated with this changeset
    :param   changeset:    the changeset instance
    :return: string        the comments string
    """
    return changeset.getComments()


def get_context_filter(changeset):
    """
    Returns the context filter for the changeset
    :param   changeset:    the changeset instance
    :return: set           the context filter as a set of string
    """
    if changeset.getContextFilter() is None:
        return None
    return changeset.getContextFilter().getContexts()


def get_contexts(changeset):
    """
    Returns the contexts for the changeset
    :param   changeset:    the changeset instance
    :return: set           the contexts as a set of string
    """
    return get_context_filter(changeset)


def get_labels(changeset):
    """
    Returns the changeset labels
    :param   changeset:    the changeset instance
    :return: set           the changeset labels as a set of string
    """
    labels = changeset.getLabels()
    if labels is None:
        return None
    return labels.getLabels()


def get_logical_file_path(changeset):
    """
    Returns the changeset logical file path
    :param   changeset:     the changeset instance
    :return:                the changeset logical file path
    """
    return changeset.getLogicalFilePath()


def get_changelog_physical_path(changeset):
    """
    Returns the file path of the changelog parent of this changeset
    :param changeset:     the changelog instance
    :return:              the changelog's file path
    """
    if changeset.getChangeLog() is None:
        return None
    return changeset.getChangeLog().getPhysicalFilePath()


def get_dbms(changeset):
    """
    Returns the dbms attribute for the changeset
    :param changeset:      the changeset instance
    :return:               the dbms as a set of string
    """
    return changeset.getDbmsSet()


def get_deployment_id(changeset):
    """
    Returns the deployment ID associated with this changeset
    :param changeset:      the changeset instance
    :return:               the changeset deployment ID
    """
    return changeset.getDeploymentId()


def get_description(changeset):
    """
    Returns the changeset description
    :param changeset:      the changeset instance
    :return:               the changeset description
    """
    return changeset.getDescription()


def is_fail_on_error(changeset):
    """
    Returns the failOnError setting for the chageset
    :param changeset:
    :return:
    """
    return changeset.getFailOnError()


def get_file_path(changeset):
    """
    Returns the changeset file path
    :param   changeset:    the changeset instance
    :return: string        the changeset file path
    """
    return changeset.getFilePath()


def is_always_run(changeset):
    """
    Returns the changeset alwaysRun value
    :param   changeset:    the changeset instance
    :return: boolean       the changeset alwaysRun attribute value
    """
    return changeset.isAlwaysRun()


def is_run_on_change(changeset):
    """
    Returns the changeset runOnChange value
    :param   changeset:    the changeset instance
    :return: boolean       the changeset runOnChange attribute value
    """
    return changeset.isRunOnChange()
