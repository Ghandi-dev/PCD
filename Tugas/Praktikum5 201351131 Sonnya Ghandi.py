import cv2
import numpy as np

# buka citra
img = cv2.imread('Lenna.png')

# menambahkan variable row, col, ch
# variable tersebut diisi dengan nilai ukuran pixel dari citra yang dibaca
# beserta banyaknya chanel pada citra
row, col, ch = img.shape

# membuat variable kanvas_hsv
# variable ini dipergunakan untuk membuat canvas kosongan yang nanti akan diisi dengan citra berformat hsv
# yang berupa array 3 dimensi yang isinya deretan angka 0 
# np.uint8 sendiri berupa fungsi untuk membatasi besaran nilai elemen-elemen pada array
# dengan maksimal nilainya adalah 8 bit
kanvas_hsv = np.zeros((row, col, 3), np.uint8)

# ubah citra tersebut menjadi HSV Color space.
for i in range (0, row):
  for j in range (0, col):
    b = img[i,j,0]/255
    g = img[i,j,1]/255
    r = img[i,j,2]/255

    vmax = max(r, g, b)
    vmin = min(r, g, b)
    
    # value
    # variable v ini diisi dengan nilai terbesar diantara variable r,g,b
    v = vmax

    # variable ini diperuntukan menyimpan nilai dari rumus v - min(R,G,B)
    # supaya tidak mengulangi menulis rumus yang sama berulang kali
    valv_min = v - vmin

    # saturation
    # variable s ini jika v tidak sama dengan 0 maka diisi dengan variable valv_min dibagi v,
    # jika v sama dengan 0 maka diisi dengan 0
    s = valv_min/v if v != 0 else 0
    
    # hue
    # mengisi variable h dengan beberapa kemungkinan
    # jika nilai v sama dengan r maka h diisi dengan (60*(g-b))/valv_min
    if v == r :
      h = (60*(g-b))/valv_min

    # jika nilai v sama dengan g maka h diisi dengan ((120+60)*(b-r))/valv_min
    elif v == g :
      h = ((120+60)*(b-r))/valv_min
    
    # jika nilai v sama dengan b maka h diisi dengan ((240+60)*(b-r))/valv_min
    elif v == b :
      h = ((240+60)*(b-r))/valv_min
    
    # jika nilai r sama dengan g dan juga sama dengan b maka h diisi dengan 0
    elif r == g and g == b :
      h = 0
    
    # untuk menghindari nilai h itu minus maka jika h kurang dari 0 nilai h diisi dengan nilai h + 360,
    # jika tidak minus maka nilai h adalah h itu sendiri 
    h = h + 360 if h < 0 else h

    kanvas_hsv[i,j,0] = h/2
    kanvas_hsv[i,j,1] = s*255
    kanvas_hsv[i,j,2] = v*255

# split citra menggunakan fungsi cv.split
h,s,v = cv2.split(kanvas_hsv)

# variable penampung untuk total setiap chanel 
total_h = 0
total_s = 0
total_v = 0

# jumlahkan setiap channel hsv menggunakan looping
for i in range (0, row):
  for j in range (0, col):
    # hue
    # variable total_h ditambah dengan nilai elemen h pada baris ke i dan kolom ke j
    total_h += h[i][j]

    # saturation
    # variable total_s ditambah dengan nilai elemen s pada baris ke i dan kolom ke j
    total_s += s[i][j]

    # value
    # variable total_v ditambah dengan nilai elemen v pada baris ke i dan kolom ke j
    total_v += v[i][j]

# menghitung jumlah n pixel pada citra
n = col * row

# rata-rata channel h
# menghitung rata - rata chanel h dengan membagi nilai total pada chanel h dengan total jumlah n pixel
rata_h = total_h / n

# rata-rata channel s
# menghitung rata - rata chanel s dengan membagi nilai total pada chanel s dengan total jumlah n pixel
rata_s = total_s / n

# rata-rata channel v
# menghitung rata - rata chanel v dengan membagi nilai total pada chanel v dengan total jumlah n pixel
rata_v = total_v / n

# lakukan thresholding manual menggunakan looping
for i in range (0, row):
  for j in range (0, col):

    # hue
    # variable kanvas_hsv chanel hue pada baris ke i dan kolom ke j
    # diisi dengan 0 jika nilai kanvas_hsv chanel hue pada baris ke i dan kolom ke j < dari rata_h
    # jika tidak diisi dengan 255
    kanvas_hsv[i,j,0] = 0 if kanvas_hsv[i,j,0] < rata_h else 255

    # saturation
    # variable kanvas_hsv chanel saturation pada baris ke i dan kolom ke j
    # diisi dengan 0 jika nilai kanvas_hsv chanel saturation pada baris ke i dan kolom ke j < dari rata_s
    # jika tidak diisi dengan 255
    kanvas_hsv[i,j,1] = 0 if kanvas_hsv[i,j,1] < rata_s else 255

    # value
    # variable kanvas_hsv chanel value pada baris ke i dan kolom ke j
    # diisi dengan 0 jika nilai kanvas_hsv chanel value pada baris ke i dan kolom ke j < dari rata_v
    # jika tidak diisi dengan 255
    kanvas_hsv[i,j,2] = 0 if kanvas_hsv[i,j,2] < rata_v else 255

# menyimpan citra chanel hue kedalam file dengan nama gambar-hue.jpg
cv2.imwrite("gambar-hue.jpg",kanvas_hsv[:,:,0])
# menyimpan citra chanel saturation kedalam file dengan nama gambar-saturation.jpg
cv2.imwrite("gambar-saturation.jpg",kanvas_hsv[:,:,1])
# menyimpan citra chanel value kedalam file dengan nama gambar-value.jpg
cv2.imwrite("gambar-value.jpg",kanvas_hsv[:,:,2])