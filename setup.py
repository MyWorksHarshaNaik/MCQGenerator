from setuptools import find_packages, setup

setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Harsha Naik',
    author_email='harshanaik8197@gmail.com',
    install_requires=["openai", "langchain", "streamlit", "python-dotenv", "PyPDF2", "gemini", "python-gemini-api"],
    packages=find_packages()
)