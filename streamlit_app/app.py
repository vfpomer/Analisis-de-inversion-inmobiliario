import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import traceback
import os
import folium
from folium.plugins import MarkerCluster, HeatMap
from PIL import Image
import plotly.graph_objects as go
import streamlit.components.v1 as components
from maps_utils import crear_mapa_oportunidades, crear_mapa_precios_valencia, crear_heatmap_ocupacion_valencia, crear_mapa_roi_por_tipo
from maps_utils import crear_mapa_precios_valencia, crear_heatmap_ocupacion_valencia,  display_interactive_map
import streamlit.components.v1 as components
from maps_utils import display_interactive_map, display_image, crear_evolucion_reseñas,mostrar_mapa_correlaciones,mostrar_matriz_correlacion,mostrar_relacion_precio_calificacion,mostrar_mapa_perfiles, crear_mapa_valencia,mostrar_mapa_con_fallback,mostrar_imagen, mostrar_imagen_con_fallback,mostrar_mapa, mostrar_mapa_con_fallback
import copy
import uuid

IMG_DIR = "img"
DOCS_DIR = "docs"
DATA_DIR = "data"

# Funciones de utilidad
def display_interactive_map(file_path, title="Mapa Interactivo"):
    """Display an interactive HTML map"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Try to find the file in different directories
        possible_paths = [
            file_path,
            os.path.join(script_dir, file_path),
            os.path.join(script_dir, 'docs', os.path.basename(file_path)),
            os.path.join(script_dir, '..', 'docs', os.path.basename(file_path)),
            os.path.join(script_dir, 'resultados_barcelona_airbnb', os.path.basename(file_path)),
            os.path.join(script_dir, '..', 'resultados_barcelona_airbnb', os.path.basename(file_path))
        ]

        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                st.components.v1.html(html_content, height=600)
                return

        st.warning(f"No se pudo encontrar el archivo: {file_path}")
    except Exception as e:
        st.error(f"Error al cargar el mapa {file_path}: {e}")

def display_image(image_path, caption=""):
    """Display an image from different possible directories"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Try to find the image in different directories
        possible_paths = [
            image_path,
            os.path.join(script_dir, image_path),
            os.path.join(script_dir, 'img', os.path.basename(image_path)),
            os.path.join(script_dir, '..', 'img', os.path.basename(image_path)),
            os.path.join(script_dir, 'resultados_barcelona_airbnb', os.path.basename(image_path)),
            os.path.join(script_dir, '..', 'resultados_barcelona_airbnb', os.path.basename(image_path))
        ]

        for path in possible_paths:
            if os.path.exists(path):
                img = Image.open(path)
                st.image(img, caption=caption, use_container_width=True)
                return

        st.warning(f"No se pudo encontrar la imagen: {image_path}")
    except Exception as e:
        st.error(f"Error al cargar la imagen {image_path}: {e}")


#Ruta base al directorio raíz del proyecto (2 niveles arriba si estás en streamlit_app/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = os.path.join(BASE_DIR, "img")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Funciones de utilidad
def display_interactive_map(file_path, title="Mapa Interactivo"):
    """Display an interactive HTML map"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Try to find the file in different directories
        possible_paths = [
            file_path,
            os.path.join(script_dir, file_path),
            os.path.join(script_dir, 'docs', os.path.basename(file_path)),
            os.path.join(script_dir, '..', 'docs', os.path.basename(file_path)),
            os.path.join(script_dir, 'resultados_barcelona_airbnb', os.path.basename(file_path)),
            os.path.join(script_dir, '..', 'resultados_barcelona_airbnb', os.path.basename(file_path))
        ]

        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                st.components.v1.html(html_content, height=600)
                return

        st.warning(f"No se pudo encontrar el archivo: {file_path}")
    except Exception as e:
        st.error(f"Error al cargar el mapa {file_path}: {e}")

def display_image(image_path, caption=""):
    """Display an image from different possible directories"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Try to find the image in different directories
        possible_paths = [
            image_path,
            os.path.join(script_dir, image_path),
            os.path.join(script_dir, 'img', os.path.basename(image_path)),
            os.path.join(script_dir, '..', 'img', os.path.basename(image_path)),
            os.path.join(script_dir, 'resultados_barcelona_airbnb', os.path.basename(image_path)),
            os.path.join(script_dir, '..', 'resultados_barcelona_airbnb', os.path.basename(image_path))
        ]

        for path in possible_paths:
            if os.path.exists(path):
                img = Image.open(path)
                st.image(img, caption=caption, use_container_width=True)
                return

        st.warning(f"No se pudo encontrar la imagen: {image_path}")
    except Exception as e:
        st.error(f"Error al cargar la imagen {image_path}: {e}")

st.set_page_config(
    page_title="Panel de Análisis de mercado inmobiliario Valencia (AirBnb)",
    page_icon="🏠📊",
    layout="wide"
)

st.title("🏠📊 Panel de Análisis de mercado inmobiliario Valencia (AirBnb)")
st.markdown("""
Este panel te permite explorar datos del mercado inmobiliario en Valencia para su inversión.
Utiliza los filtros y selectores en la barra lateral para personalizar tu análisis.
""")

