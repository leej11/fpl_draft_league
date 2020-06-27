import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fpl-draft-league", # Replace with your own username
    version="0.0.1",
    author="Liam Gower",
    author_email="lee.gower17@gmail.com",
    description="A package to capture and analyse data from draft.premierleague.com, the popular fantasy football "
                "website.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/leej11/fpl_draft_league",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)