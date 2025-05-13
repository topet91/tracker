from setuptools import setup, find_packages

setup(
    name="geometry_lib",
    version="0.1.0",
    packages=find_packages(),
    author="Петров Анатолий",
    description="Библиотека для вычисления площадей геометрических фигур",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