@st.cache_data(ttl=3600)
def load_data():
    try:
        df_valencia = pd.read_csv('data/Valencia_limpio.csv')
        df_inmobiliario = pd.read_csv("data/valencia_vivienda_limpio.csv")
        df_delincuencia = pd.read_csv("data/crimenValencia.csv", sep=';')
        
        return df_valencia, df_inmobiliario, df_delincuencia

    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        st.text(traceback.format_exc())
        return None, None, None

df_valencia, df_inmobiliario, df_delincuencia = load_data()

# Preprocesamiento básico y filtros
if df_valencia is not None and df_inmobiliario is not None:
    if 'price' in df_valencia.columns:
        df_valencia['price'] = df_valencia['price'].astype(float)
    if 'precio' in df_inmobiliario.columns:
        precio_m2_valencia = df_inmobiliario['precio'].mean()
    else:
        precio_m2_valencia = 2000  # fallback
    average_m2 = 70
    df_valencia['annual_income'] = df_valencia['price'] * df_valencia['days_rented']
    df_valencia['estimated_property_value'] = precio_m2_valencia * average_m2
    df_valencia['ROI (%)'] = (df_valencia['annual_income'] / df_valencia['estimated_property_value']) * 100
    gastos_anuales = 3000
    df_valencia['net_annual_income'] = df_valencia['annual_income'] - gastos_anuales
    df_valencia['Net ROI (%)'] = (df_valencia['net_annual_income'] / df_valencia['estimated_property_value']) * 100

    st.sidebar.header("Filtros")

# Filtro por ciudad
ciudades = ['Valencia']

if 'city' in df_valencia.columns:
    ciudad_seleccionada = st.sidebar.selectbox("Selecciona ciudad", ciudades)

    # Selecciona el dataframe según la ciudad
    if ciudad_seleccionada.lower() == 'valencia':
        df_ciudad = df_valencia
    else:
        st.warning("Ciudad no reconocida.")
        st.stop()

    # Filtro por barrios
    if 'neighbourhood' in df_ciudad.columns:
        barrios = sorted(df_ciudad['neighbourhood'].dropna().unique())
        selected_barrios = st.sidebar.multiselect("Selecciona barrios", options=barrios, default=barrios)
        df_ciudad = df_ciudad[df_ciudad['neighbourhood'].isin(selected_barrios)]
        if df_ciudad.empty:
            st.warning("No hay datos para los barrios seleccionados en la ciudad.")
            st.stop()
    else:
        st.sidebar.warning("No se encontró la columna 'neighbourhood' en los datos de la ciudad seleccionada.")
        st.stop()

else:
    st.sidebar.warning("No se encontró la columna 'city' en los datos. Mostrando todos los datos.")
    barrios = sorted(df_valencia['neighbourhood'].dropna().unique())
    selected_barrios = st.sidebar.multiselect("Selecciona barrios", options=barrios, default=barrios)
    df_valencia = df_valencia[df_valencia['neighbourhood'].isin(selected_barrios)]
    if df_valencia.empty:
        st.warning("No hay datos para los barrios seleccionados.")
        st.stop()

# Definir pestañas por ciudad usando la ciudad seleccionada del filtro
tabs_por_ciudad = {
    "valencia": [
        "📊 Resumen General",
        "🏠 Precios de Vivienda",
        "💸 Rentabilidad por Barrio",
        "📈 Competencia y Demanda",
        "🔍 Análisis Avanzado",
        "📝 Conclusiones"
    ]
}

# Añadir "Conclusiones Generales" a todas las ciudades si no está presente
for k in tabs_por_ciudad:
    if "🧭 Conclusiones Generales" not in tabs_por_ciudad[k]:
        tabs_por_ciudad[k].append("🧭 Conclusiones Generales")

# Convertir la ciudad seleccionada a minúsculas para buscar en el diccionario
ciudad_actual = ciudad_seleccionada.lower()
pestañas = tabs_por_ciudad.get(ciudad_actual, [])

if not pestañas:
    st.warning(f"No hay pestañas definidas para la ciudad '{ciudad_seleccionada}'.")
    st.stop()

main_tabs = st.tabs(pestañas)

# Mostrar contenido básico para testear acceso a pestañas (debug)
for i, tab in enumerate(main_tabs):
    with tab:
        st.write("")

