import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


# Carregar os dados do arquivo Excel
arquivo_excel = 'COMPTES.xlsx'
tabelas = pd.read_excel(arquivo_excel, sheet_name=None)

data_machines = tabelas['MACHINE']
data_comptes = tabelas['COMPTE']
data_employes = tabelas['EMPLOYÉS']
data_candidats = tabelas['CANDIDATS']

# Função para verificar sobrecarga
def verificar_sobrecarga():
    # Verificar se as colunas necessárias existem no dataframe
    if 'HEURES_COMPTES' in data_machines.columns and 'HEURES_DISPONIBLES' in data_machines.columns:
        # Calcular a diferença de horas sobrecarregadas
        data_machines['Diferença'] = data_machines['HEURES_COMPTES'] - data_machines['HEURES_DISPONIBLES']

        # Filtrar máquinas sobrecarregadas
        machines_sobrecarregadas = data_machines[data_machines['Diferença'] > 0]

        # Exibir informações em uma nova janela
        sobrecarga_window = tk.Toplevel(root)
        sobrecarga_window.title("Machines Surchargées")

        label_sobrecarga = tk.Label(sobrecarga_window, text="Machines Surchargées:", font=("Helvetica", 20))
        label_sobrecarga.pack(pady=10)

        for _, machine in machines_sobrecarregadas.iterrows():
            label_machine = tk.Label(sobrecarga_window, text=f"ID: {machine['ID_MACHINE']}, "
                                                            f"Différence Heures: {machine['Diferença']}",
                                                            font=("Helvetica", 16))
            label_machine.pack()

    else:
        tk.messagebox.showinfo("Erro", "Colunas necessárias não encontradas no dataframe.")



def exibir_informacoes(machine_id):
    # Verificar se a máquina com o ID fornecido existe no dataframe
    if machine_id in data_machines['ID_MACHINE'].values:
        # Obter as informações da máquina com o ID fornecido
        info_machine = data_machines[data_machines['ID_MACHINE'] == machine_id].iloc[0]

        # Obter os pedidos da máquina
        pedidos = data_comptes[data_comptes['ID_MACHINE'] == machine_id][['NUMÉRO_COMPTE', 'NOM_PIECE', 'QNT', 'DURÉE_TOTALE', 'DATE_LIVRAISON']]

        # Obter os colaboradores da máquina
        colaboradores = data_employes[data_employes['ID_MACHINE'] == machine_id][['ID_EMPLOYÉ', 'NOM', 'POSTE', 'SALAIRE', 'DATE_EMBAUCHE']]

        # Exibir informações em uma nova janela
        info_window = tk.Toplevel(root)
        info_window.title(f"Information Machine {machine_id}")

        label_info = tk.Label(info_window, text=f"ID: {info_machine['ID_MACHINE']}\n"
                                                f"Nombre d'Employes: {info_machine.get('QNT_EMPLOYÉS', 'N/A')}\n"
                                                f"Nombre Heures Totales Comptes: {info_machine.get('HEURES_COMPTES', 'N/A')}\n"
                                                f"Nombre Heures Disponibles: {info_machine.get('HEURES_DISPONIBLES', 'N/A')}",
                              font=("Helvetica", 14))
        label_info.pack(pady=10)

        # Adicionar lista de pedidos
        label_pedidos = tk.Label(info_window, text="Comptes:", font=("Helvetica", 14))
        label_pedidos.pack()

        for _, pedido in pedidos.iterrows():
            label_pedido = tk.Label(info_window, text=f"Numéro du Compte: {pedido['NUMÉRO_COMPTE']}, "
                                                       f"Nom de la Pièce: {pedido['NOM_PIECE']}, "
                                                       f"Quantité: {pedido['QNT']}, "
                                                       f"Durée Totale: {pedido['DURÉE_TOTALE']}, "
                                                       f"Date de Livraison: {pedido['DATE_LIVRAISON']}", font=("Helvetica", 12))
            label_pedido.pack()

        # Adicionar lista de colaboradores
        label_colaboradores = tk.Label(info_window, text="Employés:", font=("Helvetica", 14))
        label_colaboradores.pack()

        for _, colaborador in colaboradores.iterrows():
            label_colab = tk.Label(info_window, text=f"ID: {colaborador['ID_EMPLOYÉ']}, "
                                                      f"Prénom: {colaborador['NOM']}, "
                                                      f"Poste: {colaborador['POSTE']}, "
                                                      f"Salaire: {colaborador['SALAIRE']}, "
                                                      f"Date d'Embauche: {colaborador['DATE_EMBAUCHE']}", font=("Helvetica", 12))
            label_colab.pack()

    else:
        tk.messagebox.showinfo("Erro", f"Máquina com ID {machine_id} não encontrada.")

