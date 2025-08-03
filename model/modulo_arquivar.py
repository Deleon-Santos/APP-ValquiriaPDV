import sqlite3 as bd

def conectar_bd():
    conn=bd.connect("valquiria_bd")#cria o bd com nome valquiria
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
    id_inserido = cursor.lastrowid

    # Busca o item inserido
    cursor.execute("SELECT id_item, ean_produto, descricao_produto, preco_unitario FROM cadastro WHERE id_item = ?", (id_inserido,))
    cadastro = cursor.fetchone()

    conexao.commit()
    cursor.close()
    conexao.close()
    
    return cadastro


def validar_plu(plu_pro):
    try:
        conexao, cursor = conectar_bd()
        cursor.execute(
            "SELECT id_item, ean_produto, descricao_produto, preco_unitario FROM cadastro WHERE id_item = ? OR ean_produto = ?",
            (plu_pro, plu_pro)
        )
        resultado = cursor.fetchone()
        return resultado if resultado else (0, 0, 0, 0)

    except Exception as e:
        print(f"Erro ao validar PLU: {e}")
        return None, None, None, None

    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass  


def release(busca_sql):
    # Conecta ao BD
        conexao, cursor = conectar_bd()

        # Faz a pesquisa por associação (caracteres digitados)
        cursor.execute("SELECT id_item, descricao_produto, preco_unitario FROM cadastro WHERE descricao_produto LIKE ?", (busca_sql,))
        resultados = cursor.fetchall()

        # Limpa a treeview
        

        
        cursor.close()
        conexao.close()
        return resultados