from setuptools import setup, find_packages

setup(
    name="catastroguard",
    version="1.0.0",
    author="Dhananjay Vaidya",
    description="AI-powered disaster prediction and risk assessment system",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "requests",
        "matplotlib",
        "seaborn",
        "flask",
        "streamlit"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)