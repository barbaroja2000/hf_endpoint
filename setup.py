from setuptools import setup

setup(
    name='hf',
    version='0.1.0',
    description='A Python client for the HF endpoint API',
    author='AMJ',
    author_email='your.email@example.com',
    packages=['hf_endpoint'],
    install_requires=['requests','pydantic','pytest'],
    license='MIT'
)