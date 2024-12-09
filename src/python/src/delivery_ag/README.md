## Solução da atividade

Esta é a documentação referente à solução da atividade [Atividade sobre caixeiro viajante - Delivery AG](../../../../doc/classroom-tasks/01-delivery-ag.md). Trata-se de uma implementação simples desenvolvida em Python. O principal objetivo dessa solução é apresentar um esboço inicial do desenvolvimento. À medida que a solução for sendo consolidada, avançaremos para abordagens mais complexas, incluindo o uso de interfaces gráficas em vez de exibir as informações no console.

## Pré-requisitos

Para executar a solução, é altamente recomendado que o ambiente esteja configurado corretamente para este projeto, com o Python e suas devidas configurações, conforme mencionado na documentação deste repositório. Por isso, antes de executar os comandos abaixo, leia a documentação para verificar se o ambiente está configurado corretamente.

- [Link para a documentação de configuração do ambiente](../../README.md)

## Execução

Para rodar os testes relacionados a esta atividade, utilize o comando abaixo:

```shell
pytest src/python/tests/delivery_ag
```

Esse comando executa a sequência de testes predefinidos dentro do projeto, validando um cenário específico abordado em sala de aula. Por meio desses testes, é possível verificar a eficiência do algoritmo para o cenário base. Veja o exemplo de execução na imagem abaixo:

![image](https://github.com/user-attachments/assets/5706e7d8-1068-45de-831f-0b0e8706e8af)

Você também pode visualizar os resultados dos testes por meio das ferramentas de CI/CD:

- [Clique aqui para visualizar a execução no CI/CD](https://github.com/ReinanHS/algoritmo-genetico-ifs/actions/runs/12245077113/job/34158195809)

### Execução do cenário pré-definido

Para executar o cenário pré-definido sem usar testes, utilize o comando abaixo. Ele executa um cenário padrão usado em sala de aula:

```shell
python src/python/src/delivery_ag/exemplo_simples.py
```

### Execução do cenário aleatório

Conforme solicitado na atividade, foi criado um cenário onde as informações são definidas de maneira aleatória. Para executar esse cenário, em que as cidades e rotas de entrega são geradas aleatoriamente, utilize o comando abaixo:

```shell
python src/python/src/delivery_ag/exemplo_aleatorio.py
```
