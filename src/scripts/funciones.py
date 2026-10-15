"""
funciones.py
============
Definición de las seis funciones de prueba (ambiente controlado).

Cada función se entrega junto con:
  * f, f', f''   : necesarias para Newton-Raphson y Newton-Raphson mejorado.
  * g(x)         : despeje x = g(x) para el método de punto fijo.
  * [a, b]       : intervalo para los métodos cerrados (bisección, falsa posición).
  * x0 y (x0,x1) : estimaciones iniciales para los métodos abiertos.
  * rango_grafico: ventana de x usada para graficar y generar el CSV (x, f(x)).

Todo el cálculo se hace con numpy.
"""
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import numpy as np


@dataclass(frozen=True)
class Funcion:
    clave: str                       # identificador (nombres de archivos)
    nombre: str                      # nombre corto para títulos
    categoria: str
    expresion: str                   # f(x) en texto
    f: Callable
    df: Callable
    d2f: Callable
    g: Callable                      # función de iteración para punto fijo
    expr_g: str
    a: float                         # extremos del intervalo [a, b]
    b: float
    x0: float                        # estimación inicial (Newton, punto fijo)
    secante: Tuple[float, float]     # (x0, x1) para el método de la secante
    rango_grafico: Tuple[float, float]
    raiz_exacta: Optional[float] = None   # solo si se conoce analíticamente
    raiz_doble: bool = False


FUNCIONES = [
    Funcion(
        clave="f1_polinomica_simple",
        nombre="Polinómica (raíz simple)",
        categoria="Polinómica",
        expresion="f(x) = x^3 - x - 2",
        f=lambda x: x**3 - x - 2,
        df=lambda x: 3 * x**2 - 1,
        d2f=lambda x: 6 * x,
        g=lambda x: np.cbrt(x + 2),
        expr_g="g(x) = (x + 2)^(1/3)",
        a=1.0, b=2.0, x0=1.5, secante=(1.0, 2.0),
        rango_grafico=(0.5, 2.5),
    ),
    Funcion(
        clave="f2_polinomica_doble",
        nombre="Polinómica (raíz doble)",
        categoria="Polinómica (raíz doble)",
        expresion="f(x) = (x - 2)^2",
        f=lambda x: (x - 2) ** 2,
        df=lambda x: 2 * (x - 2),
        d2f=lambda x: 2.0 + 0.0 * x,
        g=lambda x: x - (x - 2) ** 2,
        expr_g="g(x) = x - f(x)",
        a=1.0, b=3.0, x0=1.2, secante=(1.2, 1.5),
        rango_grafico=(1.0, 3.0),
        raiz_exacta=2.0, raiz_doble=True,
    ),
    Funcion(
        clave="f3_logaritmica",
        nombre="Logarítmica",
        categoria="Logarítmica",
        expresion="f(x) = ln(x) + x - 4",
        f=lambda x: np.log(x) + x - 4,
        df=lambda x: 1 / x + 1,
        d2f=lambda x: -1 / x**2,
        g=lambda x: 4 - np.log(x),
        expr_g="g(x) = 4 - ln(x)",
        a=2.0, b=3.0, x0=2.5, secante=(2.0, 3.0),
        rango_grafico=(1.0, 4.0),
    ),
    Funcion(
        clave="f4_exponencial",
        nombre="Exponencial",
        categoria="Exponencial",
        expresion="f(x) = e^(-x) - x",
        f=lambda x: np.exp(-x) - x,
        df=lambda x: -np.exp(-x) - 1,
        d2f=lambda x: np.exp(-x),
        g=lambda x: np.exp(-x),
        expr_g="g(x) = e^(-x)",
        a=0.0, b=1.0, x0=0.5, secante=(0.0, 1.0),
        rango_grafico=(-0.5, 1.5),
    ),
    Funcion(
        clave="f5_trigonometrica",
        nombre="Trigonométrica",
        categoria="Trigonométrica",
        expresion="f(x) = cos(x) - x",
        f=lambda x: np.cos(x) - x,
        df=lambda x: -np.sin(x) - 1,
        d2f=lambda x: -np.cos(x),
        g=lambda x: np.cos(x),
        expr_g="g(x) = cos(x)",
        a=0.0, b=1.0, x0=0.5, secante=(0.0, 1.0),
        rango_grafico=(-0.5, 1.5),
    ),
    Funcion(
        clave="f6_mixta",
        nombre="Mixta (raíz + trigonométrica)",
        categoria="Mixta",
        expresion="f(x) = sqrt(x) - cos(x)",
        f=lambda x: np.sqrt(x) - np.cos(x),
        df=lambda x: 1 / (2 * np.sqrt(x)) + np.sin(x),
        d2f=lambda x: -1 / (4 * x**1.5) + np.cos(x),
        g=lambda x: x - (np.sqrt(x) - np.cos(x)),
        expr_g="g(x) = x - f(x)",
        a=0.1, b=1.0, x0=0.55, secante=(0.1, 1.0),
        rango_grafico=(0.01, 1.2),
    ),
]


def raiz_referencia(func: Funcion) -> float:
    """
    Raíz de referencia contra la cual se mide el error |x_n - raíz|.
    Si se conoce analíticamente se usa tal cual; si no, se calcula con 200
    bisecciones en float64 (precisión de máquina), independiente de los
    métodos que se evalúan.
    """
    if func.raiz_exacta is not None:
        return float(func.raiz_exacta)
    a, b = func.a, func.b
    fa = func.f(a)
    for _ in range(200):
        c = 0.5 * (a + b)
        fc = func.f(c)
        if fa * fc <= 0:
            b = c
        else:
            a, fa = c, fc
    return float(0.5 * (a + b))
