import json
import datetime as dt
import sqlalchemy as sqla
import sqlalchemy.orm as sqlao
import sqlalchemy.ext.declarative as sqlad

from ...utils.sqlalchemy import get_or_create, get_all_as_dict


class PostgresqlDriver:
    """Represents a PostgresSQL database driver.

    TODO If you replace the current driver name with `SqlDriver`,
        Add this to the above description:
        It supports any SQL database compatible with `sqlalchemy`.

    Attributes:
        db_url (str): URL of the running database.

    Args:
        db_url (str): URL of the running database.
        setup (bool): If true, setups the database. Default to `True`.

    Raises:
        TODO Check what's the exceptions of `sqlalchemy`

    """

    scheme = 'postgresql'
    # scheme = 'sql'  # TODO Consider using this scheme instead

    def __init__(self, db_url, setup=True):
        self.db_url = db_url

        engine = sqla.create_engine(self.db_url)

        if setup:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)

        session_cls = sqlao.sessionmaker(bind=engine)
        self.session = session_cls()

    def save(self, topic, data):
        """Saves `data` under `topic` in the database.

        Args:
            topic (str): Topic name.
            data (str): JSON-formatted raw data, as consumed from
            the message queue. The data contains the result received
            from the `topic` parser as well as the corresponding
            snapshot and user information.

        Raises:
            ValueError: If `topic` is unknown.

        """
        data = json.loads(data)
        user_dict = data['user']
        snapshot_dict = data['snapshot']
        result_dict = data['result']

        # TODO Add this conversion to `protocol.utils`
        # Convert timestamp columns to datetime
        user_dict['birthday'] = dt.datetime.fromtimestamp(int(user_dict['birthday']))
        snapshot_dict['datetime'] = dt.datetime.fromtimestamp(int(snapshot_dict['datetime']) / 1000)

        user = get_or_create(self.session, User, **user_dict)
        snapshot = get_or_create(self.session, Snapshot,
                                 **snapshot_dict, user_id=user.user_id)
        if topic == 'pose':
            trans_dict = result_dict['translation']
            rot_dict = result_dict['rotation']
            pose = Pose(snapshot_id=snapshot.snapshot_id,
                        translation_x=trans_dict['x'],
                        translation_y=trans_dict['y'],
                        translation_z=trans_dict['z'],
                        rotation_x=rot_dict['x'],
                        rotation_y=rot_dict['y'],
                        rotation_z=rot_dict['z'],
                        rotation_w=rot_dict['w'])
            self.session.add(pose)
        elif topic == 'color_image':
            color_image = ColorImage(snapshot_id=snapshot.snapshot_id,
                                     **result_dict)
            self.session.add(color_image)
        elif topic == 'depth_image':
            depth_image = DepthImage(snapshot_id=snapshot.snapshot_id,
                                     **result_dict)
            self.session.add(depth_image)
        elif topic == 'feelings':
            feelings = Feelings(snapshot_id=snapshot.snapshot_id,
                                **result_dict)
            self.session.add(feelings)
        else:
            raise ValueError(f'unknown topic: {format}')

        self.session.commit()

    def get(self, endpoint, **kwargs):
        """TODO Write doc.

        Args:
            endpoint:
            **kwargs:

        Returns:

        Raises:
            ValueError: If `endpoint` is unknown.

        """
        if endpoint == 'users':
            return get_all_as_dict(self.session, User,
                                   cols=['user_id', 'username'])
        elif endpoint == 'user':
            user = get_all_as_dict(self.session, User,
                                   single=True, **kwargs)
            user['birthday'] = user['birthday'].strftime('%B %-d, %Y')
            return user
        elif endpoint == 'snapshots':
            snapshots = get_all_as_dict(self.session, Snapshot,
                                        cols=['snapshot_id', 'datetime'],
                                        **kwargs)
            # TODO Check if you can write this function better
            #   in particular use a util from protocol.utils.display
            for snap in snapshots:
                snap['datetime'] = snap['datetime'].strftime('%B %-d, %Y at %H:%M:%S.%f')[:-3]
            return snapshots
        elif endpoint == 'snapshot':
            snapshot = get_all_as_dict(self.session, Snapshot,
                                       single=True, **kwargs)
            snapshot['results'] = get_results()
            return snapshot
        elif endpoint == 'result':
            model = result_models[kwargs.pop('result_name')]
            return get_all_as_dict(self.session, model,
                                   single=True, **kwargs)
        else:
            raise ValueError(f'unknown endpoint: {endpoint}')


###############
# DB's Tables #
###############

Base = sqlad.declarative_base()


class User(Base):
    __tablename__ = 'users'
    user_id = sqla.Column(sqla.Integer,
                          primary_key=True,
                          nullable=False)
    username = sqla.Column(sqla.String, nullable=False)
    birthday = sqla.Column(sqla.DateTime)  # TODO Maybe just gets str
    gender = sqla.Column(sqla.String, nullable=False)  # TODO Check if this is the required type


class Snapshot(Base):
    __tablename__ = 'snapshots'
    snapshot_id = sqla.Column(sqla.Integer,
                              primary_key=True)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('users.user_id'))
    datetime = sqla.Column(sqla.DateTime)  # TODO Maybe just gets str


class Pose(Base):
    __tablename__ = 'pose'
    snapshot_id = sqla.Column(sqla.Integer,
                              sqla.ForeignKey('snapshots.snapshot_id'),
                              primary_key=True)
    translation_x = sqla.Column(sqla.FLOAT)
    translation_y = sqla.Column(sqla.FLOAT)
    translation_z = sqla.Column(sqla.FLOAT)
    rotation_x = sqla.Column(sqla.FLOAT)
    rotation_y = sqla.Column(sqla.FLOAT)
    rotation_z = sqla.Column(sqla.FLOAT)
    rotation_w = sqla.Column(sqla.FLOAT)


class ColorImage(Base):
    __tablename__ = 'color_image'
    snapshot_id = sqla.Column(sqla.Integer,
                              sqla.ForeignKey('snapshots.snapshot_id'),
                              primary_key=True)
    path = sqla.Column(sqla.String, nullable=False)


class DepthImage(Base):
    __tablename__ = 'depth_image'
    snapshot_id = sqla.Column(sqla.Integer,
                              sqla.ForeignKey('snapshots.snapshot_id'),
                              primary_key=True)
    path = sqla.Column(sqla.String, nullable=False)


class Feelings(Base):
    __tablename__ = 'feelings'
    snapshot_id = sqla.Column(sqla.Integer,
                              sqla.ForeignKey('snapshots.snapshot_id'),
                              primary_key=True)
    hunger = sqla.Column(sqla.FLOAT)
    thirst = sqla.Column(sqla.FLOAT)
    exhaustion = sqla.Column(sqla.FLOAT)
    happiness = sqla.Column(sqla.FLOAT)

# TODO Compute `result_models` in a better way (like in parsers)

result_models = {
    'pose': Pose,
    'color_image': ColorImage,
    'depth_image': DepthImage,
    'feelings': Feelings
}

def get_results():
    # return {k: v for (k, v) in Base.metadata.tables if k not in {'users', 'snapshots'}}
    return list(result_models.keys())
