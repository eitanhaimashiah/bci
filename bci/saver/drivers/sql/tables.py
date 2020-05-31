import sqlalchemy as sqla
import sqlalchemy.ext.declarative as sqlad

Base = sqlad.declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = sqla.Column(sqla.Integer,
                          primary_key=True,
                          nullable=False)
    username = sqla.Column(sqla.String, nullable=False)
    birthday = sqla.Column(sqla.Date)  # TODO Maybe just gets str
    gender = sqla.Column(sqla.String, nullable=False)  # TODO Check if this is the required type


class Snapshot(Base):
    __tablename__ = 'snapshot'
    snapshot_id = sqla.Column(sqla.Integer,
                              primary_key=True,
                              nullable=False)
    user_id = sqla.Column(sqla.Integer, sqla.ForeignKey('user.user_id'))
    datetime = sqla.Column(sqla.Date)  # TODO Maybe just gets str


class Pose(Base):
    __tablename__ = 'pose'
    snapshot_id = sqla.Column(sqla.Integer,
                              sqla.ForeignKey('snapshot.snapshot_id'),
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
                              sqla.ForeignKey('snapshot.snapshot_id'),
                              primary_key=True)
    path = sqla.Column(sqla.String, nullable=False)


class DepthImage(Base):
    __tablename__ = 'depth_image'
    snapshot_id = sqla.Column(sqla.Integer,
                              sqla.ForeignKey('snapshot.snapshot_id'),
                              primary_key=True)
    path = sqla.Column(sqla.String, nullable=False)


class Feelings(Base):
    __tablename__ = 'feelings'
    snapshot_id = sqla.Column(sqla.Integer,
                              sqla.ForeignKey('snapshot.snapshot_id'),
                              primary_key=True)
    hunger = sqla.Column(sqla.FLOAT)
    thirst = sqla.Column(sqla.FLOAT)
    exhaustion = sqla.Column(sqla.FLOAT)
    happiness = sqla.Column(sqla.FLOAT)
