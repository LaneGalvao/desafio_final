CREATE DATABASE DESAFIO_FINAL;
GO
USE DESAFIO_FINAL;
GO
CREATE TABLE TB_CLIENTS(
	ID INT NOT NULL
	,NOME VARCHAR(250) NOT NULL
	,EMAIL VARCHAR(250) NOT NULL
	,DATA_CADASTRO DATETIME NOT NULL
	,TELEFONE VARCHAR(16)
	,PRIMARY KEY (ID)
);
GO
CREATE TABLE TB_TRANSACTION(
	ID INT NOT NULL
	,CLIENT_ID INT NOT NULL
	,VALOR FLOAT NOT NULL
	,DATA DATETIME
	,PRIMARY KEY (ID)
	,FOREIGN KEY (CLIENT_ID) REFERENCES TB_CLIENTS(ID)
);
GO
--VERIFICAR SE O N�MERO DE CLIENTES CORRESPONDEM AO TOTAL INFORMADO NO .CSV
SELECT *
	FROM TB_CLIENTS
GO
--VERIFICAR SE O N�MERO DE TRANSA��ES CORRESPONDEM AO TOTAL INFORMADO NO .CSV
SELECT *
	FROM TB_TRANSACTION
GO
--DESCOBRIR OS IDS QUE N�O EXISTEM NA TB_CLIENT
SELECT DISTINCT 
	T.CLIENT_ID 
FROM TB_CLIENTS C
RIGHT JOIN TB_TRANSACTION T 
	ON T.CLIENT_ID = C.ID 
WHERE C.ID IS NULL
ORDER BY T.CLIENT_ID


Drop table tb_transaction

