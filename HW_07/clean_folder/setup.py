from setuptools import setup, find_namespace_packages

setup(
    name="clean_folder",
    version="1.0",
    description="HW_07. Clean folder",
    author="Valentyna Gordynska",
    author_email="vgordynska@gmail.com",
    license="MIT",
    packages=find_namespace_packages(),
    entry_points={"console_scripts": [
        "clean_folder=clean_folder.sort:clean_folder"]}
)
