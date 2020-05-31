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
        return instance
    else:
        params = dict((k, v) for k, v in kwargs.items()
                      if not isinstance(v, sqlae.ClauseElement))
        params.update(defaults or {})
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance


def get_all_as_dict(session, model, columns):
    """TODO Write doc

    Args:
        session:
        model:
        columns:

    Returns:

    """
    instances = session.query(*columns).select_from(model).all()
    return [inst._asdict() for inst in instances]