# ------------------ Pestaña 1: Resumen General ------------------
if len(main_tabs) > 0:
    with main_tabs[0]:
        if ciudad_actual == "valencia":
            st.subheader("Resumen General del Mercado Inmobiliario de Valencia")

            # Métricas principales
            col1, col2, col3 = st.columns(3)
            col1.metric("Nº de anuncios", len(df_ciudad))

            if 'Net ROI (%)' in df_ciudad.columns and not df_ciudad['Net ROI (%)'].isnull().all():
                roi_neto_medio = df_ciudad['Net ROI (%)'].mean() * 100
                col2.metric("ROI Neto medio (%)", f"{roi_neto_medio:.2f}")
            else:
                col2.metric("ROI Neto medio (%)", "N/A")
                    
            if 'price' in df_ciudad.columns and not df_ciudad['price'].isnull().all():
                precio_medio = df_ciudad['price'].mean()
                col3.metric("Precio medio alquiler (€)", f"{precio_medio:.2f}")
            else:
                col3.metric("Precio medio alquiler (€)", "N/A")


            # Distribución de ROI Bruto y Neto (gráfico mejorado)
            st.markdown("#### Distribución de ROI Bruto y Neto (%)")
            if (
                len(df_ciudad) > 1 and 
                'ROI (%)' in df_ciudad.columns and 
                'Net ROI (%)' in df_ciudad.columns
            ):
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=df_ciudad['ROI (%)'],
                    name='ROI Bruto (%)',
                    opacity=0.6,
                    marker_color='skyblue',
                    nbinsx=40,
                    histnorm='probability density'
                ))
                fig.add_trace(go.Histogram(
                    x=df_ciudad['Net ROI (%)'],
                    name='ROI Neto (%)',
                    opacity=0.6,
                    marker_color='orange',
                    nbinsx=40,
                    histnorm='probability density'
                ))
                fig.update_layout(
                    barmode='overlay',
                    title='Distribución de ROI Bruto y Neto (%)',
                    xaxis_title='ROI (%)',
                    yaxis_title='Densidad',
                    legend=dict(x=0.7, y=0.95, bgcolor='rgba(0,0,0,0)'),
                    template='plotly_white',
                    height=400,
                    margin=dict(l=40, r=40, t=60, b=40)
                )
                fig.update_traces(marker_line_width=1, marker_line_color='white')
                st.plotly_chart(fig, use_container_width=True, key="bar_358")

            # Mapa interactivo
            st.markdown("#### Mapa de Oportunidades en Valencia")
            try:
                crear_mapa_oportunidades(df_ciudad)  # Genera el HTML
                with open(f"mapa_oportunidad_{ciudad_actual}.html", "r", encoding="utf-8") as f:
                    html_mapa = f.read()
                components.html(html_mapa, height=600, scrolling=True)
            except Exception as e:
                st.warning(f"No se pudo generar el mapa de oportunidades de Valencia. Error: {e}")

            # Distribución por tipo de habitación
            st.markdown("#### Distribución por Tipo de Alojamiento")
            if 'room_type' in df_ciudad.columns:
                room_type_counts = df_ciudad['room_type'].value_counts().reset_index()
                room_type_counts.columns = ['room_type', 'count']

                fig = px.pie(
                    room_type_counts, 
                    values='count', 
                    names='room_type',
                    title='Distribución por Tipo de Alojamiento',
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True, key=f"fig_bar_{ciudad_actual}_374")
            else:
                st.info("No hay datos de tipo de alojamiento disponibles.")

else:
    st.info("No hay datos para mostrar en esta pestaña.")


# ------------------ Pestaña 2: Precios de Vivienda ------------------
with main_tabs[1]:
    if ciudad_actual.lower() == "valencia":
       
        RUTA_MAPA = 'docs/mapa_precio_valencia.html'
        RUTA_IMG = 'img/valencia_heatmap_ocupacion.png'


        # El resto igual
        crear_mapa_precios_valencia(df_ciudad, ruta_guardado=RUTA_MAPA)
        crear_heatmap_ocupacion_valencia(df_ciudad, ruta_guardado=RUTA_IMG)
        
        st.title("Análisis de Vivienda en Valencia")
        st.subheader("Precios de Vivienda en Valencia")

        col1, col2 = st.columns(2)
        with col1:
            if 'price' in df_ciudad.columns:
                stats = df_ciudad['price'].describe()
                st.metric("Precio Medio por Noche", f"{stats['mean']:.2f}€")
                st.metric("Precio Mediano por Noche", f"{stats['50%']:.2f}€")
                st.metric("Precio Máximo", f"{stats['max']:.2f}€")

                fig = px.histogram(
                    df_ciudad,
                    x='price',
                    nbins=50,
                    title='Distribución de Precios por Noche',
                    labels={'price': 'Precio (€)'},
                    range_x=[0, stats['75%'] * 2] if stats['75%'] > 0 else None
                )
                st.plotly_chart(fig, use_container_width=True, key="hist_precio")
            else:
                st.info("No hay datos de precios de alquiler disponibles.")

        with col2:
            if 'price' in df_ciudad.columns and 'room_type' in df_ciudad.columns:
                fig_box = px.box(
                    df_ciudad,
                    x='room_type',
                    y='price',
                    title='Distribución de Precios por Tipo de Alojamiento',
                    labels={'price': 'Precio por Noche (€)', 'room_type': 'Tipo de Alojamiento'}
                )
                st.plotly_chart(fig_box, use_container_width=True, key="box_room_type1")

                avg_price_by_type = df_ciudad.groupby('room_type')['price'].mean().reset_index()
                fig_bar = px.bar(
                    avg_price_by_type,
                    x='room_type',
                    y='price',
                    title='Precio Promedio por Tipo de Alojamiento',
                    labels={'price': 'Precio Promedio (€)', 'room_type': 'Tipo de Alojamiento'}
                )
                st.plotly_chart(fig_bar, use_container_width=True, key=f"fig_bar_{ciudad_actual}_1")
            else:
                st.info("No hay datos de precios por tipo de habitación disponibles.")

        st.subheader("Precios de Compra por Barrio")
        if 'precio' in df_inmobiliario.columns:
            barrio_caros = df_inmobiliario.groupby('neighbourhood')['precio'].mean().reset_index()
            barrio_caros = barrio_caros.sort_values(by='precio', ascending=False).head(15)
            if not barrio_caros.empty:
                fig_precio = px.bar(
                    barrio_caros,
                    x='precio',
                    y='neighbourhood',
                    orientation='h',
                    labels={'precio': 'Precio medio m2 de compra (€)', 'neighbourhood': 'Barrio'},
                    title='Top 15 barrios más caros por precio medio m2 de compra'
                )
                st.plotly_chart(fig_precio, use_container_width=True, key="bar_barrio_1")
            else:
                st.info("No hay datos de precios de vivienda para mostrar.")
        else:
            st.info("No hay datos de precios de vivienda para mostrar.")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Propiedades", f"{len(df_ciudad):,}")
            if 'price' in df_ciudad.columns:
                st.metric("Precio Medio por Noche", f"{df_ciudad['price'].mean():.2f}€")
        with col2:
            if 'room_type' in df_ciudad.columns:
                room_counts = df_ciudad['room_type'].value_counts()
                st.metric("Apartamentos Completos", f"{room_counts.get('Entire home/apt', 0):,}")
                st.metric("Habitaciones Privadas", f"{room_counts.get('Private room', 0):,}")
            else:
                st.info("No hay datos de tipos de habitación disponibles")
        with col3:
            if 'neighbourhood' in df_ciudad.columns:
                st.metric("Barrios", f"{df_ciudad['neighbourhood'].nunique()}")

        st.subheader("Distribución Geográfica de Precios de Alquiler")
        display_interactive_map(RUTA_MAPA, "Mapa de Precios en Valencia")

        st.subheader("Análisis de Mercado")
        col1, col2 = st.columns(2)
        with col1:
            if 'price' in df_ciudad.columns and 'room_type' in df_ciudad.columns:
                fig = px.box(
                    df_ciudad,
                    x='room_type',
                    y='price',
                    title='Distribución de Precios por Tipo de Alojamiento',
                    labels={'price': 'Precio por noche (€)', 'room_type': 'Tipo de Alojamiento'}
                )
                st.plotly_chart(fig, use_container_width=True, key="box_analisis1")
        with col2:
            if 'neighbourhood' in df_ciudad.columns:
                top_barrios = df_ciudad['neighbourhood'].value_counts().head(10)
                fig = px.bar(
                    top_barrios,
                    title='Top 10 Barrios con Más Propiedades',
                    labels={'value': 'Número de Propiedades', 'index': 'Barrio'}
                )
                st.plotly_chart(fig, use_container_width=True, key="bar_barrios_1")

    else:
        st.info("No hay datos para mostrar en esta pestaña.")


