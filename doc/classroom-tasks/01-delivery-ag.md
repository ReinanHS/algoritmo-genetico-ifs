## Delivery AG

Considere que uma empresa de logística possui em cada região um centro de distribuição, no qual os entregadores partem e retornam das suas entregas. 
Todas as cidades são rotuladas (possuem nomes) e estão interligadas por estradas valoradas (distância em km entre as cidades). Veja o exemplo abaixo:

<img src="https://github.com/user-attachments/assets/f06aacd2-41ce-4c2c-84ae-49ecfc908d4c" width="400">

O gerente da empresa utiliza o sistema diariamente para gerar as rotas de entrega, informando as cidades que devem ser visitadas pelo entregador. 

- As estradas são de mão dupla.
- O resultado da consulta deve exibir a rota e o custo mínimo do percurso. 

Utilize algoritmo genético para solucionar o problema.

## Objetivos da atividade

- **Resolver o problema do caixeiro viajante**: Determinar a rota mais eficiente para um entregador que deve visitar um conjunto de cidades, retornando ao centro de distribuição no menor custo possível.
- **Aplicar algoritmos genéticos**: Implementar um algoritmo genético que simula o processo de seleção natural para encontrar a solução ótima ou próxima do ótimo.
- **Fornecer uma solução prática para um problema real**: Desenvolver um sistema que pode ser utilizado pelo gerente da empresa de logística para planejar as rotas de entrega.

## Requisitos funcionais

- O sistema deve permitir que o gerente insira:
  - A cidade de partida (centro de distribuição).
  - Uma lista de cidades que devem ser visitadas.
  - Um mapa representando as estradas (distâncias entre as cidades).

- Implementar o algoritmo genético com os seguintes elementos:
  - **População Inicial**: Conjunto inicial de rotas geradas aleatoriamente.
  - **Função de Avaliação (Fitness)**: Baseada no custo total da rota (distância).
  - **Operadores Genéticos**:
    - Seleção (escolher as melhores rotas).
    - Crossover (combinar rotas para gerar novas rotas).
    - Mutação (introduzir pequenas alterações para diversidade).
  - Critério de Parada: Quando um número máximo de gerações é alcançado ou uma solução satisfatória for encontrada.

- Seu algoritmo deverá exibir ao gerente:
  - A rota otimizada (sequência de cidades a serem visitadas).
  - O custo total da rota (em quilômetros).
  - O tempo de execução do cálculo (opcional).

- Interatividade e Interface:
  - Interface básica para entrada dos dados e exibição dos resultados (console, interface gráfica simples, ou interface web).

## Critérios de aceitação

- O sistema deve retornar uma rota válida (que começa e termina no centro de distribuição, passando por todas as cidades especificadas).
- O custo apresentado deve corresponder ao menor custo encontrado pelo algoritmo genético.
- O sistema deve calcular a rota em um tempo razoável, mesmo para mapas com várias cidades e conexões.
- A interface deve ser intuitiva e permitir que o gerente insira os dados necessários de forma clara.
- Os resultados devem ser exibidos em um formato compreensível.
- O sistema deve aceitar diferentes mapas de entrada e diferentes combinações de cidades para visitar sem necessidade de reconfiguração do código.

## Prazo de entrega

Esta atividade deve ser concluída e entregue, no máximo, até o dia 3 de dezembro de 2024, por meio da atividade disponível no Google Sala de Aula. 
Para mais detalhes sobre a atividade, recomendamos consultar o link abaixo:  

- [Clique aqui para visualizar a atividade](https://classroom.google.com/c/NzI2NDA0MTc3NTM0/a/NzM1NjgwMDcwNTY5/details)

## Soluções desenvolvidas

- Solução simples
  - [Python - Console](src/python/caixeiro-viajante/index.md)

## Referências

- [O Problema do caixeiro viajante através de algoritmo genético](https://aprepro.org.br/conbrepro/2019/anais/arquivos/09302019_220914_5d92b20230a58.pdf)
- [Traveling Salesman Problem (TSP) using Genetic Algorithm (Python)](https://medium.com/aimonks/traveling-salesman-problem-tsp-using-genetic-algorithm-fea640713758)
- [Evolutionary Algorithm for the Travelling Salesperson Problem (Genetic Algorithm)](https://youtu.be/Wgn_aPH3OEk)
- [Traveling Salesman Problem in R with Location Data](https://www.crowdatascience.com/travelling-salesman-problem-in-r-with-location-data/)






