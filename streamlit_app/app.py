import os
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import plotly.express as px


# --- Funciones para crear mapas folium ---

def crear_mapa_oportunidades(df, nombre_archivo="mapa_oportunidad_valencia.html"):
    centro_valencia = [39.4699, -0.3763]
    mapa = folium.Map(location=centro_valencia, zoom_start=13)
    marker_cluster = MarkerCluster().add_to(mapa)

    for _, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        price = row.get('price', 'N/A')
        roi = row.get('ROI (%)', 'N/A')

        if pd.notna(lat) and pd.notna(lon):
            popup_text = f"""
            <b>Precio:</b> €{price}<br>
            <b>ROI Bruto:</b> {roi}%
            """
            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                icon=folium.Icon(color='blue', icon='home')
            ).add_to(marker_cluster)

    mapa.save(nombre_archivo)


def crear_mapa_precios_valencia(df, nombre_archivo="mapa_precio_valencia.html"):
    centro_valencia = [39.4699, -0.3763]
    mapa = folium.Map(location=centro_valencia, zoom_start=13)

    heat_data = []

    for _, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        price = row.get('price')
        if pd.notna(lat) and pd.notna(lon) and pd.notna(price):
            heat_data.append([lat, lon, price])

    if heat_data:
        HeatMap(heat_data, radius=10, blur=15, max_zoom=13).add_to(mapa)

    mapa.save(nombre_archivo)


def crear_mapa_propiedades_valencia(df, nombre_archivo="mapa_propiedades_valencia.html"):
    centro_valencia = [39.4699, -0.3763]
    mapa = folium.Map(location=centro_valencia, zoom_start=13)
    marker_cluster = MarkerCluster().add_to(mapa)

    for _, row in df.iterrows():
        lat = row.get('latitude')
        lon = row.get('longitude')
        price = row.get('price', 'N/A')
        room_type = row.get('room_type', 'N/A')

        if pd.notna(lat) and pd.notna(lon):
            popup_text = f"""
            <b>Precio:</b> €{price}<br>
            <b>Tipo:</b> {room_type}
            """
            folium.Marker(
                location=[lat, lon],
                popup=popup_text,
                icon=folium.Icon(color='green', icon='home')
            ).add_to(marker_cluster)

    mapa.save(nombre_archivo)


def crear_mapa_roi_por_tipo(df, ruta_guardado="../docs/valencia_roi_by_type_map.html"):
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

    centro_valencia = [39.4699, -0.3763]
    mapa = folium.Map(location=centro_valencia, zoom_start=13)

    colores = {
        "Entire home/apt": "blue",
        "Private room": "green",
        "Shared room": "red",
        "Hotel room": "purple"
    }

    for _, row in df.iterrows():
        lat = row.get("latitude")
        lon = row.get("longitude")
        roi = row.get("ROI (%)")
        tipo = row.get("room_type", "Otro")

        if pd.notna(lat) and pd.notna(lon) and pd.notna(roi):
            popup = f"<b>Tipo:</b> {tipo}<br><b>ROI:</b> {roi:.2f}%"
            color = colores.get(tipo, "gray")
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                popup=popup,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(mapa)

    mapa.save(ruta_guardado)
    print(f"Mapa ROI por tipo guardado en {ruta_guardado}")


# --- Funciones para mostrar mapas e imágenes en Streamlit ---

def display_interactive_map(path_html, titulo=None):
    if not os.path.exists(path_html):
        st.warning(f"No se pudo encontrar el archivo: {path_html}")
        return
    with open(path_html, "r", encoding="utf-8") as f:
        html = f.read()
    if titulo:
        st.markdown(f"#### {titulo}")
    components.html(html, height=600, scrolling=True)


def display_image(path, caption=None):
    if not os.path.exists(path):
        st.warning(f"No se pudo encontrar la imagen: {path}")
        return
    img = Image.open(path)
    st.image(img, caption=caption, use_column_width=True)


# --- Funciones adicionales de análisis y visualización ---

