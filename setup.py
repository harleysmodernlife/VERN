from setuptools import setup, find_packages

setup(
    name="vern",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "python-dotenv",
        "anyio",
        "httpx",
        "pyyaml",
        "streamlit",
        "fastapi",
        "uvicorn",
        "pydantic",
        "sqlalchemy",
        "databases",
        "websockets",
        "pytest",
        "pytest-asyncio",
        "neo4j",
        "txtai",
    ],
    python_requires=">=3.8",
    description="VERN: Multi-Agent Life OS",
    author="VERN Team",
)
