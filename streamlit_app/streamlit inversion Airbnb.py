import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import traceback
import os
import folium
from PIL import Image
import plotly.graph_objects as go
import streamlit.components.v1 as components

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
    page_title="Panel de Análisis de mercado inmobiliario (AirBnb)",
    page_icon="🏠📊",
    layout="wide"
)

st.title("🏠📊 Panel de Análisis de mercado inmobiliario (AirBnb)")
st.markdown("""
Este panel te permite explorar datos del mercado inmobiliario en Valencia, Málaga, Madrid y Barcelona para su inversión.
Utiliza los filtros y selectores en la barra lateral para personalizar tu análisis.
""")

@st.cache_data(ttl=3600)
def load_data():
    try:
        df_valencia = pd.read_csv('data/Valencia_limpio.csv')
        df_inmobiliario = pd.read_csv("data/valencia_vivienda_limpio.csv")
        df_delincuencia = pd.read_csv("data/crimenValencia.csv", sep=';')
        df_barcelona = pd.read_csv("data/barcelona_limpio_completo.csv")
        df_barcelona_inversores = pd.read_csv("data/barcelona_inversores.csv")
        df_precios_barrios = pd.read_csv("data/precio_vivienda_barriosBarcelona_mayo2025.csv")
        df_precios_distritos = pd.read_csv("data/precio_vivienda_distritosBarcelona_mayo2025.csv")
        df_malaga = pd.read_csv("data/malaga_completed_clean.csv")
        df_malaga_crimen = pd.read_csv("data/malaga_crimen_clean.csv", sep=';')
        return df_valencia, df_inmobiliario, df_delincuencia, df_barcelona, df_barcelona_inversores, df_precios_barrios, df_precios_distritos, df_malaga, df_malaga_crimen
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        st.text(traceback.format_exc())
        return None, None, None, None, None, None, None, None, None

df_valencia, df_inmobiliario, df_delincuencia, df_barcelona, df_barcelona_inversores, df_precios_barrios, df_precios_distritos, df_malaga, df_malaga_crimen = load_data()

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
ciudades = ['Valencia', 'Malaga', 'Madrid', 'Barcelona']

if 'city' in df_valencia.columns:
    ciudad_seleccionada = st.sidebar.selectbox("Selecciona ciudad", ciudades)

    # Selecciona el dataframe según la ciudad
    if ciudad_seleccionada.lower() == 'valencia':
        df_ciudad = df_valencia
    elif ciudad_seleccionada.lower() == 'barcelona':
        df_ciudad = df_barcelona
    elif ciudad_seleccionada.lower() == 'malaga':
        df_ciudad = df_malaga
    elif ciudad_seleccionada.lower() == 'madrid':
        try:
            df_madrid = pd.read_csv("../data/madrid_limpio.csv")
        except Exception as e:
            st.warning("No se pudo cargar el dataset de Madrid.")
            st.stop()
        df_ciudad = df_madrid
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
    ],
    "barcelona": [
        "📊 Resumen General",
        "🏠 Precios de Vivienda",
        "💸 Rentabilidad por Barrio",
        "📈 Competencia y Demanda",
        "🔍 Análisis Avanzado",
        "📝 Conclusiones"
    ],
    "madrid": [
        "📊 Madrid General",
        "🏠 Madrid de Vivienda",
        "💸 Rentabilidad por Barrio",
        "📈 Competencia y Demanda",
        "🔍 Análisis Avanzado",
        "📝 Conclusiones"
    ],
    "malaga": [
        "📊 Resumen General",
        "🏠 Precios de Vivienda",
        "💸 Rentabilidad por Barrio",
        "📈 Competencia y Demanda",
        "🔍 Análisis Avanzado",
        "📝 Conclusiones"
    ]
}

# Convertir la ciudad seleccionada a minúsculas para buscar en el diccionario
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
            st.subheader("Resumen General del Mercado Inmobiliario")
        
            col1, col2, col3 = st.columns(3)
            col1.metric("Nº de anuncios", len(df_ciudad))
            col2.metric("ROI Neto medio (%)", f"{df_ciudad['Net ROI (%)'].mean():.2f}")
            col3.metric("Precio medio alquiler (€)", f"{df_ciudad['price'].mean():.2f}")

            # KDE ROI Bruto y Neto
            st.markdown("#### Distribución de ROI Bruto y Neto (%)")
            if len(df_ciudad) > 1:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.kdeplot(df_ciudad['ROI (%)'], fill=True, label='ROI Bruto (%)', color='skyblue', bw_adjust=0.7, clip=(0, 50), ax=ax)
                sns.kdeplot(df_ciudad['Net ROI (%)'], fill=True, label='ROI Neto (%)', color='orange', bw_adjust=0.7, clip=(0, 50), ax=ax)
                ax.set_title('Distribución de ROI Bruto y Neto')
                ax.set_xlabel('ROI (%)')
                ax.set_ylabel('Densidad')
                ax.set_xlim(0, 50)
                ax.legend()
                st.pyplot(fig)
            else:
                st.info("No hay suficientes datos para mostrar la distribución de ROI.")


        elif ciudad_actual == "barcelona":
            st.subheader("Resumen General del Mercado Inmobiliario de Barcelona")
        
            # Métricas principales
            col1, col2, col3 = st.columns(3)
            col1.metric("Nº de anuncios", len(df_ciudad))
            
            if 'Net ROI (%)' in df_ciudad.columns:
                col2.metric("ROI Neto medio (%)", f"{df_ciudad['Net ROI (%)'].mean():.2f}")
            else:
                col2.metric("ROI Neto medio (%)", "N/A")
                
            if 'price' in df_ciudad.columns:
                col3.metric("Precio medio alquiler (€)", f"{df_ciudad['price'].mean():.2f}")
            else:
                col3.metric("Precio medio alquiler (€)", "N/A")
            
            # Distribución de ROI Bruto y Neto
            st.markdown("#### Distribución de ROI Bruto y Neto (%)")
            if len(df_ciudad) > 1 and 'ROI (%)' in df_ciudad.columns and 'Net ROI (%)' in df_ciudad.columns:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.kdeplot(df_ciudad['ROI (%)'], fill=True, label='ROI Bruto (%)', color='skyblue', bw_adjust=0.7, clip=(0, 50), ax=ax)
                sns.kdeplot(df_ciudad['Net ROI (%)'], fill=True, label='ROI Neto (%)', color='orange', bw_adjust=0.7, clip=(0, 50), ax=ax)
                ax.set_title('Distribución de ROI Bruto y Neto')
                ax.set_xlabel('ROI (%)')
                ax.set_ylabel('Densidad')
                ax.set_xlim(0, 50)
                ax.legend()
                st.pyplot(fig)
            
            # Mapa interactivo
            st.markdown("#### Mapa de Oportunidades en Barcelona")
            try:
                display_interactive_map("../docs/mapa_oportunidad_barcelona.html", "Mapa de Oportunidades en Barcelona")
            except:
                try:
                    display_interactive_map("../docs/barcelona_investment_map.html", "Mapa de Inversión en Barcelona")
                except:
                    st.warning("No se pudo cargar el mapa de oportunidades de Barcelona.")
            
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
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de tipo de alojamiento disponibles.")
        
        
        elif ciudad_actual == "malaga":
            st.subheader("Resumen General del Mercado Inmobiliario")
        
            col1, col2, col3 = st.columns(3)
            col1.metric("Nº de anuncios", len(df_ciudad))
            col2.metric("ROI Neto medio (%)", f"{df_ciudad['net_roi'].mean():.2f}")
            col3.metric("Precio medio alquiler (€)", f"{df_ciudad['price'].mean():.2f}")

            # KDE ROI Bruto y Neto
            st.markdown("#### Distribución de ROI Bruto y Neto (%)")
            if len(df_ciudad) > 1:
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.kdeplot(df_ciudad['roi'], fill=True, label='ROI Bruto (%)', color='skyblue', bw_adjust=0.7, clip=(0, 50), ax=ax)
                sns.kdeplot(df_ciudad['net_roi'], fill=True, label='ROI Neto (%)', color='orange', bw_adjust=0.7, clip=(0, 50), ax=ax)
                ax.set_title('Distribución de ROI Bruto y Neto')
                ax.set_xlabel('ROI (%)')
                ax.set_ylabel('Densidad')
                ax.set_xlim(0, 50)
                ax.legend()
                st.pyplot(fig)
            else:
                st.info("No hay suficientes datos para mostrar la distribución de ROI.")

        elif ciudad_actual == "madrid":
            st.info("Si la ciudad es Madrid añadir código aquí")

        else:
            st.info("No hay datos para mostrar en esta pestaña.")