# ------------------ Pestaña 3: Rentabilidad por Barrio ------------------

if len(main_tabs) > 2:
    with main_tabs[2]:
        if ciudad_actual == "valencia":

            # ----------------------------------------
            # FUNCIONES DE STREAMLIT
            # ----------------------------------------

            def display_interactive_map(path, title=None):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                        if title:
                            st.markdown(f"**{title}**")
                        components.html(html_content, height=600)
                except FileNotFoundError:
                    st.warning(f"No se pudo encontrar el archivo: {path}")

            def display_image(path, caption=None):
                try:
                    image = Image.open(path)
                    st.image(image, caption=caption, use_container_width=True)
                except FileNotFoundError:
                    st.warning(f"No se pudo encontrar la imagen: {path}")

            # ----------------------------------------
            # CARGA DE DATOS Y VISUALIZACIÓN DE GRÁFICOS
            # ----------------------------------------

            st.subheader("Rentabilidad por Barrio en Valencia")

            if not df_ciudad.empty:

                if 'Net ROI (%)' in df_ciudad.columns and 'neighbourhood' in df_ciudad.columns:
                    roi_barrio = df_ciudad.groupby('neighbourhood')['Net ROI (%)'].mean().sort_values(ascending=False).head(15)
                    if not roi_barrio.empty:
                        fig_roi = px.bar(
                            x=roi_barrio.values,
                            y=roi_barrio.index,
                            orientation='h',
                            labels={'x': 'ROI Neto (%)', 'y': 'Barrio'},
                            title='Top 15 barrios por ROI Neto (%)'
                        )
                        st.plotly_chart(fig_roi, use_container_width=True, key=f"fig_roi_neto_{ciudad_actual}")

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
                        st.plotly_chart(fig_roi_bruto, use_container_width=True, key=f"fig_roi_bruto_{ciudad_actual}")

                # Verificación y generación del mapa si no existe
                map_path = "docs/valencia_roi_by_type_map.html"
                if not os.path.exists(map_path):
                    crear_mapa_roi_por_tipo(df_ciudad, map_path)

                st.markdown("#### Mapa de Rentabilidad")
                display_interactive_map(map_path, "Mapa ROI por Tipo en Valencia")

            else:
                st.info("No hay datos para mostrar en esta pestaña.")



# ------------------ Pestaña 4: Competencia y Demanda ------------------

