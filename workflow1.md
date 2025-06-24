# 🧭 Proyecto Airbnb – Análisis Dual: Inversión + Operación

## 🧑‍🤝‍🧑 Equipo y Estructura

Este proyecto se basa en el análisis del mercado Airbnb en **cuatro ciudades clave de España** con una **perspectiva dual**:  
- 🏢 Inversión: oportunidades de rentabilidad, ROI y zonas estratégicas  
- 🧑‍💼 Operación: optimización para hosts actuales, pricing y posicionamiento

### 👥 Integrantes y ciudades asignadas

| Nombre    | Ciudad     | Rol/Responsabilidad |
|-----------|------------|----------------------|
| Vanesa    | Valencia   | Análisis completo: inversión + operación en Valencia + integración general |
| Maribel   | Barcelona  | Análisis completo: inversión + operación en Barcelona + **Opcional** PowerBI |
| Pablo     | Madrid     | Análisis completo: inversión + operación en Madrid + Storytelling |
| Patricia  | Málaga     | Análisis completo en Málaga + Dashboard (Streamlit) |

---

## 🧱 Estructura de Trabajo

Cada integrante:
- Trabaja su ciudad de forma independiente
- Aplica un enfoque dual: inversión + operación
- Explora datos internos (dataset principal) y opcionales externos (precio vivienda, m², barrios)
- Prepara visualizaciones, insights y recomendaciones locales

La integración y unificación visual se hace en el dashboard final y en la presentación grupal.

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
│   └── merged_airbnb.csv ← dataset combinado con columna “ciudad”
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

## 📌 Flujo de Trabajo (orden sugerido)

1. **Exploración individual por ciudad**
   - Investigar qué se puede incluir
   - Buscar fuentes externas si se desea (precio m², zonas, turismo, etc.)

2. **Preprocesamiento interno por ciudad**
   - Columnas clave, nulos, consistencia → Sin mencionarlo en la presentación

3. **Análisis local**
   - Inversión: ROI, ingreso, zonas rentables
   - Operación: pricing óptimo, amenities, reviews, estacionalidad

4. **Unificación y dashboard**
   - Consolidar en `merged_airbnb.csv`
   - 
   - Estructura el dashboard con tabs/filtros por ciudad y rol

5. **Comparativa entre ciudades**
   - Ranking ROI
   - Recomendaciones generales
   - Insights clave agrupados

---

## 📊 ¿Qué debe incluir cada análisis por ciudad?

### Perspectiva de Inversión:
- Precio promedio por noche
- Ingreso mensual estimado
- ROI estimado *(opcional: si incluyen precio vivienda externa)*
- Zonas con mejor rentabilidad

### Perspectiva Operacional:
- Estacionalidad (ocupación por mes)
- Reviews y puntuaciones promedio
- Pricing óptimo
- Amenities más frecuentes y diferenciadores
- Recomendaciones para hosts actuales

---

### 📊 Streamlit – Estructura sugerida

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

## 🧠 Recomendaciones para organización interna

- Mantener nombres de columnas estandarizados en todas las ciudades
- Incluir columna `ciudad` desde el inicio
- Trabajar notebooks individuales pero alineados visual y conceptualmente
- Visualizaciones claras con títulos y ejes explicativos
- No presentar tareas de limpieza, pero sí asegurar comparabilidad

**Frase útil en la presentación para evitar hablar de limpieza directamente:**
> “Para garantizar comparabilidad entre ciudades, estructuramos los datos de forma unificada y aplicamos métricas consistentes en todo el análisis.”

---

## 📤 Presentación Final – Guion por minutos

| Tiempo  | Persona     | Contenido |
|---------|-------------|-----------|
| 0–3     | Maribel     | Introducción del proyecto, enfoque dual, motivación y ciudades elegidas |
| 3–4     | Vanesa      | Metodología integrada: estructura común, herramientas y coordinación |
| 4–7     | Vanesa      | Análisis de Valencia: inversión y operación |
| 7–10    | Maribel     | Análisis de Barcelona: inversión y operación |
| 10–13   | Pablo       | Análisis de Madrid: inversión y operación |
| 13–16   | Patricia    | Análisis de Málaga: inversión y operación |
| 16–20   | Patricia    | Demo del Dashboard interactivo (Streamlit) (**Maribel** también si se incluye PowerBI) |
| 20–23   | Pablo       | Comparativa entre ciudades, top insights y recomendaciones globales |
| 23–25   | Todos       | Ronda de preguntas y cierre |

📌 Durante el Q&A, responde cada quien según el tema preguntado (ciudad o perspectiva).

---

### 🎤 Sección Final: Storytelling y Cierre Narrativo

#### 🧠 ¿Qué es el storytelling en este proyecto?

El storytelling conecta todos los análisis con un **mensaje claro y accionable** para los usuarios (inversores y hosts). Es la parte donde el equipo **explica el “por qué” y el “para qué”** de los datos y visualizaciones.

Esta narrativa se debe integrar en la sección de la presentación:

> ✅ **Comparativa entre ciudades + Insights clave + Recomendaciones**

---

### ✅ ¿Qué debe incluir el storytelling final?

