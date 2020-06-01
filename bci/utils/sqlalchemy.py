import sqlalchemy as sqla
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


def row2dict(r):
    return {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


def get_all_as_dict(session, model, single=False, cols=[], **kwargs):
    """TODO Write doc

    Args:
        session:
        model:
        single:
        cols:
        kwargs:
    Returns:

    """
    if not cols:
        cols = model.__table__.columns.keys()
    rows = session.query(*cols).select_from(model) \
        .filter_by(**kwargs).all()
    result = [row._asdict() for row in rows]
    if single and result:
        result = result[0]
    return result

    # TODO Check if you can replace the above code with the following
    #  or just improve the above code
    # rows = session.query(model).filter_by(**kwargs).all()
    # rows_dict = list(map(row2dict, rows))
    # if cols:
    #     rows_dict = list(map(lambda r: {col: r[col] for col in cols},
    #                          rows_dict))
    # return rows_dict
