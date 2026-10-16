from typing import List, Tuple
import numpy as np
import metodos as m
from funciones import Funcion

#ejecuta 6 metodos sobre las funciones y calcula las metricas de convergencia
def ejecutar_metodos(func: Funcion, tol: float = m.TOL) -> List[Tuple[m.Resultado, str]]:
    """Devuelve [(Resultado, descripción de parámetros iniciales), ...]."""
    f, a, b = func.f, func.a, func.b
    x0s, x1s = func.secante
    return [
        (m.biseccion(f, a, b, tol), f"[{a}, {b}]"),
        (m.falsa_posicion(f, a, b, tol), f"[{a}, {b}]"),
        (m.punto_fijo(f, func.g, func.x0, tol), f"x0={func.x0}"),
        (m.secante(f, x0s, x1s, tol), f"x0={x0s}, x1={x1s}"),
        (m.newton_raphson(f, func.df, func.x0, tol), f"x0={func.x0}"),
        (m.newton_mejorado(f, func.df, func.d2f, func.x0, tol), f"x0={func.x0}"),
    ]


def errores(res: m.Resultado, raiz: float) -> np.ndarray:
    #error abs |x_n - raiz| en por iteracion
    return np.abs(np.asarray(res.historial, dtype=float) - raiz)


def orden_empirico(err: np.ndarray) -> float:
    #estima orden de convergencia a partir de 3 errores
    e = err[err > 1e-14]
    if len(e) < 3:
        return float("nan")
    with np.errstate(all="ignore"):
        p = np.log(e[2:] / e[1:-1]) / np.log(e[1:-1] / e[:-2])
    p = p[np.isfinite(p)]
    return float(np.median(p)) if len(p) else float("nan")


def orden_extendido(func: Funcion, res_ext: m.Resultado, raiz_ref: float) -> float:
    if not res_ext.aplica or not res_ext.historial or not res_ext.convergio:
        return float("nan")
    if res_ext.metodo == "Bisección":      # error no monótono: p no es estimable
        return float("nan")
    iniciales = {"Secante": list(func.secante),
                 "Bisección": [func.a], "Falsa posición": [func.a]}.get(res_ext.metodo, [func.x0])
    serie = np.abs(np.array(iniciales + res_ext.historial, dtype=float) - raiz_ref)
    return orden_empirico(serie)


def metricas(func: Funcion, res: m.Resultado, raiz_ref: float, res_ext=None) -> dict:
    if res.historial:
        err = errores(res, raiz_ref)
        error = float(err[-1])
        paso = (abs(res.historial[-1] - res.historial[-2])
                if len(res.historial) > 1 else float("nan"))
        with np.errstate(all="ignore"):
            f_raiz = float(func.f(np.float64(res.raiz)))
        p = orden_extendido(func, res_ext, raiz_ref) if res_ext is not None else float('nan')
    else:
        error = paso = f_raiz = p = float("nan")
    return {"error": error, "paso_final": paso, "f_raiz": f_raiz, "orden_empirico": p}
