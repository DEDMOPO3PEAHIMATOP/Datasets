import tkinter
import os
import subprocess
from sys import platform
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter.ttk import Combobox
from PIL import ImageTk, Image


class MainContextMenu(tkinter.Menu):
    ''' Контекстное меню для внутренней области директории'''

    def __init__(self, main_window, parent):
        super(MainContextMenu, self).__init__(parent, tearoff=0)
        self.main_window = main_window
        self.add_command(label="Создать директорию", command=self.create_dir)
        self.add_command(label="Создать файл", command=self.create_file)

    def popup_menu(self, event):
        ''' функция для активации контекстного меню'''
        # если активны другие меню - отменяем их
        if self.main_window.file_context_menu:
            self.main_window.file_context_menu.unpost()
        if self.main_window.dir_context_menu:
            self.main_window.dir_context_menu.unpost()
        self.post(event.x_root, event.y_root)

    def create_dir(self):
        ''' функция для создания новой директории в текущей'''
        dir_name = simpledialog.askstring("Новая директория", "Введите название новой директории")
        if dir_name:
            command = "mkdir {0}".format(dir_name).split(' ')
            # выполняем команду отдельным процессом
            process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()
            # при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Операция невозможна!", "Отказано в доступе.")
            self.main_window.refresh_window()

    def create_file(self):
        ''' функция для создания нового файла в текущей директории'''
        dir_name = simpledialog.askstring("Новый файл", "Введите название нового файла")
        if dir_name:
            command = "touch {0}".format(dir_name).split(' ')
            # выполняем команду отдельным процессом
            process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            out, err = process.communicate()
            # при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Операция невозможна!", "Отказано в доступе.")
            self.main_window.refresh_window()

    def insert_to_dir(self):
        ''' функция для копирования файла или директории в текущую директорию'''
        copy_obj = self.main_window.buff
        to_dir = self.main_window.path_text.get()
        if os.path.isdir(self.main_window.buff):
            # выполняем команду отдельным процессом
            process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            if err:
                messagebox.showwarning("Операция невозможна!", err.decode("utf-8"))
        else:
            # выполняем команду отдельным процессом
            process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            # при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Операция невозможна!", err.decode("utf-8"))
        self.main_window.refresh_window()


