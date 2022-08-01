from setuptools import setup

setup(
    name='showfiled',
    version='0.0.1',
    url='https://github.com/tieugene/utools/showfiled',
    license='GPLv3',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    description='Show a file daemon',
    py_modules=['showfiled'],
    entry_points={
        'console_scripts': [
            'showfiled = showfiled:main',
        ],
    },
)
