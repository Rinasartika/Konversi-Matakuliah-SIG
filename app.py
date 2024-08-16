import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

def color_function(feature):
    nama_desa = feature['properties']['DESA']
    
    if nama_desa == "BAURUNG":
        return '#C0C0C0'  # Light Gray
    elif nama_desa == "BARUGA DHUA":
        return '#FF0000'  # Red
    elif nama_desa == "TANDE":
        return '#FFA500'  # Orange
    elif nama_desa == "BARUGA":
        return '#FFFF00'  # Yellow
    elif nama_desa == "LABUANG":
        return '#ADFF2F'  # Green Yellow
    elif nama_desa == "LEMBANG":
        return '#00FFFF'  # Cyan
    elif nama_desa == "LABUANG UTARA":
        return '#0000FF'  # Blue
    elif nama_desa == "TANDE TIMUR":
        return '#8A2BE2'  # BlueViolet
    elif nama_desa == "BUTTU BARUGA":
        return '#A52A2A'  # Brown
    else:
        return '#FF00FF'  # Magenta

def create_map():
    # Mengambil dua file shapefile
    kec_banggae = gpd.read_file('KecBanggaeTimur\KecBanggaeTimur.shp')
    wisata_majene = gpd.read_file('KecBanggaeTimur\WisataMajene.shp')

    # Mengubah CRS ke EPSG:3857 (Web Mercator)
    kec_banggae = kec_banggae.to_crs(epsg=4236)
    wisata_majene = wisata_majene.to_crs(epsg=4236)

    # Mendapatkan koordinat tengah untuk peta
    center = [kec_banggae.geometry.centroid.y.mean(), kec_banggae.geometry.centroid.x.mean()]

    # Membuat peta folium
    m = folium.Map(location=center, zoom_start=13)

    # Menambahkan layer poligon dari KecBanggae
    folium.GeoJson(
        kec_banggae,
        style_function=lambda feature: {
            'fillColor': color_function(feature),
            'color': 'black',
            'weight': 2,
            'fillOpacity': 0.7
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["DESA"],
            aliases=["Nama Desa: "],
            localize=True
        ),
    ).add_to(m)

    # Menampilkan label berdasarkan desa
    for _, row in kec_banggae.iterrows():
        folium.Marker(
            location=[row.geometry.centroid.y, row.geometry.centroid.x],
            popup=row['DESA'],
            icon=folium.DivIcon(
                html=f"""<div style="font-weight:bold; font-size:10px; color: black;">{row['DESA']}</div>""",
                icon_size=(150, 36),
                icon_anchor=(75, 18)
            )
        ).add_to(m)
    
    # Menambahkan marker dari WisataMajene
    for _, row in wisata_majene.iterrows():
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            popup=row['Name'],
            icon=folium.Icon(color='green')
        ).add_to(m)

    return m

st.title("Kecamatan Banggae Timur, Kabupaten Majene, Provinsi Sulawesi Barat\nMenerapkan peta wisata dan wilayah pada streamlit.")

map = create_map()
st_folium(map, width=700, height=500)
