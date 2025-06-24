# 🧭 Proyecto Airbnb – Análisis Dual: Inversión + Operación

## 🧑‍🤝‍🧑 Equipo y Estructura

Este proyecto analiza el mercado Airbnb en **cuatro ciudades clave de España** con una **perspectiva dual**:  
- 🏢 **Inversión:** oportunidades de rentabilidad, ROI y zonas estratégicas  
- 🧑‍💼 **Operación:** optimización para hosts actuales, pricing y posicionamiento

### 👥 Integrantes y ciudades asignadas

| Nombre    | Ciudad     | Rol                       | Función Principal                                                        |
|-----------|------------|---------------------------|--------------------------------------------------------------------------|
| Vanesa    | Valencia   | Investment Analyst        | Análisis de ROI, precios, oportunidades de inversión                     |
| Maribel   | Barcelona  | Operations Analyst        | Análisis de optimización, pricing, amenities, recomendaciones para hosts |
| Pablo     | Madrid     | Business Intelligence     | Conexión de perspectivas, insights globales, cierre narrativo            |
| Patricia  | Málaga     | Data Engineer             | Integración técnica, base de datos, estructura del dashboard             |

---

## 🔄 Flujo de Trabajo y Responsabilidades con `merged_airbnb.csv`

Cada integrante es responsable de la **limpieza y validación de datos** de su ciudad, asegurando la estandarización de columnas y formatos. Los datos se consolidan en `merged_airbnb.csv` con la columna `ciudad` incluida.

### División de tareas y pasos detallados por rol

#### 🧑‍💻 Patricia – Data Engineer

**Objetivo:** Garantizar la calidad, integración y accesibilidad técnica de los datos y la infraestructura.

**Pasos y tareas:**
1. **Limpieza y estandarización de datos**
    - Leer cada CSV (`madrid.csv`, `barcelona.csv`, etc.) con `pandas`.
    - Renombrar columnas para que sean idénticas en todos los archivos.
    - Uniformar tipos de datos (fechas, numéricos, strings).
    - Añadir la columna `ciudad` si no existe.
    - Guardar cada dataset limpio en `data/ciudad_limpio.csv`.
2. **Unificación de datasets**
    - Concatenar los archivos limpios en un solo DataFrame.
    - Verificar duplicados y valores nulos.
    - Guardar el resultado como `merged_airbnb.csv`.
3. **Carga en SQLite**
    - Crear la base de datos `airbnb.db`.
    - Cargar el CSV unificado en la tabla `airbnb_data`.
    - Documentar el proceso en el notebook `notebooks/01_data_engineer_preprocessing.ipynb`.
4. **Ejemplos de conexión y consulta**
    - Proveer ejemplos de conexión a SQLite desde Python y Streamlit.
    - Incluir consultas SQL básicas y avanzadas.
5. **Estructura técnica del repositorio**
    - Proponer y mantener la estructura de carpetas.
    - Coordinar la integración técnica del dashboard y notebooks.

#### 📊 Pablo – Business Intelligence

**Objetivo:** Definir métricas clave, análisis comparativos y narrativa global.

**Pasos y tareas:**
1. **Definición de KPIs y métricas**
    - Reunirse con el equipo para consensuar métricas prioritarias (ingresos, ROI, ocupación, estacionalidad).
    - Documentar las fórmulas y criterios en el notebook `notebooks/02_bi_kpis_comparativos.ipynb`.
2. **Análisis comparativo**
    - Desarrollar visualizaciones comparativas entre ciudades (barras, mapas, rankings).
    - Analizar tendencias y diferencias clave.
3. **Storytelling y presentación**
    - Redactar la narrativa que conecta los hallazgos.
    - Integrar visualizaciones y conclusiones.
    - Preparar el bloque de storytelling para la presentación.
4. **Recomendaciones de visualización**
    - Sugerir herramientas y ejemplos de código (`matplotlib`, `seaborn`, `plotly`).

#### 💰 Vanesa – Investment Analyst

**Objetivo:** Analizar y visualizar la rentabilidad y oportunidades de inversión.

**Pasos y tareas:**
1. **Definición y cálculo de indicadores**
    - Documentar indicadores: ROI, rentabilidad bruta, payback, precio m².
    - Investigar fuentes externas para precios de referencia.
    - Calcular estos indicadores en el notebook `notebooks/03_investment_analysis.ipynb`.
2. **Visualización de resultados**
    - Crear gráficos de barras, mapas de calor y rankings de zonas.
    - Comparar oportunidades entre ciudades y barrios.
3. **Recomendaciones para inversores**
    - Redactar conclusiones y sugerencias basadas en los datos.

#### 🛏️ Maribel – Operations Analyst

