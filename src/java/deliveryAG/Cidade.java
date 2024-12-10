package deliveryAG;

public class Cidade {
    private String nome; // Nome da cidade

    // Construtor
    public Cidade(String nome) {
        this.nome = nome;
    }

    // Getter para o nome da cidade
    public String getNome() {
        return nome;
    }

    // Setter para o nome da cidade (opcional, se necessário)
    public void setNome(String nome) {
        this.nome = nome;
    }

    @Override
    public String toString() {
        return nome;
    }
}
