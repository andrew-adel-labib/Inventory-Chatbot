from setuptools import setup, find_packages

setup(
    name="inventory-chatbot",
    version="1.0.0",
    description="Enterprise Inventory Analytics Chatbot",

    author="Andrew Adel",
    author_email="andrewadellabib77@gmail.com",

    packages=find_packages(where="apps/api/src"),
    package_dir={"": "apps/api/src"},

    install_requires=[
        "pydantic",
    ],
)