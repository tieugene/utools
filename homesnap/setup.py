from setuptools import setup

setup(
    name='homesnap',
    version='0.0.1',
    url='https://github.com/tieugene/utools/homesnap',
    license='GPLv3',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    description='Show a file daemon',
    py_modules=['homesnap'],
    entry_points={
        'console_scripts': [
            'homesnap = homesnap:main',
        ],
    },
)
