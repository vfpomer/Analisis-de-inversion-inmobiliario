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
Este panel te permite explorar datos del mercado inmobiliario en Valencia, Málaga, Madrid y Barcelona para su inversión.
Utiliza los filtros y selectores en la barra lateral para personalizar tu análisis.
""")

@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_csv("../data/Valencia_limpio.csv")
        df_inmobiliario = pd.read_csv("../data/valencia_vivienda_limpio.csv")
        df_delincuencia = pd.read_csv("../data/crimenValencia.csv", sep=';')
        return df, df_inmobiliario, df_delincuencia
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        st.text(traceback.format_exc())
        return None, None, None

df, df_inmobiliario, df_delincuencia = load_data()

# Preprocesamiento básico y filtros
if df is not None and df_inmobiliario is not None:
    if 'price' in df.columns:
        df['price'] = df['price'].astype(float)
    if 'precio' in df_inmobiliario.columns:
        precio_m2_valencia = df_inmobiliario['precio'].mean()
    else:
        precio_m2_valencia = 2000  # fallback
    average_m2 = 70
    df['annual_income'] = df['price'] * df['days_rented']
    df['estimated_property_value'] = precio_m2_valencia * average_m2
    df['ROI (%)'] = (df['annual_income'] / df['estimated_property_value']) * 100
    gastos_anuales = 3000
    df['net_annual_income'] = df['annual_income'] - gastos_anuales
    df['Net ROI (%)'] = (df['net_annual_income'] / df['estimated_property_value']) * 100

    st.sidebar.header("Filtros")

    # Filtro por ciudad
    ciudades = ['Valencia', 'Malaga', 'Madrid', 'Barcelona']
    if 'city' in df.columns:
        ciudad_seleccionada = st.sidebar.selectbox("Selecciona ciudad", ciudades)
        df_ciudad = df[df['city'].str.lower() == ciudad_seleccionada.lower()]
        if df_ciudad.empty:
            st.warning("No hay datos para la ciudad seleccionada.")
            st.stop()
        # Filtro dinámico de barrios según ciudad
        barrios = sorted(df_ciudad['neighbourhood'].dropna().unique())
        selected_barrios = st.sidebar.multiselect("Selecciona barrios", options=barrios, default=barrios)
        df_ciudad = df_ciudad[df_ciudad['neighbourhood'].isin(selected_barrios)]
        if df_ciudad.empty:
            st.warning("No hay datos para los barrios seleccionados en la ciudad.")
            st.stop()
        df = df_ciudad
    else:
        st.sidebar.warning("No se encontró la columna 'city' en los datos. Mostrando todos los datos.")
        barrios = sorted(df['neighbourhood'].dropna().unique())
        selected_barrios = st.sidebar.multiselect("Selecciona barrios", options=barrios, default=barrios)
        df = df[df['neighbourhood'].isin(selected_barrios)]
        if df.empty:
            st.warning("No hay datos para los barrios seleccionados.")
            st.stop()
else:
    st.warning("No hay datos disponibles.")
    st.stop()

main_tabs = st.tabs([
    "📊 Resumen General",
    "🏠 Precios de Vivienda",
    "💸 Rentabilidad por Barrio",
    "📈 Competencia y Demanda",
    "🔍 Análisis Avanzado",
    "📝 Conclusiones"
])

# ------------------ Pestaña 1: Resumen General ------------------
with main_tabs[0]:
    st.subheader("Resumen General del Mercado Inmobiliario")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nº de anuncios", len(df))
    col2.metric("ROI Neto medio (%)", f"{df['Net ROI (%)'].mean():.2f}")
    col3.metric("Precio medio alquiler (€)", f"{df['price'].mean():.2f}")

    # KDE ROI Bruto y Neto
    st.markdown("#### Distribución de ROI Bruto y Neto (%)")
    if len(df) > 1:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.kdeplot(df['ROI (%)'], fill=True, label='ROI Bruto (%)', color='skyblue', bw_adjust=0.7, clip=(0, 50), ax=ax)
        sns.kdeplot(df['Net ROI (%)'], fill=True, label='ROI Neto (%)', color='orange', bw_adjust=0.7, clip=(0, 50), ax=ax)
        ax.set_title('Distribución de ROI Bruto y Neto')
        ax.set_xlabel('ROI (%)')
        ax.set_ylabel('Densidad')
        ax.set_xlim(0, 50)
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("No hay suficientes datos para mostrar la distribución de ROI.")

# ------------------ Pestaña 2: Precios de Vivienda ------------------
with main_tabs[1]:
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

# ------------------ Pestaña 3: Rentabilidad por Barrio ------------------
with main_tabs[2]:
    st.subheader("Rentabilidad por Barrio")
    if not df.empty:
        # ROI neto por barrio
        roi_barrio = df.groupby('neighbourhood')['Net ROI (%)'].mean().sort_values(ascending=False).head(15)
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
        roi_barrio_bruto = df.groupby('neighbourhood')['ROI (%)'].mean().sort_values(ascending=False).head(15)
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

# ------------------ Pestaña 4: Competencia y Demanda ------------------
with main_tabs[3]:
    st.subheader("Competencia y Demanda por Barrio")
    if not df.empty:
        # Competencia por barrio
        competencia_por_barrio = df.groupby('neighbourhood')['id'].count().reset_index().rename(columns={'id': 'n_anuncios'})
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
        if 'days_rented' in df.columns:
            activos = df[df['days_rented'] > 30]
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

# ------------------ Pestaña 5: Análisis Avanzado ------------------
with main_tabs[4]:
    st.subheader("Análisis Avanzado")
    if not df.empty:
        # Relación entre precio medio de alquiler y ROI neto por barrio
        st.markdown("#### Relación entre precio medio de alquiler y ROI neto por barrio")
        if 'city' in df.columns and df['city'].str.lower().nunique() == 1 and df['city'].str.lower().iloc[0] == 'valencia':
            if 'price' in df.columns and 'Net ROI (%)' in df.columns:
                fig_val = px.scatter(
                    df,
                    x='price',
                    y='Net ROI (%)',
                    color='neighbourhood',
                    hover_data=['neighbourhood'],
                    opacity=0.6,
                    labels={'price': 'Precio alquiler (€)', 'Net ROI (%)': 'ROI Neto (%)', 'neighbourhood': 'Barrio'},
                    title='Relación entre precio de alquiler y ROI neto por barrio (Valencia)'
                )
                fig_val.update_traces(marker=dict(size=8), selector=dict(mode='markers'))
                fig_val.update_layout(legend_title_text='Barrio', showlegend=True)
                st.plotly_chart(fig_val, use_container_width=True)
            else:
                st.info("No hay datos suficientes para mostrar el gráfico de dispersión para Valencia.")
        else:
            df_barrio = df.groupby('neighbourhood').agg({'price': 'mean', 'Net ROI (%)': 'mean'}).reset_index()
            if not df_barrio.empty:
                fig_scatter = px.scatter(
                    df_barrio,
                    x='price',
                    y='Net ROI (%)',
                    text='neighbourhood',
                    labels={'price': 'Precio medio alquiler (€)', 'Net ROI (%)': 'ROI Neto (%)'},
                    title='Precio medio de alquiler vs ROI Neto por barrio'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)
            else:
                st.info("No hay datos para mostrar la relación entre precio y ROI.")

        # Número medio de amenities por barrio
        st.markdown("#### Top 15 barrios por número medio de amenities")
        if 'amenities' in df.columns:
            df['n_amenities'] = df['amenities'].str.count(',') + 1
            barrio_amenities = df.groupby('neighbourhood')['n_amenities'].mean().reset_index()
            barrio_amenities = barrio_amenities.sort_values(by='n_amenities', ascending=False).head(15)
            if not barrio_amenities.empty:
                fig_amenities = px.bar(
                    barrio_amenities,
                    x='n_amenities',
                    y='neighbourhood',
                    orientation='h',
                    labels={'n_amenities': 'Nº medio de amenities', 'neighbourhood': 'Barrio'},
                    title='Top 15 barrios por número medio de amenities'
                )
                st.plotly_chart(fig_amenities, use_container_width=True)
            else:
                st.info("No hay datos de amenities para mostrar.")
        else:
            st.info("No hay datos de amenities para mostrar.")

        # Número total de reseñas por barrio
        st.markdown("#### Top 15 barrios por número total de reseñas")
        if 'number_of_reviews' in df.columns:
            barrio_mas_resenas = df.groupby('neighbourhood')['number_of_reviews'].sum().reset_index()
            barrio_mas_resenas = barrio_mas_resenas.sort_values(by='number_of_reviews', ascending=False).head(15)
            if not barrio_mas_resenas.empty:
                fig_resenas = px.bar(
                    barrio_mas_resenas,
                    x='number_of_reviews',
                    y='neighbourhood',
                    orientation='h',
                    labels={'number_of_reviews': 'Número total de reseñas', 'neighbourhood': 'Barrio'},
                    title='Top 15 barrios por número total de reseñas'
                )
                st.plotly_chart(fig_resenas, use_container_width=True)
            else:
                st.info("No hay datos de reseñas para mostrar.")
        else:
            st.info("No hay datos de reseñas para mostrar.")

        # Habitaciones y baños por barrio
        st.markdown("#### Top 15 barrios por número medio de habitaciones y baños")
        if 'bedrooms' in df.columns and 'bathrooms' in df.columns:
            barrio_habitaciones_banos = df.groupby('neighbourhood').agg({
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
                    title='Top 15 barrios por número medio de habitaciones'
                )
                st.plotly_chart(fig_hab, use_container_width=True)
            else:
                st.info("No hay datos de habitaciones para mostrar.")
        else:
            st.info("No hay datos de habitaciones o baños para mostrar.")

        # Histograma de precios de alquiler
        st.markdown("#### Histograma de precios de alquiler")
        if 'price' in df.columns:
            fig_hist = px.histogram(df, x='price', nbins=50, color='neighbourhood',
                                   labels={'price': 'Precio alquiler (€)'},
                                   title='Distribución de precios de alquiler por barrio')
            st.plotly_chart(fig_hist, use_container_width=True)
        else:
            st.info("No hay datos de precios para mostrar histograma.")

        # Boxplot de precios de alquiler por barrio
        st.markdown("#### Boxplot de precios de alquiler por barrio")
        if 'price' in df.columns:
            fig_box = px.box(df, x='neighbourhood', y='price', points='all',
                             labels={'price': 'Precio alquiler (€)', 'neighbourhood': 'Barrio'},
                             title='Boxplot de precios de alquiler por barrio')
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("No hay datos de precios para mostrar boxplot.")

        # Histograma de ROI Neto
        st.markdown("#### Histograma de ROI Neto (%)")
        if 'Net ROI (%)' in df.columns:
            fig_hist_roi = px.histogram(df, x='Net ROI (%)', nbins=50, color='neighbourhood',
                                        labels={'Net ROI (%)': 'ROI Neto (%)'},
                                        title='Distribución de ROI Neto por barrio')
            st.plotly_chart(fig_hist_roi, use_container_width=True)
        else:
            st.info("No hay datos de ROI Neto para mostrar histograma.")

        # Boxplot de ROI Neto por barrio
        st.markdown("#### Boxplot de ROI Neto por barrio")
        if 'Net ROI (%)' in df.columns:
            fig_box_roi = px.box(df, x='neighbourhood', y='Net ROI (%)', points='all',
                                 labels={'Net ROI (%)': 'ROI Neto (%)', 'neighbourhood': 'Barrio'},
                                 title='Boxplot de ROI Neto por barrio')
            st.plotly_chart(fig_box_roi, use_container_width=True)
        else:
            st.info("No hay datos de ROI Neto para mostrar boxplot.")

        # Histograma de días alquilados
        st.markdown("#### Histograma de días alquilados")
        if 'days_rented' in df.columns:
            fig_hist_days = px.histogram(df, x='days_rented', nbins=50, color='neighbourhood',
                                         labels={'days_rented': 'Días alquilados'},
                                         title='Distribución de días alquilados por barrio')
            st.plotly_chart(fig_hist_days, use_container_width=True)
        else:
            st.info("No hay datos de días alquilados para mostrar histograma.")

        # Boxplot de días alquilados por barrio
        st.markdown("#### Boxplot de días alquilados por barrio")
        if 'days_rented' in df.columns:
            fig_box_days = px.box(df, x='neighbourhood', y='days_rented', points='all',
                                  labels={'days_rented': 'Días alquilados', 'neighbourhood': 'Barrio'},
                                  title='Boxplot de días alquilados por barrio')
            st.plotly_chart(fig_box_days, use_container_width=True)
        else:
            st.info("No hay datos de días alquilados para mostrar boxplot.")

        # Mapa de puntos de los anuncios (si hay lat/lon)
        st.markdown("#### Mapa de anuncios")
        if 'latitude' in df.columns and 'longitude' in df.columns:
            st.map(df[['latitude', 'longitude']].dropna())
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

# ------------------ Pestaña 6: Conclusiones ------------------
with main_tabs[5]:
    st.subheader("Conclusiones finales para empresas interesadas en invertir en alquiler turístico en Valencia (AirBnB)")
    st.markdown("""
