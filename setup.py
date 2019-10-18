import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goldenpond",
    version="0.0.1",
    author="Phil Jones",
    author_email="interstar@gmail.com",
    description="Musical structure generation for use in livecoding and other musical projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/interstar/pygoldenpond",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

