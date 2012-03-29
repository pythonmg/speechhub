from setuptools import setup

setup(name='SpeechHub',
      version='0.1',
      description='A simple static blog engine',
      author='Antonio Ribeiro',
      author_email='alvesjunior.antonio@gmail.com',
      url='alvesjnr.github.com',
	  install_requires=['argparse','pystache','markdown'],
      packages=['speechhub'],
      entry_points = {
        'console_scripts': [
            'speechhub = speechhub.speechhub:main',
        ],
    }
     )
