package deliveryAG;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class Main {
    public static void main(String[] args) {
        // Lista de cidades
        List<deliveryAG.Cidade> cidades = Arrays.asList(
                new deliveryAG.Cidade("X"),
                new deliveryAG.Cidade("A"),
                new deliveryAG.Cidade("B"),
                new deliveryAG.Cidade("C"),
                new deliveryAG.Cidade("D"),
                new deliveryAG.Cidade("E")
        );

        // Matriz de rotas (-1 indica rota inexistente)
        int[][] rotas = {
                {-1, 30, 50, 20, -1, -1},
                {30, -1, 10, -1, -1, -1},
                {50, 40, -1, 15, 30, 20},
                {20, -1, 15, -1, -1, -1},
                {-1, -1, 30, -1, -1, -1},
                {-1, -1, 20, -1, -1, -1}
        };

        // Índices das cidades obrigatórias no percurso
        List<Integer> rotasEntrega = Arrays.asList(2, 3, 5);

        // Centro de distribuição (índice da cidade inicial/final)
        int centroDistribuicao = 0;

        // Parâmetros do algoritmo genético
        double taxaMutacao = 0.05;
        int numeroGeracoes = 400;
        int tamanhoPopulacao = 20;
        boolean debugMode = false;

        // Inicializa o algoritmo genético
        deliveryAG.AlgoritmoGenetico ag = new deliveryAG.AlgoritmoGenetico(
                tamanhoPopulacao, taxaMutacao, debugMode
        );

        // Resolve o problema
        ag.resolver(
                numeroGeracoes,
                cidades,
                rotas,
                rotasEntrega,
                centroDistribuicao
        );

        // Exibe o melhor resultado encontrado
        //System.out.println("\n\nO melhor resultado: \n");

       ag.visualizaMelhorGeracao();
       //ag.visualizaGeracao();



        // Exibe estatísticas (caso exista a classe Estatistica)
       /* Estatistica.mostrarEstatistica(
                ag, cidades, rotas, false // false indica que não será gerado um GIF
        );*/
    }
}
