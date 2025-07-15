from setuptools import setup, find_packages

setup(
    name="filevault-cli",
    version="1.0.0",
    description="A command-line file management system",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vault=vault:main',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)