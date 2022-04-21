from setuptools import setup, find_packages

setup(
    name="BoardGames",
    version="0.1.0",
    author="Brian Lindawson",
    author_email="brianlindawson@gmail.com",
    packages=find_packages(),
    install_requires=[
        "BeautifulSoup4",
        "Selenium",
        "webdriver-manager",
        "pandas",
    ],
    extras_require={"dev": ["pytest", "black", "pylint", "flake8", "ipykernel"]},
    python_requires=">=3.8",
)
