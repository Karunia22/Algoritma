package Algoritma;

import java.util.ArrayList;
import java.util.Scanner;

public class Algoritma_Gready {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int graph[][] = {
            {0, 12, 9, 10},
            {12, 0, 8, 5,},
            {9, 8, 0, 15},
            {10, 5, 15, 0}
        };

        ArrayList<Integer> path = new ArrayList<>();
        int mulai = in.nextInt();
        int banyakVerteks = graph.length;
        path.add(mulai);

        while (path.size() < banyakVerteks) {
            int origin = path.get(path.size() - 1);
            int min = Integer.MAX_VALUE;
            int destinasi = 0;
            for (int i = 0; i < graph.length; i++) {
                boolean cekJalur = true;
                for (int j = 0; j < path.size(); j++) {
                    if (i == path.get(j)) {
                        cekJalur = false;
                    }
                }

                if (i != origin) {
                    if (min > graph[origin][i] && cekJalur) {
                        destinasi = i;
                        min = graph[origin][i];
                    }
                }
            }
            path.add(destinasi);
        }

        path.add(mulai);
        int totalJarak = 0;
        for (int i = 0; i < path.size()-1; i++) {
            int asal = path.get(i);
            int tujuan = path.get(i+1);
            
            System.out.print(graph[asal][tujuan] + " ");
            totalJarak += graph[asal][tujuan];
        }
        System.out.println("\nTotal jarak: " + totalJarak);
        in.close();
        
    }
}

