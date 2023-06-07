import tkinter as tk
import psycopg2
from tkinter import ttk
from tkinter import messagebox



def executar_comando():
    comando = entrada_comando.get()
    try:
        conn = psycopg2.connect(
            host=entrada_host.get(),
            port=entrada_porta.get(),
            user=entrada_usuario.get(),
            password=entrada_senha.get(),
            database=entrada_banco_dados.get()
        )
        cursor = conn.cursor()
        cursor.execute(comando)
        resultado = cursor.fetchall()
        conn.commit()
        conn.close()
        status.config(text="Comando executado com sucesso!", fg="green")
        exibir_resultado(resultado)
    except Exception as e:
        status.config(text=f"Erro ao executar o comando: {str(e)}", fg="red")

def exibir_resultado(resultado):
    tabela_resultado.delete(*tabela_resultado.get_children())
    for linha in resultado:
        tabela_resultado.insert("", "end", values=linha)

def executar_comando_sql():
    comando_sql = selecionar_comando.get()
    tabela_selecionada = tabela_resultado.focus()  # Obtém a tabela selecionada
    if tabela_selecionada:
        tabela = tabela_resultado.item(tabela_selecionada)["values"][0]  # Obtém o valor da tabela selecionada
        comando_sql = comando_sql.replace("tabela", tabela)  # Substitui "tabela" pelo nome da tabela selecionada

    entrada_comando.delete(0, tk.END)
    entrada_comando.insert(0, comando_sql)


def recuperar_tabelas():
    try:
        conn = psycopg2.connect(
            host=entrada_host.get(),
            port=entrada_porta.get(),
            user=entrada_usuario.get(),
            password=entrada_senha.get(),
            database=entrada_banco_dados.get()
        )
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tabelas = cursor.fetchall()
        conn.close()
        exibir_tabelas(tabelas)
    except Exception as e:
        status.config(text=f"Erro ao recuperar tabelas: {str(e)}", fg="red")

def exibir_tabelas(tabelas):
    tabela_resultado.delete(*tabela_resultado.get_children())
    for tabela in tabelas:
        tabela_resultado.insert("", "end", values=tabela)

def teste_conexao():
    try:
        conn = psycopg2.connect(
            host=entrada_host.get(),
            port=entrada_porta.get(),
            user=entrada_usuario.get(),
            password=entrada_senha.get(),
            database=entrada_banco_dados.get()
        )
        conn.close()
        messagebox.showinfo("Teste de Conexão", "Conexão bem-sucedida!")
    except Exception as e:
        messagebox.showerror("Teste de Conexão", f"Erro ao conectar ao banco de dados:\n{str(e)}")

janela = tk.Tk()
janela.title("Teste de Comando e Conexão")
janela.geometry("500x400")
janela.configure(background='dark blue')

# Criação dos widgets
titulo = tk.Label(janela, text="Teste de Comando e Conexão", font=("Arial", 16), bg="dark blue", fg="white")
titulo.pack(pady=10)

label_host = tk.Label(janela, text="Host:", bg="dark blue", fg="white")
label_host.pack()
entrada_host = tk.Entry(janela)
entrada_host.pack()

label_porta = tk.Label(janela, text="Porta:", bg="dark blue", fg="white")
label_porta.pack()
entrada_porta = tk.Entry(janela)
entrada_porta.pack()

label_usuario = tk.Label(janela, text="Usuário:", bg="dark blue", fg="white")
label_usuario.pack()
entrada_usuario = tk.Entry(janela)
entrada_usuario.pack()

label_senha = tk.Label(janela, text="Senha:", bg="dark blue", fg="white")
label_senha.pack()
entrada_senha = tk.Entry(janela, show="*")
entrada_senha.pack()

label_banco_dados = tk.Label(janela, text="Banco de Dados:", bg="dark blue", fg="white")
label_banco_dados.pack()
entrada_banco_dados = tk.Entry(janela)
entrada_banco_dados.pack()

botao_teste_conexao = tk.Button(janela, text="Testar Conexão", command=teste_conexao)
botao_teste_conexao.pack(pady=10)

botao_recuperar_tabelas = tk.Button(janela, text="Recuperar Tabelas", command=recuperar_tabelas)
botao_recuperar_tabelas.pack(pady=10)

label_comando = tk.Label(janela, text="Comando:", bg="dark blue", fg="white")
label_comando.pack()
entrada_comando = tk.Entry(janela)
entrada_comando.pack()

label_selecionar_comando = tk.Label(janela, text="Selecionar Comando:", bg="dark blue", fg="white")
label_selecionar_comando.pack()
selecionar_comando = tk.StringVar()
selecionar_comando.set("SELECT * FROM tabela")  # Comando SQL padrão
opcoes_comando = tk.OptionMenu(janela, selecionar_comando, 
                               "SELECT * FROM tabela",
                               "INSERT INTO tabela (coluna1, coluna2) VALUES (valor1, valor2)",
                               "UPDATE tabela SET coluna = valor WHERE condicao",
                               "DELETE FROM tabela WHERE condicao",
                               "DROP TABLE tabela")
opcoes_comando.pack(pady=10)

botao_sql_predefinido = tk.Button(janela, text="Comando SQL Pré-definido", command=executar_comando_sql)
botao_sql_predefinido.pack(pady=10)

botao_executar = tk.Button(janela, text="Executar Comando", command=executar_comando)
botao_executar.pack(pady=10)

status = tk.Label(janela, text="", bg="dark blue", fg="white")
status.pack()

tabela_resultado = tk.ttk.Treeview(janela, columns=("col1",), show="headings")
tabela_resultado.heading("col1", text="Tabela")
tabela_resultado.pack(pady=10)

janela.mainloop()
