from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='TransportationProblem',
    version='0.0.3',
    packages=['transportation_problem'],
    url='https://github.com/cdfmlr/TransportationProblem/',
    license='MIT',
    author='CDFMLR',
    author_email='cdfmlr@163.com',
    description='求解产销平衡的运输问题。',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'numpy'
    ]
)
