import setuptools

setuptools.setup(
    name = "sshservices",
    version = "1.0",
    author = "Gabriel D.",
    description = "Some functions to work with SSH.",
    url = "https://github.com/gabriel-dahan/ssh-py-services",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires = ['paramiko']
)