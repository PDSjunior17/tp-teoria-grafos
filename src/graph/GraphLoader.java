package graph;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.LinkedHashMap;

public class GraphLoader {

    public static class GraphData {
        public List<String> vertices = new ArrayList<>();
        public List<Edge> edges = new ArrayList<>();
    }

    public static class Edge {
        public int source;
        public int target;
        public double weight;

        public Edge(int s, int t, double w) {
            source = s;
            target = t;
            weight = w;
        }
    }

    public static GraphData load(String csvPath) throws IOException {
        Map<String, Integer> map = new LinkedHashMap<>();
        GraphData data = new GraphData();

        try (BufferedReader br = new BufferedReader(new FileReader(csvPath))) {
            String line;
            boolean first = true;

            while ((line = br.readLine()) != null) {
                if (first) { first = false; continue; }
                String[] p = line.split(",");
                if (p.length < 3) continue;

                String src = p[0].trim();
                String tgt = p[1].trim();
                double w = Double.parseDouble(p[2].trim());

                if (!map.containsKey(src)) {
                    map.put(src, map.size());
                    data.vertices.add(src);
                }
                if (!map.containsKey(tgt)) {
                    map.put(tgt, map.size());
                    data.vertices.add(tgt);
                }

                data.edges.add(new Edge(map.get(src), map.get(tgt), w));
            }
        }
        return data;
    }
}
