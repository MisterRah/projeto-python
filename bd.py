import psycopg2
from psycopg2 import Error

class Banco:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect_to_db(self):
        try:
            print("Tentando conectar ao banco 'alunos'...")
            self.conn = psycopg2.connect(
                database="alunos",
                user="postgres",
                password="teste12345",
                host="127.0.0.1",
                port="5432"
            )
            self.cur = self.conn.cursor()
            print("Conexão com o Banco de Dados aberta com sucesso!")
        except Exception as error:
            print("Falha ao se conectar ao Banco de Dados:", error)
            self.conn = None
            self.cur = None
            raise

    def criar_banco(self, nome_banco):
        try:
            # Fechar conexão atual (caso esteja conectada a outro banco)
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()

            # Conectar no banco "postgres", que sempre existe
            print("Conectando ao banco 'postgres' para criar banco...")
            self.conn = psycopg2.connect(
                database="postgres",
                user="postgres",
                password="teste12345",
                host="127.0.0.1",
                port="5432"
            )
            self.conn.autocommit = True
            self.cur = self.conn.cursor()

            # Verificar se o banco já existe
            self.cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (nome_banco,))
            if not self.cur.fetchone():
                self.cur.execute(f"CREATE DATABASE {nome_banco}")
                print(f"Banco de dados '{nome_banco}' criado com sucesso!")
            else:
                print(f"Banco de dados '{nome_banco}' já existe.")

            self.cur.close()
            self.conn.close()
        except Exception as error:
            print("Erro ao criar banco de dados:", error)
            raise

    def criar_tabela_aluno(self):
        try:
            print("Verificando conexão para criar tabelas...")
            if not self.conn or self.conn.closed or not self.cur:
                print("Conexão inválida ou fechada, reconectando...")
                self.connect_to_db()

            if not self.cur:
                raise Exception("Cursor não inicializado após conexão.")

            print("Executando comando SQL para criar tabelas...")
            # Criar tabela aluno
            comando_sql_aluno = '''
            CREATE TABLE IF NOT EXISTS aluno (
                matricula SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                turma VARCHAR(50) NOT NULL
            )
            '''
            self.cur.execute(comando_sql_aluno)

            # Criar tabela notas
            comando_sql_notas = '''
            CREATE TABLE IF NOT EXISTS notas (
                id_nota SERIAL PRIMARY KEY,
                matricula INTEGER REFERENCES aluno(matricula) ON DELETE CASCADE,
                portugues NUMERIC(4,2),
                matematica NUMERIC(4,2),
                fisica NUMERIC(4,2),
                historia NUMERIC(4,2),
                ingles NUMERIC(4,2),
                geografia NUMERIC(4,2)
            )
            '''
            self.cur.execute(comando_sql_notas)
            self.conn.commit()
            print("Tabelas 'aluno' e 'notas' criadas com sucesso!")
        except Exception as error:
            print("Erro ao criar tabelas:", error)
            raise

    def fechar_conexao(self):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
            print("Conexão com o Banco de Dados fechada com sucesso!")
        except Exception as error:
            print("Erro ao fechar conexão:", error)

    def selecionar_dados(self):
        try:
            if not self.conn or self.conn.closed:
                self.connect_to_db()
            self.cur.execute('''
                SELECT a.matricula, a.nome, a.turma, 
                       n.portugues, n.matematica, n.fisica, 
                       n.historia, n.ingles, n.geografia
                FROM aluno a
                LEFT JOIN notas n ON a.matricula = n.matricula
                ORDER BY a.matricula
            ''')
            registros = self.cur.fetchall()
            return registros
        except Exception as error:
            print("Erro ao selecionar dados:", error)
            return []

    def inserir_dados(self, nome, turma, notas):
        try:
            if not self.conn or self.conn.closed:
                self.connect_to_db()
            
            # Inserir na tabela aluno
            self.cur.execute(
                '''INSERT INTO aluno (nome, turma) VALUES (%s, %s) RETURNING matricula''',
                (nome, turma)
            )
            matricula = self.cur.fetchone()[0]
            
            # Inserir na tabela notas
            self.cur.execute(
                '''INSERT INTO notas (matricula, portugues, matematica, fisica, historia, ingles, geografia)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (matricula, notas['portugues'], notas['matematica'], notas['fisica'],
                 notas['historia'], notas['ingles'], notas['geografia'])
            )
            self.conn.commit()
            print("Inserção realizada com sucesso!")
        except Exception as error:
            print("Erro ao inserir dados:", error)
            self.conn.rollback()

    def atualizar_dados(self, matricula, nome, turma, notas):
        try:
            if not self.conn or self.conn.closed:
                self.connect_to_db()
            
            # Atualizar tabela aluno
            self.cur.execute(
                '''UPDATE aluno SET nome = %s, turma = %s WHERE matricula = %s''',
                (nome, turma, matricula)
            )
            
            # Verificar se existe registro na tabela notas
            self.cur.execute("SELECT 1 FROM notas WHERE matricula = %s", (matricula,))
            if self.cur.fetchone():
                # Atualizar tabela notas
                self.cur.execute(
                    '''UPDATE notas SET portugues = %s, matematica = %s, fisica = %s, 
                       historia = %s, ingles = %s, geografia = %s 
                       WHERE matricula = %s''',
                    (notas['portugues'], notas['matematica'], notas['fisica'],
                     notas['historia'], notas['ingles'], notas['geografia'], matricula)
                )
            else:
                # Inserir na tabela notas se não existir
                self.cur.execute(
                    '''INSERT INTO notas (matricula, portugues, matematica, fisica, historia, ingles, geografia)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                    (matricula, notas['portugues'], notas['matematica'], notas['fisica'],
                     notas['historia'], notas['ingles'], notas['geografia'])
                )
            self.conn.commit()
            print("Atualização realizada com sucesso!")
        except Exception as error:
            print("Erro ao atualizar dados:", error)
            self.conn.rollback()

    def excluir_dados(self, matricula):
        try:
            if not self.conn or self.conn.closed:
                self.connect_to_db()
            # A exclusão na tabela notas é automática devido ao ON DELETE CASCADE
            self.cur.execute(
                '''DELETE FROM aluno WHERE matricula = %s''',
                (matricula,)
            )
            self.conn.commit()
            print("Exclusão realizada com sucesso!")
        except Exception as error:
            print("Erro ao excluir dados:", error)
            self.conn.rollback()

    def buscar_dados(self, matricula="", nome=""):
        try:
            if not self.conn or self.conn.closed:
                self.connect_to_db()
            query = '''
                SELECT a.matricula, a.nome, a.turma, 
                       n.portugues, n.matematica, n.fisica, 
                       n.historia, n.ingles, n.geografia
                FROM aluno a
                LEFT JOIN notas n ON a.matricula = n.matricula
                WHERE 1=1
            '''
            params = []
            
            if matricula:
                query += " AND a.matricula = %s"
                params.append(matricula)
            if nome:
                query += " AND a.nome ILIKE %s"
                params.append(f"%{nome}%")
                
            self.cur.execute(query, params)
            return self.cur.fetchall()
        except Exception as error:
            print("Erro ao buscar dados:", error)
            return []