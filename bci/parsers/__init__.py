from .pose import parse_pose
from .color_image import ColorImageParser
from .depth_image import DepthImageParser
from .feelings import parse_feelings

__all__ = [parse_pose, ColorImageParser, DepthImageParser, parse_feelings]


def parser(name):
    def decorator(f):
        pass
