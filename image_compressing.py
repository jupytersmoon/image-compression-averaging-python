import numpy as np                  # untuk mengubah foto ke array
import PIL.Image                    # untuk membaca foto
from tkinter.filedialog import *    # untuk upload/save foto ke directory lokal

## Definisi fungsi
# Fungsi memotong array foto menjadi 2 dimensi
def cut(m, mode:str):
  baris = len(m)
  kolom = len(m[0])

  if mode == 'rgb':
    r = [[0 for j in range(kolom)] for i in range(baris)]
    g = [[0 for j in range(kolom)] for i in range(baris)]
    b = [[0 for j in range(kolom)] for i in range(baris)]

    for x in range(baris):
      for l in range(kolom):
        for i in range(3):
          if i == 0:
            r[x][l] = m[x][l][i]
          elif i == 1:
            g[x][l] = m[x][l][i]
          else:
            b[x][l] = m[x][l][i]

    re = [r,g,b]
  elif mode == 'gs':
    re = m
  return re

# Fungsi resize rata-rata untuk mengecilkan dimensi
def mean(m, f:int):
  # pixel dari array m yang akan direratakan berukuran f x f
  baris = len(m)//f
  kolom = len(m[0])//f

  re = [[0 for j in range(kolom)] for i in range(baris)]

  q = 0
  for i in range(baris):
    k = 0
    for j in range(kolom):
      jum = 0
      for x in range(f):
        for l in range(f):
          jum += m[x+q][l+k]
      jum = jum / (f**2) # rata-rata nilai dari tiap f x f pixel
      jum = round(jum + 0.1) # ditambah 0.1 karena fungsi round() python bulat ke bawah untuk x.5
      re[i][j] = jum # nilai f x f disimpan di 1 posisi matriks re
      k += f
    q += f

  return re

# Fungsi warna rata-rata jika ingin resize tanpa mengecilkan dimensi
def meancol(m, f:int):
  # pixel dari array m yang akan direratakan berukuran f x f
  baris = len(m)
  kolom = len(m[0])

  re = [[0 for j in range(kolom)] for i in range(baris)]

  # Mengisi kolom dan baris re yang dapat dibentuk menjadi f x f
  # dengan nilai rata-ratanya
  q = 0
  for i in range(baris//f):
    k = 0
    for j in range(kolom//f):
      jum = 0
      for x in range(f):
        for l in range(f):
          jum += m[x+q][l+k]
      jum = jum / (f**2) # rata-rata nilai dari tiap f x f pixel
      jum = round(jum + 0.1)  # ditambah 0.1 karena fungsi round() python bulat ke bawah untuk x.5
      for x in range(f):
        for l in range(f):
          re[x+q][l+k] = jum  # nilai f x f disimpan di f x f posisi matriks re
      k += f
    q += f

  # Mengisi kolom dan baris sisa dengan nilai awalnya
  if baris%f != 0:
    for i in range(1, (baris%f)+1):
      for j in range(kolom):
        re[baris - i][j] = m[baris - i][j]

  if kolom%f != 0:
    for i in range(baris):
      for j in range(1, (kolom%f)+1):
        re[i][kolom - j] = m[i][kolom - j]

  return re

# Fungsi kompresi gambar
def compress(m, mode:str, rem, rec):
  if mode == 'rgb':
    row = len(m[0])
    column = len(m[0][0])

    # Matriks nol untuk menyimpan hasil kompresi
    comp = [[[0 for j in range(column)] for i in range(row)] for x in range(3)]

    # Manipulasi array pada foto dengan metode Average
    # Dimensi akan dikompresi dulu sebelum pererataan warna
    for i in range(3):
      if rem > 1: # rem = 1 berarti tidak mengubah dimensi gambar
        comp[i] = mean(m[i], rem)
      else:
        comp[i] = m[i]

      if rec > 1: # rec = 1 berarti tidak mereratakan warna gambar
        comp[i] = meancol(comp[i], rec)

    # Mengubah isi array menjadi type data "uint8" (type data image)
    a = PIL.Image.fromarray(np.asarray(comp[0], dtype="uint8"))
    b = PIL.Image.fromarray(np.asarray(comp[1], dtype="uint8"))
    c = PIL.Image.fromarray(np.asarray(comp[2], dtype="uint8"))

    # Menggabungkan kembali array RGB menjadi 1
    finish = PIL.Image.merge('RGB', (a, b, c))
  elif mode == 'gs':
    # Manipulasi array pada foto dengan metode Average
    if rem > 1: # rem = 1 berarti tidak mengubah dimensi gambar
      comp = mean(m, rem)
    else:
      comp = m

    if rec > 1: # rec = 1 berarti tidak mereratakan warna gambar
      comp = meancol(comp, rec)

    # Mengubah isi array menjadi type data "uint8" (type data image)
    finish = PIL.Image.fromarray(np.asarray(comp, dtype="uint8"))

  return finish


#### PROGRAM KOMPRESI LOSSY JPEG dan PNG DENGAN METODE AVERAGING
# rm = resize mean : Int (ukuran pengecilan dimensi)
# rc = resize color : Int (ukuran pererataan warna)

# Import foto
print("Pilih file foto (.JPEG atau .PNG) Anda yang ingin dikompresi.")
file_path = askopenfilename()
im = PIL.Image.open(file_path)

# Memilih ukuran kompresi foto
print("Masukkan angka antara 1 - 4. 1 untuk tidak memperkecil, 4 untuk sangat memperkecil.")
print("Ukuran yang disarankan adalah 2 dan 2.")
print("Pastikan ukuran kompresi sesuai dengan dimensi gambar untuk hasil kompresi yang baik!")
rm, rc = 0, 0
while rm < 1 or rm > 4 or rc < 1 or rc > 4:
  rm = int(input("Memperkecil dimensi gambar sebesar: "))
  rc = int(input("Memperkecil warna gambar sebesar: "))

print("Tergantung ukuran file foto Anda, waktu kompresi akan bervariasi. Harap menunggu...")

## MELAKUKAN KOMPRESI FOTO

# Mengubah data pixel gambar menjadi array numpy
data = np.array(im)

# Mengecek dimensi array foto apakah 3 (RGB) atau 2 (Grayscale)
if data.ndim == 2:
  mode = 'gs' # Grayscale
else:
  mode = 'rgb' # RGB

# Memotong array foto sesuai mode
resize = cut(data, mode)
# Kompresi array foto sesuai mode
finalPhoto = compress(resize, mode, rm, rc)

# Menyimpan file gambar yang telah dikompres
print("Ketik 1 untuk menyimpan gambar dalam format .JPG")
print("Ketik 2 untuk menyimpan gambar dalam format .PNG")
fileType = int(input("Disimpan dalam format: "))
save_path = asksaveasfilename()
if fileType == 1:
  finalPhoto.save(save_path + "_compressed.JPG")
elif fileType == 2:
  finalPhoto.save(save_path + "_compressed.PNG")
else:
  print("Input tidak sesuai")
