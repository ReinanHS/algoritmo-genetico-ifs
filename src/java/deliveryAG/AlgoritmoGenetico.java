package deliveryAG;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;


public class AlgoritmoGenetico {
    private int tamanhoPopulacao;
    private double taxaMutacao;
    private boolean debugMode;
    private List<deliveryAG.Individuo> populacao;
    private List<deliveryAG.Individuo> melhoresSolucoesGeracao;
    private List<deliveryAG.Individuo> historicoPopulacao;
    private deliveryAG.Individuo melhorSolucao;

    public AlgoritmoGenetico(int tamanhoPopulacao, double taxaMutacao, boolean debugMode) {
        this.tamanhoPopulacao = tamanhoPopulacao;
        this.taxaMutacao = taxaMutacao;
        this.debugMode = debugMode;
        this.populacao = new ArrayList<>();
        this.melhoresSolucoesGeracao = new ArrayList<>();
        this.historicoPopulacao = new ArrayList<>();
        this.melhorSolucao = null;
    }

    public void inicializaPopulacao(List<deliveryAG.Cidade> cidades, int[][] rotas, List<Integer> caminho, int centroDistribuicao) {
        for (int i = 0; i < this.tamanhoPopulacao; i++) {
            this.populacao.add(new deliveryAG.Individuo(cidades, rotas, caminho, centroDistribuicao,1 , null));
        }
        this.melhorSolucao = this.populacao.get(0);
        this.historicoPopulacao = this.populacao;
    }

    public void ordenaPopulacao() {
        this.populacao.sort((individuo1, individuo2) -> Double.compare(individuo1.getNotaAvaliacao(), individuo2.getNotaAvaliacao()));
    }

    public void melhorIndividuo(deliveryAG.Individuo individuo) {
        if (individuo.getNotaAvaliacao() < this.melhorSolucao.getNotaAvaliacao()) {
            this.melhorSolucao = individuo;
        }
    }

    public double somaAvaliacoes() {
        return this.populacao.stream().mapToDouble(deliveryAG.Individuo::getNotaAvaliacao).sum();
    }

    public void visualizaGeracao() {
       /* if (!this.debugMode) {
            return;
        }*/
        deliveryAG.Individuo melhor = this.populacao.get(0);
        System.out.println(" *****");
        System.out.println(" Geração: " + melhor.getGeracao());
        System.out.println(" Melhor solução: " + melhor.getNotaAvaliacao());
        System.out.println(" Distância percorrida: " + melhor.getDistanciaPercorrida());
        System.out.println(" Cidades percorridas: " + melhor.getCidadesPercorridas());
        System.out.println(" Cromossomo: " + melhor.cromossomoToView());
        System.out.println(" *****");
    }

    public void visualizaMelhorGeracao() {
       if (!this.debugMode) {
            return;
        }
        deliveryAG.Individuo melhor = this.melhorSolucao;
        System.out.println(" ***** (Melhor solução) *****");
        System.out.println(" Geração: " + melhor.getGeracao());
        System.out.println(" Melhor solução: " + melhor.getNotaAvaliacao());
        System.out.println(" Distância percorrida: " + melhor.getDistanciaPercorrida());
        System.out.println(" Cidades percorridas: " + melhor.getCidadesPercorridas());
        System.out.println(" Cromossomo: " + melhor.cromossomoToView());
        System.out.println(" ***** ================ *****");
    }

    public void gerarProbabilidade() {
        List<Double> pesos = new ArrayList<>();
        for (int i = 0; i < this.populacao.size(); i++) {
            pesos.add(1.0 / (i + 1));
        }
        double somaPesos = pesos.stream().mapToDouble(Double::doubleValue).sum();

        for (int i = 0; i < this.populacao.size(); i++) {
            deliveryAG.Individuo individuo = this.populacao.get(i);
            individuo.setProbabilidade((pesos.get(i) / somaPesos) * 100);
        }
    }

    public int selecionaPai() {
        List<Double> cumulativas = new ArrayList<>();
        double soma = 0;
        for (deliveryAG.Individuo individuo : this.populacao) {
            soma += individuo.getProbabilidade();
            cumulativas.add(soma);
        }

        Random random = new Random();
        int numeroAleatorio = random.nextInt(100);

        for (int i = 0; i < cumulativas.size(); i++) {
            if (numeroAleatorio < cumulativas.get(i)) {
                return i;
            }
        }
        return selecionaPai();
    }

    public deliveryAG.Individuo resolver(int numeroGeracoes, List<deliveryAG.Cidade> cidades, int[][] rotas, List<Integer> caminho, int centroDistribuicao) {
        inicializaPopulacao(cidades, rotas, caminho, centroDistribuicao);
        ordenaPopulacao();
        gerarProbabilidade();
        visualizaGeracao();
        this.melhoresSolucoesGeracao.add(this.populacao.get(0));

        for (int i = 0; i < numeroGeracoes; i++) {
            List<deliveryAG.Individuo> novaPopulacao = new ArrayList<>();

            for (int j = 0; j < this.tamanhoPopulacao; j += 2) {
                int pai1 = selecionaPai();
                int pai2 = selecionaPai();

                List<deliveryAG.Individuo> filhos = this.populacao.get(pai1).crossover(this.populacao.get(pai2));
                novaPopulacao.add(filhos.get(0).mutacao(this.taxaMutacao));
                novaPopulacao.add(filhos.get(1).mutacao(this.taxaMutacao));
            }

            novaPopulacao = novaPopulacao.subList(0, novaPopulacao.size() - 5);
            novaPopulacao.addAll(this.populacao.subList(0, 5));

            this.populacao = novaPopulacao;
            ordenaPopulacao();
            gerarProbabilidade();
            visualizaGeracao();
            this.historicoPopulacao.addAll(this.populacao);

            deliveryAG.Individuo melhor = this.populacao.get(0);
            melhorIndividuo(melhor);
            this.melhoresSolucoesGeracao.add(melhor);
        }

        visualizaMelhorGeracao();
        return this.melhorSolucao;
    }
}

