import pandas as pd
import random
import math
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

ds = pd.read_csv('asthma_dataset.csv')
print(ds)
ds = ds.drop(columns='Patient_ID')
print(ds.head())
print(ds.describe())
print(ds.isnull().sum())
ds['Medication'] = ds['Medication'].fillna(ds['Medication'].mode()[0])
print(ds.isnull().sum())

dataFrame = pd.DataFrame(ds)
dataFrame['Gender'] = LabelEncoder().fit_transform(dataFrame['Gender'])
dataFrame['Smoking_Status'] = LabelEncoder().fit_transform(dataFrame['Smoking_Status'])
dataFrame['Medication'] = LabelEncoder().fit_transform(dataFrame['Medication'])
fitur = dataFrame[['Age', 'Gender','Smoking_Status','Medication','Peak_Flow']]
print('data')
print(dataFrame)
# Normalisasi menggunakan StandardScaler
scaler = MinMaxScaler()
fitur_scaled = scaler.fit_transform(fitur)
print('nornalisasi')
print(fitur_scaled)
# Konversi ke array 2D
arrayData = fitur_scaled.tolist()
batasPenegcekanKlusterOptimal = 10
#=======================Mencari Kluster Optimal=================================
hasilSEE = []
for kluster in range(1, batasPenegcekanKlusterOptimal + 1):  # periksa hingga batas maksimal
    indexData = []  # untuk menyimpan index dari setiap sampel
    for i in range(len(arrayData)):
        indexData.append(i)

    # Inisialisasi centroid awal secara acak
    random.seed(42)
    indexRandom = random.sample(indexData, kluster)
    centroid = [[0 for _ in range(len(arrayData[0]))] for _ in range(kluster)]
    for i in range(len(centroid)):
        for j in range(len(centroid[0])):
            centroid[i][j] = arrayData[indexRandom[i]][j]

    error = 0.01
    iterasi = 0

    while True:
        # 1. Menentukan kluster terdekat untuk setiap data
        penugasanKluster = [0] * len(arrayData)
        for i in range(len(arrayData)):
            jarakTerdekat = float('inf')
            indexTerdekat = -1
            for j in range(len(centroid)):
                jarak = 0
                for k in range(len(arrayData[0])):
                    jarak += math.pow(arrayData[i][k] - centroid[j][k], 2)
                jarak = math.sqrt(jarak)
                if jarak < jarakTerdekat:
                    jarakTerdekat = jarak
                    indexTerdekat = j
            penugasanKluster[i] = indexTerdekat

        # 2. Mengupdate centroid berdasarkan penugasan kluster
        centroidBaru = [[0 for _ in range(len(arrayData[0]))] for _ in range(kluster)]
        jumlahAnggota = [0 for _ in range(kluster)]
        for i in range(len(arrayData)):
            idx = penugasanKluster[i]
            for j in range(len(arrayData[0])):
                centroidBaru[idx][j] += arrayData[i][j]
            jumlahAnggota[idx] += 1

        for i in range(kluster):
            if jumlahAnggota[i] != 0:
                for j in range(len(arrayData[0])):
                    centroidBaru[i][j] /= jumlahAnggota[i]
            else:
                centroidBaru[i] = centroid[i]  # jika kluster kosong, tetap pakai centroid lama

        # 3. Hitung total perubahan centroid
        perubahanTotal = 0
        for i in range(kluster):
            for j in range(len(arrayData[0])):
                perubahanTotal += abs(centroidBaru[i][j] - centroid[i][j])

        centroid = centroidBaru
        iterasi += 1

        if perubahanTotal < error:
            break

    # 4. Hitung SSE (Sum of Squared Errors)
    sigma = 0
    for i in range(len(arrayData)):
        c = penugasanKluster[i]
        jarak = 0
        for j in range(len(arrayData[0])):
            jarak += math.pow(arrayData[i][j] - centroid[c][j], 2)
        sigma += jarak

    hasilSEE.append(sigma)
# mencari jarak ntar titik yang mengalami penurunan drastis
jarakAntarSentroid = []
for index in range(len(hasilSEE)):
    if(index == 0):
        jarakAntarSentroid.append(0)
    else:
        jarakAntarSentroid.append(hasilSEE[index-1]-hasilSEE[index])

maks = float('-inf')
print(jarakAntarSentroid)

centroidOptimal = 0
print(f'hasilSEE: {hasilSEE}')
for i in range(len(jarakAntarSentroid)):
    if(maks<jarakAntarSentroid[i]):
        maks = jarakAntarSentroid[i]
        centroidOptimal = i+1
