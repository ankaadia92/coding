import pandas as pd
import streamlit as st

st.set_page_config(layout = "wide") #konfigurasi ukuran halaman web
datasampah = pd.read_excel("D:/Python/datasumbersampah.xlsx") #baca data excelnya

#print(datasampah)

#menambahkan column baru (column Total)
datasampah['total'] = datasampah['rumahtangga'] + datasampah['perkantoran'] + datasampah['pasar'] \
                      + datasampah['perniagaan'] + datasampah ['fasilitaspublik'] + datasampah ['kawasan'] + datasampah ['lainnya']

#print(datasampah)

#Breakdown/dibuat list berdasarkan provinsi
attributProvince = datasampah['provinsi'].unique().tolist() #tolist() itu dikumpulkan ke dalam list
#print(attributProvince)

row1_left, row1_middle, row1_right = st.columns((0.1, 3, 0.1)) #untuk mendesain canvas/margin dalam halaman web
with row1_middle:
    st.title('Jumlah Sampah Provinsi Berdasarkan Sumber Sampah Tahun 2021')
    st.subheader('Streamlit App by [Bosi](https://bosimanurung.com)')
    st.markdown('Sampah merupakan masalah yang dihadapi hampir seluruh Negara di dunia. Tidak hanya di Negara negara berkembang, tetapi juga di\
                 negara - negara maju, sampah selalu menjadi masalah. Rata-rata setiap harinya kota-kota besar di Indonesia menghasilkan puluhan ton sampah.\
                 Pada dashboard berikut akan ditampilkan jumlah sampah (dalam satuan Ton) pada tiap provinsi di Indonesia berdasarkan sumber sampah.')
    st.markdown('Data yang digunakan bersumber dari https://sipsn.menlhk.go.id/sipsn/public/data/sumber')
    #st.markdown untuk caption di websitenya

#sidebar
st.sidebar.markdown("*Isikan parameter berikut :*") #dropdown menu di sidebar
provinsiygdipilih = st.sidebar.selectbox('Pilih Provinsi', attributProvince)
#print(provinsiygdipilih)

#datasampahprovinsi = datasampah.loc[datasampah['provinsi'] == provinsiygdipilih].reset_index(drop = True)
#print(datasampahprovinsi)

datasampahprovinsi = datasampah.loc[datasampah['provinsi'] == provinsiygdipilih].reset_index(drop = True)
#print(datasampahprovinsi)


#untuk menampilkan tabel data sampah di browser
sektorrow2_left, row2_middle, row2_right = st.columns((.1, 3, .1))
with row2_middle:
    st.subheader('Data yang digunakan')     
    st.dataframe(datasampahprovinsi)

#datasampah.loc[datasampah['provinsi']]: menampilkan data sampah di area tertentu
#provinsiyangdipilih: provinsi yang dipilih di sidebar
#reset_index(drop = True): untuk mengurutkan index provinsi

#sektorsumbersampah = ['rumahtangga', 'perkantoran', 'pasar', 'perniagaan', 'fasilitaspublik', 'kawasan', 'lainnya']
#datasampahrumahtangga =  datasampahprovinsi['rumahtangga'].sum()
#print(datasampahrumahtangga)

#variabel sektorsumbersampah: membuat list sumber sampah
#variabel datasampahrumahtangga: menjumlahkan sumber sampah tertentu (contohnya rumah tangga)

sektorsumbersampah = ['rumahtangga', 'perkantoran', 'pasar', 'perniagaan', 'fasilitaspublik', 'kawasan', 'lainnya']
#jumlah = datasampahprovinsi.groupby(['provinsi']).agg(jumlahsampah = ('rumahtangga', pd.Series.sum))
#jumlah['kategorisampah'] = 'Sampah ' + 'rumahtangga'.capitalize()
#print(jumlah)

#agg(jumlahsampah = ('rumahtangga', pd.Series.sum)): agregasi untuk menjumlahkan sampah sektor rumahtangga

#bikin dataframe baru
jumlahsampah = pd.DataFrame(columns=['provinsi', 'jumlahsampah', 'kategorisampah']) #membuat kerangka dataframe dengan 3 kolom
for sektor in sektorsumbersampah:
    jumlah = datasampahprovinsi.groupby(['provinsi']).agg(jumlahsampah = (sektor, pd.Series.sum))
    jumlah['kategorisampah'] = 'Sampah ' + sektor.capitalize()
    jumlah = jumlah.reset_index()
    jumlahsampah = pd.concat([jumlahsampah, jumlah])

jumlahsampah = jumlahsampah.reset_index(drop=True)
#print(jumlahsampah)

#function tampilkan chart (visualisasi data)
import numpy as np #numpy untuk array multidimensi
import matplotlib.pyplot as plt #matplotlib untuk visualisasi data
def plotBar(data, x, y, color):
    #Definisikan kolom yang akan di plot
    x, y = data[x], data[y]

    #Buat 1 Figure and 1 subplot
    fig, ax = plt.subplots()
        
    #Bersihkan terlebih dahulu axes (1 area grafik)
    ax.clear()
    
    #Atur warna
    warna = plt.get_cmap(color)(np.linspace(0.25, 0.85, len(data)))
    
    #Atur ukuran figure (panjang lebar batang grafiknya)
    fig.set_size_inches(10, 6)
    
    #Plot data
    ax.barh(x, y, color = warna)
    
    #Beri label pada sumbu (labelpad = memberi jarak label terhadap grafik)
    ax.set_xlabel(xlabel = 'Jumlah Sampah (Ton)', labelpad = 12)
    
    #Memberi anotasi pada grafik
    j = 0
    for i in plt.gca().patches:
        ax.text(i.get_width()+.5, i.get_y()+.4, str(round(y[j],2)), fontsize = 8, color='blue')
        j = j + 1

        #str(round(y[j],2)): dibulatkan dengan 2 digit desimal
        
    #Hapus garis pada frame bagian kanan dan atas (atau dapat disesuaikan kebutuhan)
    frame = ['right', 'top']
    for i in frame:
        ax.spines[i].set_visible(False)
    
    return fig, ax




#fig1, ax1 = plotBar(data=jumlahsampah, x='kategorisampah', y='jumlahsampah', color='Purples')

#Supaya urut rapih grafiknya:
jumlahsampah = jumlahsampah.sort_values(by = ['jumlahsampah'])
jumlahsampah = jumlahsampah.reset_index(drop=True)
fig1, ax1 = plotBar(data=jumlahsampah, x='kategorisampah', y='jumlahsampah', color='Purples')

row3_left, row3_middle, row3_right = st.columns((0.1, 3, 0.1))
with row3_middle:
    st.subheader('Jumlah Sampah Provinsi {} Tiap Sektor'.format(provinsiygdipilih))
    st.markdown('Berikut Ditampilkan Hasil Visualisasi Dari Data Sampah Provinsi Tersebut:')
    st.pyplot(fig1)

#plt.show()




