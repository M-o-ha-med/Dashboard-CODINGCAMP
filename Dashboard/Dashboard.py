import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

data = pd.read_csv('Dashboard/data_cleaned.csv')


def show_metrics():
    col1,col2 = st.columns(2)
    
    with col1:
        st.metric(label="Total Sampel", value=data['No'].count())
    with col2:
        st.metric(label="Kota ", value=data['station'][0])

def show_clustered_barchart(start=2013 , end=2017):
    fig , axes = plt.subplots(1,2, figsize=(20,10))
    
    filtered_data_by_year = data[(data['year'] >=start) & (data['year'] <=end)]

    data_melted_PPB = pd.melt(filtered_data_by_year, id_vars=['year'], value_vars=['PM2.5', 'PM10' , 'SO2' , 'O3' , 'NO2'] , var_name='Pollutant', value_name='Consentration (µg/m³)')
    data_melted_PPM = pd.melt(filtered_data_by_year, id_vars=['year'], value_vars=['CO'] , var_name='Pollutant', value_name='Consentration (ppm)')


    data_melted_PPB_mean = data_melted_PPB.groupby(['year' , 'Pollutant'])['Consentration (µg/m³)'].mean().reset_index().sort_values(by="Consentration (µg/m³)", ascending=False)
    data_melted_PPM_mean = data_melted_PPM.groupby(['year' , 'Pollutant'])['Consentration (ppm)'].mean().reset_index().sort_values(by="Consentration (ppm)", ascending=False)

    sns.barplot(data=data_melted_PPB_mean , x='year' , y='Consentration (µg/m³)' , hue='Pollutant', ax=axes[0])
    sns.barplot(data=data_melted_PPM_mean , x='year' , y='Consentration (ppm)' , hue='Pollutant', ax=axes[1] , palette="viridis")

    axes[0].legend(loc='upper left', bbox_to_anchor=(1, 1),title="Pollutant")
    axes[1].legend(loc='upper left', bbox_to_anchor=(1, 1),title="Pollutant")

    fig.suptitle("Pollution Trend in 2013-2017", fontsize=16)
    fig.tight_layout()

    st.pyplot(fig)


def show_line_chart():
    fig, axes = plt.subplots(1,2,figsize=(20, 10))
    data_filtered = data[(data['month'] >= 1)]
    sns.lineplot(data=data_filtered , x='month', y= 'PM2.5' ,ax = axes[0] , marker="o", label='PM2.5')
    sns.lineplot(data=data_filtered , x='month', y= 'PM10' ,ax = axes[0] , marker="o", label='PM10')
    sns.lineplot(data=data_filtered , x='month', y= 'SO2' ,ax = axes[0] , marker="o", label='SO2')
    sns.lineplot(data=data_filtered , x='month', y= 'O3' ,ax = axes[0] , marker="o", label='O3')
    sns.lineplot(data=data_filtered , x='month', y= 'NO2' ,ax = axes[0] , marker="o", label='NO2')
    sns.lineplot(data=data_filtered , x='month', y= 'CO' ,ax = axes[1] , marker="o", label='CO')

    fig.suptitle('Tren Polusi dari Dari Bulan Januari - Desember')
    axes[0].set_xlabel('Month')
    axes[0].set_ylabel('Consentration (µg/m³)')

    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Consentration (PPM)')

    axes[0].grid(True)
    axes[1].grid(True)

    axes[0].legend(loc='upper left', bbox_to_anchor=(1, 1),title="Pollutant")
    axes[1].legend(loc='upper left', bbox_to_anchor=(1, 1),title="Pollutant")

    axes[1].set_ylim(0, data_filtered['CO'].max() * 1.1)

    plt.tight_layout()
    plt.subplots_adjust(hspace=2.0)
    st.pyplot(fig)


def show_heatmap():
    corr_matrix = data[['PM2.5','PM10','SO2','NO2','CO','O3','TEMP','PRES','DEWP','RAIN','WSPM']].corr()
    fig = plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation between Pollutant Material and Other Variable ')
    st.pyplot(fig)

def show_pie_chart(pollutant="PM2.5"):
    pollutant_counts = data[f'{pollutant}_binned'].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))

    colors = {
        "Rendah": "#4CAF50",       
        "Menengah": "#FF9800",     
        "Tinggi": "#F44336",       
        "Sangat Tinggi": "#B71C1C",
        "Ekstrim": "#7F0000"      
    }

    # Ambil warna sesuai kategori yang ada
    selected_colors = [colors[label] for label in pollutant_counts.index]

    # Buat pie chart
    ax.pie( pollutant_counts, labels= pollutant_counts.index, autopct='%1.1f%%', startangle=140, colors=selected_colors)

    # Tambahkan judul
    ax.set_title(f'Distribusi dari {pollutant}')

    # Tampilkan plot
    st.pyplot(fig)


def show_barcharts():
    fig , axes = plt.subplots(2,3, figsize=(15,10))
    sns.countplot(data=data, x='PM2.5_binned', ax=axes[0, 0] , order=['Rendah', 'Menengah', 'Tinggi', 'Sangat Tinggi', 'Ekstrim'])
    sns.countplot(data=data, x='PM10_binned', ax=axes[0, 1], order=['Rendah', 'Menengah', 'Tinggi', 'Sangat Tinggi', 'Ekstrim'])
    sns.countplot(data=data, x='SO2_binned', ax=axes[0, 2], order=['Rendah', 'Menengah', 'Tinggi', 'Sangat Tinggi', 'Ekstrim'])
    sns.countplot(data=data, x='O3_binned', ax=axes[1, 0], order=['Rendah', 'Menengah', 'Tinggi', 'Sangat Tinggi', 'Ekstrim'])
    sns.countplot(data=data, x='NO2_binned', ax=axes[1, 1], order=['Rendah', 'Menengah', 'Tinggi', 'Sangat Tinggi', 'Ekstrim'])
    sns.countplot(data=data, x='CO_binned', ax=axes[1, 2], order=['Rendah', 'Menengah', 'Tinggi', 'Sangat Tinggi', 'Ekstrim'])
    for column in axes:
      for row in column:
        row.set_ylabel('Jumlah kasus')
        row.set_ylim(0, data['SO2_binned'].count() * 1.1)
    
    fig.suptitle('Distribusi dari polutan berdasarkan kategori')
    plt.tight_layout()
    st.pyplot(fig)

st.title('Guangyuang Air Quality  Analysis')


show_metrics()

#Buat bikin sidebar
with st.sidebar:
    
    st.markdown('# Parameters')
    
    start , end = st.slider(
        label='Masukkan nilai tahun dengan slider dibawah ini',
        min_value=2013, max_value=2017, value=(2013, 2017)
    )
    
    
    pollutant = st.selectbox(
    label="Zat Polutan",
    options=('PM2.5' , 'PM10' , 'SO2' , 'NO2' , 'O3' , 'CO')
    )
    
    st.subheader('Dianalisa oleh Mohamed')



st.header('Distribusi Dari Konsentrasi polutan dari tahun 2013 - 2017')
show_clustered_barchart(start,end)

st.header('Tren dari konsentrasi polutan dari tahun 2013 - 2017 berdasarkan bulan')
show_line_chart()

st.header('Korelasi antara data polutan dengan data lain ')
show_heatmap()

st.header('Analisa Lanjutan : Hasil Klustering dari tingkatan polutan')

st.subheader('Jumlah kasus')
show_barcharts()

st.subheader('Persentase Berdasarkan kategori')
show_pie_chart(pollutant)

    


st.markdown(''' 
### Insight:
- Penggunaan teknik clustering (binning) bertujuan untuk memetakan data polusi yang ada di dalam kota guanyuang untuk melihat apakah tingkat polusi yang ada di kota tersebut sesuai dengan standar yang ditetapkan oleh World Health Organization atau tidak.

- Dari hasil analisa yang dilakukan, polutan dengan kasus polusi berkonsentrasi **Rendah** terbanyak adalah polutan SO2 dengan jumlah kasus pada kategori **Rendah** sebesar 32,002 kasus , dan polutan dengan kasus polusi berkonsentrasi **Rendah** terendah adalah polutan PM10 dengan jumlah kasus  sebanyak 10,848 kasus.

- polutan dengan kasus polusi berkonsentrasi **Menengah** terbanyak adalah polutan NO2 dengan jumlah kasus pada kategori **Menengah** sebesar 13,531 kasus , dan polutan dengan kasus polusi berkonsentrasi **Menengah** terendah adalah polutan SO2 dengan jumlah kasus sebanyak  3,062 kasus.

- polutan dengan kasus polusi berkonsentrasi **Tinggi** terbanyak adalah polutan PM10 dengan jumlah kasus pada kategori **Tinggi** sebesar 6,895 kasus , dan polutan dengan kasus polusi berkonsentrasi **Tinggi** terendah adalah polutan SO2 dengan jumlah kasus sebanyak 0 kasus.

- polutan dengan kasus polusi berkonsentrasi **Ekstrim** terbanyak adalah polutan SO2 dengan jumlah kasus pada kategori **Ekstrim** sebesar 28,477 kasus , dan polutan dengan kasus polusi berkonsentrasi **Ekstrim** terendah adalah polutan SO2, NO2 , dan O3 dengan jumlah kasus sebanyak 0 kasus.

- polutan dengan kasus polusi berkonsentrasi **Sangat tinggi** terbanyak adalah polutan CO dengan jumlah kasus pada kategori **Sangat tinggi** sebesar 6,066 kasus , dan polutan dengan kasus polusi berkonsentrasi **Sangat tinggi** terendah adalah polutan SO2 dengan jumlah kasus sebanyak 0 kasus.
 ''')


st.markdown(
    '''
    ###  Conclusion

    1. Tren polusi dari tahun 2013 sampai 2017 cenderung naik turun, dimana dari visualisasi yang telah dibuat diperlihatkan bahwa pada tahun 2013-2014 konsentrasi rata-rata polutan seperti PM10 , PM2.5 , NO2 , dan O3 mengalami sedikit peningkatan sebanyak 4.85% untuk PM10 , 5.67% untuk PM2.5 , 9.12% , 0.86% sedangkan polutan SO2 mengalami penurunan sebanyak 2,32%. Pada tahun 2014-2015 konsentrasi polutan mengalami sedikit penurunan dan pada tahun 2016-2017 terdapat kenaikan dari konsentrasi dari setiap polutan walau tidak secara signifikan.
    
    1. Polutan yang mengalami peningkatan konsentrasi dalam 12 bulan terakhir di rentang tahun 2013-2017 adalah polutan seperti seperti PM10 , PM2.5 , NO2 , dan O3 berdasarkan data dari tahun 2013-2014 sedangkan polutan seperti SO2 mengalami penurunan.
    
    1. korelasi antara polutan dan variabel lain cenderung memiliki korelasi yang rendah , dilihat dari heatmap bahwa hanya polutan O3 saja yang memiliki korelasi yang tinggi dengan variabel lain apabila dibandingkan dengan polutan lainnya. variabel TEMP , DEWP , WSPM  merupakan variabel yang memiliki korelasi yang cukup baik dengan polutan O3. Dari heatmap dapat dilihat bahwa justru polutan memiliki korelasi yang cenderung tinggi antar satu sama lain sehingga didapat kesimpulan bahwa  setiap polutan memiliki cukup pengaruh terhadap polutan lainnya.
    '''
)
