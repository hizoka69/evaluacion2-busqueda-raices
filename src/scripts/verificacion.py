"""
verificacion.py
===============
Demuestra numéricamente que cada función tiene raíz dentro del rango:

  * Funciones que cruzan el eje  -> Teorema de Bolzano: f continua en [a, b]
    y f(a)·f(b) < 0  =>  existe al menos una raíz en (a, b). Además se
    comprueba que f' no cambia de signo en [a, b] (f monótona => raíz única).

  * Función con raíz doble (x-2)^2 -> tangencia al eje x: f(r) = 0, f'(r) = 0,
    f''(r) > 0 y f(x) >= 0 en todo el rango (la curva toca el eje sin cruzarlo,
    por lo que Bolzano NO es aplicable aunque la raíz exista).
"""
import numpy as np

from funciones import Funcion


def verificar(func: Funcion, raiz: float) -> dict:
    fa, fb = float(func.f(func.a)), float(func.f(func.b))
    producto = fa * fb
    x = np.linspace(func.a, func.b, 2001)
    with np.errstate(all="ignore"):
        dfx = func.df(x)
    monotona = bool(np.all(dfx > 0) or np.all(dfx < 0))

    fila = {
        "funcion": func.clave,
        "expresion": func.expresion,
        "a": func.a, "b": func.b,
        "f(a)": fa, "f(b)": fb,
        "f(a)*f(b)": producto,
        "bolzano_cumple": producto < 0,
        "raiz_unica_en_[a,b]": monotona and producto < 0,
        "f(r)": float(func.f(raiz)),
        "f'(r)": float(func.df(raiz)),
        "f''(r)": float(func.d2f(raiz)),
        "tangencia": False,
        "conclusion": "",
    }

    if func.raiz_doble:
        xs = np.linspace(*func.rango_grafico, 4001)
        sin_cambio = bool(np.all(func.f(xs) >= -1e-15))
        tangencia = (abs(fila["f(r)"]) < 1e-12 and abs(fila["f'(r)"]) < 1e-12
                     and fila["f''(r)"] > 0 and sin_cambio)
        fila["tangencia"] = bool(tangencia)
        fila["conclusion"] = (
            "Raíz doble: f(r)=0, f'(r)=0, f''(r)>0 y f(x)>=0 en todo el rango "
            "(tangencia al eje). f(a)·f(b)>0, Bolzano no aplica."
        )
    else:
        fila["conclusion"] = (
            f"Bolzano: f(a)·f(b)={producto:.4g} < 0 => existe raíz en ({func.a}, {func.b}); "
            + ("f' no cambia de signo => raíz única." if monotona
               else "f' cambia de signo: podría haber más de una raíz.")
        )
    return fila
