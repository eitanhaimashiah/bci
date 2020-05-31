import sqlalchemy.sql.expression as sqlae


def get_or_create(session, model, defaults=None, **kwargs):
    """TODO Write doc

    Args:
        session:
        model:
        defaults:
        **kwargs:

    Returns:

        Returns `True` if the instance does not exist.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        print(f'GET: {kwargs}')
        return instance
    else:
        print(f'CREATE: {kwargs}')
        params = dict((k, v) for k, v in kwargs.items()
                      if not isinstance(v, sqlae.ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance
