public class TestAdjacencyMatrixGraph {

    public static void main(String[] args) {

    
        AdjacencyMatrixGraph g = new AdjacencyMatrixGraph(4);


        g.addEdge(0, 1);
        g.addEdge(1, 0);
        g.addEdge(1, 2);
        g.addEdge(1, 3);

    
        System.out.println("0 -> 1 existe? " + g.hasEdge(0, 1)); // true
        System.out.println("0 -> 2 existe? " + g.hasEdge(0, 2)); // false


        System.out.println("Grau de saída de 1: " + g.getVertexOutDegree(1)); // 3
        System.out.println("Grau de entrada de 1: " + g.getVertexInDegree(1)); // 3

  
        System.out.println("Grafo é conexo? " + g.isConnected()); // true

    
        System.out.println("Grafo está vazio? " + g.isEmptyGraph()); // false


        System.out.println("\nRepresentação do grafo:");
        System.out.println(g);
    }
}

