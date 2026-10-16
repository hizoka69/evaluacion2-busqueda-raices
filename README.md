# Evaluación 2 — La raíz que se esconde

**Universidad Católica del Maule — Laboratorio Evaluado 2**

**Unidad:** Iteración funcional para ecuaciones, búsqueda de raíces y análisis de convergencia.

**Integrantes:**
- Blas Rojas Díaz
- Joaquín Hernández Castro

## Descripción

Este proyecto implementa seis métodos numéricos para encontrar raíces de ecuaciones y comparar su convergencia en diferentes tipos de funciones.

Los métodos utilizados son:

1. Bisección
2. Falsa posición
3. Punto fijo
4. Secante
5. Newton-Raphson
6. Newton-Raphson mejorado

Se trabaja con una tolerancia de `1e-6` y un máximo de 100 iteraciones por método.

También se generan gráficos, archivos CSV y un análisis de sensibilidad para comparar los resultados.

## Estructura del proyecto

```text
evaluacion2-busqueda-raices/
├── README.md
├── requirements.txt
├── informe.md
├── .gitignore
└── src/
    ├── scripts/
    │   ├── main.py
    │   ├── funciones.py
    │   ├── verificacion.py
    │   ├── metodos.py
    │   ├── analisis.py
    │   ├── graficos.py
    │   └── sensibilidad.py
    ├── assets/
    └── data/
```

La carpeta `scripts` contiene el código Python. En `assets` se guardan los gráficos y en `data` los resultados CSV.

## Requisitos

- Python 3
- Bibliotecas indicadas en `requirements.txt`

## Instalación

Primero, clonar el repositorio:

```bash
git clone https://github.com/hizoka69/evaluacion2-busqueda-raices.git
cd evaluacion2-busqueda-raices
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo en Windows usando PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Desde la carpeta principal del proyecto, ejecutar:

```bash
python src/scripts/main.py
```

El programa realiza las verificaciones matemáticas, ejecuta los métodos numéricos y genera los archivos de resultados.

## Resultados

Los archivos se guardan en las siguientes carpetas:

- `src/data/`: resultados de los métodos, verificación de raíces y análisis de sensibilidad en formato CSV.
- `src/assets/`: gráficos de las funciones, convergencia, iteraciones y sensibilidad.

Los gráficos de convergencia utilizan una escala logarítmica para visualizar mejor la reducción del error absoluto.

## Informe

El desarrollo matemático, la comparación de los métodos y las conclusiones se encuentran en [informe.md](informe.md).