from setuptools import setup, find_packages
from setuptools.command.install import install

class InstallCommand(install):
    """Custom install command to include Celery worker start option"""
    def run(self):
        install.run(self)
        print("To start the Celery worker, run: vault celery")

setup(
    name="filevault-cli",
    version="4.0.0",
    description="A command-line file management system",
    author="Aribisala Praise",
    author_email="aribisalapraise@gmail.com",
    packages=find_packages(),
    install_requires=[
        'pymongo>=4.0',
        'bcrypt>=4.0',
        'redis>=4.0',
        'celery>=5.0',
        'Pillow>=9.0',
        'click',
        'fastapi',
        'uvicorn',
        'python-multipart',
        'passlib[bcrypt]',
        'python-jose[cryptography]',
    ],
    entry_points={
        'console_scripts': [
            # 'vault=vault:main',
            'backend=vault.api:server'
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    cmdclass={
        'install': InstallCommand,
    }
)