def tratar_machines_surchargées():
    # Verificar se as colunas necessárias existem no dataframe
    if 'HEURES_COMPTES' in data_machines.columns and 'HEURES_DISPONIBLES' in data_machines.columns:
        # Calcular a diferença de horas sobrecarregadas
        data_machines['Diferença'] = data_machines['HEURES_COMPTES'] - data_machines['HEURES_DISPONIBLES']

        # Filtrar máquinas sobrecarregadas
        machines_sobrecarregadas = data_machines[data_machines['Diferença'] > 0]

        # Verificar se há máquinas sobrecarregadas
        if not machines_sobrecarregadas.empty:
            # Criar uma nova janela para o tratamento
            tratamento_window = tk.Toplevel(root)
            tratamento_window.title("Traitement des Machines Surchargées")

            label_tratamento = tk.Label(tratamento_window, text="Traitement des Machines Surchargées", font=("Helvetica", 20))
            label_tratamento.pack(pady=10)

            label_instrucao = tk.Label(tratamento_window, text="Choisissez une machine pour effectuer le traitement.", font=("Helvetica", 16))
            label_instrucao.pack(pady=10)

            # Loop para adicionar botões para cada máquina sobrecarregada
            for _, machine in machines_sobrecarregadas.iterrows():
                btn_machine = tk.Button(tratamento_window, text=f"ID: {machine['ID_MACHINE']}, "
                                                               f"Différence Heures: {machine.get('Diferença', 'N/A')}",
                                       command=lambda id=machine['ID_MACHINE']: tratar_máquina_individual(id),
                                       font=("Helvetica", 14))
                btn_machine.pack(pady=5)

        else:
            tk.messagebox.showinfo("Traitement", "Aucune machine n'est surchargée à traiter.")

    else:
        tk.messagebox.showinfo("Erreur", "Colonnes nécessaires non trouvées dans le dataframe.")


