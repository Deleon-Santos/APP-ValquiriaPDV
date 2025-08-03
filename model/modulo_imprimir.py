from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import qrcode

def create_pdf(content, table_data):
    largura_cupom = 80 * mm
    altura_cupom = 300 * mm
    nome_arquivo = "cupom_supermercado.pdf"
    informacao = content
    items = table_data

    qr_data = "https://github.com/Deleon-Santos/APP-ValquiriaPDV/tree/master"
    logo_path = "img/logo.png"

    qr = qrcode.make(qr_data)
    qr_path = "img/qrcode_temp.png"
    qr.save(qr_path)

    # Iniciar o canvas
    c = canvas.Canvas(nome_arquivo, pagesize=(largura_cupom, altura_cupom))
    y = altura_cupom - 10 * mm

    try:
        c.drawInlineImage(logo_path, x=15*mm, y=y-25*mm, width=50*mm, height=20*mm)
        y -= 30 * mm
    except:
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(largura_cupom / 2, y, "CUPOM FISCAL")
        y -= 6 * mm

    #cabeçalho
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

    #título da tabela
    c.setFont("Courier-Bold", 6)
    c.drawString(5, y, " ID")
    c.drawString(25, y, "Descrição/AEN")
    c.drawString(largura_cupom - 100, y, "Unid.R$/QTD")
    c.drawRightString(largura_cupom - 5, y, "SubTotalR$")
    y -= 3 * mm
    c.line(5, y, largura_cupom - 5, y)
    y -= 3 * mm

    #listagem de Itens
    c.setFont("Courier", 6)
    total = 0
    print(f"Total de itens: {items}")
    for item in items:
        id_item = f"{str(item[1]).zfill(3)}"
        ean= str(item[3])
        nome = item[4]
        preco_unitario = float(item[6])
        qtd = item[5]   
        valor_item = item[7]  
        total = informacao[2]

        c.drawString(5, y, id_item)
        c.drawString(25, y, nome[:30])    
        c.drawRightString(largura_cupom - 60, y, f"{preco_unitario:.2f}") 
        c.drawRightString(largura_cupom - 5, y, f"{valor_item:.2f}")
        y -= 4 * mm
        c.drawString(25, y, ean[:20])
        c.drawRightString(largura_cupom - 60, y, f"x{qtd}")
        y -= 4 * mm
        
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


