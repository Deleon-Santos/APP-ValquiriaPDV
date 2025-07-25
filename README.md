# VALQUIRIA APP VENDAS
![App Vendas](img/banner.png)

## Sistema de Cobrança em Caixa de Supermercados

- O VALQUIRA esta conectado a um banco de dados integrado SQLite que permite o aque todas as vendas seja armazenadas e gerenciadas.

## Tecnologias Usadas

- ![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white) **Python 3.7+**
- ![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-brightgreen?style=for-the-badge&logo=customtkinter&logoColor=white) **CustomTkinter**: Para criação de interface gráfica.
- ![JSON](https://img.shields.io/badge/JSON-Data-blue?style=for-the-badge&logo=json&logoColor=white) **JSON**: Manipulação de dados persistentes.
- ![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge&logo=pdf&logoColor=white) **ReportLab**: Geração de PDFs.
- ![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?style=for-the-badge&logo=sqlite&logoColor=white) **SQLite**: Banco de dados leve e embutido.

## Funcionalidades

### Gestão de permisões
![App Vendas](img/tela-de-login.png)
- **Abertura e Fechamento do Caixa**: Possui tela de loguin que permite logar com permissões diferentes para cada usuário.

### Registro de Vendas
![App Vendas](img/tela-de-vendas.png)
- **Nova Compra**:Controle do estado do caixa, validação de CPF, abertura de novos cupons e fechamento ao final das operações.  
- **Adicionar Itens ao Carrinho**: Permite adicionar produtos ao carrinho de compras com base no código e EAN ou retorno via pesquisa. Ecessa o banco de dados, valida a entrada via ean, e mostra os valore e quantidades nos campos determinados.
- **Remover Itens do Carrinho**: Permite remover produtos já adicionados ao carrinho por meio do botão DELETE. Permite marcar um item na tabela itens e remover o valor correspondente na soma total de itens.
- **Atualização de Preços e Totais**: Calcula automaticamente os preços unitários e totais dos itens no carrinho e retorna no campo específico.
- **Voltar**: Cancela a operação e retorna ao estado inicial limpando os valores nos campos outputs.

### Consulta de Produtos

![App Vendas](img/tela-de-pesquisa.png)
- **Pesquisa de Produtos**: Permite visualizar ou retornar produtos no banco de dados pelo código, descrição ou ean. retorna a linha selecionada na tabela

### Cadastro de Produtos
![App Vendas](img/tela-de-cadastros.png)
- **Adicionar Novos Produtos**: Permite o cadastro de ean, descrição e preço de novos produtos no sistema. Essa funcionalidade possui tratamento de erros e formatação de valores nos campos de entradas

### Pagamentos
![App Vendas](img/tela-de-pagamentos.png)
- **Processamento de Pagamentos**: Calcula o valor total a pagar e registra a venda em dinheiro, cartão ou pix. O pagamento permite uma condição de informar o valor recebido se a opção 'dinheiro' for marcada, possibilitando o calculo de troco.
- **Banco de dados SQLite**: Coleta dados da empresa, cliente, Usuario logado, data, produtos selecionados e efetua o registro nas tabelas relacionadas a venda e a produtos. É validada e existencia ou a criação de tabelas e é efutuado o registro da compra.

### Relatórios
![App Vendas](img/impressãoDoc.png)
- **Visualização de Vendas Realizadas**: Exibe o registro de todas as vendas salvas no bd SQLite a partir do numero do cupom. O botão combobox exibe todos os registros de vendas do banco de dados.

### Geração de PDFs
![App Vendas](img/impressão.png)
- **Impressão de aquivo pdf**: Exibe a venda em um modelo de "Cupom Fiscal" em formato pdf pronto para impressão.

### Clonar e trabalhar nesse projeto

```
git clone https://github.com/Deleon-Santos/APP-ValquiriaPDV.git
```
### Licença de uso 
- **Esta sob a licença MIT**
```
Copyright (c) 2025 Deleon Santos

Por meio deste, é concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o 'Software'), para lidar com o Software sem restrições, incluindo, sem limitação, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software...
```
### Melhorias em andamento
- **Refatorar para o formato WEB**: Esta aplicação deve receber uma nova versão para rodar no browser com hospedagem de front-end, beck-end, e banco de dados. esta atualização devera ser com Flask ou Django mantendo o Python como linguagem predominante.

## Desenvolvedor
- **Deleon Santos**: Este é um projeto autoral para fins academico e evolui conforme aprendo novas tecnologias ou maneiras de resolver problemas.

## Versão
- **v6.1.7**

