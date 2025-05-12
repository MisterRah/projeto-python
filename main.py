import tkinter as tk
from tkinter import ttk, messagebox
import re
from bd import Banco

# Inicializar banco
try:
    db = Banco()
    db.criar_banco("alunos")
    db.connect_to_db()
    db.criar_tabela_aluno()
except Exception as e:
    messagebox.showerror("Erro", f"Falha ao inicializar o banco de dados: {str(e)}")
    exit(1)

# Funções de validação
def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome))

def validar_turma(turma):
    return bool(re.match(r"^[A-Za-z0-9]+$", turma))

def validar_nota(nota):
    if not nota:
        return True  # Permitir vazio (NULL)
    try:
        nota_float = float(nota)
        return 0 <= nota_float <= 10
    except ValueError:
        return False

# Funções principais
def adicionar_aluno():
    print("Iniciando adicionar_aluno")
    nome = entry_nome.get().strip()
    turma = entry_turma.get().strip()
    notas = {
        'portugues': entry_portugues.get().strip(),
        'matematica': entry_matematica.get().strip(),
        'fisica': entry_fisica.get().strip(),
        'historia': entry_historia.get().strip(),
        'ingles': entry_ingles.get().strip(),
        'geografia': entry_geografia.get().strip()
    }

    if not (nome and turma):
        messagebox.showwarning("Atenção", "Preencha os campos Nome e Turma.")
        return

    if not validar_nome(nome) or not validar_turma(turma):
        messagebox.showerror("Erro", "Nome ou Turma inválidos.")
        return

    for materia, nota in notas.items():
        if not validar_nota(nota):
            messagebox.showerror("Erro", f"Nota inválida para {materia.capitalize()} (deve ser entre 0 e 10).")
            return
        notas[materia] = float(nota) if nota else None

    try:
        db.inserir_dados(nome, turma, notas)
        limpar_campos()
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao adicionar aluno: {str(e)}")

def atualizar_aluno():
    print("Iniciando atualizar_aluno")
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um aluno para atualizar.")
        return

    matricula = tabela.item(selecionado, "values")[0]
    nome = entry_nome.get().strip()
    turma = entry_turma.get().strip()
    notas = {
        'portugues': entry_portugues.get().strip(),
        'matematica': entry_matematica.get().strip(),
        'fisica': entry_fisica.get().strip(),
        'historia': entry_historia.get().strip(),
        'ingles': entry_ingles.get().strip(),
        'geografia': entry_geografia.get().strip()
    }

    if not (nome and turma):
        messagebox.showwarning("Atenção", "Preencha os campos Nome e Turma.")
        return

    if not validar_nome(nome) or not validar_turma(turma):
        messagebox.showerror("Erro", "Nome ou Turma inválidos.")
        return

    for materia, nota in notas.items():
        if not validar_nota(nota):
            messagebox.showerror("Erro", f"Nota inválida para {materia.capitalize()} (deve ser entre 0 e 10).")
            return
        notas[materia] = float(nota) if nota else None

    try:
        db.atualizar_dados(matricula, nome, turma, notas)
        limpar_campos()
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao atualizar aluno: {str(e)}")

def deletar_aluno():
    print("Iniciando deletar_aluno")
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um aluno para deletar.")
        return

    matricula = tabela.item(selecionado, "values")[0]
    print(f"Deletando matrícula: {matricula}")
    try:
        db.excluir_dados(matricula)
        limpar_campos()
        atualizar_tabela()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao deletar aluno: {str(e)}")

def limpar_campos():
    print("Limpando campos")
    entry_nome.delete(0, tk.END)
    entry_turma.delete(0, tk.END)
    entry_portugues.delete(0, tk.END)
    entry_matematica.delete(0, tk.END)
    entry_fisica.delete(0, tk.END)
    entry_historia.delete(0, tk.END)
    entry_ingles.delete(0, tk.END)
    entry_geografia.delete(0, tk.END)

def selecionar_aluno(event):
    print("Iniciando selecionar_aluno")
    selecionado = tabela.selection()
    if not selecionado:
        return

    try:
        dados = tabela.item(selecionado, "values")
        print(f"Dados selecionados: {dados}")
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados[1])
        entry_turma.delete(0, tk.END)
        entry_turma.insert(0, dados[2])
        entry_portugues.delete(0, tk.END)
        entry_portugues.insert(0, dados[3] if dados[3] else "")
        entry_matematica.delete(0, tk.END)
        entry_matematica.insert(0, dados[4] if dados[4] else "")
        entry_fisica.delete(0, tk.END)
        entry_fisica.insert(0, dados[5] if dados[5] else "")
        entry_historia.delete(0, tk.END)
        entry_historia.insert(0, dados[6] if dados[6] else "")
        entry_ingles.delete(0, tk.END)
        entry_ingles.insert(0, dados[7] if dados[7] else "")
        entry_geografia.delete(0, tk.END)
        entry_geografia.insert(0, dados[8] if dados[8] else "")
    except IndexError as e:
        messagebox.showerror("Erro", "Erro ao carregar dados do aluno.")
        print("Erro ao selecionar aluno:", e)

def atualizar_tabela():
    print("Atualizando tabela")
    for linha in tabela.get_children():
        tabela.delete(linha)

    try:
        alunos = db.selecionar_dados()
        for aluno in alunos:
            tabela.insert("", tk.END, values=aluno)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao atualizar tabela: {str(e)}")

