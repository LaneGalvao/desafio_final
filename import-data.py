import os
import pandas as pd
import pyodbc
from dateutil import parser
from datetime import date

# Definindo o diretório proncipal aonde contem todos os arquivos csv
pastaPrincipal = './csv-data'

# Varrendo o diretório principal para começar a leitura de todos os aquivos existentes
for diretorio, subpastas, arquivos in os.walk(pastaPrincipal):
    for arquivo in arquivos:        
        # lendo o arquivo csv e atribuindo o conteudo na variavel data
        # no primeito parâmetro do método "read_csv()"" informamos o arquivo 
        # que aqui será definido em "os.path.join(diretorio, arquivo)"
        # e no segundo qual o separador utilizado
        data = pd.read_csv (os.path.join(diretorio, arquivo), sep=";")   

        # Atribuindo o conteudo a um dataFrame
        df = pd.DataFrame(data)
        
        # Abrindo conexão com o banco de dados
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=localhost\MSSQLSERVER01;'
                            'Database=desafio_final;'
                            'Trusted_Connection=yes;')

        cursor = conn.cursor()        

        # A cada iteração do laço for o conteudo de uma linha é atribuido a variável row. 
        # desta forma conseguimos acessar o valor de cada coluna atraves do nome ou posição
        # da coluna. Ex: row.id ou row[0]
        for row in df.itertuples():               
            # Recuperando o nome do aquivo que esta sendo trabalho e quebrando pelo "-".
            # desta forma conseguimos identificar se o arquivo é de cliente ou transação
            tipoArquivo = arquivo.split('-')[0]
            
            if tipoArquivo == 'clients':
                print("Inserindo Cliente " + str(row[1]))
                cursor.execute(
                            '''
                                INSERT INTO tb_clients (id, nome, email, data_cadastro, telefone)
                                VALUES (?,?,?,?,?)
                            ''',
                            row[1],# Coluna ID, 
                            row[2],# Coluna nome,
                            row[3],# Coluna Email
                            parser.parse(row[4]), # Coluna data de cadastro
                            row[5] # Coluna Telefone 
                            )
            elif tipoArquivo == 'transaction':                
                print("Verificando se o cliente existe " + str(row[2]))
                #Verificando se o ID do cliente existe na tabela de clientes
                cursor.execute(
                    '''
                        SELECT * FROM tb_clients where id = (?)
                    ''',
                    row[2])
        
                records = cursor.fetchall()

                # Verifico se a variável records esta vazia, pois caso esteja
                # é porque o cliente não existe então precisamo inseri-lo antes 
                # de inserir a transação
                if len(records) == 0:
                    print("Inserindo Cliente FAKE " + str(row[2]))
                    # Executando o comando para inserir um cliente fake
                    cursor.execute(
                                '''
                                    INSERT INTO tb_clients (id, nome, email, data_cadastro, telefone)
                                    VALUES (?,?,?,?,?)
                                ''',
                                row[2],# Coluna ID, 
                                'Cliente Fake-' + str(row[2]),# Coluna nome,
                                'cliente_fake-' + str(row[2]) + '@gmail.com',# Coluna Email
                                date.today(), # Coluna data de cadastro, no caso data atual
                                '+55(55)5555-5555' # Coluna Telefone 
                                )
               
                print("Inserindo Transação " + str(row[1]))     
                # Executando o comando para inserir a transação
                cursor.execute(
                            '''
                                INSERT INTO tb_transaction (id, client_id, valor, data)
                                VALUES (?,?,?,?)
                            ''',
                            row[1],# Coluna ID, 
                            row[2],# Coluna Client Id,
                            row[3],# Coluna Valor
                            parser.parse(row[4]) # Coluna data                            
                            )
            conn.commit()