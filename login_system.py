# Projeto com Banco de Dados 
# Sistema de login

import sqlite3
import random
import string

# Cria o banco de dados e a tabela (se não existir)
def criar_banco():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            usuario TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Gera nome de usuário baseado no nome + número aleatório
def gerar_usuario(nome):
    base = nome.lower().split()[0]
    numero = random.randint(100, 999)
    return f"{base}{numero}"

# Gera senha aleatória
def gerar_senha(tamanho=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

# Cadastra o usuário no banco
def cadastrar_usuario():
    nome = input("Digite seu nome completo: ")
    email = input("Digite seu e-mail: ")
    usuario = gerar_usuario(nome)
    senha = gerar_senha()

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO usuarios (nome, email, usuario, senha) VALUES (?, ?, ?, ?)',
                       (nome, email, usuario, senha))
        conn.commit()
        print("\n✅ Cadastro realizado com sucesso!")
        print(f"Seu nome de usuário: {usuario}")
        print(f"Sua senha: {senha}\n")
    except sqlite3.IntegrityError:
        print("❌ Esse nome de usuário já existe. Tente novamente.")
    finally:
        conn.close()

# Login do usuário
def login():
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"\n✅ Login bem-sucedido! Bem-vindo(a), {user[1]}.\n")
    else:
        print("\n❌ Usuário ou senha inválidos.\n")

# Menu principal
def menu():
    criar_banco()
    while True:
        print("1 - Cadastrar novo usuário")
        print("2 - Fazer login")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_usuario()
        elif opcao == '2':
            login()
        elif opcao == '3':
            print("Encerrando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.\n")

# Executa o programa
menu()

