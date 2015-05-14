import os
import sys

from cx_Freeze import setup, Executable


def include_boto():
	path_base = "C:\\Python27\\Lib\\site-packages\\boto\\"
	skip_count = len(path_base) + 1
	zip_includes = [(path_base, "boto/")]
	for root, subdirs, files in os.walk(path_base):
		for file_in_root in files:
			zip_includes.append(
				(os.path.join(root, file_in_root),
				os.path.join("boto/", root[skip_count:], file_in_root)
			)
		)
	return zip_includes

	
options = dict(
	build_exe=dict(
		packages=["boto"],
		includes=[],
		excludes=[
			"boto.compat.sys",
			"boto.compat.array",
			"boto.compat._sre",
			"boto.compat._locale",
			"boto.compat._struct",
			"boto.compat._json"
		],
		zip_includes=include_boto()
	)
)

executables = [
	Executable("c2-ec2.py", targetName="c2-ec2.exe"),
	Executable("c2rc-convert.py", targetName="c2rc-convert.exe")
]

setup(
	name="c2-ec2",
	version="0.1.2",
	author="CROC",
	author_email="devel@croc.ru",
	description="CROC c2-ec2",
	long_description="Simple command-line utility for sending custom requests to CROC Cloud platform",
	license="GPLv3",
	url="http://cloud.croc.ru/",
	executables=executables,
	options=options
)