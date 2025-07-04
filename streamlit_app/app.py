import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import traceback

st.set_page_config(
    page_title="Panel de Análisis de mercado inmobiliario (AirBnb)",
    page_icon="🏠📊",
    layout="wide"
)

st.title("🏠📊 Panel de Análisis de mercado inmobiliario (AirBnb)")
st.markdown("""
Este panel te permite explorar datos del mercado inmobiliario en Valencia, Málaga y Barcelona para su inversión.
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
        df_malaga = pd.read_csv("data/malaga_completed_clean.csv")
        df_malaga_crimen = pd.read_csv("data/malaga_crimen_clean.csv", sep=',', quotechar='"')
        return df_valencia, df_inmobiliario, df_delincuencia, df_barcelona, df_barcelona_inversores, df_malaga, df_malaga_crimen
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        st.text(traceback.format_exc())
        return None, None, None

df_valencia, df_inmobiliario, df_delincuencia, df_barcelona, df_barcelona_inversores, df_malaga, df_malaga_crimen = load_data()

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
ciudades = ['Valencia', 'Malaga', 'Barcelona']

if 'city' in df_valencia.columns:
    ciudad_seleccionada = st.sidebar.selectbox("Selecciona ciudad", ciudades)

    # Selecciona el dataframe según la ciudad
    if ciudad_seleccionada.lower() == 'valencia':
        df_ciudad = df_valencia
    elif ciudad_seleccionada.lower() == 'barcelona':
        df_ciudad = df_barcelona
    elif ciudad_seleccionada.lower() == 'malaga':
        df_ciudad = df_malaga


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
        "📊 Barcelona General",
        "🏠 Barcelona de Vivienda",
        "💸 Rentabilidad por Barrio",
       # "📈 Competencia y Demanda",
       # "🔍 Análisis Avanzado",
       # "📝 Conclusiones"
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
            st.info("Si la ciudad es Barcelona añadir código aquí")

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
        st.info("Si la ciudad es barcelona añadir codigo aqui")
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
            st.info("Si la ciudad es Barcelona añadir código aquí")

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


        # elif ciudad_actual == "barcelona":
        #     st.info("Si la ciudad es Barcelona añadir código aquí")

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
                    # Verificar columnas
                    if 'year' in df_malaga_crimen.columns and 'reported_cases' in df_malaga_crimen.columns and 'crime_type' in df_malaga_crimen.columns:
                        # Gráfico de barras agrupadas
                        fig, ax = plt.subplots(figsize=(14, 7))
                        sns.barplot(
                            data=df_malaga_crimen,
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

                        # Mapa de calor
                        st.markdown("#### Mapa de calor de delitos denunciados en Málaga por tipo y año")
                        fig2, ax2 = plt.subplots(figsize=(14, 7))
                        heatmap_data = df_malaga_crimen.pivot_table(
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
                        st.error("Las columnas necesarias ('year', 'reported_cases', 'crime_type') no están disponibles en el DataFrame.")
                else:
                    st.info("No hay datos de delincuencia para mostrar.")
            else:
                st.info("No hay datos para mostrar en esta pestaña.")

        #elif ciudad_actual.lower() == "barcelona":
        #st.info("Si la ciudad es barcelona añadir codigo aqui")
        else:
            st.info("No hay datos para mostrar en esta pestaña.")

# ------------------ Pestaña 6: Conclusiones ------------------
if len(main_tabs) > 5:
    with main_tabs[5]:
        if ciudad_actual.lower() == "valencia":
            st.subheader("Conclusiones finales para empresas interesadas en invertir en alquiler turístico en Valencia (AirBnB)")
            st.markdown("""
            El análisis exhaustivo de los datos de rentabilidad, competencia, demanda, precios y características de los barrios de Valencia permite extraer recomendaciones más precisas y accionables para empresas que buscan invertir en el mercado de alquiler turístico:

            **Rentabilidad y retorno de inversión:** Los barrios líderes en rentabilidad neta y bruta, como Ciutat Universitaria, Cami Fondo, Penya-Roja y La Roqueta, ofrecen retornos superiores al promedio de la ciudad. Sin embargo, la diferencia entre rentabilidad bruta y neta es relativamente baja en los barrios más rentables, lo que indica una estructura de costes eficiente y un mercado consolidado.

            **Demanda sostenida y visibilidad:** Barrios como Cabanyal-Canyamelar, Russafa y El Mercat destacan por su alto volumen de reseñas totales y mensuales, reflejando una demanda turística constante y una elevada rotación de huéspedes. Invertir en estas zonas garantiza visibilidad y ocupación, aunque implica enfrentarse a una competencia intensa.

            **Competencia y saturación:** La saturación de anuncios es especialmente alta en barrios turísticos y céntricos. Para destacar en estos mercados, es fundamental apostar por la diferenciación, la calidad del alojamiento y la experiencia del huésped. Por otro lado, existen barrios con alta rentabilidad y baja competencia (menor número de anuncios), que representan oportunidades para captar reservas con menor riesgo de saturación.

            **Calidad, amenities y tamaño de la vivienda:** Los barrios con mayor número medio de amenities y viviendas más espaciosas tienden a lograr mejores valoraciones y mayor rentabilidad. La inversión en equipamiento y servicios adicionales puede ser clave para maximizar ingresos y diferenciarse en mercados competitivos.

            **Diversidad de precios y accesibilidad:** Valencia presenta una amplia dispersión de precios de alquiler y compra por metro cuadrado, tanto entre barrios como dentro de cada uno. Esto permite adaptar la estrategia de inversión según el presupuesto y el perfil de riesgo, desde zonas premium hasta barrios emergentes con potencial de revalorización.

            **Relación entre precio y competencia:** Los barrios con precios de alquiler más altos suelen concentrar también mayor competencia. Sin embargo, existen zonas con precios elevados y menor saturación, que pueden ser especialmente atractivas para inversores que buscan maximizar ingresos sin enfrentarse a una oferta excesiva.

            **Factores adicionales:** Es imprescindible monitorizar la evolución de la normativa local, la estacionalidad de la demanda, la seguridad y otros factores externos que pueden impactar la rentabilidad y la sostenibilidad de la inversión.

            **Recomendación estratégica:**  
            La mejor estrategia combina la selección de barrios con alta rentabilidad neta, demanda sostenida y competencia controlada, junto con una apuesta por la calidad, el equipamiento y la diferenciación. Diversificar la cartera en diferentes zonas y perfiles de barrio permite equilibrar riesgo y retorno. Además, es clave realizar un seguimiento continuo de los indicadores clave del mercado y adaptar la oferta a las tendencias y preferencias de los huéspedes.

            En resumen, Valencia ofrece un mercado dinámico y diverso, con grandes oportunidades para empresas de alquiler turístico. El éxito dependerá de una toma de decisiones basada en datos, una gestión activa y una visión integral que combine rentabilidad, demanda, competencia y calidad.
                """)
            
        elif ciudad_actual.lower() == "malaga":
            st.subheader("Conclusiones finales para empresas interesadas en invertir en alquiler turístico en Málaga (AirBnB)")
            st.markdown("""
            El análisis detallado de los datos de Málaga muestra un mercado inmobiliario turístico con oportunidades claras y retos a considerar para empresas de alquiler vacacional:

            **Rentabilidad y retorno de inversión:**  
            Los barrios con mayor ROI neto promedio son Bailen-Miraflores (~3.0%), Churriana (~2.8%) y Puerto de la Torre (~2.1%), según los datos analizados. Estas zonas combinan precios de compra accesibles y una buena relación entre ingresos anuales y valor estimado de la propiedad. La diferencia entre ROI bruto y neto es moderada, reflejando unos gastos operativos razonables.

            **Demanda y ocupación:**  
            Zonas como Centro, Este y Carretera de Cádiz presentan alta ocupación estimada y precios elevados por metro cuadrado, lo que indica una demanda turística sostenida. Sin embargo, la rentabilidad neta es mayor en barrios como Churriana y Bailen-Miraflores, donde la ocupación es buena y los precios de compra son más bajos.

            **Competencia y saturación:**  
            El centro y las zonas costeras concentran la mayor cantidad de anuncios activos, lo que implica una competencia intensa. Por el contrario, barrios como Churriana, Puerto de la Torre y Campanillas presentan menor saturación y, en algunos casos, rentabilidades atractivas, lo que los convierte en opciones interesantes para nuevas inversiones.

            **Calidad, amenities y tamaño:**  
            Los barrios con mayor número medio de amenities, como Centro y Este, tienden a obtener mejores valoraciones y mayor ocupación. Los amenities más frecuentes incluyen Kitchen, Wifi, Hair Dryer y Dishes and Silverware. Invertir en equipamiento y servicios diferenciadores puede mejorar la rentabilidad y la percepción del alojamiento.

            **Precios y accesibilidad:**  
            Málaga muestra una dispersión significativa de precios por metro cuadrado: desde menos de 2,000 €/m² en Campanillas y Palma-Palmilla hasta más de 4,000 €/m² en Este y Centro. Esto permite adaptar la estrategia de inversión según el presupuesto y el perfil de riesgo, combinando zonas premium y barrios emergentes.

            **Seguridad:**  
            El análisis de criminalidad indica que los delitos más comunes son robos con fuerza, robos con violencia y hurtos, con mayor incidencia en zonas céntricas. La percepción de seguridad puede afectar la demanda y la rentabilidad, por lo que es recomendable considerar este factor y, si es necesario, invertir en medidas de seguridad adicionales.

            **Recomendación estratégica:**  
            La mejor estrategia combina la selección de barrios con alta rentabilidad neta (como Bailen-Miraflores, Churriana y Puerto de la Torre), demanda sostenida y competencia controlada, junto con una apuesta por la calidad, el equipamiento y la diferenciación. Diversificar la inversión en diferentes zonas y perfiles de barrio ayuda a equilibrar riesgo y retorno. Es fundamental monitorizar la evolución del mercado, la normativa local y los indicadores de seguridad para adaptar la oferta a las tendencias y preferencias de los huéspedes.

            En resumen, Málaga ofrece un mercado turístico dinámico y con oportunidades claras para empresas de alquiler vacacional. El éxito dependerá de una gestión basada en datos, una oferta diferenciada y una visión integral que combine rentabilidad, demanda, competencia, calidad y seguridad.
            """)

        elif ciudad_actual.lower() == "barcelona":
            st.info("Si la ciudad es barcelona añadir codigo aqui")
        else:
            st.info("No hay datos para mostrar en esta pestaña.")

# ------------------ Descargable ------------------
with st.expander(f"Ver datos en formato tabla ({ciudad_seleccionada})"):
    if df_ciudad is not None and not df_ciudad.empty:
        st.dataframe(df_ciudad, use_container_width=True)
        csv_ciudad = df_ciudad.to_csv(index=False).encode('utf-8')
        st.download_button(
            f"Descargar datos filtrados ({ciudad_seleccionada}) (CSV)",
            data=csv_ciudad,
            file_name=f"{ciudad_actual}_inmobiliario.csv",
            mime="text/csv",
        )
    else:
        st.info(f"No hay datos para mostrar o descargar de {ciudad_seleccionada}.")

# ------------ Información del dashboard ------------
st.sidebar.markdown("---")
st.sidebar.info("""
**Acerca de este Panel**

Este panel muestra datos del mercado inmobiliario de Valencia, Málaga y Barcelona para análisis de inversión.
Desarrollado con Streamlit, Plotly Express y Seaborn.
""")
