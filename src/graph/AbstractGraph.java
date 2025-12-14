
import java.io.IOException;

abstract class AbstractGraph {
    // ========== CLASSE ABSTRATA ==========

    /* Classe abstrata AbstractGraph, definindo a API comum, atributos compartilhados (rótulos
         e pesos de vértices), e métodos auxiliares (ex.: verificaçao de indices).
     */
    
    //Observa-se que o código foi pensando para grafos simples e direcionados!!! 
    protected int vertices;// número vértices
    protected int edges; // número arestas 

    protected String[] labels; //rótulos dos vértices
    protected double[] weightsVertices; // pesos dos vértices
    //obs: peso das arestas será tratado nas classes concretas!!!!

    //construtor 
    public AbstractGraph(int vertices) {
        if (vertices <= 0) {
            throw new IllegalArgumentException("Número de vértices não pode ser negativo ou igual a zero: " + vertices);
        }
        this.vertices = vertices;
        this.edges = 0;
        this.labels = new String[vertices];
        this.weightsVertices = new double[vertices];
    }

    //método para garantir que vértice inserido será válido 
    protected void checkVertex(int v) {
        if (v < 0 || v >= vertices) {
            throw new IndexOutOfBoundsException("Vértice inválido: " + v);
        }
    }

    //método para manter/ garantir que o grafo é simples 
    protected void checkSimpleGraph(int u, int v) {
        if (u == v) {
            throw new IllegalArgumentException("Laços não são permitidos em grafos simples: " + u + " -> " + v);
        }
    }

    //getters
    public int getVertices() {
        return this.vertices;
    }

    public int getEdges() {
        return this.edges;
    }

    public String getLabels(int v) {
        checkVertex(v);
        return this.labels[v];
    }

    public double getVertexWeight(int v) {
        checkVertex(v);
        return this.weightsVertices[v];
    }

    //setters
    public void setLabel(int v, String label) {
        checkVertex(v);
        this.labels[v] = label;
    }

    public void setVertexWeight(int v, double w) {
        checkVertex(v);
        this.weightsVertices[v] = w;
    }

    // ========== API (MÉTODOS PÚBLICOS DA CLASSE)  OBRIGATÓRIOS ==========
    public boolean isSucessor(int u, int v) { // se v é sucessor de u
        checkVertex(u);
        checkVertex(v);
        return hasEdge(u, v);
    }

    public boolean isPredessor(int u, int v) {//se u é predessor de v
        checkVertex(u);
        checkVertex(v);
        return hasEdge(u, v);
    }

    public boolean isDivergent(int u1, int v1, int u2, int v2) {//Duas arestas são divergentes se partem do mesmo vértice inicial
        checkVertex(u1);
        checkVertex(v1);
        checkVertex(u2);
        checkVertex(v2);
        return (hasEdge(u1, v1) && hasEdge(u2, v2) && u1 == u2);
    }

    public boolean isConvergent(int u1, int v1, int u2, int v2) {//Duas arestas são convergentes se chegam no mesmo vértice final
        checkVertex(u1);
        checkVertex(v1);
        checkVertex(u2);
        checkVertex(v2);
        return (hasEdge(u1, v1) && hasEdge(u2, v2) && v1 == v2);
    }

    public boolean isIncident(int u, int v, int x) {//uma aresta é incidente a um vértice se este é o vértice inicial ou final da aresta
        checkVertex(u);
        checkVertex(v);
        checkVertex(x);
        return (hasEdge(u, v) && (u == x || v == x));
    }

    // ========== MÉTODOS ABSTRATOS ==========
    public abstract boolean hasEdge(int u, int v);

    public abstract void addEdge(int u, int v);

    public abstract void removeEdge(int u, int v);

    public abstract int getVertexInDegree(int u);

    public abstract int getVertexOutDegree(int u);

    public abstract void setEdgeWeight(int u, int v, double w);

    public abstract double getEdgeWeight(int u, int v);

    public abstract boolean isConnected();

    public abstract boolean isEmptyGraph();

    public abstract boolean isCompleteGraph();

    public abstract void exportToGEPHI(String path) throws IOException;
}
