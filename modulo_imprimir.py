from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

'''pesquisa_cupom = [
    ['Fabiana', 18, "cea@modaas.com.br"],
    ['Fabiana', 18, "cea@modaas.com.br"],
    ['Fabiana', 18, "cea@modaas.com.br"],
    ['Fabiana', 18, "cea@modaas.com.br"]
]

informacao = """Razão Social: Empresa Exemplo Ltda
Número de Cupom: 123456
CNPJ: 12.345.678/0001-90
CPF: 123.456.789-10
Inscrição Municipal: 987654321
Valor: 1500.75zsddfsdfsdfsdfdsf"""'''

def create_pdf(content, table_data, filename):
    pdf_filename = filename
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Cabeçalho centralizado
    c.setFont("Helvetica-Bold", 12)
    title_text = "CUPOM FISCAL"
    c.drawCentredString(letter[0] / 2, letter[1] - 30, title_text)

    # Conteúdo centralizado
    c.setFont("Helvetica", 10)
    text_object = c.beginText(50, letter[1] - 50)
    for line in content.split('\n'):
        text_object.textLine(line)
    c.drawText(text_object)

    # Calculando a altura total do conteúdo e posicionando a tabela
    content_height = len(content.split('\n')) * 14  # Altura aproximada do conteúdo (ajuste conforme necessário)
    table_y = letter[1] - 100 - content_height

    # Tabela com ajuste de largura e quebra de página
    available_width, available_height = letter[0] - 2 * 50, table_y - 50  # Margem de 50mm
    table = Table(table_data)
    table.wrapOn(c, available_width, available_height)
    table.setStyle(get_table_style())
    table.drawOn(c, 50, table_y - len(table_data) * 14)
    print("ok, impresso")
    c.save()
    return True

def get_table_style():
    return TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centralizar todas as células
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),  # Try using Helvetica if available
        ('BOTTOMMARGIN', (0, 0), (-1, -1), 5),
    ])

#create_pdf(informacao, pesquisa_cupom, "impressora.pdf")