if len(main_tabs) > 3:
    with main_tabs[3]:
        if ciudad_actual == "valencia":
        
            st.subheader("Competencia y Demanda en Valencia")
    
            if df_ciudad.empty:
                st.info("No hay datos para mostrar.")
            else:
                # --- Competencia ---
                st.subheader("Competencia por barrio")
                top_comp = df_ciudad.groupby('neighbourhood')['id'].count().sort_values(ascending=False).head(15)
                if not top_comp.empty:
                    fig_comp = px.bar(
                        x=top_comp.values,
                        y=top_comp.index,
                        orientation='h',
                        labels={'x': 'Nº de anuncios', 'y': 'Barrio'},
                        title='Top 15 barrios con más competencia'
                    )
                    st.plotly_chart(fig_comp, use_container_width=True, key="bar_1265")
    
                # --- Mapa de Densidad de Alojamientos ---
                st.subheader("Mapa de Oportunidad en Valencia")
                mapa_path = os.path.join(DOCS_DIR, "mapa_oportunidad_valencia.html")
                display_interactive_map(mapa_path, "Mapa de Rentabilidad")
    
                # --- Reseñas como indicador de demanda ---
                st.subheader("Análisis de Reseñas")
                if 'number_of_reviews' in df_ciudad.columns:
                    top_reviews = df_ciudad.groupby('neighbourhood')['number_of_reviews'].sum().sort_values(ascending=False).head(15)
                    fig_reviews = px.bar(
                        x=top_reviews.values,
                        y=top_reviews.index,
                        orientation='h',
                        labels={'x': 'Número de reseñas', 'y': 'Barrio'},
                        title='Top 15 barrios por número de reseñas'
                    )
                    st.plotly_chart(fig_reviews, use_container_width=True, key="bar_1283")
    
                    # Crear imagen de evolución antes de mostrarla
                    img_reviews_path = os.path.join(IMG_DIR, "valencia_reviews_evolution.png")
                    crear_evolucion_reseñas(df_ciudad, img_reviews_path)  # <-- función que debes tener o crear
                    display_image(img_reviews_path, "Evolución de reseñas en el tiempo")
                else:
                    st.info("No hay datos de reseñas disponibles.")
    
                # --- Ocupación estimada ---
                st.subheader("Ocupación Estimada")
                if 'days_rented' in df_ciudad.columns:
                    top_ocup = df_ciudad.groupby('neighbourhood')['days_rented'].mean().sort_values(ascending=False).head(15)
                    fig_ocup = px.bar(
                        x=top_ocup.values,
                        y=top_ocup.index,
                        orientation='h',
                        labels={'x': 'Días ocupados', 'y': 'Barrio'},
                        title='Top 15 barrios por ocupación estimada'
                    )
                    st.plotly_chart(fig_ocup, use_container_width=True, key="bar_1303")
    
                    # Crear imagen de ocupación antes de mostrarla
                    img_ocupacion_path = os.path.join(IMG_DIR, "valencia_ocupacion_diasemana.png")
                    crear_heatmap_ocupacion_valencia(df_ciudad, img_ocupacion_path)
                    display_image(img_ocupacion_path, "Patrón de ocupación semanal")
                else:
                    st.info("No hay datos de ocupación.")

else:
     st.warning("No hay pestañas disponibles para mostrar contenido.")



