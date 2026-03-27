from modelos.funcionarios import Lista_Funcionario
from database.bd import inserir, buscar, remover, contar, exportar_csv

def inserir_funcionario(nome, matricula, idade, salario):
    funcionario = Lista_Funcionario(nome, matricula, idade, salario, 1)
    inserir(funcionario)

def remover_funcionario(matricula):
    remover(matricula)

def buscar_funcionario(matricula):
    return buscar(matricula)

def total_funcionarios():
    return contar()

def exportar_funcionarios_csv(caminho):
    exportar_csv(caminho)