def tratar_máquina_individual(machine_id):
    # Filtrar candidatos disponíveis para contratação na máquina selecionada
    candidatos_disponiveis = data_candidats[data_candidats['ID_MACHINE'] == machine_id]

    # Criar uma nova janela para exibir informações e opções de escolha
    tratamento_individual_window = tk.Toplevel(root)
    tratamento_individual_window.title("Traitement Individuel de la Machine")

    # Adicionar título
    label_titulo = tk.Label(tratamento_individual_window, text=f"Traitement Machine ID: {machine_id}", font=("Helvetica", 16))
    label_titulo.pack(pady=10)

    # Adicionar informações dos candidatos
    label_candidatos = tk.Label(tratamento_individual_window, text="Candidats Disponibles pour Embauche:", font=("Helvetica", 14))
    label_candidatos.pack()

    for _, candidato in candidatos_disponiveis.iterrows():
        label_candidato = tk.Label(tratamento_individual_window, text=f"ID Candidat: {candidato['ID_CANDIDAT']}, "
                                                                     f"Nom: {candidato['NOM']}, "
                                                                     f"Salaire Prevú: {candidato['SALAIRE_PREVÚ']}, "
                                                                     f"Années d'Expérience: {candidato['ANNÉE_EXPÉRIENCE']}", font=("Helvetica", 12))
        label_candidato.pack()

    # Adicionar opções de escolha
    escolha_var = tk.StringVar(value=candidatos_disponiveis.iloc[0]['ID_CANDIDAT'])  # Inicializar com o primeiro candidato

    label_escolha = tk.Label(tratamento_individual_window, text="Choisir un Candidat:", font=("Helvetica", 14))
    label_escolha.pack()

    dropdown_candidatos = ttk.Combobox(tratamento_individual_window, textvariable=escolha_var, values=candidatos_disponiveis['ID_CANDIDAT'])
    dropdown_candidatos.pack()

    def contratar_candidato():
        global data_employes
        global data_machines

        # Verificar se há candidatos disponíveis
        if candidatos_disponiveis.empty:
            messagebox.showinfo("Aucun Candidat Disponible", "Il n'y a pas de candidats disponibles pour embaucher.")
            return

        id_candidato_escolhido = escolha_var.get().strip()  # Remove espaços em branco
        print(f'ID Candidato Escolhido: {id_candidato_escolhido}')
        candidato_escolhido = candidatos_disponiveis[candidatos_disponiveis['ID_CANDIDAT'] == int(id_candidato_escolhido)]
        print('Candidatos Disponveis:')
        print(candidatos_disponiveis)
        print('Candidato Escolhido:', candidato_escolhido)


        # Verificar se há correspondências
        if not candidato_escolhido.empty:
            candidato_escolhido = candidato_escolhido.iloc[0]

            # Calcular novo ID_EMPLOYÉ e atualizar data_employes
            novo_id_employe = data_employes['ID_EMPLOYÉ'].max() + 1
            novo_nome = candidato_escolhido['NOM']
            novo_id_machine = candidato_escolhido['ID_MACHINE']
            novo_poste = candidato_escolhido['POSTE']
            novo_salaire = candidato_escolhido['SALAIRE_PREVÚ']
            nova_date_embauche = datetime.today().strftime('%Y-%m-%d')

            novo_employe = pd.DataFrame({
                'ID_EMPLOYÉ': [novo_id_employe],
                'NOM': [novo_nome],
                'ID_MACHINE': [novo_id_machine],
                'POSTE': [novo_poste],
                'SALAIRE': [novo_salaire],
                'DATE_EMBAUCHE': [nova_date_embauche]
            })

            data_employes = pd.concat([data_employes, novo_employe], ignore_index=True)

            # Atualizar data_machines
            data_machines.loc[data_machines['ID_MACHINE'] == novo_id_machine, 'QNT_EMPLOYÉS'] += 1
            data_machines.loc[data_machines['ID_MACHINE'] == novo_id_machine, 'HEURES_DISPONIBLES'] += 40

            # Fechar a janela de tratamento individual
            tratamento_individual_window.destroy()

            # Atualizar a interface gráfica principal (Machines Surchargées)
            verificar_sobrecarga()

            # Exibir mensagem de sucesso
            messagebox.showinfo("Candidat Embauché", "Le candidat a été embauché avec succès.")
        else:
            messagebox.showwarning("Candidat Non Trouvé", "Le candidat choisi n'a pas été trouvé.")

    # Adicionar botão para contratar candidato
    btn_contratar = tk.Button(tratamento_individual_window, text="Embaucher Candidat", command=contratar_candidato, font=("Helvetica", 14))
    btn_contratar.pack(pady=10)



# Criar a janela principal
root = tk.Tk()
root.title("Gestion des Machines - M & A")

# Adicionar um título centralizado
titulo_label = tk.Label(root, text="Gestion des Machines - M & A", font=("Helvetica", 18))
titulo_label.pack(pady=10)

# Criar um notebook (abas)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, fill='both', expand=True)

# Frame para as informações das máquinas
frame_machines = ttk.Frame(notebook)
notebook.add(frame_machines, text="Affichage des informations sur chaque Machine")

# Adicionar o texto "Machines"
label_machines = tk.Label(frame_machines, text="Machines", font=("Helvetica", 18))
label_machines.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")

# Loop para adicionar informações de cada máquina
for i, machine_id in enumerate(data_machines['ID_MACHINE']):
    label_id = tk.Label(frame_machines, text=f"ID: {machine_id}", font=("Helvetica", 16))
    label_id.grid(row=i+1, column=0, padx=5)

    btn_detalhes = tk.Button(frame_machines, text="Détails", command=lambda id=machine_id: exibir_informacoes(id), font=("Helvetica", 14))
    btn_detalhes.grid(row=i+1, column=5, padx=5)

# Adicionar um espaço para máquinas sobrecarregadas
frame_sobrecarga = ttk.Frame(notebook)
notebook.add(frame_sobrecarga, text="Machines surchargées - Vérifier et Traiter")

# Adicionar um título para máquinas sobrecarregadas
label_sobrecarga = tk.Label(frame_sobrecarga, text="Machines surchargées", font=("Helvetica", 18))
label_sobrecarga.grid(row=0, column=0, columnspan=4, pady=10)