| Elemento                         | Descripción                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| **Narrativa clara y sencilla**   | ¿Por qué se hizo este análisis? ¿Qué decisiones permite tomar?              |
| **Comparación clave entre ciudades** | ¿Dónde conviene invertir? ¿Dónde conviene operar como host?                |
| **Visuales que acompañen insights** | Ranking, gráficos de ROI, estacionalidad, pricing, mapas, etc.             |
| **Conclusión accionable**        | Qué debería hacer un inversor y qué debería mejorar un host                |
| **Visión 360°**                  | Cómo se complementan la inversión y la operación                           |

---

### 🧾 Ejemplos de cierre narrativo adaptables

#### 🎯 Ejemplo 1 (directo y profesional)
> “Nuestro análisis de cuatro ciudades estratégicas muestra que **Barcelona lidera en ingresos brutos**, pero **Valencia y Málaga presentan un mejor ROI para inversores**. Para los hosts, **Madrid y Málaga destacan por su estacionalidad y eficiencia operativa**. La clave está en combinar rentabilidad con sostenibilidad, y elegir zonas emergentes con alto potencial de crecimiento.”

---

#### 💡 Ejemplo 2 (enfocado al usuario del dashboard)
> “Gracias a este análisis comparativo y al dashboard interactivo, cualquier usuario puede **explorar oportunidades de inversión o mejora operativa en tiempo real**. Ya sea un inversor buscando maximizar retorno, o un host optimizando su alojamiento, este panel ofrece una herramienta clara para tomar decisiones informadas.”

---

#### 🧩 Ejemplo 3 (visión completa del equipo)
> “Desde el rol dual de inversión y operación, hemos detectado patrones que se repiten: los mejores resultados se logran cuando se alinea el tipo de propiedad, el canal adecuado y el momento del año. Esta visión 360º entre ciudades y perfiles permite generar estrategias más efectivas y sostenibles.”

---

#### 🎤 ¿Quién lo presenta?

- Puede presentarlo una sola persona.
- O puede ser **compartido entre todos**: 1 insight global por ciudad.

---

### 🪄 Recomendaciones rápidas

- Evitar repasar todo el análisis: enfóquense en el **"para qué sirve"**.
- Hablen con seguridad, como si ustedes **fueran los analistas contratados**.
- Cierren con 1 idea clave: “Si tuviera que invertir mañana, me iría a…” o “Un host debería evitar…”

---

## 📌 Roles Reforzados para Equilibrio

- Cada persona **presenta su ciudad**, no su especialización técnica.

---

## 🗃️ Uso de SQLite en el Proyecto

Según los requisitos del proyecto, el uso de **SQLite como base de datos local mínima es obligatorio**:

> **Herramientas obligatorias:**
> - Python (Pandas, NumPy, Matplotlib, Seaborn, Plotly)
> - **SQLite: base de datos local mínima**
> - Streamlit
> - GitHub

---

### ✅ ¿Cómo se aplica SQLite en nuestro proyecto?

Usamos **SQLite** como motor de base de datos para:
- Almacenar el dataset unificado (`merged_airbnb.csv`)
- Realizar consultas por ciudad o filtros personalizados
- Servir datos directamente al dashboard de Streamlit (opcional)

Esto nos permite trabajar con un flujo de datos más profesional y replicable.

---

### 🛠️ Crear una base de datos SQLite con Pandas

```python
import sqlite3
import pandas as pd

# Leer el dataset combinado
df = pd.read_csv("data/merged_airbnb.csv")

# Conexión y creación de la base de datos
conn = sqlite3.connect("data/airbnb.db")

# Guardar la tabla en SQLite
df.to_sql("airbnb_data", conn, if_exists="replace", index=False)

conn.close()
```

---

### 🔍 Consultar datos desde SQLite

Por ejemplo, para cargar los datos de Madrid:

```python
import sqlite3
import pandas as pd

# Conectar a la base de datos
conn = sqlite3.connect("data/airbnb.db")

# Consulta SQL
query = "SELECT * FROM airbnb_data WHERE ciudad = 'Madrid'"
df_madrid = pd.read_sql(query, conn)

conn.close()
```

---

### 📦 ¿Dónde se utiliza SQLite en el proyecto?
- En los notebooks técnicos (dashboard_building.ipynb)
- Opcionalmente en el archivo de Streamlit (app.py)
- Almacenamiento de datos estructurados y limpios de forma persistente

---

### 🗣️ ¿Cómo lo explicamos en la presentación?

> “El dataset final fue cargado en una base de datos SQLite para facilitar la consulta por ciudad y el uso posterior en el dashboard. Esto nos permitió trabajar con filtros y estructuras más robustas desde una sola fuente centralizada.”

---

## ✅ Stack tecnológico

- `Python`: pandas, seaborn, matplotlib, plotly
- `Streamlit`: dashboard central
- `SQLite`: para almacenamiento
- `Power BI`: opcional (puede integrarse en dashboard)
- `GitHub`: versionado y colaboración

---

¿Listos para brillar?  
Con esta estructura, cada uno aporta desde su ciudad pero todos hablan el mismo idioma 📊🚀