import os
from setuptools import setup


PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))

def get_description():
	with open(os.path.join(PACKAGE_PATH, "README.md")) as readme:
		return readme.read()


setup(
	name="c2-ec2",
	version="0.0.1",
	author="CROC",
	author_email="devel@croc.ru",
	description="Simple command-line utility for sending custom requests to CROC Cloud platform.",
	license="GPLv3",
	url="http://cloud.croc.ru/",
	install_requires=["boto", "argparse"],
	py_modules=["c2_ec2"],
	entry_points={
		"console_scripts": [
			"c2-ec2 = c2_ec2:main"
		]
	},
	long_description=get_description(),
)