# Botão para verificar sobrecarga
btn_verificar_sobrecarga = tk.Button(frame_sobrecarga, text="Vérifier surcharge", command=verificar_sobrecarga, font=("Helvetica", 16))
btn_verificar_sobrecarga.grid(row=1, column=0, columnspan=4, pady=10)

# Botão "Traitement" na aba de Machines Surchargées
btn_traitement = tk.Button(frame_sobrecarga, text="Traitement", command=tratar_machines_surchargées, font=("Helvetica", 16))
btn_traitement.grid(row=2, column=0, columnspan=4, pady=10)

# Configurar o peso da linha onde o notebook está localizado
root.rowconfigure(1, weight=1)

# Frame para as informações de pedidos (COMPTES)
frame_pedidos = ttk.Frame(notebook)
notebook.add(frame_pedidos, text="Affichage des comptes")

# Adicionar o texto "Pedidos"
label_pedidos = tk.Label(frame_pedidos, text="Comptes", font=("Helvetica", 18))
label_pedidos.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")  # Use columnspan para ocupar várias colunas

# Canvas para permitir rolagem
canvas_pedidos = tk.Canvas(frame_pedidos)
canvas_pedidos.grid(row=1, column=0, columnspan=5, sticky="nsew")  # Atualizei aqui para ocupar 5 colunas

# Frame dentro do canvas
frame_pedidos_scrollable = tk.Frame(canvas_pedidos)
canvas_pedidos.create_window((0, 0), window=frame_pedidos_scrollable, anchor='nw')

# Loop para adicionar informações de cada pedido
for i, pedido_id in enumerate(data_comptes['NUMÉRO_COMPTE']):
    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"Numéro Compte:", font=("Helvetica", 11, "bold"))
    label_pedido_info.grid(row=i, column=0, padx=5, sticky="w")

    pedido = data_comptes[data_comptes['NUMÉRO_COMPTE'] == pedido_id].iloc[0]
    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"{pedido_id}", font=("Helvetica", 11))
    label_pedido_info.grid(row=i, column=1, padx=5, sticky="w")

    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"Nom de la Pièce:", font=("Helvetica", 11, "bold"))
    label_pedido_info.grid(row=i, column=2, padx=5, sticky="w")

    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"{pedido['NOM_PIECE']}", font=("Helvetica", 11))
    label_pedido_info.grid(row=i, column=3, padx=5, sticky="w")

    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"Durée Totale:", font=("Helvetica", 11, "bold"))
    label_pedido_info.grid(row=i, column=4, padx=5, sticky="w")

    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"{pedido['DURÉE_TOTALE']}", font=("Helvetica", 11))
    label_pedido_info.grid(row=i, column=5, padx=5, sticky="w")

    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"Date de Livraison:", font=("Helvetica", 11, "bold"))
    label_pedido_info.grid(row=i, column=6, padx=5, sticky="w")

    label_pedido_info = tk.Label(frame_pedidos_scrollable, text=f"{pedido['DATE_LIVRAISON']}", font=("Helvetica", 11))
    label_pedido_info.grid(row=i, column=7, padx=5, sticky="w")
    
# Adicionar barra de rolagem
scrollbar_pedidos = tk.Scrollbar(frame_pedidos, orient="vertical", command=canvas_pedidos.yview)
scrollbar_pedidos.grid(row=1, column=5, sticky="ns")
canvas_pedidos.configure(yscrollcommand=scrollbar_pedidos.set)

# Configurar o peso das linhas e colunas para ocupar todo o espaço disponível
frame_pedidos.rowconfigure(1, weight=1)
frame_pedidos.columnconfigure(0, weight=1)
frame_pedidos.columnconfigure(1, weight=1)

# Atualizar o tamanho da janela quando o tamanho do canvas mudar
frame_pedidos_scrollable.update_idletasks()
canvas_pedidos.config(scrollregion=canvas_pedidos.bbox("all"))

# Frame para as informações de colaboradores (EMPLOYÉS)
frame_colaboradores = ttk.Frame(notebook)
notebook.add(frame_colaboradores, text="Affichage des employés")

