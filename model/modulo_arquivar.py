import sqlite3 as bd

def conectar_bd():
    conn=bd.connect("database/valquiria_bd")#cria o bd com nome valquiria
    curs=conn.cursor()
    return conn, curs

def gerar_cupom():
    n = 0
    try:
        conexao, cursor = conectar_bd()
        cursor.execute("SELECT COUNT(*) FROM vendas WHERE EXISTS (SELECT 1 FROM vendas)") #testa se existe algum registro e conta o numero de vendas
        count = cursor.fetchone()[0]
        print(f'count dentro de gerar cupom {count}')
        return count
    
    except Exception as e:
        print(f'erro{e}')
        return n #retorna '0' se não hover um registro no banco
    
def lista_de_vendas():
    conexao, cursor = conectar_bd()
    
    cursor.execute("""
        select n_cupom, data_venda, valor_venda, cpf_cliente, cnpj_empresa, razao_social, operador_vendedor 
        from vendas
    """)
    lista_vendas = cursor.fetchall()
    #retorna uma lista com todas as vendas na tabela vendas
    cursor.close()
    conexao.close()
    return lista_vendas

def lista_item_por_carrinho(cupom):
    conexao, cursor = conectar_bd()
    try:
        cursor.execute("""
            SELECT n_cupom, n_item, plu_produto, ean_produto, descricao_produto, qtd_produto, preco_unitario, total_preco
            FROM carrinho 
            WHERE n_cupom=?
        """, (cupom,))
        #retorna uma lista com todos os produtos com o numero do cupom indicado
        items = cursor.fetchall()
        return items

    finally:
        cursor.close()
        conexao.close()

def arquivo(cupom,data,usuario,cnpj,cpf,v_pago,empresa,carrinho):
    #criação da s tabela vendas e carrinho
    conexao, cursor = conectar_bd()
    cursor.execute("""
                    create table if not exists vendas(
                        n_cupom integer primary key,    
                        data_venda text,
                        valor_venda real,
                        cpf_cliente text,
                        cnpj_empresa text,
                        razao_social text,
                        operador_vendedor text)""")
    
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS carrinho (
            n_cupom INTEGER,
            n_item INTEGER, 
            plu_produto TEXT,  
            ean_produto TEXT,  
            descricao_produto TEXT, 
            qtd_produto INTEGER, 
            preco_unitario REAL, 
            total_preco REAL,
            FOREIGN KEY (n_cupom) REFERENCES vendas (n_cupom) )
    """)
    
    #inserindo um cupom e informações na tabela vendas
    cursor.execute("""
                        insert into vendas(
                        n_cupom, data_venda, valor_venda, cpf_cliente, cnpj_empresa, razao_social, operador_vendedor)
                        values(?,?,?,?,?,?,?)""",(cupom, data, v_pago, cpf, cnpj, empresa, usuario) )
    conexao.commit()
    print('gravadoo em vendas')
    #inserindo itens na tabela carrinho
    for compra in carrinho:         
        cursor.execute("""
                    insert into carrinho(
                    n_cupom, n_item , plu_produto ,  ean_produto ,  descricao_produto , qtd_produto , preco_unitario , total_preco)
                    values(?,?,?,?,?,?,?,?)""",
                    (cupom, compra[0], compra[1], compra[2], compra[3], compra[4], compra[5], compra[6])) 
        conexao.commit()
    
    cursor.close()
    conexao.close()
    
def salvar_novo_item(novo_item):
    conexao, cursor = conectar_bd()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cadastro (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,  
        ean_produto TEXT UNIQUE NOT NULL CHECK (length(ean_produto) <= 13),  
        descricao_produto TEXT NOT NULL CHECK (length(descricao_produto) <= 100),  
        preco_unitario REAL   
    )
    """)
    cursor.execute("""
    INSERT INTO cadastro (ean_produto, descricao_produto, preco_unitario)
    VALUES ( ?, ?, ?)
    """, novo_item)
    conexao.commit()
    cursor.close()
    conexao.close()

novo_item = [
    {"ean": "7896894900013", "item": "Acucar Refinado Caravela pt 1kg", "preco": 2.9},
    {"ean": "7891020106927", "item": "Cafe Melita Extra Forte 1kg", "preco": 16.9},
    {"ean": "7896034610017", "item": "Leite Integral Parmalate 1lt", "preco": 5.9},
    {"ean": "7896062699848", "item": "Arroz Solito Premio Polido 5kg", "preco": 15.9},
    {"ean": "7897136400155", "item": "Feijao Carioca Kicaldo pt 1kg", "preco": 6.9},
    {"ean": "7896205788040", "item": "Macarrao Spaguete Adria 500g", "preco": 3.9},
    {"ean": "7891095003389", "item": "Farinha de mandioca Yoki 500g", "preco": 4.9},
    {"ean": "7896005205860", "item": "Farinha de Trigo Dona Benta 1kg", "preco": 3.9},
    {"ean": "7894321711317", "item": "Achocolatado Toddy Mais 500g", "preco": 5.9},
    {"ean": "7896036090244", "item": "Oleo de Soja Liza Garrafa 900ml", "preco": 5.9},
    {"ean": "7891000376843", "item": "Biscoito Recheado Bono 350g", "preco": 3.9},
    {"ean": "7892320006122", "item": "Moargarina Doriana com sal 500g", "preco": 12.95},
    {"ean": "7894545010102", "item": "Feijao carioca BoaSafra 1kg", "preco": 13.9},
    {"ean": "7891515232126", "item": "Margarina Doriana com sal 500G", "preco": 12.95},
    {"ean": "7894546202021", "item": "Pao de hamburgue Panco 6 uni", "preco": 10.9},
    {"ean": "7894561230123", "item": "Detergente em po Omo Multi 2kg", "preco": 10.45},
    {"ean": "7891000325131", "item": "Bombom Nestle 251g com 12 uni", "preco": 12.95},
    {"ean": "7891035618543", "item": "Multi Inseticida Sbp Emb Eco 380Ml", "preco": 19.2},
    {"ean": "7891024027370", "item": "Enxaguante Bucal Colgate Plax 1Lt", "preco": 21.3},
    {"ean": "7898951147928", "item": "Petiscos Bistequitos Dog Sabor Carne 400G", "preco": 14.5},
    {"ean": "7898280620314", "item": "Coquitel Espumante De Maca D'Gent 660Ml", "preco": 33.9},
    {"ean": "1234567891234", "item": "Garrafa De Gin Rock'A De 600Ml", "preco": 45.9},

    {"ean": "7894578124578", "item": "Agua Sanitaria Supercandida 2Lt C Perfume", "preco": 12.9},
    {"ean": "7894545101012", "item": "Racao Para Dog Snowdog15Kg Carne", "preco": 54.9},
    {"ean": "7894561225645", "item": "Chocolate Em Barra Nestla 480G", "preco": 14.9},
    {"ean": "7895345353455", "item": "Carne Seca Defumeda Paineira", "preco": 25.9}
]

for item in novo_item:
    dados = (item['ean'], item['item'], item['preco'])
    try:
        salvar_novo_item(dados)
    except Exception as e:
        print(f"Erro ao salvar {item['item']}: {e}")

print('Itens salvos com sucesso!')
