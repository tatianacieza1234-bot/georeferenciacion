import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Visor de Coordenadas")
st.write("Sube tu archivo Excel o CSV para visualizar las ubicaciones en el mapa")

# SUBIR ARCHIVO
archivo = st.file_uploader("Selecciona un archivo", type=["xlsx", "csv"])

if archivo is not None:

    nombre = archivo.name.lower()

    # LEER ARCHIVO
    if nombre.endswith(".csv"):
        df = pd.read_csv(archivo, encoding="utf-8", dtype=str)
    else:
        df = pd.read_excel(archivo, dtype=str)

    # LIMPIAR COLUMNAS
    df.columns = (
        df.columns
        .str.replace('\ufeff', '')
        .str.replace('\xa0', ' ')
        .str.strip()
        .str.lower()
    )

    # CONVERTIR NUMÉRICOS
    df["latitud"] = pd.to_numeric(df.get("latitud"), errors="coerce")
    df["longitud"] = pd.to_numeric(df.get("longitud"), errors="coerce")

    st.subheader("Datos cargados:")
    st.dataframe(df)

    # MOSTRAR CADA REGISTRO
    for i, row in df.iterrows():
        with st.expander(f"📍 {row['descripcion']}"):
            
            # SELECTOR DE TIPO DE MAPA (ANTES DE LAS COLUMNAS)
            tipo_mapa = st.selectbox(
                "Selecciona el tipo de mapa:",
                ["🗺️ Google Híbrido", "🛰️ Google Satélite", "🚗 Google Calles", "📍 CartoDB Positron"],
                key=f"tipo_mapa_{i}"
            )
            
            col1, col2 = st.columns([1, 2])

            with col1:
                st.write(f"**Latitud:** {row['latitud']}")
                st.write(f"**Longitud:** {row['longitud']}")

            with col2:
                lat = float(row["latitud"])
                lon = float(row["longitud"])
                
                # CREAR MAPA SEGÚN LA SELECCIÓN
                mapa = folium.Map(
                    location=[lat, lon],
                    zoom_start=18,
                    max_zoom=22,
                    min_zoom=1,
                    control_scale=True,
                    tiles=None,
                    zoom_control=True,
                    scrollWheelZoom=True
                )

                # AGREGAR LA CAPA SELECCIONADA
                if tipo_mapa == "🗺️ Google Híbrido":
                    folium.TileLayer(
                        tiles="https://{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                        attr="Google Hybrid",
                        name="Google Híbrido",
                        subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                        max_zoom=22
                    ).add_to(mapa)
                
                elif tipo_mapa == "🛰️ Google Satélite":
                    folium.TileLayer(
                        tiles="https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
                        attr="Google Satellite",
                        name="Google Satélite",
                        subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                        max_zoom=22
                    ).add_to(mapa)
                
                elif tipo_mapa == "🚗 Google Calles":
                    folium.TileLayer(
                        tiles="https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                        attr="Google Streets",
                        name="Google Calles",
                        subdomains=['mt0', 'mt1', 'mt2', 'mt3'],
                        max_zoom=22
                    ).add_to(mapa)
                
                else:  # CartoDB Positron
                    folium.TileLayer(
                        tiles="CartoDB Positron",
                        name="CartoDB Positron"
                    ).add_to(mapa)

                # MARCADOR
                folium.Marker(
                    location=[lat, lon],
                    popup=row["descripcion"],
                    tooltip="Ver ubicación",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(mapa)

                # MOSTRAR MAPA
                st_folium(
                    mapa, 
                    width=420, 
                    height=420,
                    returned_objects=[],
                    key=f"mapa_display_{i}_{tipo_mapa}"
                )

else:
    st.info("⬆️ Sube un archivo para comenzar")