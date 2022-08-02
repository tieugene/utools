from setuptools import setup

setup(
    name='srvbot',
    version='0.0.3',
    url='https://github.com/tieugene/utools/srvbot',
    license='GPLv3',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    description='Telegram bot to control KVM guest',
    py_modules=['srvbot'],
    entry_points={
        'console_scripts': [
            'srvbot = srvbot:main',
        ],
    },
)
