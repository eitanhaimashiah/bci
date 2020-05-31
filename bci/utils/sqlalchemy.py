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


def get_all_as_dict(session, model, columns=[], **kwargs):
    """TODO Write doc

    Args:
        session:
        model:
        columns:
        kwargs:
    Returns:

    """
    # TODO Check if you can write this function better
    if not columns:
        instances = session.query(model).filter_by(**kwargs).all()
        return list(map(row2dict, instances))
    else:
        instances = session.query(*columns).select_from(model)\
            .filter_by(**kwargs).all()
        return [inst._asdict() for inst in instances]


def get_all_table_names(engine):
    inspector = sqla.inspect(engine)
    schemas = inspector.get_schema_names()

    for schema in schemas:
        print("schema: %s" % schema)
        for table_name in inspector.get_table_names(schema=schema):
            for column in inspector.get_columns(table_name,
                                                schema=schema):
                print("Column: %s" % column)
