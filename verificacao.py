from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def verifica_email(email_input):
    padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao_email, email_input))

def verifica_senha(senha_input):
    padrao_senha = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
    return bool(re.match(padrao_senha, senha_input))

def verifica_cpf(cpf_input):
    cpf_input = ''.join(filter(str.isdigit, cpf_input))
    if len(cpf_input) != 11 or cpf_input == cpf_input[0] * 11:
        return False
    def calcular_digito(base, peso_inicial):
        soma = sum(int(d) * p for d, p in zip(base, range(peso_inicial, 1, -1)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto
    for i in range(9, 11):
        soma = sum(int(cpf_input[j]) * (i + 1 - j) for j in range(i))
        digito = (soma * 10) % 11
        if digito == 10: digito = 0
        if digito != int(cpf_input[i]):
            return False
    return True

@app.route('/validar', methods=['POST'])
def validar_dados():
    cpf = request.form.get('cpf')
    email = request.form.get('email')
    senha = request.form.get('senha')

    resultados = {
        'cpf': verifica_cpf(cpf),
        'email': verifica_email(email),
        'senha': verifica_senha(senha)
    }

    return jsonify(resultados)

@app.route('/')
def home():
    return '''
        <form method="POST" action="/validar">
            CPF: <input type="text" name="cpf"><br>
            Email: <input type="text" name="email"><br>
            Senha: <input type="password" name="senha"><br>
            <input type="submit" value="Validar">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
