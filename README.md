
# 📊 Análisis de Inversión Inmobiliario: Inversión + Operación

> **Trabajo en progreso** – Este repositorio documenta el desarrollo, análisis y presentación de un proyecto de análisis inmobiliario basado en datos de Airbnb en España, integrando perspectivas de inversión y operación.

---

## 👥 Equipo y Contacto

| Nombre    | Ciudad     | Rol/Responsabilidad | LinkedIn                                                                 | GitHub                                      | Email                   |
|-----------|------------|---------------------|--------------------------------------------------------------------------|----------------------------------------------|-------------------------|
| Vanesa    | Valencia   | Análisis completo: inversión + operación en Valencia + integración general | [LinkedIn](https://www.linkedin.com/in/vanesa-fernandez-pomer/) | [vfpomer](https://github.com/vfpomer)        | vanesa@email.com        |
| Maribel   | Barcelona  | Análisis completo: inversión + operación en Barcelona + PowerBI (opcional) | [LinkedIn]()                                                              | [GitHub]()                                   | maribel@email.com       |
| Pablo     | Madrid     | Análisis completo: inversión + operación en Madrid + Storytelling           | [LinkedIn]()                                                              | [GitHub]()                                   | pablo@email.com         |
| Patricia  | Málaga     | Análisis completo en Málaga + Dashboard (Streamlit)                         | [LinkedIn](https://www.linkedin.com/in/patricia-jaquez/)                  | [patriciajaquez](https://github.com/patriciajaquez) | patricia@email.com      |

> Cada integrante desempeña un rol clave en el desarrollo del análisis, desde el procesamiento de datos hasta la presentación estratégica del dashboard final.

---

## 🧠 Contexto y Objetivos

Este proyecto aborda un enfoque dual para optimizar decisiones estratégicas en el sector inmobiliario, considerando:

- **Inversión:** Identificación de oportunidades, rentabilidad (ROI) y priorización de mercado.
- **Operación:** Optimización de procesos, eficiencia operativa y mejoras para los hosts.

El objetivo es integrar ambas perspectivas en un dashboard funcional, facilitando una visión 360° del negocio.

---

## 🔍 Principales Insights

1. 🚀 Las oportunidades con mayor ROI no siempre coinciden con las regiones operativamente más eficientes.
2. ⚙️ Las ineficiencias operativas impactan directamente la viabilidad de ciertas inversiones.
3. 📊 La integración de ambas dimensiones en tiempo real mejora la toma de decisiones estratégicas.

---

## ✅ Recomendaciones Clave

- Priorizar regiones con balance entre ROI alto y operación optimizada.
- Redireccionar inversión de bajo retorno a zonas con potencial operativo.
- Implementar sistemas de seguimiento en tiempo real para evitar disonancia entre inversión y operación.

---

## 🖥️ Dashboard Interactivo

- [🔗 Acceso al Dashboard en Streamlit](#) *(próximamente)*

### 📸 Capturas de Pantalla

Las imágenes representativas del dashboard y análisis se encuentran en la carpeta `/assets`.

---

## 🗂️ Estructura del Repositorio

```
airbnb-analysis-investment-hosts-multicity/
├── README.md
├── data/
│   ├── madrid.csv
│   ├── barcelona.csv
│   ├── valencia.csv
│   ├── malaga.csv
│   └── merged_airbnb.csv
├── notebooks/
│   ├── analysis_madrid.ipynb
│   ├── analysis_barcelona.ipynb
│   ├── analysis_valencia.ipynb
│   ├── analysis_malaga.ipynb
│   └── dashboard_building.ipynb
├── streamlit/
│   └── app/
│       └── app.py
├── presentation/
│   ├── slides.pdf
│   └── screenshots/
└── docs/
└── technical_notes.md
```

---

## 📌 Flujo de Trabajo

1. **Exploración individual por ciudad:** Investigación y recopilación de datos internos y externos.
2. **Preprocesamiento:** Limpieza y estandarización de datos.
3. **Análisis local:** ROI, ingresos, pricing, amenities, reviews, estacionalidad.
4. **Unificación y dashboard:** Consolidación de datos y visualizaciones en Streamlit.
5. **Comparativa entre ciudades:** Ranking, insights y recomendaciones globales.

---

## 📊 Análisis por Ciudad

Cada análisis incluye:

- **Inversión:** Precio promedio por noche, ingreso mensual estimado, ROI, zonas rentables.
- **Operación:** Estacionalidad, reviews, pricing óptimo, amenities, recomendaciones para hosts.

---

## 🛠️ Stack Tecnológico

- **Python:** pandas, seaborn, matplotlib, plotly
- **Streamlit:** dashboard central
- **SQLite:** almacenamiento de datos estructurados
- **Power BI:** opcional
- **GitHub:** control de versiones y colaboración

---

## 🗃️ Uso de SQLite

SQLite se utiliza como base de datos local para:

- Almacenar el dataset unificado (`merged_airbnb.csv`)
- Consultar datos por ciudad o filtros personalizados
- Servir datos al dashboard de Streamlit

**Ejemplo de carga de datos en SQLite:**

```python
import sqlite3
import pandas as pd

df = pd.read_csv("data/merged_airbnb.csv")
conn = sqlite3.connect("data/airbnb.db")
df.to_sql("airbnb_data", conn, if_exists="replace", index=False)
conn.close()
```

**Consulta de datos:**

```python
conn = sqlite3.connect("data/airbnb.db")
query = "SELECT * FROM airbnb_data WHERE ciudad = 'Madrid'"
df_madrid = pd.read_sql(query, conn)
conn.close()
```

---

## 🧭 Presentación y Storytelling

La presentación se estructura por ciudad y perspectiva, integrando insights clave y recomendaciones accionables. El storytelling conecta los datos con decisiones prácticas para inversores y hosts.

**Ejemplo de cierre narrativo:**

> “Nuestro análisis de cuatro ciudades estratégicas muestra que **Barcelona lidera en ingresos brutos**, pero **Valencia y Málaga presentan un mejor ROI para inversores**. Para los hosts, **Madrid y Málaga destacan por su estacionalidad y eficiencia operativa**. La clave está en combinar rentabilidad con sostenibilidad, y elegir zonas emergentes con alto potencial de crecimiento.”

---

## 🚧 Estado del Proyecto

Este repositorio está en desarrollo activo. Próximos pasos:

- Finalizar análisis individuales y comparativos
- Integrar visualizaciones y dashboard
- Documentar resultados y recomendaciones finales

---

¿Listos para brillar?  
Cada integrante aporta desde su ciudad, pero todos hablan el mismo idioma 📊🚀

