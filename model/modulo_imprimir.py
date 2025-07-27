from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PIL import Image
import qrcode

def create_pdf(content, table_data):
    largura_cupom = 80 * mm
    altura_cupom = 300 * mm
    nome_arquivo = "cupom_supermercado.pdf"

    informacao = content
    items = table_data

    qr_data = "https://github.com/Deleon-Santos/APP-ValquiriaPDV/tree/master"
    logo_path = "img/logo.png"

    # Gerar QR code
    qr = qrcode.make(qr_data)
    qr_path = "img/qrcode_temp.png"
    qr.save(qr_path)

    # Iniciar o canvas
    c = canvas.Canvas(nome_arquivo, pagesize=(largura_cupom, altura_cupom))
    y = altura_cupom - 10 * mm

    # LOGO ou Nome do Estabelecimento
    try:
        c.drawInlineImage(logo_path, x=15*mm, y=y-25*mm, width=50*mm, height=20*mm)
        y -= 30 * mm
    except:
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(largura_cupom / 2, y, "CUPOM FISCAL")
        y -= 6 * mm

    # Cabeçalho
    c.setFont("Courier", 6)
    c.drawCentredString(largura_cupom/2, y, f"{informacao[5]}")
    y -= 4 * mm
    c.drawCentredString(largura_cupom / 2, y, f"Cnpj:{informacao[4]} Data: {informacao[1]}")
    y -= 4 * mm
    c.drawCentredString(largura_cupom /2, y,f"AV. Boa Vista n:1012-Santa Rosa/SP  EI:07.112.888/000-00")
    y -= 4 * mm
    c.drawCentredString(largura_cupom /2, y, f'Client: {informacao[3]} Operador: {informacao[6]}') 
    y -= 4 * mm
    
    c.setFont("Courier-Bold", 8)
    c.drawCentredString(largura_cupom /2, y, f'Cupom: 0000{informacao[0]}')
    y -= 4 * mm
    c.line(5, y, largura_cupom - 5, y)
    y -= 4 * mm

    # Título da tabela
    c.setFont("Courier-Bold", 6)
    c.drawString(5, y, "ID")
    c.drawString(15, y, "Descrição/AEN")
    c.drawString(largura_cupom - 100, y, "Unid.R$/QTD")
    c.drawRightString(largura_cupom - 5, y, "SubTotalR$")
    y -= 3 * mm
    c.line(5, y, largura_cupom - 5, y)
    y -= 3 * mm

    # Listagem de Itens
    c.setFont("Courier", 6)
    total = 0
    print(f"Total de itens: {items}")
    for item in items:
        id_item = str(item[1])
        ean= str(item[3])
        nome = item[4]
        preco_unitario = float(item[6])
        qtd = int(item[5])
        
        valor_item = qtd * preco_unitario
        total += valor_item

        c.drawString(5, y, id_item)
        c.drawString(15, y, nome[:30])  # Descrição encurtada se necessário   
        c.drawRightString(largura_cupom - 60, y, f"{preco_unitario:.2f}") 
        c.drawRightString(largura_cupom - 5, y, f"{valor_item:.2f}")
        y -= 4 * mm
        c.drawString(15, y, ean[:20])
        c.drawRightString(largura_cupom - 60, y, f"x{qtd:.0f}")
        y -= 4 * mm
        # Evita estourar a altura do cupom
        if y < 45 * mm:
            c.showPage()
            y = altura_cupom - 10 * mm
            c.setFont("Courier", 6)

    # Total Geral
    y -= 3 * mm
    c.setFont("Courier-Bold", 7)
    c.line(5, y, largura_cupom - 5, y)
    y -= 4 * mm
    c.drawString(10, y, "TOTAL GERAL:")
    c.drawRightString(largura_cupom - 5, y, f"R$ {total:.2f}")
    y -= 4 * mm

    # Mensagem Final
    c.setFont("Courier", 7)
    c.drawCentredString(largura_cupom / 2, y, "Obrigado pela preferência!")
    y -= 4 * mm
    c.drawCentredString(largura_cupom / 2, y, "Volte sempre!")
    y -= 4 * mm

    # QR Code
    c.drawInlineImage(qr_path, x=(largura_cupom / 2 - 25), y=y - 50, width=50, height=50)

    c.save()
    return nome_arquivo

# Dados de teste
# content = ["Supermercado Exemplo","45.789.456/0001-45","19/07/2025 20:00","445.455.478-78","10008","janette","jhdjhfjdjfj"]
# table_data = [
#     [1,"7894561251412", "Arroz 5kg", 2, 22.90, 45.12],
#     [2, "7894561251412","Feijão 1kg", 1, 7.50, 7.45],
#     [3, "7894561251412","Óleo 900ml", 3, 8.30, 20.00],
#     [4, "7894561251412","Café 500g", 2, 10.00, 30.00],
#     [5,"7894561251412", "Açúcar 1kg", 4, 5.25, 21.00],
#     [6,"7894561251412", "Sabonete", 6, 2.50, 15.00],
#     [7,"7894561251412", "Leite 1L", 3, 4.80, 14.40],
#     [8,"7894561251412", "Macarrão", 2, 3.90, 7.80],
#     [9, "7894561251412","Molho Tomate", 2, 2.20, 4.40],
#     [10, "7894561251412","Farinha Trigo", 1, 7.00, 7.00],
# ]

# create_pdf(content, table_data)