**Objetivo:** Optimizar la operación para hosts y analizar performance operativa.

**Pasos y tareas:**
1. **Definición de métricas operativas**
    - Seleccionar métricas: disponibilidad, pricing, amenities, reviews.
    - Investigar benchmarks y mejores prácticas.
    - Documentar el análisis en el notebook `notebooks/04_operations_analysis.ipynb`.
2. **Análisis y visualización**
    - Analizar datos por ciudad y tipo de propiedad.
    - Crear boxplots, heatmaps y gráficos de reviews.
3. **Recomendaciones para hosts**
    - Listar acciones concretas para mejorar performance.

---

### 💡 Recomendaciones para avanzar

- **Cada rol debe documentar su proceso en un notebook individual** (ver estructura abajo).
- **Estandarizar nombres de columnas y formatos** desde el inicio.
- **Incluir la columna `ciudad`** en todos los datasets.
- **Proponer y consensuar una estructura de carpetas y notebooks** para análisis individuales y globales.
- **Definir criterios de comparabilidad y métricas prioritarias** en equipo.
- **Utilizar issues de GitHub** para asignar tareas y dar seguimiento.
- **Compartir ejemplos de visualizaciones y consultas SQL** útiles para todos.
- **No presentar tareas de limpieza en la presentación**, pero asegurar la comparabilidad.

**Frase útil para la presentación:**  
> “Para garantizar comparabilidad entre ciudades, estructuramos los datos de forma unificada y aplicamos métricas consistentes en todo el análisis.”

---

## 📁 Estructura del Repositorio

```
airbnb-analysis-investment-hosts-multicity/
├── README.md
├── data/
│   ├── madrid.csv
│   ├── barcelona.csv
│   ├── valencia.csv
│   ├── malaga.csv
│   ├── madrid_limpio.csv
│   ├── barcelona_limpio.csv
│   ├── valencia_limpio.csv
│   ├── malaga_limpio.csv
│   ├── merged_airbnb.csv  # Dataset combinado con columna “ciudad”
│   └── airbnb.db         # Base de datos SQLite
├── notebooks/
│   ├── 01_data_engineer_preprocessing.ipynb
│   ├── 02_bi_kpis_comparativos.ipynb
│   ├── 03_investment_analysis.ipynb
│   ├── 04_operations_analysis.ipynb
│   └── 05_dashboard_building.ipynb
├── streamlit/
│   └── app/
│       └── app.py
├── presentation/
│   ├── slides.pdf
│   └── screenshots/
├── docs/
└── technical_notes.md
```

**Notas:**
- Cada notebook corresponde a una tarea/rol, no a una ciudad.
- El notebook `05_dashboard_building.ipynb` documenta la integración técnica y visual del dashboard.

---

## 🛠️ Guía técnica para cada rol

### Patricia – Data Engineer

1. **Limpieza y unión de datasets:**  
    - Usar `pandas` para leer, limpiar y unir los archivos CSV.
    - Estandarizar nombres de columnas y tipos de datos.
    - Añadir columna `ciudad` si no existe.
    - Guardar archivos limpios y el dataset unificado.
2. **Carga en SQLite:**  
    ```python
    import sqlite3
    import pandas as pd

    df = pd.read_csv("data/merged_airbnb.csv")
    conn = sqlite3.connect("data/airbnb.db")
    df.to_sql("airbnb_data", conn, if_exists="replace", index=False)
    conn.close()
    ```
3. **Consulta desde Python/Streamlit:**  
    ```python
    conn = sqlite3.connect("data/airbnb.db")
    query = "SELECT * FROM airbnb_data WHERE ciudad = 'Madrid'"
    df_madrid = pd.read_sql(query, conn)
    conn.close()
    ```
4. **Documentar todo el proceso en el notebook correspondiente.**
5. **Coordinar integración técnica del dashboard.**

### Pablo – Business Intelligence

1. **Definir KPIs y métricas clave** junto al equipo.
2. **Proponer visualizaciones comparativas** (ej: ranking de ciudades, mapas de calor).
3. **Integrar resultados y redactar storytelling final.**
4. **Ejemplo de visualización:**  
    ```python
    import seaborn as sns
    sns.barplot(data=df, x="ciudad", y="ingresos_mensuales")
    ```
5. **Recomendar estructura de presentación de insights.**

### Vanesa – Investment Analyst

1. **Definir indicadores de inversión:**  
    - ROI = (Ingresos netos anuales / Inversión inicial) * 100
    - Rentabilidad bruta, payback, etc.
2. **Investigar precios de referencia externos.**
3. **Ejemplo de cálculo de ROI:**  
    ```python
    df['ROI'] = (df['ingresos_anuales'] / df['precio_compra']) * 100
    ```
