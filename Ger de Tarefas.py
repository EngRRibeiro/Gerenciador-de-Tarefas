import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry

tasks = []  # lista de dicionário de tarefas

def add_task():
    task_name = task_name_var.get().strip()
    deadline = deadline_var.get().strip()
    priority = priority_var.get().strip()

    if task_name == '' or deadline == '' or priority == '':
        messagebox.showerror('Erro!', 'Informe todos os campos!')
        return

    task = {
        'name': task_name,
        'deadline': deadline,
        'priority': priority,
        'done': False
    }

    tasks.append(task)
    refresh_task_list()

def refresh_task_list():
    for item in task_tree.get_children():
        task_tree.delete(item)

    filter_option = filter_var.get().strip().lower()
    search = search_var.get().lower().strip()

    for idx, task in enumerate(tasks):
        if filter_option == 'concluídas' and not task['done']:
            continue
        if filter_option == 'pendentes' and task['done']:
            continue
        if search and search not in task['name'].lower():
            continue

        task_tree.insert('', 'end', iid=idx, values=(task['name'], task['deadline'], task['priority'], task['done']))

def mark_done():
    selected = task_tree.selection()[0]
    idx = int(selected)
    tasks[idx]['done'] = not tasks[idx]['done']
    refresh_task_list()

# Interface Gráfica
root = tk.Tk()
root.title('Gerenciador de Tarefas')

# Frame de entrada
entry = ttk.Frame(root)
entry.pack(padx=10, pady=10, fill='x')

task_name_var = tk.StringVar()
deadline_var = tk.StringVar()
priority_var = tk.StringVar()

filter_var = tk.StringVar(value='Todas')
search_var = tk.StringVar()

ttk.Label(entry, text='Informe o nome da nova tarefa').pack(anchor='w')
ttk.Entry(entry, textvariable=task_name_var).pack(fill='x')

ttk.Label(entry, text='Informe a prioridade').pack(anchor='w')
ttk.Combobox(entry, textvariable=priority_var, values=('Alta', 'Média', 'Baixa')).pack(fill='x')

ttk.Label(entry, text='Informe o vencimento').pack(anchor='w')
DateEntry(entry, textvariable=deadline_var, date_pattern='yyyy-MM-dd').pack(fill='x')

ttk.Button(entry, text='Adicionar Tarefa', command=add_task).pack(fill='x')

# Filtro
filter = ttk.Frame(root)
filter.pack(padx=10, pady=10, fill='x')

ttk.Label(filter, text='Filtrar por').pack(side='left')
filter_option = ttk.Combobox(filter, textvariable=filter_var, values=('Todas', 'Concluídas', 'Pendentes'))
filter_option.pack(side='left')
filter_option.bind('<<ComboboxSelected>>', lambda e: refresh_task_list())

ttk.Entry(filter, textvariable=search_var).pack(side='left')
ttk.Button(filter, text='Buscar!', command=refresh_task_list).pack(side='left')

# Tabela
task_tree = ttk.Treeview(root, columns=('Name', 'Deadline', 'Priority', 'Done'), show='headings')
task_tree.heading('Name', text='Tarefa')
task_tree.heading('Deadline', text='Vencimento')
task_tree.heading('Priority', text='Prioridade')
task_tree.heading('Done', text='Concluída')
task_tree.pack(fill='both', expand='yes')

# Botão de Conclusão
ttk.Button(root, text='Marcar como Concluida', command=mark_done).pack(fill='x')

refresh_task_list()
root.mainloop()
