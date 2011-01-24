import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "django-mollom",
    version = "0.1.1",
    packages = find_packages(),
    author = "Marconi Moreto",
    author_email = "caketoad@gmail.com",
    description = "A Django wrapper app for the PyMollom module.",
    url = "https://github.com/marconi/django-mollom/",
    include_package_data = True
)
