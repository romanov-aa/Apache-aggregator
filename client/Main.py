import ttkbootstrap as ttk
import pandas as pd
from pandastable import Table
import requests


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def login():
    username = username_entry.get()
    password = password_entry.get()
    
    data = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post('http://158.160.63.79:5000/api/login', json=data)

        if response.status_code == 200:
            data = response.json()

            if data['status'] == "success":
                message_label.config(text="Успешная авторизация!")

                clear_frame(frame)
                show_filter_options()

                root.title("Выбор фильтров")
            else:
                message_label.config(text="Неверные имя пользователя или пароль!")
    except:
        message_label.config(text="API недоступен!")



def get_logs():
    checkbox_state_ip = checkbox_ip_var.get()
    checkbox_state_date = checkbox_date_var.get()

    if checkbox_state_ip == 1 and checkbox_state_date == 1:
        ip_entry_text = ip_entry.get()
        date_entry_text = date_entry.get()

        if ip_entry_text != '' and date_entry_text != '':
            if '-' in date_entry_text:
                date = date_entry_text.split('-')
                start_date = date[0]
                end_date = date[1]
                
                response = requests.get('http://158.160.63.79:5000/api/getLogsFilterAll', json={'ip': ip_entry_text, 'start_date': start_date, 'end_date': end_date})
                if response.status_code == 200:
                    data = response.json()

                    logs_window = ttk.Toplevel(root)
                    logs_window.title("Логи")
                    logs_window.geometry("900x830")

                    df = pd.DataFrame(data)
                    df = df[['id', 'access_date', 'ip_address', 'url']]
                    table = Table(logs_window, dataframe=df)
                    table.show()
            else:
                pass
        else:
            pass
    elif checkbox_state_ip == 1:
        ip_entry_text = ip_entry.get()

        if ip_entry_text != '':
            try:
                response = requests.get('http://158.160.63.79:5000/api/getLogsFilterIP', json={'ip': ip_entry_text})
                if response.status_code == 200:
                    data = response.json()

                    logs_window = ttk.Toplevel(root)
                    logs_window.title("Логи")
                    logs_window.geometry("900x830")

                    df = pd.DataFrame(data)
                    df = df[['id', 'access_date', 'ip_address', 'url']]
                    table = Table(logs_window, dataframe=df)
                    table.show()
            except:
                pass
        else:
            pass

    elif checkbox_state_date == 1:
        date_entry_text = date_entry.get()
        if date_entry_text != '':
            if '-' in date_entry_text:
                date = date_entry_text.split('-')
                start_date = date[0]
                end_date = date[1]

                try:
                    response = requests.get('http://158.160.63.79:5000/api/getLogsFilterDate', json={'start_date': start_date, 'end_date': end_date})
                    if response.status_code == 200:
                        data = response.json()

                        logs_window = ttk.Toplevel(root)
                        logs_window.title("Логи")
                        logs_window.geometry("900x830")

                        df = pd.DataFrame(data)
                        df = df[['id', 'access_date', 'ip_address', 'url']]
                        table = Table(logs_window, dataframe=df)
                        table.show()
                except:
                    pass    
            else:
                pass
        else:
            pass   
    else:
        response = requests.get('http://158.160.63.79:5000/api/getAllLogs')
    
        if response.status_code == 200:
            data = response.json()

            logs_window = ttk.Toplevel(root)
            logs_window.title("Логи")
            logs_window.geometry("900x830")

            df = pd.DataFrame(data)
            df = df[['id', 'access_date', 'ip_address', 'url']]
            table = Table(logs_window, dataframe=df)
            table.show()
        else:
            pass

def show_filter_options():
    filter_label = ttk.Label(frame, text="Выберите фильтры:")
    filter_label.pack()

    global checkbox_ip_var
    global checkbox_date_var
    checkbox_ip_var = ttk.IntVar()
    checkbox_date_var = ttk.IntVar()

    checkbox_ip = ttk.Checkbutton(frame, text="IP     ", variable=checkbox_ip_var, command=lambda: toggle_checkbox_ip(checkbox_ip_var))
    checkbox_ip.pack()

    checkbox_date = ttk.Checkbutton(frame, text="Дата", variable=checkbox_date_var , command=lambda: toggle_checkbox_date(checkbox_date_var))
    checkbox_date.pack()

    create_button = ttk.Button(root, text="Получить логи", command=get_logs)
    create_button.pack(pady=10, side="bottom")


def toggle_checkbox_ip(checkbox_ip_var):
    if checkbox_ip_var.get() == 1:
        global frame_filtre_ip
        frame_filtre_ip = ttk.Frame(frame)
        frame_filtre_ip.pack(pady=20)
        
        ip_label = ttk.Label(frame_filtre_ip, text="Введите IP")
        ip_label.pack()

        global ip_entry
        ip_entry = ttk.Entry(frame_filtre_ip)
        ip_entry.pack(pady=5)

        help_label = ttk.Label(frame_filtre_ip, text="        Пример:\n     172.10.166.60\n ТОЛЬКО 1 АДРЕС")
        help_label.pack()
    else:
        frame_filtre_ip.destroy()


def toggle_checkbox_date(checkbox_date_var):
    if checkbox_date_var.get() == 1:
        global frame_filtre_date
        frame_filtre_date = ttk.Frame(frame)
        frame_filtre_date.pack(pady=20)

        date_label = ttk.Label(frame_filtre_date, text="Введите Datе")
        date_label.pack()

        global date_entry
        date_entry = ttk.Entry(frame_filtre_date)
        date_entry.pack(pady=5)

        help_label = ttk.Label(frame_filtre_date, text="            Пример:\n  2023.06.19-2023.06.19")
        help_label.pack()
    else:
        frame_filtre_date.destroy()


root = ttk.Window(themename="darkly")

root.title("Авторизация")
root.geometry("600x530")
root.resizable(True, True)

frame = ttk.Frame(root)
frame.pack(pady=20)

username_label = ttk.Label(frame, text="Имя пользователя:")
username_label.pack()

username_entry = ttk.Entry(frame)
username_entry.pack(pady=5)

password_label = ttk.Label(frame, text="Пароль:")
password_label.pack()

password_entry = ttk.Entry(frame, show="*")
password_entry.pack(pady=5)

login_button = ttk.Button(frame, text="Войти", command=login)
login_button.pack(pady=10)

message_label = ttk.Label(frame, text="")
message_label.pack()

root.mainloop()