print(f'Selisih SSE: {jarakAntarSentroid}')
print(f"kluster optimal : {centroidOptimal}")

#============================Mencari K-Means Berdasarkan K optimal=================================
indexData = []
for i in range(len(arrayData)):
    indexData.append(i)

random.seed(42)
indexRandom = random.sample(indexData, centroidOptimal)  # mencari centroid awal

# menyimpan nilai centroid awal
centroid = [[0 for _ in range(len(arrayData[0]))] for _ in range(centroidOptimal)]
for i in range(len(centroid)):
    for j in range(len(centroid[0])):
        centroid[i][j] = arrayData[indexRandom[i]][j]

error = 0.01
iterasi = 0
anggotaSentroid = []
labelSentroid = []

while True:
    # Step 1: Hitung jarak Euclidean dan tetapkan kluster terdekat
    eucliean = [[0 for _ in range(len(centroid))] for _ in range(len(arrayData))]
    labelSentroid = []

    for i in range(len(arrayData)):
        minJarak = float('inf')
        indexKluster = -1
        for j in range(len(centroid)):
            jarak = 0
            for k in range(len(arrayData[0])):
                jarak += math.pow(arrayData[i][k] - centroid[j][k], 2)
            jarak = math.sqrt(jarak)
            eucliean[i][j] = jarak
            if jarak < minJarak:
                minJarak = jarak
                indexKluster = j
        labelSentroid.append(indexKluster)

    # Step 2: Update centroid berdasarkan label
    klasterLama = [row[:] for row in centroid]
    anggotaSentroid = [[] for _ in range(centroidOptimal)]

    for i in range(len(labelSentroid)):
        anggotaSentroid[labelSentroid[i]].append(i)

    for i in range(centroidOptimal):
        for j in range(len(arrayData[0])):
            jumlah = 0
            if len(anggotaSentroid[i]) > 0:
                for k in anggotaSentroid[i]:
                    jumlah += arrayData[k][j]
                centroid[i][j] = jumlah / len(anggotaSentroid[i])
            # jika tidak ada anggota, centroid tidak berubah

    # Step 3: Hitung perubahan total
    perubahanTotal = 0
    for i in range(len(centroid)):
        for j in range(len(centroid[0])):
            perubahanTotal += abs(centroid[i][j] - klasterLama[i][j])

    iterasi += 1
    if abs(perubahanTotal) < error:
        break
#pemberian label pada centroid

for i in range(len(arrayData)):
    min = float('inf')
    index = -1
    for j in range(len(centroid)):
        jarak = 0
        for k in range(len(arrayData[0])):
            jarak += math.pow(arrayData[i][k] - centroid[j][k], 2)
        if jarak < min:
            min = jarak
            index = j
    anggotaSentroid.append(i)
    labelSentroid.append(f'c{index+1}')

# pengelompokan anggota sentroid
labelSentroid = []
pelabelanAnggotaSentroid = [['' for _ in range(2)] for _ in range(len(arrayData))]

for i in range(len(arrayData)):
    minJarak = float('inf')
    index = -1
    for j in range(len(centroid)):
        jarak = 0
        for k in range(len(arrayData[0])):
            jarak += math.pow(arrayData[i][k] - centroid[j][k], 2)
        if jarak < minJarak:
            minJarak = jarak
            index = j

    labelSentroid.append(f'c{index+1}')
    pelabelanAnggotaSentroid[i][0] = i  # index data
    pelabelanAnggotaSentroid[i][1] = labelSentroid[i]  # label kluster
    
labelSentroidOptimal = ['' for _ in range(centroidOptimal)]
print(pelabelanAnggotaSentroid)
print('Centroid')
for x in range(len(centroid)):
    print(f'Cluster: {x+1}')
    for y in range(len(centroid[0])):
        print(f'| {centroid[x][y]}')
    print()

for x in range(len(labelSentroidOptimal)):
    labelSentroidOptimal[x] = f"c{x+1}"
print(labelSentroidOptimal)

# Hitung a
a = []
for x in range(len(arrayData)):
    label_x = pelabelanAnggotaSentroid[x][1]
    anggota_klaster = [i for i in range(len(arrayData)) if pelabelanAnggotaSentroid[i][1] == label_x and i != x]
    
    total = 0
    for y in anggota_klaster:
        jarak = 0
        for z in range(len(arrayData[0])):
            jarak += (arrayData[x][z] - arrayData[y][z]) ** 2
        total += math.sqrt(jarak)
    
    if len(anggota_klaster) > 0:
        a.append(total / len(anggota_klaster))
    else:
        a.append(0)

