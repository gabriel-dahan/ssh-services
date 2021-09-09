import setuptools

setuptools.setup(
    name = "sshservices",
    version = "1.0",
    author = "Gabriel D.",
    description = "SSH utilities to manage and connect to SSH Servers.",
    url = "https://github.com/gabriel-dahan/ssh-services",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires = ['paramiko']
)