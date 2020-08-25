from setuptools import setup

from app.version import __version__

setup(
    name='pelops',
    version=__version__,
    description='Mock API provider. Used for mocking external APIs in dev & staging.',
    url='https://git.bink.com/Olympus/pelops',
    author='Chris Latham',
    author_email='cl@bink.com',
    zip_safe=True)
