from setuptools import setup, find_packages
import os

# Read the README file for the long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="prompt-for-user-input-mcp",
    version="1.0.0",
    author="Jesse Gomez",
    author_email="goldensansapple@users.noreply.github.com",
    description="An MCP server that enables AI models to prompt users for input directly through their code editor",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/goldensansapple/prompt-for-user-input-mcp",
    project_urls={
        "Bug Reports": "https://github.com/goldensansapple/prompt-for-user-input-mcp/issues",
        "Source": "https://github.com/goldensansapple/prompt-for-user-input-mcp",
        "Documentation": "https://github.com/goldensansapple/prompt-for-user-input-mcp#readme",
    },
    packages=find_packages(),
    py_modules=["mcp_server"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "prompt-for-user-input-mcp=mcp_server:main",
        ],
    },
    keywords=[
        "mcp",
        "model-context-protocol",
        "ai",
        "assistant",
        "prompt",
        "user-input",
        "interactive",
        "cursor",
        "claude",
        "llm",
        "vscode"
    ],
    include_package_data=True,
    zip_safe=False,
) 