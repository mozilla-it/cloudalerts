from setuptools import setup, find_packages

setup(
    name="cloudalerts",
    version="0.0.1",
    description="Python tool for accessing mozilla cloud alerting services",
    python_requires=">=3.4",
    author="Mozilla IT Enterprise Systems",
    author_email="bsieber@mozilla.com",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=["google-cloud-logging", "behave", "jinja2"],
    project_urls={"Source": "https://github.com/mozilla-it/cloudalerts",},
    test_suite="tests.bdd",
    data_files=[],
)