4. **Preparar visualizaciones de inversión.**
5. **Documentar todo en el notebook correspondiente.**

### Maribel – Operations Analyst

1. **Definir métricas operativas:**  
    - Disponibilidad, pricing, amenities, reviews.
2. **Investigar benchmarks y mejores prácticas.**
3. **Ejemplo de análisis de reviews:**  
    ```python
    df.groupby('ciudad')['reviews'].mean().plot(kind='bar')
    ```
4. **Preparar recomendaciones para hosts.**
5. **Documentar todo en el notebook correspondiente.**

---

## 📊 Streamlit – Estructura sugerida

```python
st.title("Análisis Airbnb – Inversión + Operación")

st.sidebar.selectbox("Ciudad", options=["Madrid", "Barcelona", "Valencia", "Málaga"])
tab1, tab2, tab3 = st.tabs(["📈 Inversión", "💼 Operación", "🧭 Comparativa"])

with tab1:
    # ROI, ingresos, zonas recomendadas
with tab2:
    # Pricing, amenities, performance de hosts
with tab3:
    # Ranking de ciudades, resumen visual, mapas
```

---

## 🧠 Organización interna y mejores prácticas

- **Mantener nombres de columnas estandarizados** en todas las ciudades.
- **Incluir columna `ciudad`** desde el inicio.
- **Trabajar notebooks individuales** pero alineados visual y conceptualmente.
- **Visualizaciones claras** con títulos y ejes explicativos.
- **No presentar tareas de limpieza**, pero sí asegurar comparabilidad.

---

## 🎤 Estructura de Presentación – Ajustada al Formato Oficial del Profesor (25 minutos)

| # | Bloque                                              | Duración | Presenta (Rol)                |
|---|-----------------------------------------------------|----------|-------------------------------|
| 1 | 🎯 Contexto del Rol Dual                            | 3 min    | Pablo (Business Intelligence) |
| 2 | 🛠️ Metodología Integrada                            | 5 min    | Patricia (Data Engineer)      |
| 3 | 💸 Análisis de Inversión                            | 6 min    | Vanesa (Investment Analyst)   |
| 4 | 🛏️ Análisis Operacional                             | 6 min    | Maribel (Operations Analyst)  |
| 5 | 📊 Recomendaciones Integradas + Storytelling        | 5 min    | Pablo (Business Intelligence) |

---

### Q&A

- **Patricia:** Preguntas técnicas (dashboard, estructura, base de datos)
- **Vanesa:** Preguntas sobre inversión y ROI
- **Maribel:** Preguntas sobre operaciones, optimización
- **Pablo:** Preguntas sobre decisiones estratégicas y visión general

---

### Notas para preparación

- No se menciona limpieza de datos.
- Se presenta por temática, no por ciudad.
- SQLite se usa como base técnica.
- El dashboard sirve como narrativa final.

**Frase útil para evitar mencionar limpieza:**  
> “Para asegurar comparabilidad entre las ciudades, se estructuraron los datos bajo un mismo formato y se aplicaron las mismas métricas clave en todo el análisis.”

---

## 🗃️ Uso de SQLite en el Proyecto

**SQLite** es obligatorio como base de datos local mínima:

- Almacena el dataset unificado (`merged_airbnb.csv`)
- Permite consultas por ciudad o filtros personalizados
- Sirve datos al dashboard de Streamlit

### Ejemplo de carga y consulta

```python
import sqlite3
import pandas as pd

# Cargar datos
df = pd.read_csv("data/merged_airbnb.csv")
conn = sqlite3.connect("data/airbnb.db")
df.to_sql("airbnb_data", conn, if_exists="replace", index=False)
conn.close()

# Consultar datos de una ciudad
conn = sqlite3.connect("data/airbnb.db")
df_madrid = pd.read_sql("SELECT * FROM airbnb_data WHERE ciudad = 'Madrid'", conn)
conn.close()
```

---

## ✅ Stack tecnológico

- `Python`: pandas, seaborn, matplotlib, plotly
- `Streamlit`: dashboard central
- `SQLite`: almacenamiento de datos
- `GitHub`: versionado y colaboración

---

## 🧠 Storytelling y cierre narrativo

El storytelling conecta los análisis con un **mensaje claro y accionable** para inversores y hosts.  
Debe incluir:

| Elemento                         | Descripción                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| **Narrativa clara y sencilla**   | ¿Por qué se hizo este análisis? ¿Qué decisiones permite tomar?              |
| **Comparación clave entre ciudades** | ¿Dónde conviene invertir? ¿Dónde conviene operar como host?                |
| **Visuales que acompañen insights** | Ranking, gráficos de ROI, estacionalidad, pricing, mapas, etc.             |
| **Conclusión accionable**        | Qué debería hacer un inversor y qué debería mejorar un host                |
| **Visión 360°**                  | Cómo se complementan la inversión y la operación                           |

