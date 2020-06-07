from setuptools import setup, find_packages


setup(
    name='bci',
    version='0.1.0',
    author='Eitan-Hai Mashiah',
    description='A system that supports a Brain Computer Interface.',
    packages=find_packages(),
    package_dir={'bci': 'bci'},
    install_requires=['click', 'flask', 'Flask-Cors', 'furl',
                      'matplotlib', 'numpy', 'pika', 'protobuf',
                      'Pillow', 'requests', 'psycopg2-binary',
                      'SQLAlchemy'],
    # tests_require=['pytest', 'pytest-cov']
    tests_require=['pytest', 'codecov']
)

