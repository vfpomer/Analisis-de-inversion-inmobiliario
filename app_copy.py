# 1. Añade la nueva pestaña al final de cada lista de tabs_por_ciudad
for k in tabs_por_ciudad:
    if "🧭 Conclusiones Generales" not in tabs_por_ciudad[k]:
        tabs_por_ciudad[k].append("🧭 Conclusiones Generales")

# 2. Después de la definición de las pestañas principales, añade el contenido de la nueva pestaña
if len(main_tabs) > 6:
    with main_tabs[6]:
        st.title("🧭 Conclusiones Generales: Estrategia de Inversión por Ciudad")
        st.markdown("""
**Resumen Ejecutivo**

Tras analizar el mercado de alquiler turístico en Barcelona, Málaga y Valencia, la estrategia de inversión propuesta para el fondo familiar de 5 millones de euros es la siguiente:

- **Barcelona:** Ciudad con alta rentabilidad y demanda, pero con fuerte incertidumbre regulatoria y criminalidad creciente. Recomendamos reservar solo un 20% del presupuesto para oportunidades con licencia existente.
- **Málaga:** Destino principal de inversión (40% del presupuesto) por su alta rentabilidad, baja regulación y potencial de expansión inmediata. Foco en barrios como Bailen-Miraflores, Churriana y Puerto de la Torre.
- **Valencia:** Inversión estable y prudente (30% del presupuesto), con margen de crecimiento en barrios clave como Ruzafa, El Carmen, Ciutat Universitaria, Cami Fondo, Penya-Roja y La Roqueta.

La estrategia equilibra agresividad en Málaga, solidez en Valencia y prudencia táctica en Barcelona.
        """)

        # Gráfico 1: Distribución del presupuesto recomendado
        st.subheader("Distribución Recomendada del Presupuesto de Inversión")
        presupuesto = pd.DataFrame({
            "Ciudad": ["Málaga", "Valencia", "Barcelona"],
            "Porcentaje": [40, 30, 20]
        })
        fig_pie = px.pie(presupuesto, names="Ciudad", values="Porcentaje", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Pastel,
                         title="Distribución del presupuesto (%)")
        st.plotly_chart(fig_pie, use_container_width=True)

        # Gráfico 2: Comparativa de ROI Neto Medio (si los datos están cargados)
        st.subheader("Comparativa de ROI Neto Medio por Ciudad")
        roi_data = []
        if df_malaga is not None and not df_malaga.empty:
            roi_data.append({"Ciudad": "Málaga", "ROI Neto (%)": df_malaga['net_roi'].mean()})
        if df_valencia is not None and not df_valencia.empty:
            roi_data.append({"Ciudad": "Valencia", "ROI Neto (%)": df_valencia['Net ROI (%)'].mean()})
        if df_barcelona is not None and not df_barcelona.empty and 'Net ROI (%)' in df_barcelona.columns:
            roi_data.append({"Ciudad": "Barcelona", "ROI Neto (%)": df_barcelona['Net ROI (%)'].mean()})
        if roi_data:
            df_roi = pd.DataFrame(roi_data)
            fig_bar = px.bar(df_roi, x="Ciudad", y="ROI Neto (%)", color="Ciudad",
                             color_discrete_sequence=px.colors.qualitative.Pastel,
                             title="ROI Neto Medio por Ciudad")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No hay datos suficientes para mostrar la comparativa de ROI.")

        # Tabla resumen de barrios recomendados
        st.subheader("Barrios Recomendados por Ciudad")
        st.markdown("""
| Ciudad    | Barrios Recomendados                                      | Tipo de Inmueble Sugerido         | Precio Aproximado (€)   |
|-----------|----------------------------------------------------------|------------------------------------|------------------------|
| Málaga    | Bailen-Miraflores, Churriana, Puerto de la Torre         | Piso completo, 2 hab, 1-2 baños    | 180,000 - 250,000      |
| Valencia  | Ruzafa, El Carmen, Ciutat Universitaria, Cami Fondo, Penya-Roja, La Roqueta | Piso 2 hab, 1 baño                | 160,000 - 220,000      |
| Barcelona | Solo con licencia existente (diversos barrios)           | Piso con licencia                  | Según oportunidad      |
        """)

        st.markdown("""
**Conclusión:**  
La diversificación entre Málaga y Valencia permite aprovechar el potencial de crecimiento y rentabilidad, mientras que la cautela en Barcelona protege el capital ante cambios regulatorios.  
La clave será la gestión activa, la selección de barrios con demanda sostenida y la adaptación a la normativa y tendencias del mercado.
        """)