**Ejemplo de cierre narrativo:**  
> “Nuestro análisis de cuatro ciudades estratégicas muestra que **Barcelona lidera en ingresos brutos**, pero **Valencia y Málaga presentan un mejor ROI para inversores**. Para los hosts, **Madrid y Málaga destacan por su estacionalidad y eficiencia operativa**. La clave está en combinar rentabilidad con sostenibilidad, y elegir zonas emergentes con alto potencial de crecimiento.”

---

¿Listos para brillar?  
Con esta estructura, cada uno aporta desde su especialidad, pero todos hablan el mismo idioma 📊🚀

---

## 🏙️ Justificación de la selección de ciudades

Las cuatro ciudades seleccionadas — **Madrid, Barcelona, Valencia y Málaga** — representan polos clave del mercado Airbnb en España por su relevancia turística, diversidad de perfiles de viajeros y dinamismo inmobiliario:

- **Madrid** y **Barcelona**: principales destinos urbanos, alta demanda internacional, mercados maduros y competitivos.
- **Valencia**: ciudad en crecimiento, atractiva para inversión por su relación calidad-precio y auge turístico reciente.
- **Málaga**: referente en turismo vacacional, fuerte estacionalidad y oportunidades en zonas emergentes.

Esta selección permite comparar realidades diversas y extraer aprendizajes aplicables a distintos contextos urbanos y turísticos.

---

## ⚠️ Matriz de riesgos y posibles limitaciones

| Riesgo / Limitación                        | Impacto Potencial                         | Mitigación / Nota Actual                |
|--------------------------------------------|-------------------------------------------|-----------------------------------------|
| Diferencias en calidad y cobertura de datos| Puede afectar comparabilidad              | Estandarización y limpieza exhaustiva   |
| Cobertura desigual de barrios              | Análisis menos granular en algunas ciudades| Foco en métricas globales y por ciudad  |
| Fuentes externas con metodologías distintas| Variabilidad en precios de referencia     | Documentar fuentes y criterios usados   |
| Cambios recientes en regulación Airbnb     | Dificultad para proyectar tendencias      | Contextualizar resultados en la narrativa|
| Datos faltantes o nulos                    | Sesgo en análisis de KPIs                 | Imputación o exclusión justificada      |

---

## 🌐 Breve mención de fuentes externas

Para enriquecer el análisis de inversión, se consultarán fuentes externas como:

- **Portales inmobiliarios** (Idealista, Fotocasa) para precios de referencia de compra y alquiler.
- **Instituto Nacional de Estadística (INE)** para datos de turismo y contexto socioeconómico.
- **Ayuntamientos y normativas locales** para información sobre regulación de alquiler turístico.

Estas fuentes se citarán en los notebooks correspondientes y se utilizarán solo como referencia contextual, no como dato principal.

---

## ☑️ Checklist de entregables

| Entregable                        | Descripción                                              | Responsable(s)         |
|-----------------------------------|----------------------------------------------------------|------------------------|
| Datasets limpios por ciudad       | CSVs estandarizados con columna `ciudad`                 | Data Engineer          |
| Dataset unificado (`merged_airbnb.csv`) | Consolidado y validado                              | Data Engineer          |
| Base de datos SQLite (`airbnb.db`)| Carga del dataset unificado                             | Data Engineer          |
| Notebooks individuales            | 01_data_engineer_preprocessing.ipynb, etc.              | Cada rol               |
| Notebook de integración dashboard | 05_dashboard_building.ipynb                             | Data Engineer          |
| Dashboard Streamlit               | Visualización interactiva                               | Todo el equipo         |
| Presentación final (`slides.pdf`) | Resumen ejecutivo y storytelling                        | Todo el equipo         |
| Documentación técnica (`README.md`, `technical_notes.md`) | Guía de uso y decisiones técnicas         | Data Engineer, BI      |

---

## 🔒 Nota sobre ética y datos personales

El análisis se realiza exclusivamente con **datos públicos y anonimizados**. Se respeta la privacidad de los usuarios y se cumplen las normativas vigentes sobre protección de datos.

---

## 📚 Recursos clave y navegación

- [README del proyecto](https://github.com/vfpomer/Analisis-de-inversion-inmobiliario/blob/main/README.md): guía rápida de estructura, instalación y objetivos.
- [technical_notes.md](../technical_notes.md): detalles técnicos y decisiones de ingeniería.
- [Repositorio en GitHub](https://github.com/vfpomer/Analisis-de-inversion-inmobiliario): para seguimiento de issues y colaboración.