# ------------------ Pestaña 5: Análisis Avanzado ------------------
if len(main_tabs) > 4:
    with main_tabs[4]:
        if ciudad_actual.lower() == "valencia":
            st.subheader("Análisis Avanzado")
            
            if not df_valencia.empty:
                columnas_corr = ['price', 'Net ROI (%)', 'review_scores_rating', 'days_rented']
                columnas_corr = [col for col in columnas_corr if col in df_valencia.columns]
                
                if len(columnas_corr) > 1:
                    mostrar_matriz_correlacion(df_valencia, columnas_corr)
                else:
                    st.info("No hay suficientes columnas para matriz de correlación.")
                
                mostrar_relacion_precio_calificacion(df_valencia)
        
                try:
                    mostrar_mapa_perfiles(df_valencia)
                except Exception as e:
                    st.error(f"Error al mostrar el mapa de perfiles: {e}")
        
                mostrar_mapa_correlaciones(df_valencia)
        
                # Relación entre precio medio de alquiler y ROI neto por barrio
                st.markdown("#### Relación entre precio medio de alquiler y ROI neto por barrio")
        
                if ('city' in df_valencia.columns 
                    and df_valencia['city'].str.lower().nunique() == 1 
                    and df_valencia['city'].str.lower().iloc[0] == 'valencia'):
                    
                    if 'price' in df_valencia.columns and 'Net ROI (%)' in df_valencia.columns:
                        fig_val = px.scatter(
                            df_valencia,
                            x='price',
                            y='Net ROI (%)',
                            color='neighbourhood',
                            hover_data=['neighbourhood'],
                            opacity=0.6,
                            labels={'price': 'Precio alquiler (€)', 'Net ROI (%)': 'ROI Neto (%)', 'neighbourhood': 'Barrio'},
                            title='Relación entre precio de alquiler y ROI neto por barrio (Valencia)'
                        )
                        fig_val.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
                        fig_val.update_layout(
                            legend_title_text='Barrio',
                            showlegend=False,
                            height=500,
                            margin=dict(l=40, r=40, t=60, b=40)
                        )
                        st.plotly_chart(fig_val, use_container_width=True, key="bar_1490")
                    else:
                        st.info("No hay datos suficientes para mostrar el gráfico de dispersión para Valencia.")
                
                else:
                    df_barrio = df_valencia.groupby('neighbourhood').agg({'price': 'mean', 'Net ROI (%)': 'mean'}).reset_index()
                    if not df_barrio.empty:
                        fig_scatter = px.scatter(
                            df_barrio,
                            x='price',
                            y='Net ROI (%)',
                            text='neighbourhood',
                            labels={'price': 'Precio medio alquiler (€)', 'Net ROI (%)': 'ROI Neto (%)'},
                            title='Precio medio de alquiler vs ROI Neto por barrio'
                        )
                        fig_scatter.update_traces(marker=dict(size=12, color='royalblue', line=dict(width=1, color='DarkSlateGrey')))
                        fig_scatter.update_layout(
                            height=500,
                            margin=dict(l=40, r=40, t=60, b=40)
                        )
                        st.plotly_chart(fig_scatter, use_container_width=True, key="bar_1510")
                    else:
                        st.info("No hay datos para mostrar la relación entre precio y ROI.")
            else:
                st.info("No hay datos para Valencia.")



            # Número medio de amenities por barrio
            st.markdown("#### Top 15 barrios por número medio de amenities")
            if 'amenities' in df_valencia.columns:
                df_valencia['n_amenities'] = df_valencia['amenities'].str.count(',') + 1
                barrio_amenities = df_valencia.groupby('neighbourhood')['n_amenities'].mean().reset_index()
                barrio_amenities = barrio_amenities.sort_values(by='n_amenities', ascending=False).head(15)
                if not barrio_amenities.empty:
                    fig_amenities = px.bar(
                        barrio_amenities,
                        x='n_amenities',
                        y='neighbourhood',
                        orientation='h',
                        labels={'n_amenities': 'Nº medio de amenities', 'neighbourhood': 'Barrio'},
                        title='Top 15 barrios por número medio de amenities',
                        color='n_amenities',
                        color_continuous_scale='Purples'
                    )
                    fig_amenities.update_layout(
                        height=500,
                        margin=dict(l=40, r=40, t=60, b=40),
                        yaxis=dict(tickfont=dict(size=12)),
                        xaxis=dict(tickfont=dict(size=12))
                    )
                    st.plotly_chart(fig_amenities, use_container_width=True, key="bar_1540")
                else:
                    st.info("No hay datos de amenities para mostrar.")
            else:
                st.info("No hay datos de amenities para mostrar.") 

            # Número total de reseñas por barrio
            st.markdown("#### Top 15 barrios por número total de reseñas")
            if 'number_of_reviews' in df_valencia.columns:
                barrio_mas_resenas = df_valencia.groupby('neighbourhood')['number_of_reviews'].sum().reset_index()
                barrio_mas_resenas = barrio_mas_resenas.sort_values(by='number_of_reviews', ascending=False).head(15)
                if not barrio_mas_resenas.empty:
                    fig_resenas = px.bar(
                        barrio_mas_resenas,
                        x='number_of_reviews',
                        y='neighbourhood',
                        orientation='h',
                        labels={'number_of_reviews': 'Número total de reseñas', 'neighbourhood': 'Barrio'},
                        title='Top 15 barrios por número total de reseñas',
                        color='number_of_reviews',
                        color_continuous_scale='Blues'
                    )
                    fig_resenas.update_layout(
                        height=500,
                        margin=dict(l=40, r=40, t=60, b=40),
                        yaxis=dict(tickfont=dict(size=12)),
                        xaxis=dict(tickfont=dict(size=12))
                    )
                    st.plotly_chart(fig_resenas, use_container_width=True, key="bar_1596")
                else:
                    st.info("No hay datos de reseñas para mostrar.")
            else:
                st.info("No hay datos de reseñas para mostrar.")

            # Habitaciones y baños por barrio
            st.markdown("#### Top 15 barrios por número medio de habitaciones y baños")
            if 'bedrooms' in df_valencia.columns and 'bathrooms' in df_valencia.columns:
                barrio_habitaciones_banos = df_valencia.groupby('neighbourhood').agg({
                    'bedrooms': 'mean',
                    'bathrooms': 'mean'
                }).reset_index()
                barrio_habitaciones_banos = barrio_habitaciones_banos.sort_values(by='bedrooms', ascending=False).head(15)
                if not barrio_habitaciones_banos.empty:
                    fig_hab = px.bar(
                        barrio_habitaciones_banos,
                        x='bedrooms',
                        y='neighbourhood',
                        orientation='h',
                        labels={'bedrooms': 'Habitaciones medias', 'neighbourhood': 'Barrio'},
                        title='Top 15 barrios por número medio de habitaciones',
                        color='bedrooms',
                        color_continuous_scale='Teal'
                    )
                    fig_hab.update_layout(
                        height=500,
                        margin=dict(l=40, r=40, t=60, b=40),
                        yaxis=dict(tickfont=dict(size=12)),
                        xaxis=dict(tickfont=dict(size=12))
                    )
                    st.plotly_chart(fig_hab, use_container_width=True, key="bar_1654")
                else:
                    st.info("No hay datos de habitaciones para mostrar.")
            else:
                st.info("No hay datos de habitaciones o baños para mostrar.")

          
            # Histograma de precios de alquiler
            st.markdown("#### Histograma de precios de alquiler")
            if 'price' in df_valencia.columns:
                fig_hist = px.histogram(
                    df_valencia, x='price', nbins=40, color='neighbourhood',
                    labels={'price': 'Precio alquiler (€)'},
                    title='Distribución de precios de alquiler por barrio',
                    opacity=0.7
                )
                fig_hist.update_layout(
                    height=400,
                    margin=dict(l=40, r=40, t=60, b=40),
                    xaxis=dict(tickfont=dict(size=12)),
                    yaxis=dict(tickfont=dict(size=12)),
                    barmode='overlay'
                )
                st.plotly_chart(fig_hist, use_container_width=True, key="bar_1725")
            else:
                st.info("No hay datos de precios para mostrar histograma.")

           
            # Boxplot de precios de alquiler por barrio (solo top 15 barrios)
            st.markdown("#### Boxplot de precios de alquiler por barrio (Top 15)")
            if 'price' in df_valencia.columns:
                top_barrios = df_valencia['neighbourhood'].value_counts().head(15).index
                df_top = df_valencia[df_valencia['neighbourhood'].isin(top_barrios)]
                fig_box = px.box(
                    df_top, x='neighbourhood', y='price', points='outliers',
                    labels={'price': 'Precio alquiler (€)', 'neighbourhood': 'Barrio'},
                    title='Boxplot de precios de alquiler por barrio (Top 15)'
                )
                fig_box.update_layout(
                    height=500,
                    margin=dict(l=40, r=40, t=60, b=40),
                    xaxis=dict(tickangle=45, tickfont=dict(size=12)),
                    yaxis=dict(tickfont=dict(size=12))
                )
                st.plotly_chart(fig_box, use_container_width=True, key="bar_1764")
            else:
                st.info("No hay datos de precios para mostrar boxplot.")

           
            # Histograma de ROI Neto
            st.markdown("#### Histograma de ROI Neto (%)")
            if 'Net ROI (%)' in df_valencia.columns:
                fig_hist_roi = px.histogram(
                    df_valencia, x='Net ROI (%)', nbins=40, color='neighbourhood',
                    labels={'Net ROI (%)': 'ROI Neto (%)'},
                    title='Distribución de ROI Neto por barrio',
                    opacity=0.7
                )
                fig_hist_roi.update_layout(
                    height=400,
                    margin=dict(l=40, r=40, t=60, b=40),
                    xaxis=dict(tickfont=dict(size=12)),
                    yaxis=dict(tickfont=dict(size=12)),
                    barmode='overlay'
                )
                st.plotly_chart(fig_hist_roi, use_container_width=True, key="bar_1803")
            else:
                st.info("No hay datos de ROI Neto para mostrar histograma.")

          
            # Boxplot de ROI Neto por barrio (solo top 15 barrios)
            st.markdown("#### Boxplot de ROI Neto por barrio (Top 15)")
            if 'Net ROI (%)' in df_valencia.columns:
                top_barrios = df_valencia['neighbourhood'].value_counts().head(15).index
                df_top = df_valencia[df_valencia['neighbourhood'].isin(top_barrios)]
                fig_box_roi = px.box(
                    df_top, x='neighbourhood', y='Net ROI (%)', points='outliers',
                    labels={'Net ROI (%)': 'ROI Neto (%)', 'neighbourhood': 'Barrio'},
                    title='Boxplot de ROI Neto por barrio (Top 15)'
                )
                fig_box_roi.update_layout(
                    height=500,
                    margin=dict(l=40, r=40, t=60, b=40),
                    xaxis=dict(tickangle=45, tickfont=dict(size=12)),
                    yaxis=dict(tickfont=dict(size=12))
                )
                st.plotly_chart(fig_box_roi, use_container_width=True, key="bar_1842")
            else:
                st.info("No hay datos de ROI Neto para mostrar boxplot.")

         # Histograma de días alquilados
            st.markdown("#### Histograma de días alquilados")
            if 'days_rented' in df_valencia.columns:
                fig_hist_days = px.histogram(
                    df_valencia, x='days_rented', nbins=40, color='neighbourhood',
                    labels={'days_rented': 'Días alquilados'},
                    title='Distribución de días alquilados por barrio',
                    opacity=0.7
                )
                fig_hist_days.update_layout(
                    height=400,
                    margin=dict(l=40, r=40, t=60, b=40),
                    xaxis=dict(tickfont=dict(size=12)),
                    yaxis=dict(tickfont=dict(size=12)),
                    barmode='overlay'
                )
                st.plotly_chart(fig_hist_days, use_container_width=True, key="bar_1862")
            else:
                st.info("No hay datos de días alquilados para mostrar histograma.")
            
            # Boxplot de días alquilados por barrio (Top 15)
            st.markdown("#### Boxplot de días alquilados por barrio (Top 15)")
            if 'days_rented' in df_valencia.columns:
                top_barrios = df_valencia['neighbourhood'].value_counts().head(15).index
                df_top = df_valencia[df_valencia['neighbourhood'].isin(top_barrios)]
                fig_box_days = px.box(
                    df_top, x='neighbourhood', y='days_rented', points='outliers',
                    labels={'days_rented': 'Días alquilados', 'neighbourhood': 'Barrio'},
                    title='Boxplot de días alquilados por barrio (Top 15)'
                )
                fig_box_days.update_layout(
                    height=500,
                    margin=dict(l=40, r=40, t=60, b=40),
                    xaxis=dict(tickangle=45, tickfont=dict(size=12)),
                    yaxis=dict(tickfont=dict(size=12))
                )
                st.plotly_chart(fig_box_days, use_container_width=True, key="bar_1901")
            else:
                st.info("No hay datos de días alquilados para mostrar boxplot.")
            
            # Delincuencia: Gráfico de barras agrupadas
            st.markdown("#### Delitos denunciados en Valencia por año")
            if df_delincuencia is not None and not df_delincuencia.empty:
                df_delincuencia_filtrado = df_delincuencia[df_delincuencia['Parámetro'] != 'Total']
                
                fig, ax = plt.subplots(figsize=(14, 7))
                sns.barplot(
                    data=df_delincuencia_filtrado,
                    x='Año',
                    y='Denuncias',
                    hue='Parámetro',
                    ax=ax
                )
                ax.set_title('Delitos denunciados en Valencia por año')
                ax.set_ylabel('Número de denuncias')
                ax.set_xlabel('Año')
                ax.legend(title='Tipo de delito', bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                st.pyplot(fig)
            
                # Mapa de calor
                st.markdown("#### Mapa de calor de delitos denunciados en Valencia por tipo y año")
                fig2, ax2 = plt.subplots(figsize=(14, 7))
                heatmap_data = df_delincuencia_filtrado.pivot_table(
                    index='Parámetro',
                    columns='Año',
                    values='Denuncias',
                    aggfunc='sum'
                ).fillna(0)
                sns.heatmap(
                    heatmap_data,
                    cmap='YlOrRd',
                    annot=True,
                    fmt='.0f',
                    linewidths=.5,
                    cbar_kws={'label': 'Número de denuncias'},
                    annot_kws={"size": 10},
                    ax=ax2
                )
                ax2.set_title('Mapa de calor de delitos denunciados en Valencia por tipo y año')
                ax2.set_xlabel('Año')
                ax2.set_ylabel('Tipo de delito')
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig2)
            else:
                st.info("No hay datos de delincuencia para mostrar.")

        else:
            st.info("No hay datos para mostrar en esta pestaña.")

