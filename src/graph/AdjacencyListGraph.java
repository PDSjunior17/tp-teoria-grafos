
import java.io.*;
import java.util.*;

/**
 * ---------------Implementação de grafo usando Lista de Adjacência---------------
 *
 * LÓGICA PRINCIPAL: Lista sucessores!! Cada vértice tem uma lista de vizinhos
 * (sucessores) Cada vizinho tem um peso associado Usamos um
 * Map<Integer, Double> para armazenar: destino -> peso
 *
 *
 */
public class AdjacencyListGraph extends AbstractGraph {

    private List<Map<Integer, Double>> adjList;

    public AdjacencyListGraph(int vertices) {
        super(vertices);
        this.adjList = new ArrayList<>(vertices);
        for (int i = 0; i < vertices; i++) {
            adjList.add(new HashMap<>());
        }
    }

    @Override
    public void addEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);
        checkSimpleGraph(u, v);
        if (!adjList.get(u).containsKey(v)) {//verifica se a aresta já não existe
            adjList.get(u).put(v, 1.0); //coloca o peso inical igual a 1
            edges++;
        }
    }

    @Override
    public boolean hasEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);
        return adjList.get(u).containsKey(v); //verifica se v está nesse Map
    }

    @Override
    public void removeEdge(int u, int v) {
        checkVertex(u);
        checkVertex(v);

        // Só remove se a aresta existir
        if (adjList.get(u).containsKey(v)) {
            adjList.get(u).remove(v);
            edges--;
        }
    }

    @Override
    public double getEdgeWeight(int u, int v) {
        checkVertex(u);
        checkVertex(v);
        // getOrDefault: retorna o peso se existir, senão retorna 0.0
        return adjList.get(u).getOrDefault(v, 0.0);
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
        adjList.get(u).put(v, w);
    }

    @Override
    public int getVertexOutDegree(int u) {
        checkVertex(u);
        // O tamanho do Map é o número de vizinhos (sucessores)
        return adjList.get(u).size();
    }

    @Override
    public int getVertexInDegree(int u) {
        checkVertex(u);
        int inDegree = 0;
        for (int i = 0; i < vertices; i++) {
            if (adjList.get(i).containsKey(u)) { //analisa onde o u aparece nas listas de sucessores - conta predecessores de u basicamente 
                inDegree++;
            }
        }
        return inDegree;
    }

    private void buscaProf(int v, boolean[] visited) {
        visited[v] = true;
        for (Integer i : adjList.get(v).keySet()) {//pega todos os vizinhos de v (sucessores)
            if (!visited[i]) { // Se i não foi visitado ainda
                buscaProf(i, visited);
            }
        }
        for (int i = 0; i < vertices; i++) {
            if (!visited[i] && adjList.get(i).containsKey(v)) {//Pega todos os predecessores de v
                buscaProf(i, visited);
            }
        }
    }

    @Override
    //Dado um grafo direcionado G = (V, E), ele é considerado conexo quando seu grafo subjacenteG’ for conexo.
    public boolean isConnected() {//vamos verificar o grafo subjacente com busca por profundidade APAPTADO 
        if (vertices == 0) {
            return true;
        }
        boolean[] visited = new boolean[vertices];
        buscaProf(0, visited);
        // Verifica se TODOS os vértices foram visitados - se todos tiverem sido visitados é conexo 
        for (boolean v : visited) {
            if (!v) {
                return false;
            }
        }
        return true;
    }

    @Override
    public boolean isEmptyGraph() {//para ver se o grafo não tem arestas 
        return edges == 0;
    }

    @Override
    public boolean isCompleteGraph() {
        int expectedEdges = vertices * (vertices - 1); //para grafos direcionados
        return edges == expectedEdges;
    }

    @Override
    public void exportToGEPHI(String filename) throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            // ===== CABEÇALHO XML =====
            writer.println("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            writer.println("<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\">");
            writer.println("  <graph mode=\"static\" defaultedgetype=\"directed\">");
            // ===== SEÇÃO DE VÉRTICES (NODES) =====
            writer.println("    <nodes>");
            for (int i = 0; i < vertices; i++) {
                String label = labels[i] != null ? labels[i] : "V" + i;
                writer.println("      <node id=\"" + i + "\" label=\"" + label + "\">");
                // Se o vértice tem peso, adiciona como atributo
                if (weightsVertices[i] != 0) {
                    writer.println("        <attvalues>");
                    writer.println("          <attvalue for=\"weight\" value=\""
                            + weightsVertices[i] + "\"/>");
                    writer.println("        </attvalues>");
                }
                writer.println("      </node>");
            }
            writer.println("    </nodes>");
            // ===== SEÇÃO DE ARESTAS (EDGES) =====
            writer.println("    <edges>");
            int edgeId = 0;
            for (int i = 0; i < vertices; i++) {
                // Para cada vizinho j de i (e seu peso)
                for (Map.Entry<Integer, Double> entry : adjList.get(i).entrySet()) {
                    int target = entry.getKey();
                    double weight = entry.getValue();
                    // Escreve a aresta no formato GEXF
                    writer.println("      <edge id=\"" + edgeId++
                            + "\" source=\"" + i
                            + "\" target=\"" + target
                            + "\" weight=\"" + weight + "\"/>");
                }
            }
            writer.println("    </edges>");
            writer.println("  </graph>");
            writer.println("</gexf>");
        }
    }

    public Set<Integer> getNeighbors(int u) {
        checkVertex(u);
        return adjList.get(u).keySet();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("AdjacencyListGraph (")
                .append(vertices).append(" vértices, ")
                .append(edges).append(" arestas)\n");
        sb.append("Lista de Adjacência:\n");

        // Para cada vértice
        for (int i = 0; i < vertices; i++) {
            // Rótulo do vértice (se existir)
            String label = labels[i] != null ? labels[i] : "V" + i;
            sb.append(i).append(" (").append(label).append("): ");

            // Se não tem vizinhos
            if (adjList.get(i).isEmpty()) {
                sb.append("[]");
            } else {
                // Lista os vizinhos e seus pesos
                sb.append("[");
                boolean first = true;

                for (Map.Entry<Integer, Double> entry : adjList.get(i).entrySet()) {
                    if (!first) {
                        sb.append(", ");
                    }

                    int target = entry.getKey();
                    double weight = entry.getValue();
                    String targetLabel = labels[target] != null
                            ? labels[target] : "V" + target;

                    sb.append(target).append("(").append(targetLabel).append(")");

                    // Só mostra peso se for diferente de 1.0
                    if (weight != 1.0) {
                        sb.append(":").append(String.format("%.1f", weight));
                    }

                    first = false;
                }
                sb.append("]");
            }
            sb.append("\n");
        }

        return sb.toString();
    }
}
