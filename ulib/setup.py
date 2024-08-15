from setuptools import setup

setup(
    name='ulib',
    version='0.0.2',
    url='https://github.com/tieugene/utools',
    license='GPLv3',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    description='Utility micro-library',
    packages=['ulib'],
    py_modules=['homesnap'],
    entry_points={
        'console_scripts': [
            'homesnap = homesnap:main',
        ],
    },
)
