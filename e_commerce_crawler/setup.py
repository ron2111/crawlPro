from setuptools import setup, find_packages

setup(
    name="e_commerce_crawler",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
        "beautifulsoup4",
        "pyyaml",
        "aiodns",
        "cchardet",
        "tqdm",
    ],
)