# Hitung b
b = []
for x in range(len(arrayData)):
    tampung_b = []
    label_cluster_x = pelabelanAnggotaSentroid[x][1]

    for y in range(len(labelSentroidOptimal)):
        if labelSentroidOptimal[y] != label_cluster_x:
            anggota = []
            for z in range(len(pelabelanAnggotaSentroid)):
                if labelSentroidOptimal[y] == pelabelanAnggotaSentroid[z][1]:
                    anggota.append(pelabelanAnggotaSentroid[z][0])
            
            jarak_total = 0
            for i in range(len(anggota)):
                jarak = 0
                for j in range(len(arrayData[0])):
                    jarak += math.pow(arrayData[x][j] - arrayData[anggota[i]][j], 2)
                jarak_total += math.sqrt(jarak)

            if len(anggota) > 0:
                tampung_b.append(jarak_total / len(anggota))

    # cari nilai b terkecil
    nilaiMin = float('inf')
    for nilai in tampung_b:
        if nilai < nilaiMin:
            nilaiMin = nilai
    b.append(nilaiMin)

s = []
for i in range(len(arrayData)):
    if max(a[i], b[i]) > 0:
        s.append((b[i] - a[i]) / max(a[i], b[i]))
    else:
        s.append(0)

# Rata-rata silhouette score
SCI = sum(s) / len(s)
print(f"Silhouette Coefficient Index (SCI): {SCI:.4f}")


# Impelemntasi DBI 
# mencari jarak untuk setiap setroid

def kombinasi(n):
    kombinasi = []
    for x in range(n):
        for y in range(x+1, n):
            if(x!=y):
                kombinasi.append((x, y))
    
    return [list(p) for p in kombinasi]
# print(kombinasi(4))

# Hitung rata-rata jarak antar anggota klaster ke centroid (sᵢ)
s = []
for i in range(len(labelSentroidOptimal)):
    wadah = []
    for x in range(len(pelabelanAnggotaSentroid)):
        if(labelSentroidOptimal[i] == pelabelanAnggotaSentroid[x][1]):
            jarak = 0
            for y in range(len(arrayData[0])):
                jarak += math.pow(centroid[i][y] - arrayData[pelabelanAnggotaSentroid[x][0]][y], 2)
            wadah.append(math.sqrt(jarak))
    s.append(sum(wadah) / len(wadah) if wadah else 0)

# Hitung nilai Mij (jarak antar centroid)
kombinasi_m = kombinasi(len(labelSentroidOptimal))
mij = []
for i, j in kombinasi_m:
    jarak = 0
    for y in range(len(centroid[0])):
        jarak += math.pow(centroid[i][y] - centroid[j][y], 2)
    mij.append(math.sqrt(jarak))

# Hitung Sij = si + sj
sij = []
for i, j in kombinasi_m:
    sij.append(s[i] + s[j])

# Hitung Rij = Sij / Mij
r = []
for i in range(len(sij)):
    if mij[i] != 0:
        r.append(sij[i] / mij[i])
    else:
        r.append(float('inf'))  # hindari pembagian 0

# Hitung DBI
rij = [-1 for _ in range(len(labelSentroidOptimal))]

for i in range(len(labelSentroidOptimal)):
    max_rij = float('-inf')
    for j in range(len(labelSentroidOptimal)):
        if i != j:
            # cari index (i,j) atau (j,i)
            if [i, j] in kombinasi_m:
                idx = kombinasi_m.index([i, j])
            elif [j, i] in kombinasi_m:
                idx = kombinasi_m.index([j, i])
            else:
                continue
            max_rij = max(max_rij, r[idx])
    rij[i] = max_rij

hasilDBI = sum(rij) / len(rij)
print(f'Hasil DBI : {hasilDBI:.4f}')

# Melakukan PCA ke 2 dimensi untuk visualisasi
# Lakukan PCA ke 2 dimensi
pca = PCA(n_components=2)
X_pca = pca.fit_transform(arrayData)

# Konversi ke DataFrame untuk visualisasi
df_pca = pd.DataFrame({
    'PC1': X_pca[:, 0],
    'PC2': X_pca[:, 1],
    'Cluster': labelSentroid  # dari pelabelanSentroid kamu
})

# Buat scatter plot
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_pca, x='PC1', y='PC2', hue='Cluster', palette='viridis', s=80, edgecolor='black')
plt.title('Visualisasi Clustering dengan PCA (2D)', fontsize=14)
plt.xlabel('Principal Component 1', fontsize=12)
plt.ylabel('Principal Component 2', fontsize=12)
plt.legend(title='Cluster')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
