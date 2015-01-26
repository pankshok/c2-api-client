import os
import sys
from setuptools import setup


PACKAGE_PATH = os.path.abspath(os.path.dirname(__file__))

def get_description():
	with open(os.path.join(PACKAGE_PATH, "README.md")) as readme:
		return readme.read()

install_requires = [
	"boto"
]

# argparse moved to stdlib in python2.7
if sys.version_info[0] == 2 and sys.version_info[1] <= 6:
	install_requires.append("argparse")

setup(
	name="c2-ec2",
	version="0.1.1",
	author="CROC",
	author_email="devel@croc.ru",
	description="Simple command-line utility for sending custom requests to CROC Cloud platform.",
	license="GPLv3",
	url="http://cloud.croc.ru/",
	install_requires=install_requires,
	py_modules=["c2_ec2"],
	entry_points={
		"console_scripts": [
			"c2-ec2 = c2_ec2:main"
		]
	},
	long_description=get_description(),
)
