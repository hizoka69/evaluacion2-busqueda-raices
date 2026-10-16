import matplotlib
matplotlib.use("Agg")                      # no requiere pantalla
import matplotlib.pyplot as plt
import numpy as np
import metodos as m
from funciones import Funcion

ESTILO = {
    "Bisección":       ("tab:blue",   "o", "-"),
    "Falsa posición":  ("tab:orange", "s", "-"),
    "Punto fijo":      ("tab:green",  "^", "--"),
    "Secante":         ("tab:red",    "D", "-"),
    "Newton-Raphson":  ("tab:purple", "v", "-"),
    "Newton mejorado": ("tab:brown",  "P", "-"),
}
DPI = 150



#funcion con la raiz marcada
def graficar_funcion(func: Funcion, raiz: float, ruta: str) -> None:
    x = np.linspace(*func.rango_grafico, 600)
    with np.errstate(all="ignore"):
        y = func.f(x)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color="tab:blue", lw=2, label=func.expresion)
    ax.axhline(0, color="black", lw=1)

    if func.raiz_doble:
        ax.axvline(raiz, color="gray", ls=":", lw=1)
        ax.plot(raiz, 0, "ro", ms=9, zorder=5,
                label=f"Raíz doble r = {raiz:.1f} (tangente al eje x)")
        ax.annotate("f(2) = 0 y f'(2) = 0\nla curva toca el eje\nsin cruzarlo",
                    xy=(raiz, 0), xytext=(raiz + 0.15, 0.45),
                    arrowprops=dict(arrowstyle="->"), fontsize=9)
        ax.plot([func.a, func.b], [func.f(func.a)] * 2, "ks", ms=6,
                label=f"f(a)=f(b)={func.f(func.a):.0f} > 0: no hay cambio de signo")
        ax.axvspan(func.a, func.b, color="orange", alpha=0.08)
    else:
        fa, fb = func.f(func.a), func.f(func.b)
        ax.axvspan(func.a, func.b, color="orange", alpha=0.12, label=f"Intervalo [{func.a}, {func.b}]")
        ax.plot([func.a, func.b], [fa, fb], "ks", ms=6,
                label=f"f(a)={fa:.3f}, f(b)={fb:.3f} (cambio de signo)")
        ax.plot(raiz, 0, "ro", ms=9, zorder=5, label=f"Raíz r ≈ {raiz:.6f}")
        ax.axvline(raiz, color="gray", ls=":", lw=1)

    ax.set_title(f"{func.nombre}: {func.expresion}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(alpha=0.3)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=DPI)
    plt.close(fig)


#convergencia |error| vs iteracion
def graficar_convergencia(func: Funcion, raiz: float, resultados, ruta: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    no_aplica = []
    for res, _ in resultados:
        if not res.aplica:
            no_aplica.append(res.metodo)
            continue
        if not res.historial:
            continue
        err = np.maximum(np.abs(np.asarray(res.historial) - raiz), 1e-17)  # 0 no se ve en log
        it = np.arange(1, len(err) + 1)
        color, marca, linea = ESTILO[res.metodo]
        etiqueta = res.metodo if res.convergio else f"{res.metodo} ({res.estado.split(':')[0].lower()})"
        ax.semilogy(it, err, marker=marca, ls=linea, color=color, lw=1.6, ms=5, label=etiqueta)

    ax.axhline(m.TOL, color="gray", ls=":", lw=1.2, label="tol = 1e-6")
    ax.set_title(f"Convergencia: {func.nombre}\n{func.expresion}")
    ax.set_xlabel("Iteración n")
    ax.set_ylabel("|error| = |x_n − r|  (escala log)")
    ax.set_ylim(bottom=1e-17)
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="upper right", fontsize=8)
    if no_aplica:
        ax.text(0.02, 0.03, "No aplican (sin cambio de signo): " + ", ".join(no_aplica),
                transform=ax.transAxes, fontsize=8,
                bbox=dict(boxstyle="round", fc="lightyellow", ec="gray"))
    fig.tight_layout()
    fig.savefig(ruta, dpi=DPI)
    plt.close(fig)


# resumen de iteraciones por metodo y funcion
def graficar_resumen(todos: dict, ruta: str) -> None:
    """todos: {Funcion: [(Resultado, params), ...]}"""
    funciones = list(todos.keys())
    n_met = len(m.NOMBRES)
    ancho = 0.8 / n_met
    fig, ax = plt.subplots(figsize=(12, 5.5))
    for j, nombre in enumerate(m.NOMBRES):
        color = ESTILO[nombre][0]
        for i, fn in enumerate(funciones):
            res = next(r for r, _ in todos[fn] if r.metodo == nombre)
            xpos = i + (j - n_met / 2 + 0.5) * ancho
            if not res.aplica:
                ax.text(xpos, 0.8, "N/A", rotation=90, ha="center", va="bottom", fontsize=7, color="gray")
            elif res.convergio:
                ax.bar(xpos, res.iteraciones, ancho, color=color, label=nombre if i == 0 else None)
                ax.text(xpos, res.iteraciones + 0.5, str(res.iteraciones), ha="center", fontsize=7)
            else:
                ax.bar(xpos, max(res.iteraciones, 1), ancho, color="white", edgecolor="red", hatch="///")
                ax.text(xpos, max(res.iteraciones, 1) + 0.5, "✗", ha="center", fontsize=9, color="red")
    ax.set_xticks(range(len(funciones)))
    ax.set_xticklabels([f.categoria.replace(" (", "\n(") for f in funciones], fontsize=9)
    ax.set_ylabel("Iteraciones hasta tol = 1e-6")
    ax.set_title("Resumen de iteraciones por método y función  (N/A = no aplica, ✗ = no converge/falla)")
    ax.grid(axis="y", alpha=0.3)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, ncol=3, fontsize=8, loc="upper left")
    fig.tight_layout()
    fig.savefig(ruta, dpi=DPI)
    plt.close(fig)