def crear_heatmap_ocupacion_valencia(df, ruta_guardado="../img/valencia_heatmap_ocupacion.png"):
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

    df_valencia = df[df['city'].str.lower() == 'valencia'].dropna(subset=['latitude', 'longitude', 'estimated_occupancy_l365d'])

    if df_valencia.empty:
        print("No hay datos para Valencia con ocupación estimada.")
        return

    plt.figure(figsize=(10,8))
    sns.kdeplot(
        x=df_valencia['longitude'],
        y=df_valencia['latitude'],
        weights=df_valencia['estimated_occupancy_l365d'],
        fill=True,
        cmap="Reds",
        bw_adjust=0.5,
        thresh=0.1
    )
    plt.title("Heatmap de Ocupación Estimada en Valencia")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")

    plt.savefig(ruta_guardado)
    plt.close()
    print(f"Heatmap guardado en {ruta_guardado}")


def crear_evolucion_reseñas(df, ruta_guardado):
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

    df_valencia = df[df['city'].str.lower() == 'valencia'].copy()

    if 'last_review' not in df_valencia.columns:
        print("No se encontró columna 'last_review' para evolución de reseñas")
        return

    df_valencia = df_valencia.dropna(subset=['last_review', 'number_of_reviews'])
    df_valencia['last_review'] = pd.to_datetime(df_valencia['last_review'], errors='coerce')
    df_valencia = df_valencia.dropna(subset=['last_review'])

    df_valencia['year_month'] = df_valencia['last_review'].dt.to_period('M')
    resumen = df_valencia.groupby('year_month')['number_of_reviews'].sum()

    if resumen.empty:
        print("No hay datos de reseñas para crear evolución")
        return

    plt.figure(figsize=(12,6))
    resumen.plot(kind='line', marker='o')
    plt.title('Evolución mensual de número de reseñas en Valencia')
    plt.xlabel('Mes')
    plt.ylabel('Número de reseñas')
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(ruta_guardado)
    plt.close()
    print(f"Imagen de evolución de reseñas guardada en {ruta_guardado}")


def mostrar_matriz_correlacion(df, columnas):
    st.markdown("#### Matriz de correlación de variables de inversión")
    corr = df[columnas].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)


def mostrar_relacion_precio_calificacion(df):
    st.markdown("#### Relación entre precio y calificación")
    if 'price' in df.columns and 'review_scores_rating' in df.columns:
        fig = px.scatter(
            df,
            x='price',
            y='review_scores_rating',
            color='room_type' if 'room_type' in df.columns else None,
            title='Relación entre precio y calificación',
            labels={'price': 'Precio (€)', 'review_scores_rating': 'Calificación (0-100)', 'room_type': 'Tipo de habitación'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos suficientes de precio y calificación.")


def mostrar_mapa_perfiles(df):
    st.markdown("#### Mapa de anuncios")
    if 'latitude' in df.columns and 'longitude' in df.columns:
        st.map(df[['latitude', 'longitude']].dropna(), key="mapa_anuncios")
    else:
        st.info("No hay datos de localización para mostrar el mapa.")


def mostrar_mapa_correlaciones(df):
    if not {'latitude', 'longitude', 'Net ROI (%)'}.issubset(df.columns):
        st.warning("Faltan columnas necesarias para generar el mapa de correlaciones.")
        return

    df_plot = df.dropna(subset=['latitude', 'longitude', 'Net ROI (%)']).copy()

    if df_plot.empty:
        st.warning("No hay datos suficientes para mostrar el mapa de correlaciones.")
        return

    min_roi = df_plot['Net ROI (%)'].min()
    if min_roi < 0:
        df_plot['size_positive'] = df_plot['Net ROI (%)'] + abs(min_roi) + 1  # hacer todos > 0
    else:
        df_plot['size_positive'] = df_plot['Net ROI (%)']

    fig = px.scatter_mapbox(
        df_plot,
        lat='latitude',
        lon='longitude',
        color='Net ROI (%)',
        size='size_positive',
        color_continuous_scale='Viridis',
        size_max=15,
        zoom=12,
        mapbox_style='open-street-map',
        title="Mapa de Correlaciones: ROI Neto por ubicación"
    )

    st.plotly_chart(fig, use_container_width=True)


# --- Función para crear mapa de barrios ejemplo ---

def crear_mapa_valencia():
    m = folium.Map(location=[39.4699, -0.3763], zoom_start=13)

    barrios = {
        "Ciutat Universitaria": (39.4811, -0.3450),
        "Penya-Roja": (39.4567, -0.3487),
        "Cabanyal": (39.4702, -0.3235)
    }

    for nombre, coords in barrios.items():
        folium.Marker(coords, tooltip=nombre).add_to(m)

    m.save("mapa_completo_valencia.html")


# --- Ejemplo de uso ---

if __name__ == "__main__":
    crear_mapa_valencia()
