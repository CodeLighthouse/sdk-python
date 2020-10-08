import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CodeLighthouse", # Replace with your own username
    version="0.0.1",
    author="CodeLighthouse",
    author_email="hello@codelighthouse.io",
    description="The python SDK for CodeLighthouse",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeLighthouse/sdk-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)