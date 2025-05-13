# Cadastro de Alunos

Uma atividade da disciplina de desenvolvimento rápido de aplicações em python, utilizando o metódo CRUD (create, read, update, delete). Um programa que basicamente
faz essas quatro operações para realizar o cadastro de alunos. Além do mais, foi acrescentado algumas funcionalidades a mais para deixar o programa mais dinâmico.

## Funcionalidades

- **Cadastro de alunos**: Adicione novos alunos com nome, turma e notas em seis disciplinas (Português, Matemática, Física, História, Inglês e Geografia).
- **Atualização**: Edite informações de alunos existentes.
- **Exclusão**: Remova alunos do banco de dados.
- **Busca**: Pesquise alunos por matrícula ou nome.
- **Visualização**: Exiba todos os alunos em uma tabela com barra de rolagem.
- **Validação**: Garante que nomes, turmas e notas sejam válidos (notas entre 0 e 10, ou vazias).

## Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL 12 ou superior
- Bibliotecas Python:
  - `psycopg2-binary` (para a comunicação do python com o banco de dados postgreSQL)
  - `tkinter` (geralmente incluído com Python)
   - `re` (usado para definir tipos de entradas nos labels)

## Instalação e configuração de ambiente

### Observações:

> Eu estou utilizando uma distribuição linux (Ubuntu 24.04.2 LTS), portanto, configurações de ambiente vão ser um pouco diferentes dependendo do sistema operacional utilizado.

1. **Instale as dependências**: 
   - Instalar e configurar dependências citadas no pré-requisitos
   - Crie um ambiente virtual (opcional, mas recomendado) e instale as bibliotecas necessárias :
   ```bash
   # esse processo é feito após instalação do python em sua máquina
   sudo apt install python3-venv # para instalar um lib do ambiente virtual
   python -m venv venv #criar o ambiente virtual
   source venv/bin/activate  # ativar ambiente virtual
   pip install psycopg2-binary
   pip install re  
   ```


2. **Configure o PostgreSQL**:
   - Instale o PostgreSQL e inicie o servidor.
   - use o usuário padrão do PostgreSQL (postgres) e configure a senha. Exemplo:
     ```sql
     CREATE USER postgres WITH PASSWORD 'sua-senha';  
     ```

2. **Mudanças no código para rodar em seu postgreSQL** 
	- Entre no arquivo bd.py e procure a váriavel global chamada DB_PASSWORD e altere para sua senha do usuário postgres (usuário padrão do PostegreSQL)
	
		
## Uso

1. **Execute o programa**:
   ```bash
   python main.py
   ```

2. **Interface**:
   - **Campos de entrada**: Insira nome, turma e notas (opcional, entre 0 e 10).
   - **Botões**:
     - **Adicionar**: Insere um novo aluno no banco.
     - **Atualizar**: Edita o aluno selecionado.
     - **Deletar**: Remove o aluno selecionado.
     - **Limpar**: Limpa os campos de entrada.
     - **Buscar**: Pesquisa por matrícula ou nome.
     - **Mostrar Todos**: Exibe todos os alunos na tabela.
   - **Tabela**: Clique em um aluno para carregar seus dados nos campos de entrada.

3. **Sair**: Feche a janela para encerrar o programa e desconectar do banco.

## Estrutura do projeto

- `main.py`: Código principal com a interface gráfica (Tkinter) e lógica da aplicação.
- `bd.py`: Módulo para gerenciamento do banco de dados PostgreSQL (conexão, criação de tabelas, CRUD).
- `README.md`: Este arquivo com instruções do projeto.