El análisis integral de los datos de rentabilidad, competencia, demanda y características de los barrios de Valencia permite extraer las siguientes conclusiones clave para una empresa que busca invertir en el mercado de alquiler turístico:

- **Rentabilidad excepcional en barrios específicos:** Zonas como Pinedo, Carpesa y La Gran Vía destacan por su altísima rentabilidad neta y bruta, superando ampliamente la media de la ciudad. Estos barrios ofrecen oportunidades únicas para maximizar el retorno de la inversión, aunque pueden tener menor volumen de anuncios y demanda más estacional.

- **Equilibrio entre rentabilidad y competencia:** Los barrios céntricos y turísticos (Cabanyal-Canyamelar, Russafa, El Mercat, El Carme) combinan buena rentabilidad con una demanda sostenida, pero presentan una competencia elevada. Invertir en estas zonas requiere estrategias de diferenciación y calidad para destacar frente a la saturación del mercado.

- **Demanda y flujo de huéspedes:** El número total de reseñas y las reseñas mensuales son indicadores sólidos de demanda real. Barrios con altos valores en estos indicadores aseguran un flujo constante de huéspedes y menor riesgo de vacancia, aunque suelen estar asociados a mayor competencia.

- **Importancia de la calidad y el equipamiento:** Los barrios con mayor número medio de amenities y viviendas más grandes tienden a mantener mejores niveles de ocupación y rentabilidad. Invertir en la mejora de la calidad, el equipamiento y la experiencia del huésped puede marcar la diferencia en mercados competitivos.

