from setuptools import setup


with open("requirements.txt", "r") as f:
    install_reqs = [
        s
        for s in [line.strip(" \n") for line in f]
        if not s.startswith("#") and s != ""
    ]

setup(
    name="dados_abertos_feira",
    version="0.1.0",
    url="https://github.com/anapaulagomes/licitacoes-de-feira.git",
    author="Ana Paula Gomes",
    author_email="apgomes88@gmail.com",
    description="Scripts to collect open data from Feira de Santana.",
    packages=["data_collection"],
    include_package_data=True,
    install_reqs=install_reqs,
)
