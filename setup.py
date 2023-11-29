from setuptools import find_packages, setup

setup(
    name='hfendpoint3',
    version='0.1.2',
    description='A Python client for the HF endpoint API',
    author='AMJ',
    author_email='your.email@example.com',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=['requests','pydantic','pytest'],
    license='MIT'
)