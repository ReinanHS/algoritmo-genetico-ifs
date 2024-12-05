# Estrutura em Python

Esta estrutura foi criada para realizar experimentos utilizando a linguagem de programação Python. Dentro deste diretório, você encontrará uma organização básica que permite a execução de todo o código desenvolvido com esta linguagem. É altamente recomendado que você siga os pré-requisitos para garantir que a execução ocorra corretamente no seu ambiente.

## Requisitos

Recomendamos que você tenha o [Conda](https://docs.conda.io/projects/conda/en/latest/index.html) instalado na sua máquina. Esta ferramenta facilita a criação de ambientes virtuais necessários para a execução do código. Caso você não tenha o Conda instalado, pode utilizar o interpretador padrão do Python. No entanto, a maioria dos testes deste projeto foram desenvolvidos utilizando ambientes gerados pelo Conda.

---

## Atenção

Para executar os próximos comandos, recomendamos que você esteja no diretório correto do código Python. Geralmente, ao abrir este projeto, você verá a raiz principal do repositório. Entretanto, como o objetivo deste repositório é apresentar exemplos em diversas linguagens de programação, sugerimos que acesse especificamente o diretório referente ao Python antes de prosseguir com os comandos. O caminho para o diretório Python é:

> src/python

## Criação do ambiente virtual

Para criar um ambiente virtual e executar o código, você pode seguir os passos abaixo:

### Para usuários de Python 3:

1. Instale o virtualenv:
   ```bash
   pip install virtualenv
   ```
2. Crie o ambiente virtual:
   ```bash
   virtualenv algoritmo_genetico_ifs
   ```
3. Ative o ambiente virtual:
   ```bash
   source caminho_para/algoritmo_genetico_ifs/bin/activate
   ```

### Para usuários do Anaconda:
1. Crie um ambiente Conda:
   ```bash
   conda create --name algoritmo_genetico_ifs
   ```
2. Ative o ambiente Conda:
   ```bash
   conda activate algoritmo_genetico_ifs
   ```
3. Instale o pip no ambiente:
   ```bash
   conda install pip
   ```

## Execução dos testes

Para executar os testes disponíveis neste projeto, siga os passos abaixo:

1. Instale o pacote no modo de desenvolvimento:
   ```bash
   pip install -r src/python/requirements.txt
   pip install -e .
   ```
2. Após a instalação, execute os testes com o seguinte comando:
   ```bash
   pytest src/python
   pylint src/python/**/*.py
   autopep8 --recursive --in-place --aggressive --aggressive src/python
   ```
