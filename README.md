# Repositório Data Azure - Desafio final

# Descrição do projeto

## Sumário

# 1 - Descrição do projeto
# 2 - Tecnologias usadas
# 3 - Criação do banco de dados
# 4 - Exportação de dados e carregando o banco de dados em Python
# 5 - Relatórios de análise no SQL
# 6 - Relatórios no Power BI
# 7 - Hospedagem na nuvem

## 3 - Criação do banco de dados

# Recebemos uma carga de arquivos em csv contendo 4 tabelas de clientes e 63 de transações. Visando a descoberta de fraudes. Para fazer a importação desses dados no python o primeiro passo foi criar um banco de dados no SQL e duas tabelas relacionadas as informações contidas na carga de arquivos, que não aceitasse valores nulos e com chave primaria em seus IDs e a chave estrangeira no cliente_id referenciado da tabela de clientes, validando a integridade dos dados, e mostrando o vínculo forte entre as tabelas, como podemos ver no script:

# CREATE DATABASE DESAFIO_FINAL;
# GO
# USE DESAFIO_FINAL;
# GO
# CREATE TABLE TB_CLIENTS(
# 	ID INT NOT NULL,
# 	NOME VARCHAR(250) NOT NULL,
# 	EMAIL VARCHAR(250) NOT NULL,
# 	DATA_CADASTRO DATETIME NOT NULL,
# 	TELEFONE VARCHAR(16),
# 	PRIMARY KEY (ID)
# );
# GO

# CREATE TABLE TB_TRANSACTION(
# 	ID INT NOT NULL,
# 	CLIENT_ID INT NOT NULL,
# 	VALOR FLOAT NOT NULL,
# 	DATA DATETIME,
# 	PRIMARY KEY (ID),
# 	FOREIGN KEY (CLIENT_ID) REFERENCES TB_CLIENTS(ID)
# );

## 4 - Exportação de dados e carregando o banco de dados em Python

## 5 - Relatórios de análise no SQL

# Após a inserção dos valores nas tabelas podemos gerar alguns relatórios através dos selectes, 1° mostrando a quantidade total de clientes, que foram 401:
# select * from tb_clients

# Depois quantas transações foram feitas: 6722
# --(nem todos os clientes fizeram transações pois aparecem valores e data null)
# select C.id, C.nome, T.data, T.valor
# 	from tb_clients C
# left join tb_transaction T on C.id=T.client_id


# A quantidade de clientes que não fizeram transações que foram 341.
# -- clientes sem transações - 341 linhas
# select C.id, C.nome, T.data, T.valor
# 	from tb_clients C
# left join tb_transaction T on C.id=T.client_id
# where T.data is null
# order by C.id


# E por fim quantos clientes fizeram transações (60 clientes) e quantas transações cada cliente fez
# select T.client_id,
# 	count (*) as "número de transações"
# 	from tb_transaction T
# 	group by T.client_id

## 6 - Relatórios no Power BI

# Para realizar o cálculo e descobrir os clientes fraudados, utilizamos o DAX, a biblioteca de funções e operadores do Power BI.

# Criamos três colunas: segundo, categoria e transação.
# A coluna segundo é baseada na análise do cálculo do espaçamento de tempo entre as transações de cada cliente:

# SEGUNDO =
# VAR TEMP =
# TOPN (1, FILTER ('TB_TRANSACTION', 'TB_TRANSACTION'[CLIENT_ID] = EARLIER ( 'TB_TRANSACTION'[CLIENT_ID] ) && 'TB_TRANSACTION'[DATA] < EARLIER ( 'TB_TRANSACTION'[DATA] )),
# [DATA], DESC) RETURN DATEDIFF ( MINX ( TEMP, [DATA] ), [DATA], SECOND )


# A coluna segundo recebe a variável *temp, que por sua vez possui uma *expressão* onde é feito o cálculo que nos retorna a diferença de tempo entre as transações, agrupando os # dados por cliente e data e comparando se os dois tempos verificados são do mesmo cliente.


# A próxima coluna criada foi categoria, que verifica se a coluna segundo é menor que 120 segundos, se sim, retorna 0, em caso negativo, retorna 1.

# CATEGORIA = IF(TB_TRANSACTION[SEGUNDO] >= 1 && TB_TRANSACTION[SEGUNDO] < 120, 1, 0 

# A última coluna criada foi transação, para melhor visualização do resultado no reslatório, a mesma verifica a coluna categoria e retorna 1 em caso de fraude e 0, caso negativo.

# TRANSAÇÃO = IF(TB_TRANSACTION[CATEGORIA] = 0 , "Normal","Fraude")
