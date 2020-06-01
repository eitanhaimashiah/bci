from setuptools import setup, find_packages


setup(
    name='bci',
    version='0.1.0',
    author='Eitan-Hai Mashiah',
    description='A system that supports a Brain Computer Interface.',
    packages=find_packages(),
    # install_requires=['click', 'flask'],
    install_requires=['click',
                      'flask',
                      'Flask-Cors'
                      'furl',
                      'matplotlib',
                      'numpy',
                      'pika',
                      'protobuf',
                      'Pillow',
                      'requests',
                      'Werkzeug',
                      ],
    tests_require=['pytest', 'pytest-cov'])