class FileContextMenu(tkinter.Menu):
    def __init__(self, main_window, parent):
        super(FileContextMenu, self).__init__(parent, tearoff=0)
        self.main_window = main_window
        self.add_command(label="Открыть файл", command=self.open_file)
        self.add_separator()
        self.add_command(label="Копировать", command=self.copy_file)
        self.add_command(label="Переименовать", command=self.rename_file)
        self.add_separator()
        self.add_command(label="Удалить", command=self.delete_file)

    def work_file(self):
        pass

    def open_file(self):
        ''' функция для открытия файла сторонними программами'''
        ext = self.main_window.take_extention_file(self.main_window.selected_file)
        full_path = self.main_window.path_text.get() + self.main_window.selected_file

        if ext in ['txt', 'py', 'html', 'css', 'js']:
            if 'mousepad' in self.main_window.all_program:
                subprocess.Popen(["mousepad", full_path], start_new_session=True)
            else:
                self.problem_message()
        elif ext == 'pdf':
            if 'evince' in self.main_window.all_program:
                subprocess.run(["evince", full_path], start_new_session=True)
            else:
                self.problem_message()
        elif ext in ['png', 'jpeg', 'jpg', 'gif']:
            if 'ristretto' in self.main_window.all_program:
                subprocess.run(["ristretto", full_path], start_new_session=True)
            else:
                # self.problem_message()
                print(full_path)
                print(self.main_window.buff)
                # print(self.main_window.all_program)
                # subprocess.run(["gimp", full_path], start_new_session=True)
                return full_path
        else:
            self.problem_message()

    def problem_message(self):
        messagebox.showwarning("Проблема при открытии файла", 'Прости, но я не могу открыть этот файл')

    def copy_file(self):
        ''' функция для копирования файла'''
        # заносим полный путь к файлу в буффер
        self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
        self.main_window.refresh_window()

    def delete_file(self):
        ''' функция для удаления выбранного файла'''
        full_path = self.main_window.path_text.get() + self.main_window.selected_file
        # выполняем команду отдельным процессом
        process = subprocess.Popen(['rm', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        # при возникновении ошибки выводим сообщение
        if err:
            messagebox.showwarning("Проблема при удалении файла", 'У Вас нет прав для удаления данного файла')
        self.main_window.refresh_window()

    def rename_file(self):
        ''' функция для переименования выбранного файла'''
        new_name = simpledialog.askstring("Переименование файла", "Введите новое название файла")
        if new_name:
            old_file = self.main_window.path_text.get() + self.main_window.selected_file
            new_file = self.main_window.path_text.get() + new_name
            # выполняем команду отдельным процессом
            process = subprocess.Popen(['mv', old_file, new_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()
            # при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Проблема при переименовании файла",
                                       'У Вас нет прав для переименования данного файла')
            self.main_window.refresh_window()

    def popup_menu(self, event):
        ''' функция для активации контекстного меню'''
        self.post(event.x_root, event.y_root)
        # если активны другие меню - отменяем их
        if self.main_window.main_context_menu:
            self.main_window.main_context_menu.unpost()
        if self.main_window.dir_context_menu:
            self.main_window.dir_context_menu.unpost()
        self.main_window.selected_file = event.widget["text"]


class DirContextMenu(tkinter.Menu):
    def __init__(self, main_window, parent):
        super(DirContextMenu, self).__init__(parent, tearoff=0)
        self.main_window = main_window
        self.add_command(label="Переименовать", command=self.rename_dir)
        self.add_command(label="Копировать", command=self.copy_dir)
        self.add_separator()
        self.add_command(label="Удалить", command=self.delete_dir)

    def copy_dir(self):
        ''' функция для копирования директории'''
        self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
        self.main_window.refresh_window()

    def delete_dir(self):
        ''' функция для удаления выбранной директории'''
        full_path = self.main_window.path_text.get() + self.main_window.selected_file
        if os.path.isdir(full_path):
            # выполняем команду отдельным процессом
            process = subprocess.Popen(['rm', '-rf', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()
            # при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Проблема при удалении директории",
                                       'У Вас нет прав для удаления данной директории')
        self.main_window.refresh_window()

    def rename_dir(self):
        ''' функция для переименования выбранной директории'''
        new_name = simpledialog.askstring("Переименование директории", "Введите новое название директории")
        if new_name:
            old_dir = self.main_window.path_text.get() + self.main_window.selected_file
            new_dir = self.main_window.path_text.get() + new_name
            # выполняем команду отдельным процессом
            process = subprocess.Popen(['mv', old_dir, new_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()
            # при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Проблема при переименовании директории",
                                       'У Вас нет прав для переименования данной директории')
            self.main_window.refresh_window()

    def popup_menu(self, event):
        ''' функция для активации контекстного меню'''
        self.post(event.x_root, event.y_root)
        # если активны другие меню - отменяем их
        if self.main_window.main_context_menu:
            self.main_window.main_context_menu.unpost()
        if self.main_window.file_context_menu:
            self.main_window.file_context_menu.unpost()
        self.main_window.selected_file = event.widget["text"]


class MainWindow():
    ''' Класс основного окна'''

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Программа для создания датасета")
        # self.root.resizable(width=False, height=False)
        self.root.geometry('1500x650')

        self.buff = None
        if platform == "linux" or platform == "linux2":
            self.all_program = os.listdir('/usr/bin')
        elif platform == "darwin":
            self.all_program = os.listdir('/usr/bin')
        elif platform == "win32":
            self.all_program = os.listdir('C:\\')

        self.file_work = ''
        self.counter = 1

        # top frame
        self.title_frame = tkinter.Frame(self.root)
        self.title_frame.pack(fill='both', expand=True)

        self.lbl_result = tkinter.Label(self.title_frame, text="Папка для обработанных фото")
        self.lbl_result.pack(side='left')

        self.btn_result = tkinter.Button(self.title_frame, text="Выбрать!", command=self.results_dir)
        self.btn_result.pack(side='left')

        # work frame
        self.title_2_frame = tkinter.Frame(self.root)
        self.title_2_frame.pack(fill='both', expand=True)

        self.root.bind('<Button-1>', self.root_click)
        self.root.bind('<FocusOut>', self.root_click)

        self.lbl_view = tkinter.Label(self.title_2_frame, text="Выберите файл")
        self.lbl_view.pack(side='left')

        # back button
        self.back_button = tkinter.Button(self.title_2_frame, text="..", command=self.parent_dir, width=1, height=1)
        self.back_button.pack(side='left')

        # path entry
        self.path_text = tkinter.StringVar()
        self.path_text.set('/')
        self.current_path = tkinter.Entry(self.title_2_frame, textvariable=self.path_text, width=40, state='readonly')
        self.current_path.pack(side='left')

        self.lbl_animal = tkinter.Label(self.title_2_frame, text="Вид животного")
        self.lbl_animal.pack(side='left')
        self.text_animal = tkinter.Entry(self.title_2_frame, width=40)
        self.text_animal.pack(side='left')

        self.lbl_sex = tkinter.Label(self.title_2_frame, text="Пол животного")
        self.lbl_sex.pack(side='left')
        self.combo = Combobox(self.title_2_frame, width=5, state="readonly")
        self.combo['values'] = ('Нет', 'Самка', 'Самец')
        self.combo.current(0)
        self.combo.pack(side='left')

        self.lbl_age = tkinter.Label(self.title_2_frame, text="Возраст животного")
        self.lbl_age.pack(side='left')
        self.combo_age = Combobox(self.title_2_frame, width=11, state="readonly")
        self.combo_age['values'] = ('Нет', 'Детеныш', 'Половозрелый')
        self.combo_age.current(0)
        self.combo_age.pack(side='left')

        self.btn_work = tkinter.Button(self.title_2_frame, text="Обработать", command=self.work_dir)
        self.btn_work.pack(side='left')

        # main frame
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack(side='left')

        # scroll bar
        self.scrollbar_vert = tkinter.Scrollbar(self.main_frame, orient="vertical")
        self.scrollbar_vert.pack(side='right', fill='y')

        self.scrollbar_hor = tkinter.Scrollbar(self.main_frame, orient="horizontal")
        self.scrollbar_hor.pack(side='bottom', fill='x')

        # canvas
        self.canvas = tkinter.Canvas(self.main_frame, borderwidth=0, bg='white')
        self.inner_frame = tkinter.Frame(self.canvas, bg='white')

        # команды для прокрутки
        self.scrollbar_vert["command"] = self.canvas.yview
        self.scrollbar_hor["command"] = self.canvas.xview

        # настройки для canvas
        self.canvas.configure(yscrollcommand=self.scrollbar_vert.set, xscrollcommand=self.scrollbar_hor.set, width=400,
                              heigh=900)

        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # look frame
        self.look_frame = tkinter.Frame(self.root)
        self.look_frame.pack(side='left')

        # scroll bar
        self.scrollbar_look_vert = tkinter.Scrollbar(self.look_frame, orient="vertical")
        self.scrollbar_look_vert.pack(side='right', fill='y')

        self.scrollbar_look_hor = tkinter.Scrollbar(self.look_frame, orient="horizontal")
        self.scrollbar_look_hor.pack(side='bottom', fill='x')

        # canvas
        self.canvas_look = tkinter.Canvas(self.look_frame, borderwidth=0, bg='white')
        self.inner_frame_look = tkinter.Frame(self.canvas_look, bg='white')

        # команды для прокрутки
        self.scrollbar_look_vert["command"] = self.canvas_look.yview
        self.scrollbar_look_hor["command"] = self.canvas_look.xview

        # настройки для canvas
        self.canvas_look.configure(yscrollcommand=self.scrollbar_look_vert.set,
                                   xscrollcommand=self.scrollbar_look_hor.set,
                                   width=1400,
                                   heigh=900)

        self.canvas_look.pack(side='left', fill='both', expand=True)
        self.canvas_look.create_window((0, 0), window=self.inner_frame_look, anchor="nw")

        # отрисовываем содержимое лиректории
        self.dir_content()

    def work_dir(self):
        '''функция для перемещения обработанных файлов'''
        try:
            if self.file_work == '':
                messagebox.showerror('Не могу обработать', 'Не указан файл для перемещения')
            if self.text_animal.get() == '':
                messagebox.showerror('Не могу обработать', 'Не указан вид животного')
            if self.combo.get() == 'Нет':
                messagebox.showerror('Не могу обработать', 'Не указан пол животного')
            if self.combo_age.get() == 'Нет':
                messagebox.showerror('Не могу обработать', 'Не указан возраст животного')
            if self.file_work != '' and self.text_animal.get() != '' and self.combo.get() != 'Нет' and self.combo_age.get() != 'Нет':
                old_file = self.file_work

                new_name = f'{self.text_animal.get()}_{self.combo.get()}_{self.combo_age.get()}_{self.counter}'

                pass_name = f'{self.text_animal.get()}_{self.combo.get()}_{self.combo_age.get()}_{self.counter}.{self.take_extention_file(old_file)}'

                new_file = f'{self.folder_result_selected}/{new_name}.{self.take_extention_file(old_file)}'
                dir_list = os.listdir(self.folder_result_selected + '/')
                if pass_name in dir_list:
                    num = []
                    for file in dir_list:
                        if file.split('.')[0] == new_name:
                            num.append(file.split('.')[0].split('_')[-1])
                    self.counter = int(max(num)) + 1
                    new_name = f'{self.text_animal.get()}_{self.combo.get()}_{self.combo_age.get()}_{self.counter}'
                    new_file = f'{self.folder_result_selected}/{new_name}.{self.take_extention_file(old_file)}'
                    process = subprocess.Popen(['mv', old_file, new_file], stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)
                    output, err = process.communicate()
                else:
                    # выполняем команду отдельным процессом
                    process = subprocess.Popen(['mv', old_file, new_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    output, err = process.communicate()
                # при возникновении ошибки выводим сообщение
                if err:
                    messagebox.showwarning("Проблема при переименовании файла",
                                           'У Вас нет прав для переименования данного файла')
            self.refresh_window()
            self.dir_content()
        except:
            messagebox.showerror('Не могу обработать', 'Не указана папка для обработанных файлов')

    def results_dir(self):
        '''функция запоминания пути для сохранения обработанных файлов'''
        self.folder_result_selected = filedialog.askdirectory()
        self.lbl_result_dir = tkinter.Label(self.title_frame,
                                            text=f'Директория для перемещения файлов: {self.folder_result_selected}')
        self.lbl_result_dir.pack(side='left', padx=20, pady=30)
        return self.folder_result_selected

    def root_click(self, event):
        ''' функция для обработки события клика в root'''
        # если есть контекстные меню - отменяем
        if self.file_context_menu:
            self.file_context_menu.unpost()
        if self.main_context_menu:
            self.main_context_menu.unpost()
        if self.dir_context_menu:
            self.dir_context_menu.unpost()

    def dir_content(self):
        ''' функция для определения содержимого текущей директории'''
        # содержимое в текущей директории
        dir_list = os.listdir(self.path_text.get())
        path = self.path_text.get()

        if not dir_list:
            # общее контекстное меню
            self.main_context_menu = MainContextMenu(self, self.canvas)
            self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
            if self.buff:
                self.main_context_menu.add_command(label="Вставить", command=self.main_context_menu.insert_to_dir)
            self.inner_frame.bind('<Button-3>', self.main_context_menu.popup_menu)
            # контекстное меню для файлов
            self.file_context_menu = None
            # контекстное меню для директории
            self.dir_context_menu = None
            return None

        # общее контекстное меню
        self.main_context_menu = MainContextMenu(self, self.canvas)
        self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
        if self.buff:
            self.main_context_menu.add_command(label="Вставить", command=self.main_context_menu.insert_to_dir)
        # контекстное меню для файлов
        self.file_context_menu = FileContextMenu(self, self.inner_frame)
        # контекстное меню для директории
        self.dir_context_menu = DirContextMenu(self, self.inner_frame)

        i = 0
        flag = False

        for item in dir_list:

            if os.path.isdir(str(path) + item):
                # обрабатываем директории
                if os.access(str(path) + item, os.R_OK):
                    if not item.startswith('.'):
                        photo = tkinter.PhotoImage(file="img/folder.png")

                        icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                        icon.image = photo
                        icon.grid(row=i + 1, column=0)

                        folder_name = tkinter.Label(self.inner_frame, text=item, bg='white', cursor='hand1')
                        folder_name.bind("<Button-1>", self.move_to_dir)
                        # folder_name.bind("<Button-3>", self.dir_context_menu.popup_menu)
                        folder_name.grid(row=i + 1, column=1, sticky='w')
                else:
                    if not item.startswith('.'):
                        photo = tkinter.PhotoImage(file="img/folder_access.png")

                        icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                        icon.image = photo
                        icon.grid(row=i + 1, column=0)

                        folder_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                        folder_name.bind("<Button-1>", self.move_to_dir)
                        folder_name.grid(row=i + 1, column=1, sticky='w')

            else:
                # обрабатываем файлы
                if not item.startswith('.'):
                    ext = self.take_extention_file(item)
                    # фото, картинки
                    if ext in ['jpeg', 'jpg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']:

                        photo = tkinter.PhotoImage(file="img/photo.png")

                        icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                        icon.image = photo
                        icon.grid(row=i + 1, column=0)

                        file_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                        file_name.grid(row=i + 1, column=1, sticky='w')

                        # file_name.bind("<Button-3>", self.file_context_menu.popup_menu)

                        if not flag:
                            image = ImageTk.PhotoImage(Image.open(path + item))
                            self.file_work = path + item
                            icon_look = tkinter.Label(self.inner_frame_look, image=image, bg='white')
                            icon_look.image = image
                            icon_look.grid(row=1, column=0)

                            file_name_look = tkinter.Label(self.inner_frame_look, text=item, bg='white')
                            file_name_look.grid(row=1, column=1, sticky='w')

                            # file_name_look.bind("<Button-3>", self.file_context_menu.popup_menu)

                            flag = True

                    else:
                        # другие файлы
                        if os.access(str(path) + item, os.R_OK):
                            photo = tkinter.PhotoImage(file="img/file.png")

                            icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                            icon.image = photo
                            icon.grid(row=i + 1, column=0)

                            folder_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                            folder_name.grid(row=i + 1, column=1, sticky='w')

                            # folder_name.bind("<Button-3>", self.file_context_menu.popup_menu)

                        else:
                            photo = tkinter.PhotoImage(file="img/file_access.png")

                            icon = tkinter.Label(self.inner_frame, image=photo, bg='white')
                            icon.image = photo
                            icon.grid(row=i + 1, column=0)

                            folder_name = tkinter.Label(self.inner_frame, text=item, bg='white')
                            folder_name.grid(row=i + 1, column=1, sticky='w')
            i += 1

        # обновляем inner_frame и устанавливаем прокрутку для нового содержимого
        self.inner_frame.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.inner_frame_look.update()
        self.canvas_look.configure(scrollregion=self.canvas_look.bbox("all"))

    def move_to_dir(self, event):
        ''' функция для перехода в выбранную директорию'''
        elem = event.widget
        dir_name = elem["text"]
        fool_path = self.path_text.get() + dir_name
        if os.path.isdir(fool_path) and os.access(fool_path, os.R_OK):
            old_path = self.path_text.get()
            self.path_text.set(old_path + dir_name + '/')
            self.root_click('<Button-1>')
            self.refresh_window()

    def parent_dir(self):
        ''' функция для перемещения в родительскую директорию'''
        old_path = [i for i in self.path_text.get().split('/') if i]
        new_path = '/' + '/'.join(old_path[:-1])
        if not new_path:
            new_path = '/'
        if os.path.isdir(new_path):
            if new_path == '/':
                self.path_text.set(new_path)

            else:
                self.path_text.set(new_path + '/')
            self.refresh_window()

    def take_extention_file(self, file_name):
        ''' функция для получения расширения файла'''
        ls = file_name.split('.')
        if len(ls) > 1:
            return ls[-1]
        else:
            return None

    def refresh_window(self):
        ''' функция для обновления текущего отображения директорий/файлов'''
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.dir_content()
        self.canvas.yview_moveto(0)


def main():
    vin = MainWindow()
    vin.root.mainloop()


if __name__ == '__main__':
    main()
