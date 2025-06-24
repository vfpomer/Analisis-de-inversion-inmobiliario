
# 🏠 Análisis de Inversión Inmobiliaria con Airbnb: Visión Dual

Bienvenido/a al proyecto **Airbnb – Análisis Dual: Inversión + Operación**. Este repositorio explora oportunidades de inversión y optimización operativa en los mercados de **Madrid, Barcelona, Valencia y Málaga** mediante análisis de datos y visualización interactiva.

---

## 🚀 Estado del Proyecto

> **En desarrollo:** El dashboard y análisis están en progreso. ¡Colaboraciones y sugerencias son bienvenidas!

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Equipo](#equipo)
- [Objetivo y Alcance](#objetivo-y-alcance)
- [Principales Insights](#principales-insights)
- [Recomendaciones](#recomendaciones)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Guía Técnica](#guía-técnica)
- [Stack Tecnológico](#stack-tecnológico)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Recursos](#recursos)

---

## 📖 Descripción

Este proyecto analiza el mercado Airbnb desde una **perspectiva dual**:

- **Inversión:** Identificación de zonas con mayor rentabilidad, ROI y potencial de crecimiento.
- **Operación:** Optimización de eficiencia, pricing y experiencia para hosts.

El objetivo es construir un **dashboard interactivo** que integre ambas dimensiones para facilitar la toma de decisiones informada.

---

## 👥 Equipo

| Nombre    | Ciudad     | Rol                   | LinkedIn / GitHub                                               |
|-----------|------------|-----------------------|-----------------------------------------------------------------|
| Vanesa    | Valencia   | Investment Analyst    | [LinkedIn](https://www.linkedin.com/in/vanesa-fernandez-pomer/) / [GitHub](https://github.com/vfpomer) |
| Maribel   | Barcelona  | Operations Analyst    | [LinkedIn]() / [GitHub]()                                       |
| Pablo     | Madrid     | Business Intelligence | [LinkedIn]() / [GitHub]()                                       |
| Patricia  | Málaga     | Data Engineer         | [LinkedIn](https://www.linkedin.com/in/patricia-jaquez/) / [GitHub](https://github.com/patriciajaquez) |

---

## 🎯 Objetivo y Alcance

- Analizar el mercado Airbnb en **Madrid, Barcelona, Valencia y Málaga**.
- Integrar análisis de inversión y operación para identificar oportunidades y riesgos.
- Desarrollar un dashboard interactivo para visualización y toma de decisiones.

---

## 🔍 Principales Insights

1. **ROI y eficiencia operativa no siempre coinciden:** Las zonas más rentables pueden no ser las más eficientes para operar.
2. **La operación impacta la inversión:** Ineficiencias operativas pueden limitar el potencial de retorno.
3. **Visión integrada = decisiones más inteligentes:** Analizar inversión y operación en conjunto revela oportunidades y riesgos ocultos.

---

## ✅ Recomendaciones

- Priorizar regiones con equilibrio entre alto ROI y operación optimizada.
- Redirigir inversión de bajo retorno a zonas con potencial operativo.
- Implementar seguimiento en tiempo real para alinear inversión y operación.

---

## 🗂️ Estructura del Repositorio

```
airbnb-analysis-investment-hosts-multicity/
├── README.md
├── data/
│   ├── madrid.csv, barcelona.csv, valencia.csv, malaga.csv
│   ├── *_limpio.csv
│   ├── merged_airbnb.csv
│   └── airbnb.db
├── notebooks/
│   ├── 01_data_engineer_preprocessing.ipynb
│   ├── 02_bi_kpis_comparativos.ipynb
│   ├── 03_investment_analysis.ipynb
│   ├── 04_operations_analysis.ipynb
│   └── 05_dashboard_building.ipynb
├── streamlit/app/app.py
├── presentation/slides.pdf
├── docs/
└── technical_notes.md
```

---

## 🛠️ Guía Técnica

### Data Engineer
- Limpieza y unión de datasets con `pandas`.
- Carga en SQLite:
    ```python
    import sqlite3, pandas as pd
    df = pd.read_csv("data/merged_airbnb.csv")
    conn = sqlite3.connect("data/airbnb.db")
    df.to_sql("airbnb_data", conn, if_exists="replace", index=False)
    conn.close()
    ```
- Ejemplo de consulta:
    ```python
    conn = sqlite3.connect("data/airbnb.db")
    df_madrid = pd.read_sql("SELECT * FROM airbnb_data WHERE ciudad = 'Madrid'", conn)
    conn.close()
    ```

### Business Intelligence
- Definir KPIs y visualizaciones comparativas.
    ```python
    import seaborn as sns
    sns.barplot(data=df, x="ciudad", y="ingresos_mensuales")
    ```

### Investment Analyst
- Indicadores de inversión y visualizaciones.
    ```python
    df['ROI'] = (df['ingresos_anuales'] / df['precio_compra']) * 100
    ```

### Operations Analyst
- Métricas operativas y visualizaciones.
    ```python
    df.groupby('ciudad')['reviews'].mean().plot(kind='bar')
    ```

---

## 💻 Stack Tecnológico

- **Python:** pandas, seaborn, matplotlib, plotly
- **Streamlit:** dashboard central
- **SQLite:** almacenamiento de datos
- **GitHub:** versionado y colaboración

---

## 🤝 Contribución

¿Te gustaría aportar?  
- Abre un issue para sugerencias o reportar bugs.
- Haz un fork y envía un pull request.
- Consulta la [Guía técnica](./workflow2.md) para detalles del flujo de trabajo.

---

## 📄 Licencia

Este proyecto utiliza solo **datos públicos y anonimizados**. Consulta el archivo [LICENSE](./LICENSE) para más detalles.

---

## 📚 Recursos

- [Guía técnica y workflow del proyecto](./workflow2.md)
- [Notas técnicas](./technical_notes.md)
- [Repositorio en GitHub](https://github.com/vfpomer/Analisis-de-inversion-inmobiliario)
- [README del proyecto original](https://github.com/vfpomer/Analisis-de-inversion-inmobiliario/blob/main/README.md)

---

> “Para garantizar comparabilidad entre ciudades, estructuramos los datos de forma unificada y aplicamos métricas consistentes en todo el análisis.”

---

¿Listos para descubrir el futuro de la inversión inmobiliaria en Airbnb?  
¡Sigue el avance y sé parte de la innovación! 🚀

