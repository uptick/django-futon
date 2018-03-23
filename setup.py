import os
import re

from setuptools import find_packages, setup

with open('./futon/__init__.py') as f:
    exec(re.search(r'VERSION = .*', f.read(), re.DOTALL).group())

setup(
    name='django-futon',
    version=__version__,
    author='Luke Hodkinson',
    author_email='luke.hodkinson@uptickhq.com',
    maintainer='Uptick',
    maintainer_email='dev@uptickhq.com',
    url='https://github.com/uptick/django-futon',
    description='A lightweight application for synchronising Django models between sites using RESTful APIs.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.js', '*.html', '*.*']},
    install_requires=[
        'setuptools',
        'six',
        'requests',
        'redis',
    ],
    zip_safe=False,
)
