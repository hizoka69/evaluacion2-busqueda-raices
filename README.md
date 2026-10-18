# Evaluación 2 — La raíz que se esconde

Universidad Católica del Maule, Laboratorio Evaluado 2.

Integrantes: Blas Rojas Díaz y Joaquín Hernández Castro.

## Qué hace el proyecto

Implementa seis métodos de búsqueda de raíces (bisección, falsa posición, punto fijo, secante, Newton-Raphson y Newton mejorado) y los compara en seis funciones: polinómica, polinómica con raíz doble, logarítmica, exponencial, trigonométrica y mixta. La tolerancia es 1e-6 y el máximo es 100 iteraciones. Las conclusiones están en [informe.md](informe.md).

## Estructura

```text
evaluacion2-busqueda-raices/
├── README.md
├── requirements.txt
├── informe.md
└── src/
    ├── scripts/   código Python
    ├── data/      CSV generados
    └── assets/    gráficos PNG generados
```

## Scripts (src/scripts/)

- `main.py`: es el que se ejecuta. Corre todo y guarda los CSV y los gráficos.
- `funciones.py`: define las seis funciones, sus derivadas, la g(x) del punto fijo, los intervalos y las estimaciones iniciales.
- `verificacion.py`: comprueba que hay raíz (cambio de signo, o tangencia en la raíz doble).
- `metodos.py`: los seis métodos.
- `analisis.py`: ejecuta los métodos por función y calcula error y orden de convergencia.
- `graficos.py`: genera los gráficos con matplotlib.
- `sensibilidad.py`: prueba distintos intervalos y estimaciones iniciales (pregunta 5 del informe).

## Cómo ejecutarlo

Clonar el repositorio y crear el entorno virtual:

```bash
git clone https://github.com/hizoka69/evaluacion2-busqueda-raices.git
cd evaluacion2-busqueda-raices
python -m venv .venv
```

Activarlo:

```bash
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

Instalar dependencias y ejecutar:

```bash
pip install -r requirements.txt
python src/scripts/main.py
```

## Resultados

- `src/data/`: un CSV `(x, f(x))` por función, `resumen_convergencia.csv`, `verificacion_raices.csv` y `sensibilidad.csv`.
- `src/assets/`: gráfico de cada función con su raíz, gráfico de convergencia |error| vs iteración (escala log), `resumen_iteraciones.png` y los dos gráficos de sensibilidad.