# Adicionar o texto "Colaboradores"
label_colaboradores = tk.Label(frame_colaboradores, text="Employés", font=("Helvetica", 18))
label_colaboradores.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")  # Use columnspan para ocupar várias colunas

# Canvas para permitir rolagem
canvas_colaboradores = tk.Canvas(frame_colaboradores)
canvas_colaboradores.grid(row=1, column=0, columnspan=5, sticky="nsew")  # Atualizei aqui para ocupar 5 colunas

# Frame dentro do canvas
frame_colaboradores_scrollable = tk.Frame(canvas_colaboradores)
canvas_colaboradores.create_window((0, 0), window=frame_colaboradores_scrollable, anchor='nw')

# Loop para adicionar informações de cada colaborador
for i, colaborador_id in enumerate(data_employes['ID_EMPLOYÉ']):
    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"ID Employé:", font=("Helvetica", 11, "bold"))
    label_colaborador_info.grid(row=i, column=0, padx=5, sticky="w")

    colaborador = data_employes[data_employes['ID_EMPLOYÉ'] == colaborador_id].iloc[0]
    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"{colaborador_id}", font=("Helvetica", 11))
    label_colaborador_info.grid(row=i, column=1, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"Prénom:", font=("Helvetica", 11, "bold"))
    label_colaborador_info.grid(row=i, column=2, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"{colaborador['NOM']}", font=("Helvetica", 11))
    label_colaborador_info.grid(row=i, column=3, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"Poste:", font=("Helvetica", 11, "bold"))
    label_colaborador_info.grid(row=i, column=4, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"{colaborador['POSTE']}", font=("Helvetica", 11))
    label_colaborador_info.grid(row=i, column=5, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"Salaire:", font=("Helvetica", 11, "bold"))
    label_colaborador_info.grid(row=i, column=6, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"{colaborador['SALAIRE']}", font=("Helvetica", 11))
    label_colaborador_info.grid(row=i, column=7, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"Date d'Embauche:", font=("Helvetica", 11, "bold"))
    label_colaborador_info.grid(row=i, column=8, padx=5, sticky="w")

    label_colaborador_info = tk.Label(frame_colaboradores_scrollable, text=f"{colaborador['DATE_EMBAUCHE']}", font=("Helvetica", 11))
    label_colaborador_info.grid(row=i, column=9, padx=5, sticky="w")

# Adicionar barra de rolagem
scrollbar_colaboradores = tk.Scrollbar(frame_colaboradores, orient="vertical", command=canvas_colaboradores.yview)
scrollbar_colaboradores.grid(row=1, column=5, sticky="ns")
canvas_colaboradores.configure(yscrollcommand=scrollbar_colaboradores.set)

# Configurar o peso das linhas e colunas para ocupar todo o espaço disponível
frame_colaboradores.rowconfigure(1, weight=1)
frame_colaboradores.columnconfigure(0, weight=1)
frame_colaboradores.columnconfigure(1, weight=1)

# Atualizar o tamanho da janela quando o tamanho do canvas mudar
frame_colaboradores_scrollable.update_idletasks()
canvas_colaboradores.config(scrollregion=canvas_colaboradores.bbox("all"))

# Frame para as informações de candidatos (CANDIDATS)
frame_candidatos = ttk.Frame(notebook)
notebook.add(frame_candidatos, text="Affichage des candidats")

# Adicionar o texto "Candidatos"
label_candidatos = tk.Label(frame_candidatos, text="Candidats", font=("Helvetica", 18))
label_candidatos.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")  # Use columnspan para ocupar várias colunas

# Canvas para permitir rolagem
canvas_candidatos = tk.Canvas(frame_candidatos)
canvas_candidatos.grid(row=1, column=0, columnspan=5, sticky="nsew")  # Atualizei aqui para ocupar 5 colunas

# Frame dentro do canvas
frame_candidatos_scrollable = tk.Frame(canvas_candidatos)
canvas_candidatos.create_window((0, 0), window=frame_candidatos_scrollable, anchor='nw')

