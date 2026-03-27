import sqlite3
import csv

def conectar():
    return sqlite3.connect("funcionarios.db")

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        matricula INTEGER PRIMARY KEY,
        nome TEXT,
        idade INTEGER,
        salario REAL,
        ativo INTEGER
    )
    """)

    conexao.commit()
    conexao.close()

def inserir(funcionario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO funcionarios VALUES (?, ?, ?, ?, ?)
    """, (funcionario.matricula, funcionario.nome,
          funcionario.idade, funcionario.salario, funcionario.ativo))

    conexao.commit()
    conexao.close()

def buscar(matricula):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionarios WHERE matricula = ?", (matricula,))
    resultado = cursor.fetchone()

    conexao.close()
    return resultado

def remover(matricula):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM funcionarios WHERE matricula = ?", (matricula,))

    conexao.commit()
    conexao.close()

def contar():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM funcionarios WHERE ativo = 1")
    total = cursor.fetchone()[0]

    conexao.close()
    return total

def exportar_csv(caminho):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT matricula, nome, idade, salario FROM funcionarios")
    dados = cursor.fetchall()

    conexao.close()

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)

        writer.writerow(["Matricula", "Nome", "Idade", "Salario"])
        writer.writerows(dados)

    writer.writerow(["Matrícula", "Nome", "Idade", "Salário (R$)"])

    for d in dados:
        writer.writerow([
            str(d[0]).ljust(10),
            d[1].ljust(20),
            str(d[2]).ljust(10),
            f"R$ {d[3]:.2f}".ljust(15)
        ])