# ------------------ Pestaña 6: Conclusiones ------------------

# Función para mostrar conclusiones por ciudad
def mostrar_conclusiones(ciudad_actual, ciudad_seleccionada):
    st.subheader(f"Conclusiones para Invertir en {ciudad_seleccionada}")
    st.write("Ciudad seleccionada:", ciudad_actual)

    if ciudad_actual.lower() == "valencia":
        st.markdown("""
### Análisis Estratégico por Barrios de Valencia 🏙️
#### Tabla Comparativa de Barrios

| Barrio                 | ROI Neto (%) | ROI Bruto (%) | Competencia | Estrategia Recomendada | Justificación                                                                                   |
|------------------------|--------------|---------------|-------------|-----------------------|------------------------------------------------------------------------------------------------|
| Ciutat Universitaria    | 11.0         | 14.1          | 92          | Diferenciación        | Alta rentabilidad y público recurrente. Potencial en el mercado estudiantil y turístico.        |
| Penya-Roja             | 10.7         | 13.8          | 87          | Expansión             | Barrios en desarrollo cerca del cauce del Turia. Ideal para posicionarse temprano.              |
| Cami Fondo             | 10.4         | 13.3          | 68          | Oportunidad           | Rentabilidad elevada con baja competencia. Alta eficiencia operativa.                           |
| La Roqueta             | 10.1         | 13.0          | 115         | Equilibrio            | Conectividad excelente y buena rotación. Equilibrar calidad y precio.                           |
| Cabanyal-Canyamelar    | 9.8          | 12.6          | 204         | Diferenciación        | Demanda turística alta. Necesita destacar por estilo y servicios.                               |
| Russafa                | 9.5          | 12.4          | 189         | Autenticidad          | Barrio bohemio con atractivo cultural. Ideal para propuestas boutique.                          |
| El Mercat              | 9.2          | 12.1          | 173         | Premium               | Ubicación central y demanda constante. Estrategia de precios altos y servicios premium.         |
| Nou Moles              | 8.8          | 11.5          | 71          | Renovación            | Potencial de revalorización tras mejoras. Buen ROI si se invierte en modernización.            |
| Montolivet             | 8.5          | 11.2          | 59          | Diversificación       | Barrios con riesgo bajo y rentabilidad sólida. Ideal para balancear cartera.                    |
| Tres Forques           | 8.2          | 10.9          | 49          | Optimización          | Poca competencia. Optimización de tarifas y servicios puede mejorar ROI.                        |
""")

        st.markdown("---")

        try:
            display_interactive_map("mapa_completo_valencia.html", "Recomendaciones Estratégicas por Barrio - Valencia")
        except Exception as e:
            st.warning(f"No se pudo cargar el mapa de recomendaciones estratégicas: {e}")

   

# Uso de la función en la pestaña 6 (índice 5)
if len(main_tabs) > 5:
    with main_tabs[5]:
        mostrar_conclusiones(ciudad_actual, ciudad_seleccionada)

# ------------------ Descargable ------------------
with st.expander("Ver y descargar datos filtrados"):
    if not df_ciudad.empty:
        st.dataframe(df_ciudad, use_container_width=True)
        csv = df_ciudad.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Descargar datos filtrados (CSV)",
            data=csv,
            file_name=f"{ciudad_actual}_inmobiliario.csv",
            mime="text/csv",
        )
    else:
        st.info("No hay datos para mostrar o descargar.")


# ------------ Información del dashboard ------------
# Sidebar de información
st.sidebar.info(
'''
**Acerca de este Panel**

Este panel muestra datos del mercado inmobiliario de Valencia para análisis de inversión.

Desarrollado con Streamlit, Plotly Express y Seaborn.
'''
)
