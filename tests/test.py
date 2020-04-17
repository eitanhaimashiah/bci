import pathlib
from bci.reader import read
from bci.client import upload_sample

ROOT = pathlib.Path(__file__).absolute().parent.parent
PROTO_SAMPLE_PATH = ROOT / 'sample.mind.gz'
BINARY_SAMPLE_PATH = ROOT / 'sample.mind'

if __name__ == '__main__':
    # Test Reader
    # read(PROTO_SAMPLE_PATH)
    read(BINARY_SAMPLE_PATH, format='binary')

    # Test Client
    # upload_sample(path=PROTO_SAMPLE_PATH)
    # upload_sample(path=BINARY_SAMPLE_PATH, format='binary')
