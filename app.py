import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Sólido de revolución - Capas cilíndricas", layout="centered")

st.title("Sólido de revolución por capas cilíndricas")
st.write("Región entre f(x) = 4x - x² (arriba) y g(x) = x (abajo), girada alrededor del eje y.")

def f(x):
    return 4 * x - x**2

def g(x):
    return x

def trapecio(x, y):
    return np.sum((y[1:] + y[:-1]) / 2 * np.diff(x))

x_max = st.slider("Perilla: hasta dónde se llena el sólido (x)", min_value=0.05, max_value=3.0, value=3.0, step=0.05)

n_theta = 60
n_x = 60

x_vals = np.linspace(0.0001, x_max, n_x)
theta = np.linspace(0, 2 * np.pi, n_theta)
X, T = np.meshgrid(x_vals, theta)

Xs = X * np.cos(T)
Zs = X * np.sin(T)
Ytop = f(X)
Ybot = g(X)

fig = go.Figure()
fig.add_trace(go.Surface(x=Xs, y=Ytop, z=Zs, colorscale="Oranges", showscale=False, opacity=0.9))
fig.add_trace(go.Surface(x=Xs, y=Ybot, z=Zs, colorscale="Blues", showscale=False, opacity=0.9))

t_vals = np.linspace(g(x_max), f(x_max), 20)
Theta2, Tt = np.meshgrid(theta, t_vals)
Xr = x_max * np.cos(Theta2)
Zr = x_max * np.sin(Theta2)
Yr = Tt
fig.add_trace(go.Surface(x=Xr, y=Yr, z=Zr, colorscale="Greens", showscale=False, opacity=0.9))

fig.update_layout(
    scene=dict(xaxis_title="x", yaxis_title="y (eje de rotación)", zaxis_title="z", aspectmode="data"),
    margin=dict(l=0, r=0, t=30, b=0),
)

st.plotly_chart(fig, use_container_width=True)

radio = x_max
altura = f(x_max) - g(x_max)

xs_vol = np.linspace(0, x_max, 400)
integrand = xs_vol * (f(xs_vol) - g(xs_vol))
vol = 2 * np.pi * trapecio(xs_vol, integrand)

st.write(f"**Radio actual (x):** {radio:.2f}")
st.write(f"**Altura de la capa en ese punto:** {altura:.2f}")
st.metric("Volumen acumulado", f"{vol:.2f} unidades³")
