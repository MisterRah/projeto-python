import tkinter as tk
from tkinter import messagebox
import re  # Para validar strings

# Lista para armazenar os dados
alunos = []
materias = ["Matemática", "Português", "História", "Geografia", "Física", "Química"]

# Validações auxiliares
def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome))  # Apenas letras e espaços

def validar_turma(turma):
    return bool(re.match(r"^[A-Za-z0-9]+$", turma))  # Letras e números (ex: 3A, 2B)

def validar_nota(nota):
    try:
        nota_float = float(nota)
        return 0 <= nota_float <= 10
    except ValueError:
        return False

# Adicionar aluno
def adicionar_aluno():
    nome = entry_nome.get()
    turma = entry_turma.get()
    materia = materia_var.get()
    nota = entry_nota.get()

    if not (nome and turma and materia and nota):
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    if not validar_nome(nome):
        messagebox.showerror("Erro", "Nome deve conter apenas letras.")
        return

    if not validar_turma(turma):
        messagebox.showerror("Erro", "Turma deve conter apenas letras e/ou números (sem espaços).")
        return

    if not validar_nota(nota):
        messagebox.showerror("Erro", "Nota deve ser um número entre 0 e 10.")
        return

    alunos.append({'nome': nome, 'turma': turma, 'materia': materia, 'nota': nota})
    limpar_campos()
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")

# Atualizar aluno
def atualizar_aluno():
    indice = listbox_alunos.curselection()
    if not indice:
        messagebox.showwarning("Atenção", "Selecione um aluno para atualizar.")
        return

    nome = entry_nome.get()
    turma = entry_turma.get()
    materia = materia_var.get()
    nota = entry_nota.get()

    if not (nome and turma and materia and nota):
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    if not validar_nome(nome):
        messagebox.showerror("Erro", "Nome deve conter apenas letras.")
        return

    if not validar_turma(turma):
        messagebox.showerror("Erro", "Turma deve conter apenas letras e/ou números.")
        return

    if not validar_nota(nota):
        messagebox.showerror("Erro", "Nota deve ser um número entre 0 e 10.")
        return

    alunos[indice[0]] = {'nome': nome, 'turma': turma, 'materia': materia, 'nota': nota}
    limpar_campos()
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")

# Deletar
def deletar_aluno():
    indice = listbox_alunos.curselection()
    if not indice:
        messagebox.showwarning("Atenção", "Selecione um aluno para deletar.")
        return

    alunos.pop(indice[0])
    atualizar_lista()
    limpar_campos()
    messagebox.showinfo("Sucesso", "Aluno deletado com sucesso!")

# Limpar campos
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_turma.delete(0, tk.END)
    entry_nota.delete(0, tk.END)
    materia_var.set(materias[0])

# Selecionar aluno
def selecionar_aluno(event):
    indice = listbox_alunos.curselection()
    if not indice:
        return

    aluno = alunos[indice[0]]
    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, aluno['nome'])
    entry_turma.delete(0, tk.END)
    entry_turma.insert(0, aluno['turma'])
    materia_var.set(aluno['materia'])
    entry_nota.delete(0, tk.END)
    entry_nota.insert(0, aluno['nota'])

# Atualizar lista
def atualizar_lista():
    listbox_alunos.delete(0, tk.END)
    for i, aluno in enumerate(alunos, start=1):
        item = f"{i}. {aluno['nome']} | Turma: {aluno['turma']} | {aluno['materia']} - Nota: {aluno['nota']}"
        listbox_alunos.insert(tk.END, item)

# Interface
janela = tk.Tk()
janela.title("CRUD de Alunos com Validação")

# Labels e Entradas
tk.Label(janela, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_nome = tk.Entry(janela, width=30)
entry_nome.grid(row=0, column=1)

tk.Label(janela, text="Turma:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_turma = tk.Entry(janela, width=30)
entry_turma.grid(row=1, column=1)

tk.Label(janela, text="Matéria:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
materia_var = tk.StringVar(janela)
materia_var.set(materias[0])
menu_materia = tk.OptionMenu(janela, materia_var, *materias)
menu_materia.config(width=27)
menu_materia.grid(row=2, column=1)

tk.Label(janela, text="Nota (0 a 10):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
entry_nota = tk.Entry(janela, width=30)
entry_nota.grid(row=3, column=1)

# Botões
tk.Button(janela, text="Adicionar", command=adicionar_aluno, bg="#4CAF50", fg="white").grid(row=4, column=0, pady=10)
tk.Button(janela, text="Atualizar", command=atualizar_aluno, bg="#2196F3", fg="white").grid(row=4, column=1)
tk.Button(janela, text="Deletar", command=deletar_aluno, bg="#f44336", fg="white").grid(row=5, column=0)
tk.Button(janela, text="Limpar Campos", command=limpar_campos, bg="#607D8B", fg="white").grid(row=5, column=1)

# Lista de alunos
listbox_alunos = tk.Listbox(janela, width=80)
listbox_alunos.grid(row=6, column=0, columnspan=2, padx=5, pady=10)
listbox_alunos.bind("<<ListboxSelect>>", selecionar_aluno)

# Loop
janela.mainloop()
