import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QInputDialog, QMessageBox, QMenuBar, QMenu, QAction
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Modulos fictícios usados
'''import modulo_pagar as pagar
import modulo_remover as remover
import modulo_pesquisar as pesquisar
import modulo_cadastro as cadastrar
import modulo_limpar as limpar
import modulo_adicionar as adicionar
import modulo_visualisar as visualizar
import modulo_arquivar as arquivar
import modulo_cpf'''

class SistemaCaixa(QWidget):
    def __init__(self, usuario, data, empresa):
        super().__init__()
        self.usuario = usuario
        self.data = data
        self.empresa = empresa

        self.carrinho = []
        self.valor_pagar = 0
        self.num_item = 0
        self.cupom = 1000
        self.cpf = "000.000.000-00"
        self.cnpj = '45.333.0001/45'
        
        # Criar UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sistema de Caixa")
        self.setGeometry(100, 100, 800, 600)

        # Menu
        menu_bar = QMenuBar(self)
        novo_menu = menu_bar.addMenu("Novo")
        novo_compra = QAction("Nova Compra", self)
        novo_compra.triggered.connect(self.nova_compra)
        novo_menu.addAction(novo_compra)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setMenuBar(menu_bar)

        # Caixa fechado label
        self.label_caixa = QLabel("CAIXA FECHADO", self)
        self.label_caixa.setFont(QFont("Arial", 18, QFont.Bold))
        main_layout.addWidget(self.label_caixa)

        # Tabela de produtos
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Item", "Cod", "EAN", "Descrição do Produto", "QTD", "PUni R$", "Preço R$"])
        main_layout.addWidget(self.table)

        # Preço unitário e subtotal
        self.label_preco_unitario = QLabel("Preço Unitário R$", self)
        self.input_preco_unitario = QLineEdit(self)
        self.label_subtotal_item = QLabel("SubTotal Item R$", self)
        self.input_subtotal_item = QLineEdit(self)

        form_layout = QHBoxLayout()
        form_layout.addWidget(self.label_preco_unitario)
        form_layout.addWidget(self.input_preco_unitario)
        form_layout.addWidget(self.label_subtotal_item)
        form_layout.addWidget(self.input_subtotal_item)
        main_layout.addLayout(form_layout)

        # Botões
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("ADICIONAR", self)
        self.add_button.clicked.connect(self.adicionar_produto)
        self.pay_button = QPushButton("PAGAR", self)
        self.pay_button.clicked.connect(self.pagar_compra)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.pay_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Carregar dados iniciais
        try:
            with open('dados/bd.txt', 'r') as file:
                self.dic = json.load(file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Erro", "Arquivo 'bd.txt' não encontrado.")
            self.dic = {}

    def adicionar_produto(self):
        ean, ok = QInputDialog.getText(self, "Adicionar Produto", "Código EAN:")
        if ok and ean:
            descricao, qtd = pesquisar.pesquisar(self.dic, ean)
            if descricao:
                item_num = self.num_item + 1
                preco_unitario = adicionar.achar_preco(self.dic, ean)
                preco = preco_unitario * qtd
                self.carrinho.append([item_num, ean, descricao, qtd, preco_unitario, preco])
                self.num_item += 1
                self.valor_pagar += preco
                self.atualizar_tabela()
                self.input_preco_unitario.setText(f"{preco_unitario:.2f}")
                self.input_subtotal_item.setText(f"{self.valor_pagar:.2f}")
            else:
                QMessageBox.warning(self, "Erro", "Produto não encontrado.")

    def atualizar_tabela(self):
        self.table.setRowCount(len(self.carrinho))
        for row, item in enumerate(self.carrinho):
            for col, data in enumerate(item):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))

    def nova_compra(self):
        self.cupom += 1
        self.carrinho = []
        self.num_item = 0
        self.valor_pagar = 0
        self.atualizar_tabela()
        self.label_caixa.setText(f"CAIXA ABERTO - Cupom {self.cupom}")

    def pagar_compra(self):
        if self.valor_pagar > 0:
            pagar.pagar(self.valor_pagar)
            arquivar.arquivar(self.cupom, self.data, self.usuario, self.cnpj, self.cpf, self.valor_pagar, self.empresa, self.carrinho)
            QMessageBox.information(self, "Pagamento", f"Compra finalizada. Total pago: R$ {self.valor_pagar:.2f}")
            self.nova_compra()
        else:
            QMessageBox.warning(self, "Erro", "Nenhum valor a pagar.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sistema = SistemaCaixa("Administrador", "2024-03-21 17:41:22", "Tem De Tudo ME")
    sistema.show()
    sys.exit(app.exec_())
