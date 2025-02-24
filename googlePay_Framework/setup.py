from setuptools import setup, find_packages

setup(
    name="google_pay_framework",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=4.0.0",
        "dataclasses",
        "typing-extensions"
    ],
    author="Seu Nome",
    description="Framework Python para integração com Google Pay",
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 