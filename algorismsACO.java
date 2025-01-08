
import java.util.ArrayList;
import java.util.Random;

public class algorismsACO {
    public static void main(String[] args) {
        double[][] arrayJarak = {
                { 0, 10, 15, 20 },
                { 10, 0, 35, 25 },
                { 15, 35, 0, 30 },
                { 20, 25, 30, 0 }
        };

        int jumlahSiklusSemut, jumlahSemut, depot, banyakVertex;
        double alpha, beta, Q, rho;
        jumlahSiklusSemut = 100;
        jumlahSemut = 5;
        depot = 3;
        banyakVertex = arrayJarak.length;
        alpha = 0.5;
        beta = 0.6;
        Q = 5.0;
        rho = 0.5;

        double[][] eta = new double[arrayJarak.length][arrayJarak.length];
        for (int i = 0; i < eta.length; i++) {
            for (int j = 0; j < eta.length; j++) {
                if (i!=j) {
                    eta[i][j] = 1 / arrayJarak[i][j];
                }
            }
        }

        double[][] tau = new double[arrayJarak.length][arrayJarak.length];
        for (int i = 0; i < tau.length; i++) {
            for (int j = 0; j < tau.length; j++) {
                if (i!=j) {
                    tau[i][j] = 1.0;
                }
            }
        }

        int c = 1;
        Random random = new Random();

        int solusi[] = new int[arrayJarak.length + 1];

        while (c <= jumlahSiklusSemut) {

            double jarakTerbaik = Double.MAX_VALUE;
            double[][] deltaTau = new double[arrayJarak.length][arrayJarak.length];
            for (int i = 1; i <= jumlahSemut; i++) {
                ArrayList<Integer> alamat = new ArrayList<>();
                int totalJarakSementara = 0;
                alamat.add(depot);
                while (alamat.size() < banyakVertex) {
                    int ori = alamat.get(alamat.size() - 1);
                    int destinasi = 0;
                    ArrayList<Integer> kandidat = new ArrayList<>();
                    for (int j = 0; j < arrayJarak.length; j++) {
                        if (ori != j && !alamat.contains(j)) {
                            kandidat.add(j);
                        }
                    }
    
                    double sigma = 0.0;
                    double[] pembilang = new double[kandidat.size()];
                    for (int j = 0; j < pembilang.length; j++) {
                        pembilang[j] = Math.pow(tau[ori][kandidat.get(j)], alpha)
                                * Math.pow(eta[ori][kandidat.get(j)], beta);
                        sigma += pembilang[j];
                    }
    
                    double[] probabilitas = new double[kandidat.size()];
                    for (int j = 0; j < probabilitas.length; j++) {
                        probabilitas[j] = pembilang[j] / sigma;
                    }
    
                    double kumulatif[] = new double[probabilitas.length];
                    for (int j = 0; j < kumulatif.length; j++) {
                        kumulatif[j] = probabilitas[j];
                    }
    
                    for (int j = 0; j < kumulatif.length; j++) {
                        for (int k = 0; k < kumulatif.length - 1; k++) {
                            if (kumulatif[k] < kumulatif[k + 1]) {
                                double wadah = kumulatif[k + 1];
                                kumulatif[k + 1] = kumulatif[k];
                                kumulatif[k] = wadah;
                            }
                        }
                    }
    
                    double hasilKumulatif[] = new double[kumulatif.length + 1];
                    for (int j = 0; j < hasilKumulatif.length; j++) {
                        double n = 0.0;
                        for (int k = j; k < kumulatif.length; k++) {
                            n += kumulatif[k];
                        }
                        hasilKumulatif[j] = n;
                    }
    
                    double jalur = random.nextDouble();
                    for (int j = 0; j < hasilKumulatif.length - 1; j++) {
                        if (j == hasilKumulatif.length - 1) {
                            if (jalur >= hasilKumulatif[j + 1] && jalur <= hasilKumulatif[j]) {
                                for (int k = 0; k < probabilitas.length; k++) {
                                    if (kumulatif[j] == probabilitas[k]) {
                                        destinasi = kandidat.get(k);
                                    }
                                }
                                break;
                            }
                        } else {
                            if (jalur > hasilKumulatif[j + 1] && jalur <= hasilKumulatif[j]) {
                                for (int k = 0; k < probabilitas.length; k++) {
                                    if (kumulatif[j] == probabilitas[k]) {
                                        destinasi = kandidat.get(k);
                                    }
                                }
                                break;
                            }
                        }
                    }
                    alamat.add(destinasi);
                } // Selesai mencari jalur
                alamat.add(depot);
                for (int j = 0; j < alamat.size() - 1; j++) {
                    int ori = alamat.get(j);
                    int destinasi = alamat.get(j + 1);
                    totalJarakSementara += arrayJarak[ori][destinasi];
                }
    
                if (jarakTerbaik > totalJarakSementara) {
                    jarakTerbaik = totalJarakSementara;
                    for (int j = 0; j < solusi.length; j++) {
                        solusi[j] = alamat.get(j);
                    }
                }
    
                for (int j = 0; j < deltaTau.length; j++) {
                    int ori = alamat.get(j);
                    int destinasi = alamat.get(j+1);
                    deltaTau[ori][destinasi] += Q / (double) totalJarakSementara;
                }
            } // Setelah semut selesai melalui jalur
    
            for (int i = 0; i < tau.length; i++) {
                for (int j = 0; j < deltaTau.length; j++) {
                    tau[i][j] = (1-rho) * tau [i][j] + deltaTau [i][j];
                }
            }
    
            c++;
        }

        for (int i : solusi) {
            System.out.print(i + " ");
        }
        System.out.println();
    }
}