import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="tagged",
    version="0.0.1",
    author="Joachim Viide",
    author_email="jviide@iki.fi",
    description="Tagged templates for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jviide/tagged",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
