
from setuptools import setup, find_packages

setup(
    name='myLib',
    version='1.0.0',
    description="A first draft of publishing a package",
    long_description="First trying out the package and later on do further modifications",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
    ],
    
    include_package_data=True,
)