#sensibilidad (intervalo inicial / estimacion inicial)
def graficar_sensibilidad(filas: list, metodos: list, titulo: str, ruta: str) -> None:
    """
    filas: lista de dicts con claves funcion, nombre_funcion, escenario, metodo,
           convergio, aplica, iteraciones.
    """
    claves = []
    for fila in filas:
        if fila["funcion"] not in claves:
            claves.append(fila["funcion"])
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, clave in zip(axes.ravel(), claves):
        sub = [f for f in filas if f["funcion"] == clave]
        escenarios = []
        for f in sub:
            if f["escenario"] not in escenarios:
                escenarios.append(f["escenario"])
        ancho = 0.8 / len(metodos)
        for j, met in enumerate(metodos):
            color = ESTILO[met][0]
            for i, esc in enumerate(escenarios):
                fila = next(f for f in sub if f["escenario"] == esc and f["metodo"] == met)
                xpos = i + (j - len(metodos) / 2 + 0.5) * ancho
                if fila["convergio"] and not fila.get("convergencia_espuria", False):
                    ax.bar(xpos, fila["iteraciones"], ancho, color=color,
                           label=met if i == 0 else None)
                    ax.text(xpos, fila["iteraciones"], str(fila["iteraciones"]),
                            ha="center", va="bottom", fontsize=7)
                else:
                    ax.plot(xpos, 0.3, "rx", ms=8, mew=2,
                            label="falla / no aplica" if (i == 0 and j == 0) else None)
        ax.set_xticks(range(len(escenarios)))
        ax.set_xticklabels(escenarios, fontsize=7, rotation=20)
        ax.set_title(sub[0]["nombre_funcion"], fontsize=10)
        ax.set_ylabel("Iteraciones")
        ax.grid(axis="y", alpha=0.3)
    handles, labels = {}, {}
    for ax in axes.ravel():
        for h, l in zip(*ax.get_legend_handles_labels()):
            handles.setdefault(l, h)
    fig.legend(list(handles.values()), list(handles.keys()), loc="lower center",
               ncol=len(handles), fontsize=9)
    fig.suptitle(titulo, fontsize=13)
    fig.tight_layout(rect=(0, 0.05, 1, 0.96))
    fig.savefig(ruta, dpi=DPI)
    plt.close(fig)
