from flask import Flask, render_template, request
import sympy as sp

app = Flask(__name__)

def evaluate_function(expr_str, x_value):
    x = sp.Symbol('x')
    expr = sp.sympify(expr_str)
    return float(expr.subs(x, x_value))

def backward_difference(fx_values, h, order):
    if order == 1:
        return (fx_values[-1] - fx_values[-2]) / h
    elif order == 2:
        return (fx_values[-1] - 2*fx_values[-2] + fx_values[-3]) / h**2
    return None

def central_difference(fx_values, h, order):
    if order == 1:
        return (fx_values[2] - fx_values[0]) / (2*h)
    elif order == 2:
        return (fx_values[0] - 2*fx_values[1] + fx_values[2]) / h**2
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        method = request.form['method']
        function = request.form['function']
        x_point = float(request.form['x_point'])
        h = float(request.form['h'])
        derivative_order = int(request.form['derivative_order'])

        x = sp.Symbol('x')

        if method == 'backward':
            n_raw = request.form.get('n')
            if not n_raw:
                return render_template('index.html', result="<div style='color:red;'>Jumlah titik (n) harus diisi untuk metode selisih mundur.</div>")
            n = int(n_raw)
            fx_values = [evaluate_function(function, x_point - i*h) for i in reversed(range(n))]
            approx = backward_difference(fx_values, h, derivative_order)
            actual = sp.diff(sp.sympify(function), x, derivative_order).subs(x, x_point).evalf()
            error = abs(actual - approx)

            rumus = 'f\'(x) ≈ (f(x) - f(x - h)) / h' if derivative_order == 1 else 'f\'' + str(derivative_order) + '(x) ≈ (f(x) - 2f(x-h) + f(x-2h)) / h²'

            result = f"""
<h1>Jawaban</h1>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h2>Rumus</h2>
  Untuk turunan ke-{derivative_order} menggunakan metode selisih mundur, rumus yang digunakan adalah:<br><b>{rumus}</b>
</div>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h2>Substitusikan</h2>
  Diketahui h = {h}, dan nilai f(x) pada titik-titik mundur:<br>
  {', '.join(f"f({round(x_point - i*h, 5)}) = {round(val, 5)}" for i, val in zip(reversed(range(n)), fx_values))}<br><br>
  Maka nilai hampiran turunan ke-{derivative_order} adalah:<br>
  ≈ {round(approx, 5)}
</div>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h3>Galat</h3>
  Nilai turunan eksak f({x_point}) = {round(actual, 5)}<br>
  Maka galat absolut = |{round(actual, 5)} - {round(approx, 5)}| = {round(error, 5)}
</div>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h2>Kesimpulan</h2>
  Nilai hampiran turunan ke-{derivative_order} di titik x = {x_point} menggunakan metode selisih mundur adalah:<br>
  <b>{round(approx, 5)}</b><br>
  Dengan galat absolut sebesar <b>{round(error, 5)}</b>
</div>
            """

        elif method == 'central':
            fx_values = [evaluate_function(function, x_point - h), evaluate_function(function, x_point), evaluate_function(function, x_point + h)]
            approx = central_difference(fx_values, h, derivative_order)
            actual = sp.diff(sp.sympify(function), x, derivative_order).subs(x, x_point).evalf()
            error = abs(actual - approx)

            rumus = 'f\'(x) ≈ (f(x+h) - f(x−h)) / 2h' if derivative_order == 1 else 'f\'' + str(derivative_order) + '(x) ≈ (f(x-h) - 2f(x) + f(x+h)) / h²'

            titik = [x_point - h, x_point, x_point + h]

            result = f"""
<h1>Jawaban</h1>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h2>Rumus</h2>
  Untuk turunan ke-{derivative_order} menggunakan metode selisih pusat, rumus yang digunakan adalah:<br><b>{rumus}</b>
</div>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h2>Substitusikan</h2>
  Diketahui h = {h}, dan nilai f(x) pada titik-titik di sekitar x = {x_point}:<br>
  {', '.join(f"f({round(titik[i], 5)}) = {round(fx_values[i], 5)}" for i in range(3))}<br><br>
  Maka nilai hampiran turunan ke-{derivative_order} adalah:<br>
  ≈ {round(approx, 5)}
</div>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h3>Galat</h3>
  Nilai turunan eksak f({x_point}) = {round(actual, 5)}<br>
  Maka galat absolut = |{round(actual, 5)} - {round(approx, 5)}| = {round(error, 5)}
</div>
<br><br>
<div style='border: 1px solid #ccc; padding: 10px;'>
  <h2>Kesimpulan</h2>
  Nilai hampiran turunan ke-{derivative_order} di titik x = {x_point} menggunakan metode selisih pusat adalah:<br>
  <b>{round(approx, 5)}</b><br>
  Dengan galat absolut sebesar <b>{round(error, 5)}</b>
</div>
            """

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