def buscar_alunos():
    print("Iniciando buscar_alunos")
    matricula = entry_busca_matricula.get().strip()
    nome = entry_busca_nome.get().strip()

    # Limpar tabela antes de exibir resultados
    for linha in tabela.get_children():
        tabela.delete(linha)

    try:
        # Buscar no banco com filtros
        alunos = db.buscar_dados(matricula=matricula, nome=nome)
        if not alunos:
            messagebox.showinfo("Resultado", "Nenhum aluno encontrado.")
            return

        for aluno in alunos:
            tabela.insert("", tk.END, values=aluno)
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao buscar alunos: {str(e)}")

# Interface
janela = tk.Tk()
janela.title("Cadastro de Alunos PostgreSQL")

# Frame principal para organização
frame_principal = tk.Frame(janela)
frame_principal.grid(row=0, column=0, padx=10, pady=10)

# Labels e entradas
tk.Label(frame_principal, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nome = tk.Entry(frame_principal, width=30)
entry_nome.grid(row=0, column=1)

tk.Label(frame_principal, text="Turma:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_turma = tk.Entry(frame_principal, width=30)
entry_turma.grid(row=1, column=1)

tk.Label(frame_principal, text="Português (0 a 10):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
entry_portugues = tk.Entry(frame_principal, width=30)
entry_portugues.grid(row=2, column=1)

tk.Label(frame_principal, text="Matemática (0 a 10):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_matematica = tk.Entry(frame_principal, width=30)
entry_matematica.grid(row=3, column=1)

tk.Label(frame_principal, text="Física (0 a 10):").grid(row=4, column=0, sticky="w", padx=5, pady=5)
entry_fisica = tk.Entry(frame_principal, width=30)
entry_fisica.grid(row=4, column=1)

tk.Label(frame_principal, text="História (0 a 10):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
entry_historia = tk.Entry(frame_principal, width=30)
entry_historia.grid(row=5, column=1)

tk.Label(frame_principal, text="Inglês (0 a 10):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
entry_ingles = tk.Entry(frame_principal, width=30)
entry_ingles.grid(row=6, column=1)

tk.Label(frame_principal, text="Geografia (0 a 10):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
entry_geografia = tk.Entry(frame_principal, width=30)
entry_geografia.grid(row=7, column=1)

# Botões
tk.Button(frame_principal, text="Adicionar", command=adicionar_aluno, bg="#4CAF50", fg="white").grid(row=8, column=0, pady=10)
tk.Button(frame_principal, text="Atualizar", command=atualizar_aluno, bg="#2196F3", fg="white").grid(row=8, column=1)
tk.Button(frame_principal, text="Deletar", command=deletar_aluno, bg="#f44336", fg="white").grid(row=9, column=0)
tk.Button(frame_principal, text="Limpar", command=limpar_campos, bg="#607D8B", fg="white").grid(row=9, column=1)

# Frame para busca
frame_busca = tk.Frame(frame_principal)
frame_busca.grid(row=10, column=0, columnspan=2, pady=10)

tk.Label(frame_busca, text="Buscar por Matrícula:").grid(row=0, column=0, sticky="w", padx=5)
entry_busca_matricula = tk.Entry(frame_busca, width=15)
entry_busca_matricula.grid(row=0, column=1, padx=5)

tk.Label(frame_busca, text="Buscar por Nome:").grid(row=0, column=2, sticky="w", padx=5)
entry_busca_nome = tk.Entry(frame_busca, width=20)
entry_busca_nome.grid(row=0, column=3, padx=5)

tk.Button(frame_busca, text="Buscar", command=buscar_alunos, bg="#FFC107", fg="black").grid(row=0, column=4, padx=5)
tk.Button(frame_busca, text="Mostrar Todos", command=atualizar_tabela, bg="#607D8B", fg="white").grid(row=0, column=5, padx=5)

# Tabela (Treeview)
tabela = ttk.Treeview(frame_principal, columns=("matricula", "nome", "turma", "portugues", "matematica", "fisica", "historia", "ingles", "geografia"), show="headings")
tabela.heading("matricula", text="Matrícula")
tabela.heading("nome", text="Nome")
tabela.heading("turma", text="Turma")
tabela.heading("portugues", text="Português")
tabela.heading("matematica", text="Matemática")
tabela.heading("fisica", text="Física")
tabela.heading("historia", text="História")
tabela.heading("ingles", text="Inglês")
tabela.heading("geografia", text="Geografia")

# Ajustar largura
tabela.column("matricula", width=70, anchor="center")
tabela.column("nome", width=150, anchor="w")
tabela.column("turma", width=80, anchor="center")
tabela.column("portugues", width=70, anchor="center")
tabela.column("matematica", width=70, anchor="center")
tabela.column("fisica", width=70, anchor="center")
tabela.column("historia", width=70, anchor="center")
tabela.column("ingles", width=70, anchor="center")
tabela.column("geografia", width=70, anchor="center")

tabela.grid(row=11, column=0, columnspan=2, padx=5, pady=10)
tabela.bind("<<TreeviewSelect>>", selecionar_aluno)

# Inicializar tabela
atualizar_tabela()

janela.mainloop()

# Fechar conexão no final
try:
    db.fechar_conexao()
except Exception as e:
    print(f"Erro ao fechar conexão: {str(e)}")