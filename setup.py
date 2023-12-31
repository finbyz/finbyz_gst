from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in finbyz_gst/__init__.py
from finbyz_gst import __version__ as version

setup(
	name="finbyz_gst",
	version=version,
	description="Custom App for GSP Einvoice API",
	author="Finbyz Tech Pvt. Ltd.",
	author_email="info@finbyz.tech",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
