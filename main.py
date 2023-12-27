import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
import re


# Подключение к MongoDB
client = MongoClient('localhost', 27017)
db = client['project_management']


class Application(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Менеджер проектов")
        self.geometry("900x800")

        self.tabControl = ttk.Notebook(self)

        # Вкладка "Поручения"
        self.tab_assignments = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_assignments, text="Поручения")
        self.create_assignments_tab()

        # Вкладка "Работники"
        self.tab_employees = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_employees, text="Работники")
        self.create_employees_tab()

        # Вкладка "Проекты"
        self.selected_assignments = []
        self.selected_employees = []
        self.tab_projects = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab_projects, text="Проекты")
        self.create_projects_tab()

        self.tabControl.pack(expand=1, fill="both")

        self.display_all_records("assignments", db.assignments.find())
        self.display_all_records("employees", db.employees.find())
        self.display_all_records("projects", db.projects.find())

    def create_assignments_tab(self):
        # Создание поручения
        frame_assignment_creation = ttk.LabelFrame(self.tab_assignments, text="Создание поручения")
        frame_assignment_creation.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="w")

        self.label_cipher = tk.Label(frame_assignment_creation, text="Шифр:")
        self.label_cipher.grid(row=0, column=0, padx=5, pady=5)

        self.entry_cipher = tk.Entry(frame_assignment_creation)
        self.entry_cipher.grid(row=0, column=1, padx=5, pady=5)

        self.label_title = tk.Label(frame_assignment_creation, text="Название:")
        self.label_title.grid(row=1, column=0, padx=5, pady=5)

        self.entry_title = tk.Entry(frame_assignment_creation)
        self.entry_title.grid(row=1, column=1, padx=5, pady=5)

        self.label_effort = tk.Label(frame_assignment_creation, text="Трудоемкость:")
        self.label_effort.grid(row=2, column=0, padx=5, pady=5)

        self.entry_effort = tk.Entry(frame_assignment_creation)
        self.entry_effort.grid(row=2, column=1, padx=5, pady=5)

        self.label_deadline = tk.Label(frame_assignment_creation, text="Крайний срок:")
        self.label_deadline.grid(row=3, column=0, padx=5, pady=5)

        self.entry_deadline = tk.Entry(frame_assignment_creation)
        self.entry_deadline.grid(row=3, column=1, padx=5, pady=5)

        self.save_button = tk.Button(frame_assignment_creation, text="Сохранить", command=self.save_assignment)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Список поручений
        frame_assignment_list = ttk.LabelFrame(self.tab_assignments, text="Список поручений")
        frame_assignment_list.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="w")

        self.listbox_assignments = tk.Listbox(frame_assignment_list, width=80, height=10)
        self.listbox_assignments.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.label_search_cipher = tk.Label(frame_assignment_list, text="Поиск по шифру:")
        self.label_search_cipher.grid(row=6, column=0, padx=5, pady=5)

        self.entry_search_cipher = tk.Entry(frame_assignment_list)
        self.entry_search_cipher.grid(row=6, column=1, padx=5, pady=5)

        self.search_button_assignments = tk.Button(frame_assignment_list, text="Найти", command=lambda: self.search_records("assignments"))
        self.search_button_assignments.grid(row=6, column=2, padx=5, pady=5)

        self.label_messages_assignments = tk.Label(frame_assignment_list, text="", fg="green")
        self.label_messages_assignments.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def create_employees_tab(self):
        # Создание работников
        frame_employee_creation = ttk.LabelFrame(self.tab_employees, text="Создание работника")
        frame_employee_creation.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="w")

        self.label_id = tk.Label(frame_employee_creation, text="Идентификатор:")
        self.label_id.grid(row=0, column=0, padx=5, pady=5)

        self.entry_id = tk.Entry(frame_employee_creation)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        self.label_name = tk.Label(frame_employee_creation, text="ФИО:")
        self.label_name.grid(row=1, column=0, padx=5, pady=5)

        self.entry_name = tk.Entry(frame_employee_creation)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        self.label_position = tk.Label(frame_employee_creation, text="Должность:")
        self.label_position.grid(row=2, column=0, padx=5, pady=5)

        self.entry_position = tk.Entry(frame_employee_creation)
        self.entry_position.grid(row=2, column=1, padx=5, pady=5)

        self.save_button = tk.Button(frame_employee_creation, text="Сохранить", command=self.save_employee)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Список работников
        frame_employee_list = ttk.LabelFrame(self.tab_employees, text="Список работников")
        frame_employee_list.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="w")

        self.listbox_employees = tk.Listbox(frame_employee_list, width=80, height=10)
        self.listbox_employees.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.label_search_id = tk.Label(frame_employee_list, text="Поиск по идентификатору:")
        self.label_search_id.grid(row=5, column=0, padx=5, pady=5)

        self.entry_search_id = tk.Entry(frame_employee_list)
        self.entry_search_id.grid(row=5, column=1, padx=5, pady=5)

        self.search_button_employees = tk.Button(frame_employee_list, text="Найти", command=lambda: self.search_records("employees"))
        self.search_button_employees.grid(row=5, column=2, padx=5, pady=5)

        self.label_messages_employees = tk.Label(frame_employee_list, text="", fg="green")
        self.label_messages_employees.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def create_projects_tab(self):
        # Создание проекта
        frame_project_creation = ttk.LabelFrame(self.tab_projects, text="Создание проекта")
        frame_project_creation.grid(row=0, column=0, padx=10, pady=10, columnspan=3, sticky="w")

        self.label_project_name = tk.Label(frame_project_creation, text="Название проекта:")
        self.label_project_name.grid(row=0, column=0, padx=5, pady=5)

        self.entry_project_name = tk.Entry(frame_project_creation)
        self.entry_project_name.grid(row=0, column=1, padx=5, pady=5)

        self.label_project_date = tk.Label(frame_project_creation, text="Дата проекта:")
        self.label_project_date.grid(row=1, column=0, padx=5, pady=5)

        self.entry_project_date = tk.Entry(frame_project_creation)
        self.entry_project_date.grid(row=1, column=1, padx=5, pady=5)

        frame_assignments_project = ttk.LabelFrame(frame_project_creation, text="Выберите поручения")
        frame_assignments_project.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.checkbuttons_project_assignments = self.create_checkbuttons(frame_assignments_project, self.get_assignments_list())

        frame_employees_project = ttk.LabelFrame(frame_project_creation, text="Выберите работников")
        frame_employees_project.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.checkbuttons_project_employees = self.create_checkbuttons(frame_employees_project, self.get_employees_list())

        self.save_button = tk.Button(frame_project_creation, text="Сохранить", command=self.save_project)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Список проектов
        frame_project_list = ttk.LabelFrame(self.tab_projects, text="Список проектов")
        frame_project_list.grid(row=1, column=0, padx=10, pady=10, columnspan=3, sticky="w")

        self.listbox_projects = tk.Listbox(frame_project_list, width=120, height=10)
        self.listbox_projects.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.label_search_project_name = tk.Label(frame_project_list, text="Поиск по названию проекта:")
        self.label_search_project_name.grid(row=6, column=0, padx=5, pady=5)

        self.entry_search_project_name = tk.Entry(frame_project_list)
        self.entry_search_project_name.grid(row=6, column=1, padx=5, pady=5)

        self.search_button_projects = tk.Button(frame_project_list, text="Найти", command=lambda: self.search_records("projects"))
        self.search_button_projects.grid(row=6, column=2, padx=5, pady=5)

        self.label_messages_projects = tk.Label(frame_project_list, text="", fg="green")
        self.label_messages_projects.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    def create_checkbuttons(self, parent, items):
        checkbuttons = []
        for item in items:
            var = tk.BooleanVar(value=False)
            checkbutton = tk.Checkbutton(parent, text=item, variable=var)
            checkbutton.grid(sticky="w")
            checkbuttons.append((checkbutton, var))
        return checkbuttons

    def update_checkbuttons(self, checkbuttons, items):
        for cb, var in checkbuttons:
            cb.destroy()

        for item in items:
            var = tk.BooleanVar(value=False)
            checkbutton = tk.Checkbutton(checkbuttons[0][0].master, text=item, variable=var)
            checkbutton.grid(sticky="w")
            checkbuttons.append((checkbutton, var))

    def save_assignment(self):
        cipher = self.entry_cipher.get()
        title = self.entry_title.get()
        effort = self.entry_effort.get()
        deadline = self.entry_deadline.get()

        if cipher and title and effort and deadline:
            assignment_data = {
                "cipher": cipher,
                "title": title,
                "effort": effort,
                "deadline": deadline
            }
            db.assignments.insert_one(assignment_data)
            self.display_message("assignments", "Поручение сохранено в базе данных.", "green")
            self.display_all_records("assignments", db.assignments.find())
            self.clear_input_fields(["entry_cipher", "entry_title", "entry_effort", "entry_deadline"])
            self.update_checkbuttons(self.checkbuttons_project_assignments, self.get_assignments_list())
        else:
            self.display_message("assignments", "Заполните все поля перед сохранением.", "red")

    def save_employee(self):
        employee_id = self.entry_id.get()
        name = self.entry_name.get()
        position = self.entry_position.get()

        if employee_id and name and position:
            employee_data = {
                "employee_id": employee_id,
                "name": name,
                "position": position
            }
            db.employees.insert_one(employee_data)
            self.display_message("employees", "Работник сохранен в базе данных.", "green")
            self.display_all_records("employees", db.employees.find())
            self.clear_input_fields(["entry_id", "entry_name", "entry_position"])
            self.update_checkbuttons(self.checkbuttons_project_employees, self.get_employees_list())
        else:
            self.display_message("employees", "Заполните все поля перед сохранением.", "red")

    def save_project(self):
        project_name = self.entry_project_name.get()
        project_date = self.entry_project_date.get()
        project_assignments = [item[0]['text'] for item in self.checkbuttons_project_assignments if item[1].get()]
        project_employees = [item[0]['text'] for item in self.checkbuttons_project_employees if item[1].get()]

        if project_name and project_date:
            project_data = {
                "project_name": project_name,
                "project_date": project_date,
                "project_assignments": project_assignments,
                "project_employees": project_employees
            }
            db.projects.insert_one(project_data)
            self.display_message("projects", "Проект сохранен в базе данных.", "green")
            self.display_all_records("projects", db.projects.find())
            self.clear_input_fields(["entry_project_name", "entry_project_date"])

            for item in self.checkbuttons_project_assignments:
                item[1].set(False)
            for item in self.checkbuttons_project_employees:
                item[1].set(False)
        else:
            self.display_message("projects", "Заполните все поля перед сохранением.", "red")

    def get_assignments_list(self):
        assignments = db.assignments.find()
        return [assignment["title"] for assignment in assignments]

    def get_employees_list(self):
        employees = db.employees.find()
        return [employee["name"] for employee in employees]

    def display_message(self, tab_name, message, color):
        if tab_name == "assignments":
            self.label_messages_assignments.config(text=message, fg=color)
        elif tab_name == "employees":
            self.label_messages_employees.config(text=message, fg=color)
        elif tab_name == "projects":
            self.label_messages_projects.config(text=message, fg=color)

    def display_all_records(self, tab_name, results):
            self.clear_results(tab_name)
            for result in results:
                self.display_result(tab_name, result)

    def search_records(self, tab_name):
        search_text = ""

        if tab_name == "assignments":
            search_text = self.entry_search_cipher.get()
            if not search_text:
                results = db.assignments.find()
            else:
                regex = re.compile(re.escape(search_text), re.IGNORECASE)
                results = db.assignments.find({"cipher": {"$regex": regex}})

        elif tab_name == "employees":
            search_text = self.entry_search_id.get()
            if not search_text:
                results = db.employees.find()
            else:
                regex = re.compile(re.escape(search_text), re.IGNORECASE)
                results = db.employees.find({"employee_id": {"$regex": regex}})

        elif tab_name == "projects":
            search_text = self.entry_search_project_name.get()
            if not search_text:
                results = db.projects.find()
            else:
                regex = re.compile(re.escape(search_text), re.IGNORECASE)
                results = db.projects.find({"project_name": {"$regex": regex}})

        self.clear_results(tab_name)

        for result in results:
            self.display_result(tab_name, result)

    def clear_input_fields(self, field_names):
        for field_name in field_names:
            getattr(self, field_name).delete(0, tk.END)
         
    def clear_results(self, tab_name):
        if tab_name == "assignments":
            self.listbox_assignments.delete(0, tk.END)
        elif tab_name == "employees":
            self.listbox_employees.delete(0, tk.END)
        elif tab_name == "projects":
            self.listbox_projects.delete(0, tk.END)

    def display_result(self, tab_name, result):
        if tab_name == "assignments":
            self.listbox_assignments.insert(
                tk.END,
                f"[{result['cipher']}], "
                f"{result['title']}, "
                f"Трудозатрата: {result['effort']}, "
                f"Крайний срок: {result['deadline']}"
            )

        elif tab_name == "employees":
            self.listbox_employees.insert(
                tk.END,
                f"[{result['employee_id']}], "
                f"ФИО: {result['name']}, "
                f"Должность: {result['position']}"
            )

        elif tab_name == "projects":
            assignments = result.get('project_assignments', [])
            employees = result.get('project_employees', [])
            self.listbox_projects.insert(
                tk.END,
                f"[{result['project_name']}], "
                f"Крайний срок: {result['project_date']}, "
                f"Поручения: [{', '.join(assignments)}], "
                f"Работники: [{', '.join(employees)}]"
            )


if __name__ == "__main__":
    app = Application()
    app.mainloop()  