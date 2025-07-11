![analisis inmobiliario](https://github.com/user-attachments/assets/8c08a0d6-6c09-455a-8a27-1d417fbdf238)

# 📊 Proyecto de Análisis de Inversión Inmobiliaria: Inversión + Operación

Este proyecto explora la **rentabilidad y el mercado de alquiler turístico en Valencia, Málaga y Barcelona** mediante un análisis exhaustivo de datos de Airbnb y fuentes inmobiliarias. El objetivo es identificar las mejores oportunidades de inversión y optimización operativa, considerando rentabilidad, competencia, demanda y características de los barrios.

---

## 👥 Información del Equipo

| Nombre    | Rol                        | Perfil/Contacto                                                                 |
|-----------|----------------------------|---------------------------------------------------------------------------------|
| Vanesa    | Analytics Engineer - Valencia| [LinkedIn](https://www.linkedin.com/in/vanesa-fernandez-pomer/) / [GitHub](https://github.com/vfpomer) |
| Maribel   | Analytics Engineer - Barcelona| [LinkedIn](https://www.linkedin.com/) / [GitHub](https://github.com/Maribelgarcia-art) |                                                  
| Patricia  | Analytics Engineer - Málaga  | [LinkedIn](https://www.linkedin.com/in/patricia-jaquez/) / [GitHub](https://github.com/patriciajaquez) |
| Pablo     | Business Intelligence Analyst | [LinkedIn](https://www.linkedin.com/in/pablo-anchustegui-mezquita/) / [GitHub](https://github.com/anchuslol) |

🔗 Cada integrante desempeñó un rol clave en el desarrollo del análisis, desde el procesamiento de datos hasta la presentación estratégica del dashboard final.

---

## 🧠 Contexto y Objetivos

Este proyecto aborda un enfoque dual de análisis para optimizar decisiones estratégicas desde dos dimensiones críticas:

- **Inversión:** Identificación de oportunidades, rentabilidad (ROI) y priorización de mercado.
- **Operación:** Optimización de procesos, eficiencia operativa y mejoras para los hosts.

El objetivo fue integrar ambas perspectivas en un solo dashboard funcional, facilitando una visión 360° del negocio.

---

```markdown
Analisis-de-inversion-inmobiliario/
├── README.md                # Portada profesional del proyecto
├── data/                    # Datos procesados y fuentes originales (listados, precios, crimen, geojson de barrios)
├── notebooks/               # Jupyter Notebooks para EDA, limpieza y análisis avanzado
├── streamlit_app/           # Dashboard interactivo en Streamlit para visualización y toma de decisiones
├── presentation/            # Slides y capturas para presentaciones
└── docs/                    # Documentación técnica y material de apoyo
```

---

## 📊 Principales Análisis

- **Rentabilidad bruta y neta por barrio:** Cálculo de ROI considerando ingresos estimados y gastos operativos.
- **Precio óptimo de compra y alquiler:** Estimaciones basadas en demanda, calidad y rentabilidad objetivo.
- **Competencia:** Saturación de anuncios activos por barrio y tipo de propiedad.
- **Demanda y reseñas:** Análisis de reviews totales y mensuales como proxy de demanda real.
- **Calidad y amenities:** Relación entre número de servicios, tamaño de vivienda y rentabilidad.
- **Factores de riesgo:** Análisis de criminalidad y saturación del mercado.
- **Visualización geográfica:** Mapas coropléticos de ROI y competencia por barrio.

---

## 🔍 Top 3 Insights del Análisis

- 🚀 Las oportunidades con mayor ROI no siempre coinciden con las regiones operativamente más eficientes.
- ⚙️ Las ineficiencias operativas impactan directamente la viabilidad de ciertas inversiones.
- 📊 La integración de ambas dimensiones en tiempo real mejora la toma de decisiones estratégicas.

---

## ✅ Recomendaciones Clave

- Priorizar regiones con balance entre ROI alto y operación optimizada.
- Redireccionar inversión de bajo retorno a zonas con potencial operativo.
- Implementar sistemas de seguimiento en tiempo real para evitar disonancia entre inversión y operación.
- Apostar por la calidad y diferenciación del alojamiento.
- Diversificar la inversión en diferentes zonas para equilibrar riesgo y retorno.
- Monitorizar continuamente los indicadores clave del mercado y la regulación local.

---

## 📈 Tecnologías
- Python, Pandas, Numpy, Matplotlib, Seaborn, Plotly, Folium
- Jupyter Notebook
- Streamlit

---

## 🚀 Cómo usar este proyecto

1. **Requisitos**  
   Instala las dependencias:
   ```sh
   pip install -r docs/requirements.txt
   ```

2. **Ejecutar el Dashboard**
   Corre la aplicación interactiva en Streamlit:
   ```sh
   streamlit run streamlit_app/app.py
   ```

---

Enlace al dashboard en streamlit : https://airbnbvalencia.streamlit.app/

Este análisis permite tomar decisiones de inversión basadas en datos, maximizando el retorno y minimizando riesgos en el mercado de alquiler turístico en España.

---

## 📚 Fuentes de Datos

- [EPData - Precio del alquiler en cada municipio de España](https://www.epdata.es/datos/precio-alquiler-cada-municipio-espana-estadisticas-datos-graficos/)
- [Idealista - Informes de precio de vivienda](https://www.idealista.com/sala-de-prensa/informes-precio-vivienda/)
- [Inside Airbnb - Datos de listados y reviews](https://insideairbnb.com/get-the-data/)

---
