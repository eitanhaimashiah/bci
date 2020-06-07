import sqlalchemy.sql.expression as sqlae


def get_or_create(session, entity, **kwargs):
    """Gets the instance of `entity` that meets `kwargs` if one
    exists; Otherwise, create the required `entity`'s instance and
    adds it to `session`.

    Args:
        session (sqlalchemy.orm.session.Session): The session with
            which the query will be associated.
        entity (sqlalchemy.ext.declarative.api.Base): The entity on
            which the query is performed.
        kwargs (dict): Keyword expressions to filter by.

    Returns:
        `entity`: The required instance.

    """
    instance = session.query(entity).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict((k, v) for k, v in kwargs.items()
                      if not isinstance(v, sqlae.ClauseElement))
        instance = entity(**params)
        session.add(instance)
        session.commit()
        return instance


def get_all_as_dict(session, entity, single=False, cols=[], **kwargs):
    """Gets all instances of `entity` that meet `kwargs` in dictionary
    representation, while selecting `cols`.

    Args:
        session (sqlalchemy.orm.session.Session): The session with
            which the query will be associated.
        entity (sqlalchemy.ext.declarative.api.Base): The entity on
            which the query is performed.
        single (bool): If true, we expect only one instance.
        cols (list): The columns to select from each instance.
        kwargs (dict): Keyword expressions to filter by.

    Returns:
        list: The list of the required instances converted to
            dictionary representation.

    """
    if not cols:
        cols = entity.__table__.columns.keys()
    instances = session.query(*cols).select_from(entity) \
        .filter_by(**kwargs).all()
    result = [instance._asdict() for instance in instances]
    if single and result:
        result = result[0]
    return result
