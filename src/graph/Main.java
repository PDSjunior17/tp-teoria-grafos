package graph;

import java.util.Scanner;
import java.io.IOException;

public class Main {

    private static final Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {

        System.out.println("=== TP Teoria dos Grafos ===");

        String csvPath = escolherGrafo();
        int rep = escolherRepresentacao();

        try {
            GraphLoader.GraphData data = GraphLoader.load(csvPath);

            AbstractGraph graph
                    = (rep == 1)
                            ? new AdjacencyListGraph(data.vertices.size())
                            : new AdjacencyMatrixGraph(data.vertices.size());

            for (int i = 0; i < data.vertices.size(); i++) {
                graph.setLabel(i, data.vertices.get(i));
            }

            for (GraphLoader.Edge e : data.edges) {
                graph.addEdge(e.source, e.target);
                if (e.weight != 1.0) {
                    graph.setEdgeWeight(e.source, e.target, e.weight);
                }
            }

            menuOperacoes(graph);

        } catch (IOException e) {
            System.err.println("Erro ao carregar CSV: " + e.getMessage());
        }
    }

    private static String escolherGrafo() {
        System.out.println("\nEscolha o grafo:");
        System.out.println("1 - Comentarios");
        System.out.println("2 - Closures");
        System.out.println("3 - Reviews");
        System.out.println("4 - Integrado"); //CSV integrado já contém pesos consolidados!!!!!!

        int opcao = sc.nextInt();

        switch (opcao) {
            case 1:
                return "../data/raw/vercel_next.js_comments.csv";

            case 2:
                return "../data/raw/vercel_next.js_closures.csv";

            case 3:
                return "../data/raw/vercel_next.js_reviews.csv";

            case 4:
                return "../data/raw/vercel_next.js_integrated.csv";

            default:
                return "../data/raw/vercel_next.js_comments.csv";
        }
    }

    private static int escolherRepresentacao() {
        System.out.println("\nEscolha a representacao:");
        System.out.println("1 - Lista");
        System.out.println("2 - Matriz");

        int opcao = sc.nextInt();
        return (opcao == 2) ? 2 : 1;
    }

    private static void menuOperacoes(AbstractGraph graph) {
        int opcao;
        do {
            System.out.println("\n--- Operacoes ---");
            System.out.println("1 - Mostrar grafo");
            System.out.println("2 - Grafo vazio?");
            System.out.println("3 - Grafo completo?");
            System.out.println("4 - Grafo conexo?");
            System.out.println("5 - Voltar ao início");
            System.out.println("0 - Sair");

            opcao = sc.nextInt();

            switch (opcao) {
                case 1:
                    System.out.println(graph);
                    break;
                case 2:
                    System.out.println(graph.isEmptyGraph());
                    break;
                case 3:
                    System.out.println(graph.isCompleteGraph());
                    break;
                case 4:
                    System.out.println(graph.isConnected());
                    break;
                case 5:
                    main(null);
            }
        } while (opcao != 0);
    }
}
