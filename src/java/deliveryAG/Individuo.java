package deliveryAG;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Individuo {
    private List<deliveryAG.Cidade> cidades; // Lista de cidades disponíveis
    private int[][] rotas; // Matriz de distâncias entre as cidades
    private List<Integer> caminho; // Cidades obrigatórias a serem visitadas
    private int centroDistribuicao; // Cidade inicial e final obrigatória
    private int geracao; // Número da geração do indivíduo
    private List<Integer> cromossomo; // Sequência de cidades percorridas
    private double distanciaPercorrida; // Distância total percorrida
    private int cidadesPercorridas; // Número de cidades diferentes visitadas
    private double notaAvaliacao; // Avaliação da qualidade da rota
    private double probabilidade; // Probabilidade de seleção

    private static final Random RANDOM = new Random();

    // Construtor
    public Individuo(List<deliveryAG.Cidade> cidades, int[][] rotas, List<Integer> caminho, int centroDistribuicao, int geracao, List<Integer> cromossomo) {
        this.cidades = cidades;
        this.rotas = rotas;
        this.caminho = caminho;
        this.centroDistribuicao = centroDistribuicao;
        //this.geracao = geracao;
        this.geracao = (geracao > 0) ? geracao : 1;
        this.cromossomo = cromossomo != null ? cromossomo : gerarCromossomo();
        this.notaAvaliacao = avaliacao();
    }

    // Gera um cromossomo aleatório
    private List<Integer> gerarCromossomo() {
        List<Integer> novoCromossomo = new ArrayList<>();
        for (int i = 0; i < rotas.length; i++) {
            novoCromossomo.add(RANDOM.nextInt(rotas.length));
        }
        return novoCromossomo;
    }

    // Calcula a avaliação do indivíduo
    private double avaliacao() {
        double somaDistancia = 0;
        List<Integer> cidadesVisitadas = new ArrayList<>();

        for (int i = 0; i < cromossomo.size() - 1; i++) {
            int origem = cromossomo.get(i);
            int destino = cromossomo.get(i + 1);
            int distancia = rotas[origem][destino];

            somaDistancia += (distancia == -1) ? 5000 : distancia;

            if (caminho.contains(origem) && !cidadesVisitadas.contains(origem)) {
                cidadesVisitadas.add(origem);
            }
        }

        distanciaPercorrida = somaDistancia;
        cidadesPercorridas = cidadesVisitadas.size();

        int cidadesFaltando = caminho.size() - cidadesVisitadas.size();
        somaDistancia += 100 * cidadesFaltando;

        if (cromossomo.get(0) != centroDistribuicao) {
            somaDistancia += 5000;
        }
        if (cromossomo.get(cromossomo.size() - 1) != centroDistribuicao) {
            somaDistancia += 5000;
        }

        return somaDistancia;
    }

    // Realiza o crossover com outro indivíduo
    public List<Individuo> crossover(Individuo outroIndividuo) {
        int corte = RANDOM.nextInt(cromossomo.size());
        List<Integer> filho1 = new ArrayList<>();
        List<Integer> filho2 = new ArrayList<>();

        filho1.addAll(outroIndividuo.cromossomo.subList(0, corte));
        filho1.addAll(cromossomo.subList(corte, cromossomo.size()));

        filho2.addAll(cromossomo.subList(0, corte));
        filho2.addAll(outroIndividuo.cromossomo.subList(corte, outroIndividuo.cromossomo.size()));

        List<Individuo> filhos = new ArrayList<>();
        filhos.add(new Individuo(cidades, rotas, caminho, centroDistribuicao, geracao + 1, filho1));
        filhos.add(new Individuo(cidades, rotas, caminho, centroDistribuicao, geracao + 1, filho2));

        return filhos;
    }

    // Aplica mutação ao cromossomo
    public Individuo mutacao(double taxaMutacao) {
        for (int i = 0; i < cromossomo.size(); i++) {
            if (RANDOM.nextDouble() <= taxaMutacao) {
                cromossomo.set(i, RANDOM.nextInt(rotas.length));
            }
        }
        notaAvaliacao = avaliacao();
        return this;
    }

    // Converte o cromossomo para uma visualização com os nomes das cidades
    public List<String> cromossomoToView() {
        List<String> nomesCidades = new ArrayList<>();
        for (int indice : cromossomo) {
            nomesCidades.add(cidades.get(indice).getNome());
        }
        return nomesCidades;
    }

    // Imprime informações do indivíduo
    public void print() {
        System.out.println(" ***** ");
        System.out.println(" Geração: " + geracao);
        System.out.println(" Cromossomo: " + cromossomoToView());
        System.out.println(" Distância percorrida: " + distanciaPercorrida);
        System.out.println(" Cidades percorridas: " + cidadesPercorridas);
        System.out.println(" Avaliação: " + notaAvaliacao);
        System.out.println(" ***** ");
    }

    // Getters
    public double getNotaAvaliacao() {
        return notaAvaliacao;
    }

    public List<Integer> getCromossomo() {
        return cromossomo;
    }

    // Métodos adicionais para corrigir os erros
    public int getGeracao() {
        return geracao;
    }

    public double getDistanciaPercorrida() {
        return distanciaPercorrida;
    }

    public int getCidadesPercorridas() {
        return cidadesPercorridas;
    }

    public void setProbabilidade(double probabilidade) {
        this.probabilidade = probabilidade;
    }

    public double getProbabilidade() {
        return probabilidade;
    }
}
