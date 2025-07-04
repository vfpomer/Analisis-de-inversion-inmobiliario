import os
import folium
from folium.plugins import MarkerCluster, HeatMap
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st





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


def crear_mapa_calor_valencia(df, nombre_archivo="mapa_calor_precios_valencia.html"):
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

import os
import matplotlib.pyplot as plt
import seaborn as sns

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

def crear_mapa_precios_valencia(df, ruta_guardado="../docs/mapa_precio_valencia.html"):
    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)

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
        HeatMap(heat_data, radius=15, blur=20, max_zoom=13).add_to(mapa)

    mapa.save(ruta_guardado)
    print(f"Mapa de precios guardado en {ruta_guardado}")

import streamlit.components.v1 as components
import streamlit as st


def display_interactive_map(path_html, titulo):
    st.markdown(f"#### {titulo}")
    try:
        with open(path_html, "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=600, scrolling=True)
    except FileNotFoundError:
        st.warning(f"No se pudo encontrar el archivo: {path_html}")

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

import streamlit as st
from PIL import Image

# Función para mostrar mapas interactivos

def display_interactive_map(path, title=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            if title:
                st.markdown(f"**{title}**")
            st.components.v1.html(html_content, height=600)
    except FileNotFoundError:
        st.warning(f"No se pudo encontrar el archivo: {path}")

# Función para mostrar imágenes

from PIL import Image

# Función para mostrar mapas interactivos
def display_interactive_map(path, title=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            if title:
                st.markdown(f"**{title}**")
            st.components.v1.html(html_content, height=600)
    except FileNotFoundError:
        st.warning(f"No se pudo encontrar el archivo: {path}")

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

# Cargar datos
@st.cache_data
def load_data(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"No se pudo encontrar el archivo de datos: {path}")
        return pd.DataFrame()  # Devuelve un df vacío si no encuentra archivo

df_ciudad = load_data("data/Valencia_limpio.csv")

# Función para mostrar mapas interactivos
def display_interactive_map(path, title=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            if title:
                st.markdown(f"**{title}**")
            st.components.v1.html(html_content, height=600)
    except FileNotFoundError:
        st.warning(f"No se pudo encontrar el archivo: {path}")

# Función para mostrar imágenes
def display_image(path, caption=None):
    try:
        image = Image.open(path)
        st.image(image, caption=caption, use_column_width=True)
    except FileNotFoundError:
        st.warning(f"No se pudo encontrar la imagen: {path}")

    if not df_ciudad.empty:
        # ROI neto por barrio (Valencia)
        if 'Net ROI (%)' in df_ciudad.columns and 'neighbourhood' in df_ciudad.columns:
            roi_barrio = df_ciudad.groupby('neighbourhood')['Net ROI (%)'].mean().sort_values(ascending=False).head(15)
            if not roi_barrio.empty:
                fig_roi = px.bar(
                    roi_barrio,
                    x=roi_barrio.values,
                    y=roi_barrio.index,
                    orientation='h',
                    labels={'x': 'ROI Neto (%)', 'y': 'neighbourhood'},
                    title='Top 15 barrios por ROI Neto (%)'
                )
                st.plotly_chart(fig_roi, use_container_width=True, key="plotly_280")
            else:
                st.info("No hay datos de ROI Neto para mostrar.")
        else:
            st.info("No hay columnas de ROI Neto o barrio en los datos.")

        # ROI bruto por barrio (Valencia)
        if 'ROI (%)' in df_ciudad.columns and 'neighbourhood' in df_ciudad.columns:
            roi_barrio_bruto = df_ciudad.groupby('neighbourhood')['ROI (%)'].mean().sort_values(ascending=False).head(15)
            if not roi_barrio_bruto.empty:
                fig_roi_bruto = px.bar(
                    roi_barrio_bruto,
                    x=roi_barrio_bruto.values,
                    y=roi_barrio_bruto.index,
                    orientation='h',
                    labels={'x': 'ROI Bruto (%)', 'y': 'neighbourhood'},
                    title='Top 15 barrios por ROI Bruto (%)'
                )
                st.plotly_chart(fig_roi_bruto, use_container_width=True, key="plotly_298")
            else:
                st.info("No hay datos de ROI Bruto para mostrar.")
        else:
            st.info("No hay columnas de ROI Bruto o barrio en los datos.")

        # Mapa de rentabilidad
        st.markdown("#### Mapa de Rentabilidad")
        try:
            display_interactive_map("docs/valencia_roi_by_type_map.html", "Mapa ROI por Tipo en Valencia")
        except FileNotFoundError:
            try:
                display_interactive_map("docs/valencia_breakeven_map.html", "Mapa de Punto de Equilibrio")
            except FileNotFoundError:
                st.warning("No se pudo cargar el mapa de rentabilidad de Valencia.")
    else:
        st.info("No hay datos para mostrar en esta pestaña.")

def crear_evolucion_reseñas(df, ruta_guardado):
    os.makedirs(os.path.dirname(ruta_guardado), exist_ok=True)
    
    # Filtrar datos de Valencia y columna de fecha o timestamp de la reseña
    df_valencia = df[df['city'].str.lower() == 'valencia'].copy()
    
    # Asumimos que tienes una columna con la fecha de la reseña, por ejemplo 'last_review' o 'review_date'
    # Si no la tienes, debes usar la que corresponda o un resumen temporal adecuado.
    if 'last_review' not in df_valencia.columns:
        print("No se encontró columna 'last_review' para evolución de reseñas")
        return
    
    df_valencia = df_valencia.dropna(subset=['last_review', 'number_of_reviews'])
    
    # Convertir a datetime
    df_valencia['last_review'] = pd.to_datetime(df_valencia['last_review'], errors='coerce')
    df_valencia = df_valencia.dropna(subset=['last_review'])
    
    # Agrupar por mes/año
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

    import streamlit as st

def mostrar_imagen_con_fallback(path_ciudad, path_fallback, descripcion):
    try:
        display_image(path_ciudad, descripcion)
    except:
        try:
            display_image(path_fallback, descripcion + " (fallback)")
        except:
            st.warning(f"No se pudo cargar la imagen: {descripcion}")

def mostrar_mapa_con_fallback(path_ciudad, path_fallback, descripcion):
    try:
        display_interactive_map(path_ciudad, descripcion)
    except:
        try:
            display_interactive_map(path_fallback, descripcion + " (fallback)")
        except:
            st.warning(f"No se pudo cargar el mapa: {descripcion}")


def display_image(path, caption=None):
    try:
        img = Image.open(path)
        st.image(img, caption=caption)
    except Exception as e:
        raise e

def display_interactive_map(path, caption=None):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html_data = f.read()
        st.components.v1.html(html_data, height=600)
    except Exception as e:
        raise e

def mostrar_imagen(path, descripcion):
    try:
        display_image(path, descripcion)
    except Exception as e:
        st.warning(f"No se pudo cargar la imagen: {descripcion}\nError: {e}")

def mostrar_mapa(path, descripcion):
    try:
        display_interactive_map(path, descripcion)
    except Exception as e:
        st.warning(f"No se pudo cargar el mapa: {descripcion}\nError: {e}")

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
        st.plotly_chart(fig, use_container_width=True, key="plotly_420")
    else:
        st.info("No hay datos suficientes de precio y calificación.")

def mostrar_mapa_perfiles(df):
    st.markdown("#### Mapa de anuncios")
    if 'latitude' in df.columns and 'longitude' in df.columns:
        st.map(df[['latitude', 'longitude']].dropna())
    else:
        st.info("No hay datos de localización para mostrar el mapa.")

def mostrar_mapa_correlaciones(df):
    # Asegúrate de que las columnas necesarias existan
    if 'latitude' not in df.columns or 'longitude' not in df.columns or 'Net ROI (%)' not in df.columns:
        st.warning("Faltan columnas necesarias para generar el mapa de correlaciones.")
        return

    df_plot = df.dropna(subset=['latitude', 'longitude', 'Net ROI (%)']).copy()

    if df_plot.empty:
        st.warning("No hay datos suficientes para mostrar el mapa de correlaciones.")
        return

    # Ajustamos el tamaño de los puntos para evitar valores negativos
    min_roi = df_plot['Net ROI (%)'].min()
    if min_roi < 0:
        df_plot['size_positive'] = df_plot['Net ROI (%)'] + abs(min_roi) + 1  # todos > 0
    else:
        df_plot['size_positive'] = df_plot['Net ROI (%)']

    # Crear el mapa
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

    st.plotly_chart(fig, use_container_width=True, key="plotly_464")

    import folium

def crear_mapa_valencia():
    m = folium.Map(location=[39.4699, -0.3763], zoom_start=13)

    # Ejemplo de puntos, puedes personalizarlos
    barrios = {
        "Ciutat Universitaria": (39.4811, -0.3450),
        "Penya-Roja": (39.4567, -0.3487),
        "Cabanyal": (39.4702, -0.3235)
    }

    for nombre, coords in barrios.items():
        folium.Marker(coords, tooltip=nombre).add_to(m)

    m.save("mapa_completo_valencia.html")

crear_mapa_valencia()