else:
    st.warning("No hay pestañas disponibles para mostrar contenido.")


# ------------------ Pestaña 2: Precios de Vivienda ------------------
with main_tabs[1]:
    if ciudad_actual.lower() == "valencia":
        st.subheader("Precios de Vivienda por Barrio")
    
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
                st.plotly_chart(fig_precio, use_container_width=True)
            else:
                st.info("No hay datos de precios de vivienda para mostrar.")
        else:
            st.info("No hay datos de precios de vivienda para mostrar.")
    elif ciudad_actual.lower() == "malaga":
        st.subheader("Precios de Vivienda por Barrio")

        if 'price_per_m2' in df_malaga.columns:
            barrio_caros = df_malaga.groupby('neighbourhood')['price_per_m2'].mean().reset_index()
            barrio_caros = barrio_caros.sort_values(by='price_per_m2', ascending=False).head(15)
            if not barrio_caros.empty:
                fig_precio = px.bar(
                    barrio_caros,
                    x='price_per_m2',
                    y='neighbourhood',
                    orientation='h',
                    labels={'price_per_m2': 'Precio medio m2 de compra (€)', 'neighbourhood': 'Barrio'},
                    title='Top 15 barrios más caros por precio medio m2 de compra'
                )
                st.plotly_chart(fig_precio, use_container_width=True)
            else:
                st.info("No hay datos de precios de vivienda para mostrar.")
        else:
            st.info("No hay datos de precios de vivienda para mostrar.")
    elif ciudad_actual.lower() == "barcelona":
        st.subheader("Precios de Vivienda en Barcelona")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Estadísticas básicas de precios
            if 'price' in df_ciudad.columns:
                stats = df_ciudad['price'].describe()
                st.metric("Precio Medio por Noche", f"{stats['mean']:.2f}€")
                st.metric("Precio Mediano por Noche", f"{stats['50%']:.2f}€")
                st.metric("Precio Máximo", f"{stats['max']:.2f}€")
                
                # Histograma de precios
                fig = px.histogram(
                    df_ciudad, 
                    x='price',
                    nbins=50,
                    title='Distribución de Precios por Noche',
                    labels={'price': 'Precio (€)'},
                    range_x=[0, stats['75%'] * 2]  # Limitar el rango para mejor visualización
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de precios disponibles.")
        
        with col2:
            # Precios por tipo de habitación
            if 'price' in df_ciudad.columns and 'room_type' in df_ciudad.columns:
                fig = px.box(
                    df_ciudad,
                    x='room_type',
                    y='price',
                    title='Distribución de Precios por Tipo de Alojamiento',
                    labels={'price': 'Precio por Noche (€)', 'room_type': 'Tipo de Alojamiento'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Precio promedio por tipo de habitación
                avg_price_by_type = df_ciudad.groupby('room_type')['price'].mean().reset_index()
                fig = px.bar(
                    avg_price_by_type,
                    x='room_type',
                    y='price',
                    title='Precio Promedio por Tipo de Alojamiento',
                    labels={'price': 'Precio Promedio (€)', 'room_type': 'Tipo de Alojamiento'}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No hay datos de precios por tipo de habitación disponibles.")
        
        # Mapa de precios
        st.subheader("Distribución Geográfica de Precios")
        try:
            display_interactive_map("../docs/mapa_precio_barcelona.html", "Mapa de Precios en Barcelona")
        except:
            try:
                display_interactive_map("../docs/barcelona_category_map.html", "Mapa de Categorías de Precios en Barcelona")
            except:
                st.warning("No se pudo cargar el mapa de precios de Barcelona.")
        
        # Datos generales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Propiedades", f"{len(df_ciudad):,}")
            st.metric("Precio Medio por Noche", f"{df_ciudad['price'].mean():.2f}€")
        
        with col2:
            if 'room_type' in df_ciudad.columns:
                room_counts = df_ciudad['room_type'].value_counts()
                st.metric("Apartamentos Completos", f"{room_counts.get('Entire home/apt', 0):,}")
                st.metric("Habitaciones Privadas", f"{room_counts.get('Private room', 0):,}")
            else:
                st.info("No hay datos de tipos de habitación disponibles")
        
        with col3:
            if 'neighbourhood_group' in df_ciudad.columns:
                st.metric("Distritos", f"{df_ciudad['neighbourhood_group'].nunique()}")
            if 'neighbourhood' in df_ciudad.columns:
                st.metric("Barrios", f"{df_ciudad['neighbourhood'].nunique()}")
        
        # Mostrar mapa interactivo
        st.subheader("Distribución de Propiedades en Barcelona")
        try:
            display_interactive_map("../docs/barcelona_airbnb_map.html", "Mapa de Propiedades en Barcelona")
        except:
            try:
                display_interactive_map("../docs/mapa_propiedades_barcelona.html", "Mapa de Propiedades en Barcelona")
            except:
                st.warning("No se pudo cargar el mapa interactivo de Barcelona.")
        
        # Mostrar estadísticas adicionales
        st.subheader("Análisis de Mercado")
        col1, col2 = st.columns(2)
        
        with col1:
            if 'price' in df_ciudad.columns and 'room_type' in df_ciudad.columns:
                fig = px.box(df_ciudad, 
                             x='room_type', 
                             y='price', 
                             title='Distribución de Precios por Tipo de Alojamiento',
                             labels={'price': 'Precio por noche (€)', 'room_type': 'Tipo de Alojamiento'})
                fig.update_layout(xaxis_title='Tipo de Alojamiento', yaxis_title='Precio por noche (€)')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'neighbourhood_group' in df_ciudad.columns:
                fig = px.pie(df_ciudad, 
                             names='neighbourhood_group', 
                             title='Distribución de Propiedades por Distrito',
                             hole=0.4)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            elif 'neighbourhood' in df_ciudad.columns:
                top_barrios = df_ciudad['neighbourhood'].value_counts().head(10)
                fig = px.bar(top_barrios, 
                             title='Top 10 Barrios con Más Propiedades',
                             labels={'value': 'Número de Propiedades', 'index': 'Barrio'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar imagen de análisis estacional
        st.subheader("Análisis Estacional")
        try:
            display_image("../img/barcelona_heatmap_ocupacion.png", "Patrón de Ocupación Estacional en Barcelona")
        except:
            try:
                display_image("../img/barcelona_precio_ocupacion_mensual.png", "Patrón de Ocupación Mensual en Barcelona")
            except:
                st.warning("No se pudieron cargar las imágenes de análisis estacional.")
                
        # Mapa de calor de precios
        st.subheader("Distribución Geográfica de Precios")
        try:
            display_interactive_map("../docs/mapa_calor_precios_barcelona.html", "Mapa de Calor de Precios en Barcelona")
        except:
            try:
                display_interactive_map("../docs/barcelona_category_map.html", "Mapa de Categorías de Precios en Barcelona")
            except:
                st.warning("No se pudo cargar el mapa de calor de precios de Barcelona.")
    else:
        st.info("No hay datos para mostrar en esta pestaña.")

# ------------------ Pestaña 3: Rentabilidad por Barrio ------------------
if len(main_tabs) > 2:
    with main_tabs[2]:
        if ciudad_actual == "valencia":
            st.subheader("Rentabilidad por Barrio")

            if not df_ciudad.empty:
                # ROI neto por barrio
                roi_barrio = df_ciudad.groupby('neighbourhood')['Net ROI (%)'].mean().sort_values(ascending=False).head(15)
                if not roi_barrio.empty:
                    fig_roi = px.bar(
                        roi_barrio,
                        x=roi_barrio.values,
                        y=roi_barrio.index,
                        orientation='h',
                        labels={'x': 'ROI Neto (%)', 'y': 'Barrio'},
                        title='Top 15 barrios por ROI Neto (%)'
                    )
                    st.plotly_chart(fig_roi, use_container_width=True)
                else:
                    st.info("No hay datos de ROI Neto para mostrar.")

                # ROI bruto por barrio
                roi_barrio_bruto = df_ciudad.groupby('neighbourhood')['ROI (%)'].mean().sort_values(ascending=False).head(15)
                if not roi_barrio_bruto.empty:
                    fig_roi_bruto = px.bar(
                        roi_barrio_bruto,
                        x=roi_barrio_bruto.values,
                        y=roi_barrio_bruto.index,
                        orientation='h',
                        labels={'x': 'ROI Bruto (%)', 'y': 'Barrio'},
                        title='Top 15 barrios por ROI Bruto (%)'
                    )
                    st.plotly_chart(fig_roi_bruto, use_container_width=True)
                else:
                    st.info("No hay datos de ROI Bruto para mostrar.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")
        elif ciudad_actual == "malaga":
            st.subheader("Rentabilidad por Barrio")

            if not df_ciudad.empty:
                # ROI neto por barrio (Málaga)
                roi_barrio = df_ciudad.groupby('neighbourhood')['net_roi'].mean().sort_values(ascending=False).head(15)
                if not roi_barrio.empty:
                    fig_roi = px.bar(
                        roi_barrio,
                        x=roi_barrio.values,
                        y=roi_barrio.index,
                        orientation='h',
                        labels={'x': 'ROI Neto (%)', 'y': 'Barrio'},
                        title='Top 15 barrios por ROI Neto (%)'
                    )
                    st.plotly_chart(fig_roi, use_container_width=True)
                else:
                    st.info("No hay datos de ROI Neto para mostrar.")

                # ROI bruto por barrio (Málaga)
                roi_barrio_bruto = df_ciudad.groupby('neighbourhood')['roi'].mean().sort_values(ascending=False).head(15)
                if not roi_barrio_bruto.empty:
                    fig_roi_bruto = px.bar(
                        roi_barrio_bruto,
                        x=roi_barrio_bruto.values,
                        y=roi_barrio_bruto.index,
                        orientation='h',
                        labels={'x': 'ROI Bruto (%)', 'y': 'Barrio'},
                        title='Top 15 barrios por ROI Bruto (%)'
                    )
                    st.plotly_chart(fig_roi_bruto, use_container_width=True)
                else:
                    st.info("No hay datos de ROI Bruto para mostrar.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")

        elif ciudad_actual == "barcelona":
            st.subheader("Rentabilidad por Barrio en Barcelona")

            if not df_ciudad.empty:
                # ROI neto por barrio (Barcelona)
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
                        st.plotly_chart(fig_roi, use_container_width=True)
                    else:
                        st.info("No hay datos de ROI Neto para mostrar.")
                else:
                    st.info("No hay columnas de ROI Neto o barrio en los datos.")

                # ROI bruto por barrio (Barcelona)
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
                        st.plotly_chart(fig_roi_bruto, use_container_width=True)
                    else:
                        st.info("No hay datos de ROI Bruto para mostrar.")
                else:
                    st.info("No hay columnas de ROI Bruto o barrio en los datos.")
                
                # Mapa de rentabilidad
                st.markdown("#### Mapa de Rentabilidad")
                try:
                    display_interactive_map("../docs/barcelona_roi_by_type_map.html", "Mapa de ROI por Tipo de Alojamiento")
                except:
                    try:
                        display_interactive_map("../docs/barcelona_breakeven_map.html", "Mapa de Punto de Equilibrio")
                    except:
                        st.warning("No se pudo cargar el mapa de rentabilidad de Barcelona.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")
        else:
            st.info("No hay datos para mostrar en esta pestaña.")
else:
     st.warning("No hay pestañas disponibles para mostrar contenido.")



# ------------------ Pestaña 4: Competencia y Demanda ------------------
if len(main_tabs) > 3:
    with main_tabs[3]:
        if ciudad_actual == "valencia":
            st.subheader("Competencia y Demanda por Barrio")

            if not df_ciudad.empty:
                # Competencia por barrio
                competencia_por_barrio = df_ciudad.groupby('neighbourhood')['id'].count().reset_index().rename(columns={'id': 'n_anuncios'})
                top_comp = competencia_por_barrio.sort_values(by='n_anuncios', ascending=False).head(15)
                if not top_comp.empty:
                    fig_comp = px.bar(
                        top_comp,
                        x='n_anuncios',
                        y='neighbourhood',
                        orientation='h',
                        labels={'n_anuncios': 'Nº de anuncios', 'neighbourhood': 'Barrio'},
                        title='Top 15 barrios con más competencia (nº de anuncios)'
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)
                else:
                    st.info("No hay datos de competencia para mostrar.")

                # Anuncios activos (>30 días alquilados/año)
                if 'days_rented' in df_ciudad.columns:
                    activos = df_ciudad[df_ciudad['days_rented'] > 30]
                    competencia_activa = activos.groupby('neighbourhood')['id'].count().reset_index().rename(columns={'id': 'n_anuncios_activos'})
                    top_activos = competencia_activa.sort_values(by='n_anuncios_activos', ascending=False).head(15)
                    if not top_activos.empty:
                        fig_activos = px.bar(
                            top_activos,
                            x='n_anuncios_activos',
                            y='neighbourhood',
                            orientation='h',
                            labels={'n_anuncios_activos': 'Nº de anuncios activos', 'neighbourhood': 'Barrio'},
                            title='Top 15 barrios con más anuncios activos (>30 días alquilados/año)'
                        )
                        st.plotly_chart(fig_activos, use_container_width=True)
                    else:
                        st.info("No hay datos de anuncios activos para mostrar.")
                else:
                    st.info("No hay datos de días alquilados para mostrar anuncios activos.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")

        elif ciudad_actual == "malaga":
            st.subheader("Competencia y Demanda por Barrio")

            if not df_ciudad.empty:
                # Competencia por barrio (Málaga)
                competencia_por_barrio = df_ciudad.groupby('neighbourhood')['id'].count().reset_index().rename(columns={'id': 'n_anuncios'})
                top_comp = competencia_por_barrio.sort_values(by='n_anuncios', ascending=False).head(15)
                if not top_comp.empty:
                    fig_comp = px.bar(
                        top_comp,
                        x='n_anuncios',
                        y='neighbourhood',
                        orientation='h',
                        labels={'n_anuncios': 'Nº de anuncios', 'neighbourhood': 'Barrio'},
                        title='Top 15 barrios con más competencia (nº de anuncios)'
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)
                else:
                    st.info("No hay datos de competencia para mostrar.")

                # Anuncios activos (>150 días ocupados/año, usando estimated_occupancy_l365d)
                if 'estimated_occupancy_l365d' in df_ciudad.columns:
                    activos = df_ciudad[df_ciudad['estimated_occupancy_l365d'] > 150]
                    competencia_activa = activos.groupby('neighbourhood')['id'].count().reset_index().rename(columns={'id': 'n_anuncios_activos'})
                    top_activos = competencia_activa.sort_values(by='n_anuncios_activos', ascending=False).head(15)
                    if not top_activos.empty:
                        fig_activos = px.bar(
                            top_activos,
                            x='n_anuncios_activos',
                            y='neighbourhood',
                            orientation='h',
                            labels={'n_anuncios_activos': 'Nº de anuncios activos', 'neighbourhood': 'Barrio'},
                            title='Top 15 barrios con más anuncios activos (>150 días ocupados/año)'
                        )
                        st.plotly_chart(fig_activos, use_container_width=True)
                    else:
                        st.info("No hay datos de anuncios activos para mostrar.")
                else:
                    st.info("No hay datos de ocupación estimada para mostrar anuncios activos.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")


        elif ciudad_actual == "barcelona":
            st.subheader("Competencia y Demanda en Barcelona")

            if not df_ciudad.empty:
                # Competencia por barrio
                competencia_por_barrio = df_ciudad.groupby('neighbourhood')['id'].count().reset_index().rename(columns={'id': 'n_anuncios'})
                top_comp = competencia_por_barrio.sort_values(by='n_anuncios', ascending=False).head(15)
                if not top_comp.empty:
                    fig_comp = px.bar(
                        top_comp,
                        x='n_anuncios',
                        y='neighbourhood',
                        orientation='h',
                        labels={'n_anuncios': 'Nº de anuncios', 'neighbourhood': 'Barrio'},
                        title='Top 15 barrios con más competencia (nº de anuncios)'
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)
                else:
                    st.info("No hay datos de competencia para mostrar.")

                # Mapa de competencia
                st.subheader("Mapa de Densidad de Alojamientos")
                try:
                    display_interactive_map("../docs/barcelona_airbnb_map.html", "Mapa de Densidad de Alojamientos")
                except:
                    st.warning("No se pudo cargar el mapa de densidad de alojamientos.")
                
                # Análisis de reseñas (demanda)
                st.subheader("Análisis de Reseñas y Demanda")
                
                if 'number_of_reviews' in df_ciudad.columns and 'last_review' in df_ciudad.columns:
                    # Barrios con más reseñas
                    reviews_por_barrio = df_ciudad.groupby('neighbourhood')['number_of_reviews'].sum().reset_index()
                    top_reviews = reviews_por_barrio.sort_values(by='number_of_reviews', ascending=False).head(15)
                    
                    if not top_reviews.empty:
                        fig_reviews = px.bar(
                            top_reviews,
                            x='number_of_reviews',
                            y='neighbourhood',
                            orientation='h',
                            labels={'number_of_reviews': 'Número de reseñas', 'neighbourhood': 'Barrio'},
                            title='Top 15 barrios con más reseñas (indicador de demanda)'
                        )
                        st.plotly_chart(fig_reviews, use_container_width=True)
                    
                    # Mapa de reseñas
                    try:
                        display_interactive_map("../docs/barcelona_reviews_map.html", "Mapa de Reseñas")
                    except:
                        st.warning("No se pudo cargar el mapa de reseñas.")
                    
                    # Distribución temporal de reseñas
                    try:
                        display_image("../img/barcelona_reviews_evolution.png", "Evolución temporal de reseñas en Barcelona")
                    except:
                        try:
                            display_image("../img/barcelona_horizonte_reservas.png", "Horizonte de reservas en Barcelona")
                        except:
                            st.warning("No se pudo cargar la imagen de evolución de reseñas.")
                
                # Ocupación estimada por barrio
                if 'days_rented' in df_ciudad.columns:
                    ocupacion_por_barrio = df_ciudad.groupby('neighbourhood')['days_rented'].mean().reset_index()
                    top_ocupacion = ocupacion_por_barrio.sort_values(by='days_rented', ascending=False).head(15)
                    
                    if not top_ocupacion.empty:
                        fig_ocupacion = px.bar(
                            top_ocupacion,
                            x='days_rented',
                            y='neighbourhood',
                            orientation='h',
                            labels={'days_rented': 'Días ocupados promedio', 'neighbourhood': 'Barrio'},
                            title='Top 15 barrios con mayor ocupación estimada'
                        )
                        st.plotly_chart(fig_ocupacion, use_container_width=True)
                    
                    # Patrón semanal de ocupación
                    try:
                        display_image("../img/barcelona_precio_ocupacion_diasemana.png", "Patrón de ocupación semanal en Barcelona")
                    except:
                        st.warning("No se pudo cargar la imagen de patrón semanal de ocupación.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")

        else:
            st.info("No hay datos para mostrar en esta pestaña.")
else:
     st.warning("No hay pestañas disponibles para mostrar contenido.")


# ------------------ Pestaña 5: Análisis Avanzado ------------------
if len(main_tabs) > 4:
    with main_tabs[4]:
        if ciudad_actual.lower() == "valencia":
            st.subheader("Análisis Avanzado")
        
            if not df_valencia.empty:
                # Relación entre precio medio de alquiler y ROI neto por barrio
                st.markdown("#### Relación entre precio medio de alquiler y ROI neto por barrio")
                if 'city' in df_valencia.columns and df_valencia['city'].str.lower().nunique() == 1 and df_valencia['city'].str.lower().iloc[0] == 'valencia':
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
                        st.plotly_chart(fig_val, use_container_width=True)
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
                        st.plotly_chart(fig_scatter, use_container_width=True)
                    else:
                        st.info("No hay datos para mostrar la relación entre precio y ROI.")

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
                        st.plotly_chart(fig_amenities, use_container_width=True)
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
                        st.plotly_chart(fig_resenas, use_container_width=True)
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
                        st.plotly_chart(fig_hab, use_container_width=True)
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
                    st.plotly_chart(fig_hist, use_container_width=True)
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
                    st.plotly_chart(fig_box, use_container_width=True)
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
                    st.plotly_chart(fig_hist_roi, use_container_width=True)
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
                    st.plotly_chart(fig_box_roi, use_container_width=True)
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
                    st.plotly_chart(fig_hist_days, use_container_width=True)
                else:
                    st.info("No hay datos de días alquilados para mostrar histograma.")

                # Boxplot de días alquilados por barrio (solo top 15 barrios)
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
                    st.plotly_chart(fig_box_days, use_container_width=True)
                else:
                    st.info("No hay datos de días alquilados para mostrar boxplot.")

                # Mapa de puntos de los anuncios (si hay lat/lon)
                st.markdown("#### Mapa de anuncios")
                if 'latitude' in df_valencia.columns and 'longitude' in df_valencia.columns:
                    st.map(df_valencia[['latitude', 'longitude']].dropna())
                else:
                    st.info("No hay datos de localización para mostrar el mapa.")

                # Delincuencia: Gráfico de barras agrupadas y heatmap
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

        elif ciudad_actual.lower() == "malaga":
            st.subheader("Análisis Avanzado")

            if not df_malaga.empty:
                # Relación entre precio medio de alquiler y ROI neto por barrio
                st.markdown("#### Relación entre precio medio de alquiler y ROI neto por barrio")
                if 'price' in df_malaga.columns and 'net_roi' in df_malaga.columns:
                    fig_malaga = px.scatter(
                        df_malaga,
                        x='price',
                        y='net_roi',
                        color='neighbourhood',
                        hover_data=['neighbourhood'],
                        opacity=0.6,
                        labels={'price': 'Precio alquiler (€)', 'net_roi': 'ROI Neto (%)', 'neighbourhood': 'Barrio'},
                        title='Relación entre precio de alquiler y ROI neto por barrio (Málaga)'
                    )
                    fig_malaga.update_traces(marker=dict(size=10, line=dict(width=1, color='DarkSlateGrey')))
                    fig_malaga.update_layout(
                        legend_title_text='Barrio',
                        showlegend=False,
                        height=500,
                        margin=dict(l=40, r=40, t=60, b=40)
                    )
                    st.plotly_chart(fig_malaga, use_container_width=True)
                else:
                    st.info("No hay datos suficientes para mostrar el gráfico de dispersión para Málaga.")

                # Número medio de amenities por barrio
                st.markdown("#### Top 15 barrios por número medio de amenities")
                if 'amenities' in df_malaga.columns:
                    # Convertir string de lista a lista real si es necesario
                    if df_malaga['amenities'].apply(lambda x: isinstance(x, str) and x.startswith('[')).all():
                        df_malaga['n_amenities'] = df_malaga['amenities'].apply(lambda x: len(eval(x)) if pd.notnull(x) else 0)
                    else:
                        df_malaga['n_amenities'] = df_malaga['amenities'].str.count(',') + 1
                    barrio_amenities = df_malaga.groupby('neighbourhood')['n_amenities'].mean().reset_index()
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
                        st.plotly_chart(fig_amenities, use_container_width=True)
                    else:
                        st.info("No hay datos de amenities para mostrar.")
                else:
                    st.info("No hay datos de amenities para mostrar.")

                # Número total de reseñas por barrio
                st.markdown("#### Top 15 barrios por número total de reseñas")
                if 'number_of_reviews' in df_malaga.columns:
                    barrio_mas_resenas = df_malaga.groupby('neighbourhood')['number_of_reviews'].sum().reset_index()
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
                        st.plotly_chart(fig_resenas, use_container_width=True)
                    else:
                        st.info("No hay datos de reseñas para mostrar.")
                else:
                    st.info("No hay datos de reseñas para mostrar.")

                # Habitaciones y baños por barrio
                st.markdown("#### Top 15 barrios por número medio de habitaciones y baños")
                if 'bedrooms' in df_malaga.columns and 'bathrooms' in df_malaga.columns:
                    barrio_habitaciones_banos = df_malaga.groupby('neighbourhood').agg({
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
                        st.plotly_chart(fig_hab, use_container_width=True)
                    else:
                        st.info("No hay datos de habitaciones para mostrar.")
                else:
                    st.info("No hay datos de habitaciones o baños para mostrar.")

                # Histograma de precios de alquiler
                st.markdown("#### Histograma de precios de alquiler")
                if 'price' in df_malaga.columns:
                    fig_hist = px.histogram(
                        df_malaga, x='price', nbins=40, color='neighbourhood',
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
                    st.plotly_chart(fig_hist, use_container_width=True)
                else:
                    st.info("No hay datos de precios para mostrar histograma.")

                # Boxplot de precios de alquiler por barrio (solo top 15 barrios)
                st.markdown("#### Boxplot de precios de alquiler por barrio (Top 15)")
                if 'price' in df_malaga.columns:
                    top_barrios = df_malaga['neighbourhood'].value_counts().head(15).index
                    df_top = df_malaga[df_malaga['neighbourhood'].isin(top_barrios)]
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
                    st.plotly_chart(fig_box, use_container_width=True)
                else:
                    st.info("No hay datos de precios para mostrar boxplot.")

                # Histograma de ROI Neto
                st.markdown("#### Histograma de ROI Neto (%)")
                if 'net_roi' in df_malaga.columns:
                    fig_hist_roi = px.histogram(
                        df_malaga, x='net_roi', nbins=40, color='neighbourhood',
                        labels={'net_roi': 'ROI Neto (%)'},
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
                    st.plotly_chart(fig_hist_roi, use_container_width=True)
                else:
                    st.info("No hay datos de ROI Neto para mostrar histograma.")

                # Boxplot de ROI Neto por barrio (solo top 15 barrios)
                st.markdown("#### Boxplot de ROI Neto por barrio (Top 15)")
                if 'net_roi' in df_malaga.columns:
                    top_barrios = df_malaga['neighbourhood'].value_counts().head(15).index
                    df_top = df_malaga[df_malaga['neighbourhood'].isin(top_barrios)]
                    fig_box_roi = px.box(
                        df_top, x='neighbourhood', y='net_roi', points='outliers',
                        labels={'net_roi': 'ROI Neto (%)', 'neighbourhood': 'Barrio'},
                        title='Boxplot de ROI Neto por barrio (Top 15)'
                    )
                    fig_box_roi.update_layout(
                        height=500,
                        margin=dict(l=40, r=40, t=60, b=40),
                        xaxis=dict(tickangle=45, tickfont=dict(size=12)),
                        yaxis=dict(tickfont=dict(size=12))
                    )
                    st.plotly_chart(fig_box_roi, use_container_width=True)
                else:
                    st.info("No hay datos de ROI Neto para mostrar boxplot.")

                # Histograma de ocupación estimada
                st.markdown("#### Histograma de ocupación estimada (días al año)")
                if 'estimated_occupancy_l365d' in df_malaga.columns:
                    fig_hist_days = px.histogram(
                        df_malaga, x='estimated_occupancy_l365d', nbins=40, color='neighbourhood',
                        labels={'estimated_occupancy_l365d': 'Días ocupados'},
                        title='Distribución de días ocupados por barrio',
                        opacity=0.7
                    )
                    fig_hist_days.update_layout(
                        height=400,
                        margin=dict(l=40, r=40, t=60, b=40),
                        xaxis=dict(tickfont=dict(size=12)),
                        yaxis=dict(tickfont=dict(size=12)),
                        barmode='overlay'
                    )
                    st.plotly_chart(fig_hist_days, use_container_width=True)
                else:
                    st.info("No hay datos de ocupación estimada para mostrar histograma.")

                # Boxplot de ocupación estimada por barrio (solo top 15 barrios)
                st.markdown("#### Boxplot de ocupación estimada por barrio (Top 15)")
                if 'estimated_occupancy_l365d' in df_malaga.columns:
                    top_barrios = df_malaga['neighbourhood'].value_counts().head(15).index
                    df_top = df_malaga[df_malaga['neighbourhood'].isin(top_barrios)]
                    fig_box_days = px.box(
                        df_top, x='neighbourhood', y='estimated_occupancy_l365d', points='outliers',
                        labels={'estimated_occupancy_l365d': 'Días ocupados', 'neighbourhood': 'Barrio'},
                        title='Boxplot de días ocupados por barrio (Top 15)'
                    )
                    fig_box_days.update_layout(
                        height=500,
                        margin=dict(l=40, r=40, t=60, b=40),
                        xaxis=dict(tickangle=45, tickfont=dict(size=12)),
                        yaxis=dict(tickfont=dict(size=12))
                    )
                    st.plotly_chart(fig_box_days, use_container_width=True)
                else:
                    st.info("No hay datos de ocupación estimada para mostrar boxplot.")

                # Mapa de puntos de los anuncios (si hay lat/lon)
                st.markdown("#### Mapa de anuncios")
                if 'latitude' in df_malaga.columns and 'longitude' in df_malaga.columns:
                    st.map(df_malaga[['latitude', 'longitude']].dropna())
                else:
                    st.info("No hay datos de localización para mostrar el mapa.")

                # Delincuencia: Gráfico de barras agrupadas y heatmap
                st.markdown("#### Delitos denunciados en Málaga por año")
                if df_malaga_crimen is not None and not df_malaga_crimen.empty:
                    if 'crime_type' in df_malaga_crimen.columns and 'year' in df_malaga_crimen.columns and 'reported_cases' in df_malaga_crimen.columns:
                        df_malaga_crimen_filtrado = df_malaga_crimen.copy()
                        fig, ax = plt.subplots(figsize=(14, 7))
                        sns.barplot(
                            data=df_malaga_crimen_filtrado,
                            x='year',
                            y='reported_cases',
                            hue='crime_type',
                            ax=ax
                        )
                        ax.set_title('Delitos denunciados en Málaga por año')
                        ax.set_ylabel('Número de denuncias')
                        ax.set_xlabel('Año')
                        ax.legend(title='Tipo de delito', bbox_to_anchor=(1.05, 1), loc='upper left')
                        plt.tight_layout()
                        st.pyplot(fig)

                        st.markdown("#### Mapa de calor de delitos denunciados en Málaga por tipo y año")
                        fig2, ax2 = plt.subplots(figsize=(14, 7))
                        heatmap_data = df_malaga_crimen_filtrado.pivot_table(
                            index='crime_type',
                            columns='year',
                            values='reported_cases',
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
                        ax2.set_title('Mapa de calor de delitos denunciados en Málaga por tipo y año')
                        ax2.set_xlabel('Año')
                        ax2.set_ylabel('Tipo de delito')
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        st.pyplot(fig2)
                    else:
                        st.info("No hay columnas adecuadas de delincuencia para mostrar.")
                else:
                    st.info("No hay datos de delincuencia para mostrar.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")

        elif ciudad_actual.lower() == "barcelona":
            st.subheader("Análisis Avanzado de Barcelona")

            if not df_ciudad.empty:
                # Correlaciones entre variables clave
                st.markdown("#### Correlaciones entre variables de inversión")
                try:
                    display_image("../img/correlaciones_inversion_barcelona.png", "Matriz de correlaciones de variables de inversión")
                except:
                    st.warning("No se pudo cargar la imagen de correlaciones.")

                # Relación entre precio y calificaciones
                st.markdown("#### Relación entre precio y calificaciones")
                if 'price' in df_ciudad.columns and 'review_scores_rating' in df_ciudad.columns:
                    fig = px.scatter(
                        df_ciudad,
                        x='price',
                        y='review_scores_rating',
                        color='room_type',
                        title='Relación entre precio y calificación',
                        labels={'price': 'Precio (€)', 'review_scores_rating': 'Calificación (0-100)', 'room_type': 'Tipo de habitación'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    try:
                        display_image("../img/barcelona_rating_reviews_relationship.png", "Relación entre precio y calificaciones")
                    except:
                        st.warning("No se pudieron cargar datos de calificaciones.")
                
                # Análisis de reseñas
                st.markdown("#### Análisis de Reseñas")
                try:
                    display_image("../img/barcelona_review_scores_analysis.png", "Análisis de calificaciones por categoría")
                except:
                    st.warning("No se pudo cargar la imagen de análisis de reseñas.")
                
                # Perfiles de inversión
                st.markdown("#### Perfiles de Inversión")
                try:
                    display_image("../img/perfiles_inversion_barcelona.png", "Perfiles de inversión en Barcelona")
                except:
                    st.warning("No se pudo cargar la imagen de perfiles de inversión.")
                
                # Mapas avanzados
                st.markdown("#### Mapas de Análisis Avanzado")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    try:
                        display_interactive_map("../docs/mapa_perfiles_barcelona.html", "Mapa de Perfiles de Inversión")
                    except:
                        st.warning("No se pudo cargar el mapa de perfiles de inversión.")
                
                with col2:
                    try:
                        display_interactive_map("../docs/mapa_correlaciones_barcelona.html", "Mapa de Correlaciones")
                    except:
                        st.warning("No se pudo cargar el mapa de correlaciones.")
                
                # Análisis estacional
                st.markdown("#### Análisis Estacional")
                try:
                    display_image("../img/barcelona_estacionalidad_premium.png", "Estacionalidad en Barcelona")
                except:
                    try:
                        display_interactive_map("../docs/barcelona_seasonal_map.html", "Mapa Estacional")
                    except:
                        st.warning("No se pudo cargar el análisis estacional.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")
        else:
            st.info("No hay datos para mostrar en esta pestaña.")

# ------------------ Pestaña 6: Conclusiones ------------------
# ------------------ Pestaña 6: Conclusiones ------------------
def mostrar_conclusiones(ciudad_actual, ciudad_seleccionada):
    st.subheader(f"Conclusiones para Invertir en {ciudad_seleccionada}")

    if ciudad_actual.lower() == "valencia":
        st.markdown("""
        El análisis exhaustivo de los datos de rentabilidad, competencia, demanda, precios y características de los barrios de Valencia permite extraer recomendaciones más precisas y accionables para empresas que buscan invertir en el mercado de alquiler turístico:

        **Rentabilidad y retorno de inversión:** Los barrios líderes en rentabilidad neta y bruta, como Ciutat Universitaria, Cami Fondo, Penya-Roja y La Roqueta, ofrecen retornos superiores al promedio de la ciudad. Sin embargo, la diferencia entre rentabilidad bruta y neta es relativamente baja en los barrios más rentables, lo que indica una estructura de costes eficiente y un mercado consolidado.

        **Demanda sostenida y visibilidad:** Barrios como Cabanyal-Canyamelar, Russafa y El Mercat destacan por su alto volumen de reseñas totales y mensuales, reflejando una demanda turística constante y una elevada rotación de huéspedes. Invertir en estas zonas garantiza visibilidad y ocupación, aunque implica enfrentarse a una competencia intensa.

        **Competencia y saturación:** La saturación de anuncios es especialmente alta en barrios turísticos y céntricos. Para destacar en estos mercados, es fundamental apostar por la diferenciación, la calidad del alojamiento y la experiencia del huésped. Por otro lado, existen barrios con alta rentabilidad y baja competencia (menor número de anuncios), que representan oportunidades para captar reservas con menor riesgo de saturación.

        **Calidad, amenities y tamaño de la vivienda:** Los barrios con mayor número medio de amenities y viviendas más espaciosas tienden a lograr mejores valoraciones y mayor rentabilidad. La inversión en equipamiento y servicios adicionales puede ser clave para maximizar ingresos y diferenciarse en mercados competitivos.

        **Recomendación estratégica:**  
        La mejor estrategia combina la selección de barrios con alta rentabilidad neta, demanda sostenida y competencia controlada, junto con una apuesta por la calidad, el equipamiento y la diferenciación. Diversificar la cartera en diferentes zonas y perfiles de barrio permite equilibrar riesgo y retorno. Además, es clave realizar un seguimiento continuo de los indicadores clave del mercado y adaptar la oferta a las tendencias y preferencias de los huéspedes.
        """)

    elif ciudad_actual.lower() == "malaga":
        st.markdown("""
            El análisis de los datos de Málaga revela oportunidades y retos clave para empresas interesadas en el alquiler turístico:

            **Rentabilidad y retorno de inversión:** Los barrios con mayor ROI neto, como Bailen-Miraflores, Churriana y Puerto de la Torre, destacan por ofrecer retornos superiores a la media de la ciudad. La diferencia entre ROI bruto y neto suele ser moderada, lo que indica una estructura de costes razonable en las zonas más rentables.

            **Demanda y ocupación:** Barrios céntricos y turísticos presentan una alta ocupación estimada y un volumen elevado de reseñas, lo que refleja una demanda sostenida. Sin embargo, la competencia también es intensa en estas zonas, por lo que la diferenciación y la calidad del alojamiento son fundamentales para captar huéspedes.

            **Competencia y saturación:** La saturación de anuncios es elevada en el centro y zonas costeras. Existen barrios con buena rentabilidad y menor competencia, que pueden ser atractivos para nuevas inversiones con menor riesgo de saturación.

            **Seguridad:** El análisis de datos de criminalidad indica que la seguridad varía entre barrios y puede influir en la percepción de los huéspedes y la rentabilidad. Es recomendable considerar este factor en la selección de zonas para invertir.

            **Recomendación estratégica:**  
            La estrategia óptima combina la selección de barrios con alta rentabilidad neta, demanda sostenida y competencia controlada, junto con una apuesta por la calidad, el equipamiento y la diferenciación. Diversificar la inversión en diferentes zonas y perfiles de barrio ayuda a equilibrar riesgo y retorno. Es fundamental monitorizar la evolución del mercado, la normativa local y los indicadores de seguridad para adaptar la oferta a las tendencias y preferencias de los huéspedes.
            """)

      
    elif ciudad_actual.lower() == 'barcelona':
        st.markdown("""
            # Análisis Estratégico por Barrios de Barcelona 🏙️
            ## Tabla Comparativa de Barrios
            | Barrio | ROI Neto (%) | ROI Bruto (%) | Competencia | Estrategia Recomendada | Justificación |
            |---|---|---|---|---|---|
            | 🏮 El Raval | 11.2 | 14.5 | 387 | 🌟 Diferenciación | Alta competencia pero retorno superior. Invertir en calidad y experiencias únicas para destacar. |
            | 🌆 Poble Sec | 10.8 | 13.9 | 245 | ⚙️ Optimización | Buena relación rentabilidad/competencia. Maximizar amenities y optimizar precios por temporada. |
            | 🥘 Sant Antoni | 9.7 | 12.8 | 198 | 📈 Expansión | Emergente con demanda creciente. Momento ideal para adquirir propiedades antes del incremento de precios. |
            | 🚂 Sants | 9.5 | 12.3 | 176 | ⚖️ Equilibrio | Rentabilidad estable con competencia moderada. Equilibrar precio y calidad para maximizar ocupación. |
            | 🏘️ Hostafrancs | 9.3 | 12.1 | 89 | 💎 Oportunidad | Alta rentabilidad con baja competencia. Excelente oportunidad para nuevos inversores. |
            | 🏛️ Sagrada Família | 8.9 | 11.8 | 412 | 👑 Premium | Alta demanda turística. Estrategia de precio premium con servicios de alta calidad. |
            | 🎭 Gràcia | 8.7 | 11.5 | 356 | 🎨 Autenticidad | Atractivo cultural distintivo. Enfatizar experiencia local auténtica para atraer viajeros experimentados. |
            | 🏺 Sant Pere | 8.4 | 11.2 | 267 | 🔨 Renovación | Potencial de revalorización. Invertir en renovaciones para aumentar categoría y tarifa. |
            | 🏢 El Fort Pienc | 8.1 | 10.9 | 124 | 💰 Valor | Buena relación calidad-precio. Enfocarse en viajeros que buscan optimizar presupuesto sin sacrificar ubicación. |
            | 🌳 La Nova Esquerra | 7.8 | 10.5 | 185 | 🔄 Diversificación | Equilibrio entre variables. Ideal para diversificar cartera con riesgo moderado. |
            
            ## Variables Utilizadas para el Cálculo de Estrategias
            **ROI Neto (%)**: Rentabilidad neta anual calculada como: - Ingresos netos después de gastos operativos / Inversión total × 100 - Los gastos operativos incluyen: impuestos, mantenimiento, servicios, comisiones de plataforma y gestión.
            **ROI Bruto (%)**: Rentabilidad bruta anual calculada como: - Ingresos brutos / Inversión total × 100
            **Competencia**: Número de anuncios activos en el barrio, indicando saturación del mercado.
            **Ocupación Media**: Porcentaje de días al año que la propiedad está alquilada.
            **Precio Medio por Noche**: Tarifa promedio que se puede cobrar en el barrio.
            **Valoraciones de Huéspedes**: Puntuación media recibida por propiedades en el barrio.
            **Índice de Estacionalidad**: Variación de ocupación y precios entre temporada alta y baja.
            **Precio de Adquisición**: Coste medio de compra por m² en el barrio.
            
            ## Explicación de Estrategias
            ### 🌟 Diferenciación
            **Aplicable a**: El Raval, barrios con alta competencia pero buen ROI. **Enfoque**: Crear propiedades que destaquen.
            ### ⚙️ Optimización
            **Aplicable a**: Poble Sec, barrios con buen equilibrio. **Enfoque**: Maximizar rendimiento mediante gestión eficiente.
            ### 📈 Expansión
            **Aplicable a**: Sant Antoni, barrios emergentes. **Enfoque**: Aprovechar crecimiento antes de la saturación.
            """)
        st.markdown("---")
        
        try:
            display_interactive_map("../docs/mapa_completo_post_prohibicion_barcelona.html", "Recomendaciones Estratégicas Post-Prohibición")
        except:
            st.warning("No se pudo cargar el mapa de recomendaciones estratégicas.")
        
        st.markdown("---")

        st.markdown("""
            # Análisis del Impacto de la Prohibición del Alquiler Turístico en Barcelona 2028
            ## Escenario de Prohibición
            Barcelona ha anunciado la eliminación de **10,000 licencias de alquiler turístico** para 2028, una medida sin precedentes que transformará radicalmente el mercado inmobiliario de la ciudad. Esta prohibición busca recuperar vivienda para uso residencial y frenar la gentrificación en barrios centrales.
            
            ## Impacto Proyectado en el Mercado
            | 📊 Indicador | 🔴 Escenario Prohibición Total | 🟠 Escenario Restricción Parcial | 🟢 Escenario Regulación Moderada |
            |---|---|---|---|
            | Oferta legal | ↓ 80-100% | ↓ 40-60% | ↓ 20-30% |
            | Precios alquiler residencial | ↓ 10-15% | ↓ 5-8% | ↓ 2-4% |
            | ROI inversión turística | ↓ 100% (eliminación) | ↓ 30-50% | ↓ 15-25% |
            | Valor licencias restantes | ↑ 300-400% | ↑ 100-150% | ↑ 30-50% |
            | Mercado ilegal | ↑ 40-60% | ↑ 20-30% | ↑ 5-10% |
            
            ## Estrategias para Inversores
            ### 1. 🔄 Adaptación Anticipada
            - ✅ Reconvertir propiedades turísticas a residenciales antes de la saturación del mercado
            - 🔍 Adquirir propiedades con licencias que sobrevivirán (categorías premium o históricas)
            
            ## Escenarios Alternativos y Estrategias
            | 📋 Escenario | 📈 Probabilidad | 💼 Estrategia Recomendada | 🔍 Señales de Alerta |
            |---|---|---|---|
            | **Prohibición Total** | 60% | Reconversión inmediata a alquiler tradicional | Aprobación definitiva del plan en pleno municipal |
            | **Restricción por Zonas** | 25% | Concentrar inversiones en áreas permitidas | Publicación de mapas de zonificación específicos |
            | **Moratoria Extendida** | 10% | Mantener posiciones con licencia válida | Ampliación de plazos en comunicados oficiales |
            | **Marcha Atrás** | 5% | Mantener cartera diversificada | Cambios políticos o presión judicial significativa |
            """)
    
    else:
        st.info(f"Conclusiones para {ciudad_seleccionada} no implementadas.")

if len(main_tabs) > 5:
    with main_tabs[5]:
        mostrar_conclusiones(ciudad_actual, ciudad_seleccionada)

# ------------------ Descargable ------------------
def mostrar_datos_descargables(df_ciudad, ciudad_actual):
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

mostrar_datos_descargables(df_ciudad, ciudad_actual)



# ------------ Información del dashboard ------------
st.sidebar.markdown("---")
st.sidebar.info("""
**Acerca de este Panel**

Este panel muestra datos del mercado inmobiliario de Valencia, Málaga, Madrid y Barcelona para análisis de inversión.
Desarrollado con Streamlit, Plotly Express y Seaborn.
""")