# Loop para adicionar informações de cada candidato
for i, candidato_id in enumerate(data_candidats['ID_CANDIDAT']):
    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"ID Candidat:", font=("Helvetica", 11, "bold"))
    label_candidato_info.grid(row=i, column=0, sticky="e", pady=2)

    candidato = data_candidats[data_candidats['ID_CANDIDAT'] == candidato_id].iloc[0]
    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"{candidato_id}", font=("Helvetica", 11))
    label_candidato_info.grid(row=i, column=1, sticky="w", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"Prénom:", font=("Helvetica", 11, "bold"))
    label_candidato_info.grid(row=i, column=2, sticky="e", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"{candidato['NOM']}", font=("Helvetica", 11))
    label_candidato_info.grid(row=i, column=3, sticky="w", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"Poste:", font=("Helvetica", 11, "bold"))
    label_candidato_info.grid(row=i, column=4, sticky="e", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"{candidato['POSTE']}", font=("Helvetica", 11))
    label_candidato_info.grid(row=i, column=5, sticky="w", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"Salaire Prevú:", font=("Helvetica", 11, "bold"))
    label_candidato_info.grid(row=i, column=6, sticky="e", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"{candidato['SALAIRE_PREVÚ']}", font=("Helvetica", 11))
    label_candidato_info.grid(row=i, column=7, sticky="w", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"Années d'Expérience:", font=("Helvetica", 11, "bold"))
    label_candidato_info.grid(row=i, column=8, sticky="e", pady=2)

    label_candidato_info = tk.Label(frame_candidatos_scrollable, text=f"{candidato['ANNÉE_EXPÉRIENCE']}", font=("Helvetica", 11))
    label_candidato_info.grid(row=i, column=9, sticky="w", pady=2)


# Adicionar barra de rolagem
scrollbar_candidatos = tk.Scrollbar(frame_candidatos, orient="vertical", command=canvas_candidatos.yview)
scrollbar_candidatos.grid(row=1, column=5, sticky="ns")
canvas_candidatos.configure(yscrollcommand=scrollbar_candidatos.set)

# Configurar o peso das linhas e colunas para ocupar todo o espaço disponível
frame_candidatos.rowconfigure(1, weight=1)
frame_candidatos.columnconfigure(0, weight=1)
frame_candidatos.columnconfigure(1, weight=1)

# Atualizar o tamanho da janela quando o tamanho do canvas mudar
frame_candidatos_scrollable.update_idletasks()
canvas_candidatos.config(scrollregion=canvas_candidatos.bbox("all"))

# Frame para as informações de pedidos vencendo (Pedidos com a menor data de entrega)
frame_pedidos_vencendo = ttk.Frame(notebook)
notebook.add(frame_pedidos_vencendo, text="Commandes Expirant")

# Adicionar o texto "Pedidos Vencendo"
label_pedidos_vencendo = tk.Label(frame_pedidos_vencendo, text="Commandes Expirant", font=("Helvetica", 18))
label_pedidos_vencendo.grid(row=0, column=0, columnspan=5, pady=10, sticky="nsew")  

# Canvas para permitir rolagem
canvas_pedidos_vencendo = tk.Canvas(frame_pedidos_vencendo)
canvas_pedidos_vencendo.grid(row=1, column=0, columnspan=5, sticky="nsew")  

# Frame dentro do canvas
frame_pedidos_vencendo_scrollable = tk.Frame(canvas_pedidos_vencendo)
canvas_pedidos_vencendo.create_window((0, 0), window=frame_pedidos_vencendo_scrollable, anchor='nw')

# Ordenar os pedidos pela data de entrega (do menor para o maior)
pedidos_ordenados_vencendo = data_comptes.sort_values(by='DATE_LIVRAISON')

# Pegar os 10 primeiros pedidos (os que têm a menor data de entrega)
top_10_pedidos_vencendo = pedidos_ordenados_vencendo.head(10)

# Loop para adicionar informações de cada pedido
for i, pedido_id in enumerate(top_10_pedidos_vencendo['NUMÉRO_COMPTE']):
    # Código semelhante ao loop anterior
    label_pedido_info = tk.Label(frame_pedidos_vencendo_scrollable, text=f"Numéro Compte: {pedido_id}, "
                                                                       f"Date de Livraison: {top_10_pedidos_vencendo['DATE_LIVRAISON'].iloc[i]}",
                                 font=("Helvetica", 11))
    label_pedido_info.grid(row=i, column=0, padx=5, sticky="w")

