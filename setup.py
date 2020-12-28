import setuptools

from gameoflifeemulator import gameoflife
long_description = gameoflife.GameOfLife.__doc__

setuptools.setup(
    name="gameoflifeemulator",
    version="0.0.1",
    author="parsa shahmaleki",
    author_email="parsampsh@gmail.com",
    description="The game of life emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/parsampsh/gameoflife",
    packages=setuptools.find_packages(),
    scripts=['bin/gameoflife'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

