import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLineEdit, QLabel, QStackedWidget, QFileDialog
)

from Servicos.funcoes import (
    inserir_funcionario,
    buscar_funcionario,
    remover_funcionario,
    total_funcionarios,
    exportar_funcionarios_csv
)
from database.bd import criar_tabela


def criar_container(layout):
    container = QWidget()
    container.setObjectName("container")

    container_layout = QVBoxLayout(container)
    container_layout.addLayout(layout)

    main_layout = QVBoxLayout()
    main_layout.addWidget(container)

    return main_layout


class PaginaCadastro(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        self.nome = QLineEdit()
        self.nome.setPlaceholderText("Nome")

        self.matricula = QLineEdit()
        self.matricula.setPlaceholderText("Matrícula")

        self.idade = QLineEdit()
        self.idade.setPlaceholderText("Idade")

        self.salario = QLineEdit()
        self.salario.setPlaceholderText("Salário")

        self.resposta = QLabel("")
        self.resposta.setObjectName("resposta")

        btn = QPushButton("Cadastrar")
        btn.setObjectName("success")
        btn.clicked.connect(self.cadastrar)

        layout.addWidget(self.nome)
        layout.addWidget(self.matricula)
        layout.addWidget(self.idade)
        layout.addWidget(self.salario)
        layout.addWidget(btn)
        layout.addWidget(self.resposta)

        self.setLayout(criar_container(layout))

    def cadastrar(self):
        try:
            inserir_funcionario(
                self.nome.text(),
                int(self.matricula.text()),
                int(self.idade.text()),
                float(self.salario.text())
            )
            self.resposta.setText("✅ Cadastrado!")
        except:
            self.resposta.setText("❌ Erro")


class PaginaBuscar(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.matricula = QLineEdit()
        self.matricula.setPlaceholderText("Matrícula")

        self.resposta = QLabel("")
        self.resposta.setObjectName("resposta")

        btn = QPushButton("Buscar")
        btn.clicked.connect(self.buscar)

        layout.addWidget(self.matricula)
        layout.addWidget(btn)
        layout.addWidget(self.resposta)

        self.setLayout(criar_container(layout))

    def buscar(self):
        try:
            resultado = buscar_funcionario(int(self.matricula.text()))

            if resultado:
                self.resposta.setText(
                    f"{resultado[1]} | {resultado[2]} anos | R$ {resultado[3]}"
                )
            else:
                self.resposta.setText("❌ Não encontrado")
        except:
            self.resposta.setText("❌ Erro")


class PaginaRemover(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.matricula = QLineEdit()
        self.matricula.setPlaceholderText("Matrícula")

        self.resposta = QLabel("")
        self.resposta.setObjectName("resposta")

        btn = QPushButton("Remover")
        btn.setObjectName("danger")
        btn.clicked.connect(self.remover)

        layout.addWidget(self.matricula)
        layout.addWidget(btn)
        layout.addWidget(self.resposta)

        self.setLayout(criar_container(layout))

    def remover(self):
        try:
            remover_funcionario(int(self.matricula.text()))
            self.resposta.setText("🗑️ Removido!")
        except:
            self.resposta.setText("❌ Erro")


class PaginaTotal(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.resposta = QLabel("")
        self.resposta.setObjectName("resposta")

        btn = QPushButton("Ver Total")
        btn.clicked.connect(self.mostrar)

        layout.addWidget(btn)
        layout.addWidget(self.resposta)

        self.setLayout(criar_container(layout))

    def mostrar(self):
        total = total_funcionarios()
        self.resposta.setText(f"📊 Total: {total}")


class PaginaCSV(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.resposta = QLabel("")
        self.resposta.setObjectName("resposta")

        btn = QPushButton("Baixar CSV")
        btn.setObjectName("success")
        btn.clicked.connect(self.baixar_csv)

        layout.addWidget(btn)
        layout.addWidget(self.resposta)

        self.setLayout(criar_container(layout))

    def baixar_csv(self):
        try:
            caminho, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar CSV",
                "funcionarios.csv",
                "CSV Files (*.csv)"
            )

            if not caminho:
                return

            exportar_funcionarios_csv(caminho)

            self.resposta.setText("📥 CSV salvo com sucesso!")
        except:
            self.resposta.setText("❌ Erro")


class Sistema(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Funcionários")

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        btn_cadastro = QPushButton("Cadastro")
        btn_buscar = QPushButton("Buscar")
        btn_remover = QPushButton("Remover")
        btn_total = QPushButton("Total")
        btn_csv = QPushButton("Baixar CSV")

        layout.addWidget(btn_cadastro)
        layout.addWidget(btn_buscar)
        layout.addWidget(btn_remover)
        layout.addWidget(btn_total)
        layout.addWidget(btn_csv)

        self.stack = QStackedWidget()

        self.stack.addWidget(PaginaCadastro())
        self.stack.addWidget(PaginaBuscar())
        self.stack.addWidget(PaginaRemover())
        self.stack.addWidget(PaginaTotal())
        self.stack.addWidget(PaginaCSV())

        layout.addWidget(self.stack)

        btn_cadastro.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_buscar.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_remover.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_total.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        btn_csv.clicked.connect(lambda: self.stack.setCurrentIndex(4))

        self.setLayout(layout)


if __name__ == "__main__":
    criar_tabela()

    app = QApplication(sys.argv)

    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())

    janela = Sistema()
    janela.showMaximized()

    sys.exit(app.exec_())