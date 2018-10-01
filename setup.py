from setuptools import setup

setup(
    name='cstr',
    long_description=__doc__,
    packages=['cstr'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['waitress', 'Flask', 'fhirclient']
)