- **Oportunidades en barrios con baja competencia:** Existen barrios con alta rentabilidad neta y un número reducido de anuncios activos, lo que los convierte en opciones especialmente atractivas para empresas que buscan menor riesgo de saturación y mayor facilidad para captar reservas.

- **Diversidad de precios y accesibilidad:** Valencia presenta una amplia gama de precios de alquiler y compra por metro cuadrado. Esto permite adaptar la estrategia de inversión según el presupuesto y el perfil de riesgo de la empresa, desde barrios exclusivos hasta zonas emergentes con potencial de revalorización.

- **Factores adicionales a considerar:** Además de la rentabilidad y la demanda, es fundamental analizar la regulación local, la evolución de la competencia, la estacionalidad y los posibles cambios en la normativa turística.

**Recomendación general:**  
La mejor estrategia de inversión combina la selección de barrios con alta rentabilidad neta, demanda sostenida y competencia controlada, junto con una apuesta por la calidad y la diferenciación del producto. Es recomendable diversificar la cartera en diferentes zonas para equilibrar riesgo y retorno, y monitorizar de forma continua los indicadores clave del mercado.

En resumen, Valencia ofrece un mercado dinámico y con grandes oportunidades para empresas de alquiler turístico, siempre que la toma de decisiones esté basada en datos y en un análisis integral de rentabilidad, competencia y demanda.
    """)

# ------------------ Descargable ------------------
with st.expander("Ver datos en formato tabla"):
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Descargar datos filtrados (CSV)",
            data=csv,
            file_name="valencia_inmobiliario.csv",
            mime="text/csv",
        )
    else:
        st.info("No hay datos para mostrar o descargar.")

# ------------ Información del dashboard ------------
st.sidebar.markdown("---")
st.sidebar.info("""
**Acerca de este Panel**

Este panel muestra datos del mercado inmobiliario de Valencia, Málaga, Madrid y Barcelona para análisis de inversión.
Desarrollado con Streamlit, Plotly Express y Seaborn.
""")