# Adicionar barra de rolagem
scrollbar_pedidos_vencendo = tk.Scrollbar(frame_pedidos_vencendo, orient="vertical", command=canvas_pedidos_vencendo.yview)
scrollbar_pedidos_vencendo.grid(row=1, column=5, sticky="ns")
canvas_pedidos_vencendo.configure(yscrollcommand=scrollbar_pedidos_vencendo.set)

# Configurar o peso das linhas e colunas para ocupar todo o espaço disponível
frame_pedidos_vencendo.rowconfigure(1, weight=1)
frame_pedidos_vencendo.columnconfigure(0, weight=1)
frame_pedidos_vencendo.columnconfigure(1, weight=1)

# Atualizar o tamanho da janela quando o tamanho do canvas mudar
frame_pedidos_vencendo_scrollable.update_idletasks()
canvas_pedidos_vencendo.config(scrollregion=canvas_pedidos_vencendo.bbox("all"))

# Botão para mostrar os 10 pedidos com a maior data de entrega
def mostrar_top_10_pedidos_mais_tarde():
    # Pegar os 10 últimos pedidos (os que têm a maior data de entrega)
    top_10_pedidos_mais_tarde = pedidos_ordenados_vencendo.tail(10)

    # Limpar o frame antes de adicionar novas informações
    for widget in frame_pedidos_vencendo_scrollable.winfo_children():
        widget.destroy()

    # Loop para adicionar informações de cada pedido
    for i, pedido_id in enumerate(top_10_pedidos_mais_tarde['NUMÉRO_COMPTE']):
        # Código semelhante ao loop anterior
        label_pedido_info = tk.Label(frame_pedidos_vencendo_scrollable, text=f"Numéro Compte: {pedido_id}, "
                                                                           f"Date de Livraison: {top_10_pedidos_mais_tarde['DATE_LIVRAISON'].iloc[i]}",
                                     font=("Helvetica", 11))
        label_pedido_info.grid(row=i, column=0, padx=5, sticky="w")

    # Atualizar o tamanho da janela quando o tamanho do canvas mudar
    frame_pedidos_vencendo_scrollable.update_idletasks()
    canvas_pedidos_vencendo.config(scrollregion=canvas_pedidos_vencendo.bbox("all"))

# Botão para mostrar os 10 pedidos com a maior data de entrega
btn_top_10_mais_tarde = tk.Button(frame_pedidos_vencendo, text="Top 10 Commandes en Retard", command=mostrar_top_10_pedidos_mais_tarde, font=("Helvetica", 16))
btn_top_10_mais_tarde.grid(row=2, column=0, columnspan=5, pady=10)


# Função para mostrar os 10 pedidos com a menor data de entrega
def mostrar_top_10_pedidos_mais_novos():
    # Pegar os 10 primeiros pedidos (os que têm a menor data de entrega)
    top_10_pedidos_mais_novos = pedidos_ordenados_vencendo.head(10)

    # Limpar o frame antes de adicionar novas informações
    for widget in frame_pedidos_vencendo_scrollable.winfo_children():
        widget.destroy()

    # Loop para adicionar informações de cada pedido
    for i, pedido_id in enumerate(top_10_pedidos_mais_novos['NUMÉRO_COMPTE']):
        # Código semelhante ao loop anterior
        label_pedido_info = tk.Label(frame_pedidos_vencendo_scrollable, text=f"Numéro Compte: {pedido_id}, "
                                                                           f"Date de Livraison: {top_10_pedidos_mais_novos['DATE_LIVRAISON'].iloc[i]}",
                                     font=("Helvetica", 11))
        label_pedido_info.grid(row=i, column=0, padx=5, sticky="w")

    # Atualizar o tamanho da janela quando o tamanho do canvas mudar
    frame_pedidos_vencendo_scrollable.update_idletasks()
    canvas_pedidos_vencendo.config(scrollregion=canvas_pedidos_vencendo.bbox("all"))
    
# Botão para mostrar os 10 pedidos com a menor data de entrega
btn_top_10_mais_novos = tk.Button(frame_pedidos_vencendo, text="Top 10 des Demmandes les Plus Récentes", command=mostrar_top_10_pedidos_mais_novos, font=("Helvetica", 16))
btn_top_10_mais_novos.grid(row=3, column=0, columnspan=5, pady=10)


# Iniciar o loop principal da interface gráfica
root.mainloop()
