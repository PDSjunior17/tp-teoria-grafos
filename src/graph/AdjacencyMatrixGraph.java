
import java.io.*;

public class AdjacencyMatrixGraph extends AbstractGraph {
    // ---------------Matriz de adjacência para representar o grafo------------

    /*Lógica Principal: Matrix [i][j] = 1,se existir arestasa indo de i e entrando em j
    0,caso contrário 
    edgeWeights[i][j] = peso da aresta (0 se não existe)
     */
    private int[][] matrix;
    private double[][] edgeWeights;

    public AdjacencyMatrixGraph(int vertices) {
        super(vertices); // chama o construtor de AbstractGraph
        this.matrix = new int[vertices][vertices];
        this.edgeWeights = new double[vertices][vertices];

    }

//Primeiro vamos desenvolver os métodos de criação/modificação/remoção dentro do grafo: 
    @Override
    public void addEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);
        checkSimpleGraph(u, v);

        if (matrix[u][v] == 0) {
            matrix[u][v] = 1;
            edges++;
        }
    }

    @Override
    public boolean hasEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);
        if (matrix[u][v] == 1) {
            return true;
        } else {
            return false;
        }
    }

    @Override
    public void removeEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);

        if (matrix[u][v] == 1) {
            matrix[u][v] = 0;
            edgeWeights[u][v] = 0; //remoção lógica
            edges--;
        }
    }

    @Override
    public double getEdgeWeight(int u, int v) {
        checkVertex(u);
        checkVertex(v);
        return this.edgeWeights[u][v];
    }

    @Override
    public void setEdgeWeight(int u, int v, double w) {
        checkVertex(u);
        checkVertex(v);

        if (!hasEdge(u, v)) {
            throw new IllegalStateException("Aresta (" + u + "," + v + ") não existe");
        }

        if (w == 0) {
            throw new IllegalArgumentException("Peso 0 removeria a aresta. Use removeEdge()");
        }

        this.edgeWeights[u][v] = w;
    }

    @Override
    public int getVertexInDegree(int u) {//quantos vértices chegam em u
        checkVertex(u);
        int inDegree = 0;
        for (int i = 0; i < this.vertices; i++) {
            if (matrix[i][u] == 1) {
                inDegree++;
            }
        }
        return inDegree;
    }

    @Override
    public int getVertexOutDegree(int u) {
        checkVertex(u);
        int outDegree = 0;
        for (int j = 0; j < this.vertices; j++) {
            if (matrix[u][j] == 1) {
                outDegree++;
            }
        }
        return outDegree;
    }

    public void buscaProf(int v, boolean[] visited) {
        visited[v] = true; //marca o vértice atual como visitado
        for (int i = 0; i < this.vertices; i++) {
            if ((matrix[v][i] == 1 || matrix[i][v] == 1) && !visited[i]) {//precisa não ter sido visitado antes 
                buscaProf(i, visited);
            }
        }

    }

    @Override
//Dado um grafo direcionado G = (V, E), ele é considerado conexo quando seu grafo subjacenteG’ for conexo.
    public boolean isConnected() {//vamos verificar o grafo subjacente com busca por profundidade APAPTADO 
        boolean[] visited = new boolean[this.vertices]; //cada vértice vamos identificar se foi visitado
        buscaProf(0, visited);
        for (boolean v : visited) {
            if (!v) {
                return false; // Se algum vértice não foi visitado, o grafo não é conexo
            }
        }
        return true; // Todos os vértices foram visitados, o grafo é conexo
    }

    @Override
    public boolean isEmptyGraph() {//para ver se o grafo não tem arestas 
        return this.edges == 0;

    }

    @Override
    public boolean isCompleteGraph() {
        int n = this.vertices;
        int expectedEdges = (n * (n - 1)); //para grafos direcionados
        return this.edges == expectedEdges;
    }

    @Override
    public void exportToGEPHI(String filename) throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            // Formato GEXF (Graph Exchange XML Format)
            writer.println("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            writer.println("<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\">");
            writer.println("  <graph mode=\"static\" defaultedgetype=\"directed\">");

            // ========== NÓS (VÉRTICES) ==========
            writer.println("    <nodes>");
            for (int i = 0; i < this.vertices; i++) {
                String label = labels[i] != null ? labels[i] : "V" + i;
                writer.println("      <node id=\"" + i + "\" label=\"" + label + "\">");

                // Adiciona peso do vértice como atributo (se diferente de 0)
                if (weightsVertices[i] != 0) {
                    writer.println("        <attvalues>");
                    writer.println("          <attvalue for=\"weight\" value=\""
                            + weightsVertices[i] + "\"/>");
                    writer.println("        </attvalues>");
                }
                writer.println("      </node>");
            }
            writer.println("    </nodes>");

            // ========== ARESTAS ==========
            writer.println("    <edges>");
            int edgeId = 0;
            for (int i = 0; i < this.vertices; i++) {
                for (int j = 0; j < this.vertices; j++) {
                    if (matrix[i][j] == 1) {
                        double weight = edgeWeights[i][j];
                        writer.println("      <edge id=\"" + edgeId++
                                + "\" source=\"" + i
                                + "\" target=\"" + j
                                + "\" weight=\"" + weight + "\"/>");
                    }
                }
            }
            writer.println("    </edges>");

            writer.println("  </graph>");
            writer.println("</gexf>");
        }
    }

    /**
     * Retorna representação textual da matriz
     */
      @Override
public String toString() {
    StringBuilder sb = new StringBuilder();

    sb.append("AdjacencyMatrixGraph (")
      .append(vertices).append(" vertices, ")
      .append(edges).append(" arestas)\n");

    sb.append("Matriz de Adjacencia (0 = sem aresta, 1 = com aresta):\n   ");

    // Cabeçalho
    for (int j = 0; j < vertices; j++) {
        sb.append(String.format("%3d", j));
    }
    sb.append("\n");

    // Linhas da matriz
    for (int i = 0; i < vertices; i++) {
        sb.append(String.format("%2d:", i));
        for (int j = 0; j < vertices; j++) {
            sb.append(String.format("%3d", matrix[i][j]));
        }

        // Rótulo do vértice
        if (labels[i] != null) {
            sb.append("  (").append(labels[i]).append(")");
        }
        sb.append("\n");
    }

    return sb.toString();
}

}
