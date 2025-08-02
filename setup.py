from setuptools import setup, find_packages

setup(
    name="vern",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # Add your dependencies here, e.g.:
        "streamlit",
        "requests",
        # etc.
    ],
    python_requires=">=3.8",
    description="VERN: Multi-Agent Life OS",
    author="VERN Team",
)
