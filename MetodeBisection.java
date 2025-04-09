import java.util.Scanner;

public class MetodeBisection {
     public static void main(String[] args) {
          MetodeDinamis m = new MetodeDinamis();
          Scanner input = new Scanner(System.in);
          System.out.print("Persamaan : ");
          String soal = input.nextLine();
          System.out.print("Interval a : ");
          double a = input.nextDouble();
          System.out.print("Interval b : ");
          double b = input.nextDouble();
          System.out.print("Error : ");
          double error = input.nextDouble();

          double fa = m.persamaan(soal, a);
          double fb = m.persamaan(soal, b);
          if (fa < 0 && fb > 0) {
               int k = 0;
               Double akar = null;
               while (true) {
                    double c = (a + b) / 2;
                    double fc = m.persamaan(soal, c);
                    if (fc < 0) {
                         a = c;
                    }
                    if (fc > 0) {
                         b = c;
                    }

                    if (Math.abs(fc) < error ) {
                         akar = c;
                         k++;
                         break;
                    }
                    k++;
               }

               System.out.println("Akar = " + akar);
               System.out.println("Interval akhir : " + a + "," + b);
               System.out.println("Iterasi : " + k);
          } else {
               System.out.println("tidka memiliki akar");
          }

          input.close();
     }

     char[] operator(String persamaan) {
          int banyakOperator = 0;
          String wadah = "";
          for (int i = 0; i < persamaan.length(); i++) {
               if (persamaan.charAt(i) == '-' || persamaan.charAt(i) == '+') {
                    wadah += persamaan.charAt(i);
                    banyakOperator++;
               }
          }

          char[] operator = new char[banyakOperator];
          for (int i = 0; i < wadah.length(); i++) {
               operator[i] = wadah.charAt(i);
          }
          return operator;
     }

     String update(String persamaan) {
          operator(persamaan);

          String wadah = "";
          for (int i = 0; i < persamaan.length(); i++) {
               if (persamaan.charAt(i) == '-' || persamaan.charAt(i) == '+') {
                    wadah += " ";
               } else {
                    wadah += persamaan.charAt(i);
               }
          }
          wadah = wadah.trim();
          return wadah;
     }
     
     double[] konstanta(String persamaan) {
          String persamaanBaru = update(persamaan);
          String wadah = "";
          String nilai[] = persamaanBaru.split(" ");
          for (int i = 0; i < nilai.length; i++) {
               nilai[i] = nilai[i].trim();
          }

          double konstanta[] = new double[nilai.length];
          for (int i = 0; i < konstanta.length; i++) {
               boolean variabel = false; 
               int index = -1;
               for (int j = 0; j < nilai[i].length(); j++) {
                    if (nilai[i].charAt(j) == 'x') {
                         variabel = true;
                         index = j;
                    }
               }
               if (variabel) {
                    if (index == 0) {
                         konstanta[i] = 1.0;
                    } else {
                         wadah = "";
                         for (int j = 0; j < index; j++) {
                              wadah += nilai[i].charAt(j);
                         }
                         konstanta[i] = Double.parseDouble(wadah);
                    }
               } else {
                    konstanta[i] = Double.parseDouble(nilai[i]);
               }
          }
          return konstanta;
     }

     double[] pangkat(String persamaan) {
          String persemaanBaru = update(persamaan);
          String nilai[] = persemaanBaru.split(" ");
          for (int i = 0; i < nilai.length; i++) {
               nilai[i] = nilai[i].trim();
          }
          double[] pangkat = new double[nilai.length];
          for (int i = 0; i < pangkat.length; i++) {
               boolean ada = false;
               int index = -1;
               for (int j = 0; j < nilai[i].length(); j++) {
                    if (nilai[i].charAt(j) == 'x' || nilai[i].charAt(j) == '^') {
                         ada = true;
                         index = j;
                    }
               }

               if (ada) {
                    String wadah = "";
                    if (index < nilai[i].length() - 1) { 
                         for (int j = index + 1; j < nilai[i].length(); j++) {
                              wadah += nilai[i].charAt(j);
                         }
                         pangkat[i] = Double.parseDouble(wadah);
                    } else {
                         pangkat[i] = 1.0;
                    }
               } else {
                    pangkat[i] = 0.0;
               }
          }
          return pangkat;
     }

     double persamaan(String persamaan, double parameter) {
          double[] konstanta = konstanta(persamaan);
          double[] pangkat = pangkat(persamaan);
          char[] operator = operator(persamaan);
          double hasil = 0.0;
          if (operator.length == konstanta.length) {
               for (int i = 0; i < konstanta.length; i++) {
                    if (operator[i] == '-') {
                         if (pangkat[i] != 0.0) {
                              hasil -= (konstanta[i] * Math.pow(parameter, pangkat[i]));
                         } else {
                              hasil -= konstanta[i];
                         }
                    } else {
                         if (pangkat[i] != 0.0) {
                              hasil += (konstanta[i] * Math.pow(parameter, pangkat[i]));
                         } else {
                              hasil += konstanta[i];
                         }
                    }
               }
          } else {
               for (int i = 0; i < konstanta.length; i++) {
                    if (i == 0) {
                         if (pangkat[i] != 0.0) {
                              hasil += (konstanta[i] * Math.pow(parameter, pangkat[i]));
                         } else {
                              hasil += konstanta[i];
                         }
                         continue;
                    }
                    if (operator[i - 1] == '-') {
                         if (pangkat[i] != 0.0) {
                              hasil -= (konstanta[i] * Math.pow(parameter, pangkat[i]));
                         } else {
                              hasil -= konstanta[i];
                         }
                    } else {
                         if (pangkat[i] != 0.0) {
                              hasil += (konstanta[i] * Math.pow(parameter, pangkat[i]));
                         } else {
                              hasil += konstanta[i];
                         }
                    }
               }
          }
          return hasil;
     }
}
