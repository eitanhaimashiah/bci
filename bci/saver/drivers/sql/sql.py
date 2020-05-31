import sqlalchemy as sqla
import sqlalchemy.orm as sqlao

from .tables import Base, User, Snapshot, Pose, \
    ColorImage, DepthImage, Feelings
from ....utils.sqlalchemy import get_or_create


class SqlDriver:
    """Represents a SQL database driver. It supports any SQL database
    compatible with `sqlalchemy`.

    Attributes:
        db_url (str): URL of the running database.

    Args:
        db_url (str): URL of the running database.

    Raises:
        TODO Check what's the exceptions of `sqlalchemy`

    """

    scheme = 'postgresql'

    def __init__(self, db_url):
        self.db_url = db_url

        # Setup the database and create a new session with it
        engine = sqla.create_engine(self.db_url)
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
        result = data['result']
        user_dict = result['user']
        snapshot_dict = result['snapshot']
        user = get_or_create(self.session, User, **user_dict)
        snapshot = get_or_create(self.session, Snapshot,
                                 **snapshot_dict, user_id=user.user_id)
        if topic == 'pose':
            trans_dict = result['translation']
            rot_dict = result['rotation']
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
                                     **result)
            self.session.add(color_image)
        elif topic == 'depth_image':
            depth_image = DepthImage(snapshot_id=snapshot.snapshot_id,
                                     **result)
            self.session.add(depth_image)
        elif topic == 'feelings':
            feelings = Feelings(snapshot_id=snapshot.snapshot_id,
                                **result)
            self.session.add(feelings)
        else:
            raise ValueError(f'unknown topic: {format}')

        self.session.commit()
