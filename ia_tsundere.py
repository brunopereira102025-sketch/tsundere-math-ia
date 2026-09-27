from flask import Flask, request, render_template_string, session
import sympy as sp
import re

app = Flask(__name__)
app.secret_key = "tsundere_matematica_2026"

x = sp.Symbol("x")

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tsundere Math IA</title>
<style>
body { background: #241722; color: white; font-family: Arial; margin: 0; }
header { background: #9c285e; text-align: center; padding: 18px; font-size: 22px; font-weight: bold; }
main { max-width: 800px; margin: auto; padding: 15px; min-height: 70vh; }
.msg { padding: 13px; margin: 12px 0; border-radius: 10px; white-space: pre-wrap; }
.ia { background: #4b2b40; border: 1px solid #cf6397; }
.user { background: #35333c; border: 1px solid #777; }
form { display: flex; gap: 8px; padding: 15px; max-width: 800px; margin: auto; }
input { flex: 1; padding: 14px; border-radius: 8px; border: 1px solid #b35d89; background: #352535; color: white; font-size: 16px; }
button { padding: 14px; border: 0; border-radius: 8px; background: #d1377c; color: white; font-weight: bold; }
a { color: #ffbedb; display: block; text-align: center; padding: 10px; }
</style>
</head>
<body>
<header>🧮 Tsundere Math IA<br><small>Resolve equações... mas não pense que é por você.</small></header>
<main>
{% for m in mensagens %}
<div class="msg {{ m.tipo }}">
<b>{% if m.tipo == "ia" %}🤖 Tsundere Math IA{% else %}👤 Você{% endif %}</b><br>
{{ m.texto }}
</div>
{% endfor %}
</main>
<form method="POST">
<input name="pergunta" placeholder="Exemplo: x**2 - 5*x + 6 = 0" required autocomplete="off">
<button type="submit">Enviar</button>
</form>
<a href="/limpar">🗑️ Limpar conversa</a>
</body>
</html>
"""

def fala_tsundere(texto):
    texto = texto.lower().strip()
    if texto in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]:
        return "O-oi. Digite uma conta ou equação. Não vou ficar esperando o dia todo, tá?"
    if "obrigad" in texto:
        return "Hmph... não precisa agradecer. Eu só resolvi porque matemática merece ser resolvida direito."
    if "quem é você" in texto or "seu nome" in texto:
        return "Eu sou a Tsundere Math IA. Resolvo contas e equações. Agora mande uma conta logo."
    if "ajuda" in texto:
        return "Use * para multiplicar e ** para potência. Exemplo: x**2 - 5*x + 6 = 0."
    return None

def resolver(pergunta):
    try:
        texto = pergunta.strip()
        texto = texto.replace("^", "**")
        texto = texto.replace("²", "**2")
        texto = texto.replace("³", "**3")
        texto = texto.replace("×", "*")
        texto = texto.replace("÷", "/")
        texto = texto.replace("−", "-")

        permitidos = {"x": x, "X": x}

        if "=" not in texto:
            resultado = sp.simplify(sp.sympify(texto, locals=permitidos))
            return "Resultado: " + texto + " = " + str(resultado) + ". Pronto. Era só isso?"

        if texto.count("=") != 1:
            return "Use somente um sinal de igual. Exemplo: x**2 - 5*x + 6 = 0."

        esquerda, direita = texto.split("=")
        expressao = sp.sympify(esquerda, locals=permitidos) - sp.sympify(direita, locals=permitidos)
        expressao = sp.simplify(expressao)
        solucoes = sp.solve(expressao, x)

        if not solucoes:
            return "Não encontrei soluções para x. Confira sua equação."

        lista = ", ".join(["x" + str(i + 1) + " = " + str(valor) for i, valor in enumerate(solucoes)])
        return "Equação simplificada: " + str(expressao) + " = 0. Soluções: " + lista + ". Pronto. Não é porque eu gosto de ajudar, entendeu?"

    except Exception as erro:
        return "Erro encontrado: " + str(erro)

@app.route("/", methods=["GET", "POST"])
def inicio():
    if "mensagens" not in session:
        session["mensagens"] = [{"tipo": "ia", "texto": "Hmph. Digite uma expressão como 2*2 ou uma equação como x**2 - 5*x + 6 = 0."}]

    if request.method == "POST":
        pergunta = request.form.get("pergunta", "").strip()
        if pergunta:
            mensagens = session["mensagens"]
            mensagens.append({"tipo": "user", "texto": pergunta})
            resposta = fala_tsundere(pergunta)
            if resposta is None:
                resposta = resolver(pergunta)
            mensagens.append({"tipo": "ia", "texto": resposta})
            session["mensagens"] = mensagens

    return render_template_string(HTML, mensagens=session["mensagens"])

@app.route("/limpar")
def limpar():
    session.pop("mensagens", None)
    return '<script>window.location.href="/";</script>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
git init
git add ia_tsundere.py requirements.txtgit commit -m "Primeira versão da IA Matemática Tsundere"
