# !/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import webbrowser
import tkinter as tk
from PIL import ImageTk
from tkinter import ttk, messagebox


class MainWindow:
    def __init__(self, root):
        root.title('Tkinter Books')
        root.geometry("900x500")
        root.resizable(0, 0)

        root.update_idletasks()
        width = root.winfo_width()
        frm_width = root.winfo_rootx() - root.winfo_x()
        win_width = width + 2 * frm_width
        height = root.winfo_height()
        titlebar_height = root.winfo_rooty() - root.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = root.winfo_screenwidth() // 2 - win_width // 2
        y = root.winfo_screenheight() // 2 - win_height // 2
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        root.deiconify()

        wrapper_books = tk.LabelFrame(root, text="Listado de Libros")
        wrapper_books.pack(fill="both", expand="yes", padx=20, pady=100)
        self.root = root
        self.treeXScroll = ttk.Scrollbar(wrapper_books, orient="vertical")
        self.treeXScroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.my_tree_cate = ttk.Treeview(wrapper_books, columns=(1, 2, 3, 4, 5, 6), show="headings", height="10",
                                         yscrollcommand=self.treeXScroll.set)
        self.my_tree_cate.pack(fill=tk.BOTH)
        self.treeXScroll.config(command=self.my_tree_cate.yview)
        self.my_tree_cate.heading(1, text="ISBN")
        self.my_tree_cate.column(1, minwidth=120, width=120, stretch=tk.NO)
        self.my_tree_cate.heading(2, text="TITULO")
        self.my_tree_cate.column(2, minwidth=350, width=350, stretch=tk.NO)
        self.my_tree_cate.heading(3, text="SUBTITULO")
        self.my_tree_cate.column(3, minwidth=400, width=400, stretch=tk.NO)
        self.my_tree_cate.heading(4, text="PRECIO")
        self.my_tree_cate.heading(5, text="IMAGEN")
        self.my_tree_cate.heading(6, text="URL")

        self.my_tree_cate.bind('<Double 1>', self.list_get)
        self.main_books(root)

    def main_books(self, root):
        self.search = tk.StringVar()
        self.page = tk.StringVar()
        label_search = tk.Label(root, text="Buscador:", font=("Arial", 12)).place(x=15, y=20)
        entry_search = tk.Entry(root, width=50, textvariable=self.search).place(x=100, y=20)
        label_page = tk.Label(root, text="Pagina:", font=("Arial", 12)).place(x=530, y=20)
        entry_page = tk.Entry(root, width=10, textvariable=self.page).place(x=590, y=20)
        button_search = tk.Button(root, text="Buscar", font=("Arial", 12), command=lambda :self.list_search(self.page.get())).place(x=700, y=15)
        button_edit = tk.Button(root, text="Ver Libro", font=("Arial", 12), command=self.view_books).place(x=20, y=55)


        button_next = tk.Button(root, text="Next-Page", font=("Arial", 12), command=lambda :self.list_search(str(1+1))).place(x=530, y=355)
        button_prev = tk.Button(root, text="Prev-Page", font=("Arial", 12), command=lambda :self.list_search(str(1))).place(x=230, y=355)

    def list_search(self,page=1):
        search_list = self.search.get()
        try:
            url = "https://api.itbook.store/1.0/search/" + search_list.lower()+ "/"+page
            response = requests.get(url)
            if response.status_code == 200:
                payload = response.json()
                self.books = payload.get('books', [])
                total = payload.get('total')
                if self.books:
                    lista = []
                    messagebox.showinfo(title="Busqueda Completada", message='Registros encontrados')
                    for book in self.books:
                        tuple = (
                            book['isbn13'], book['title'], book['subtitle'], book['price'], book['image'], book['url'])
                        lista.append(tuple)
                    self.list_update(lista)
                else:
                    messagebox.showerror("Error", 'Registros no encontrados')
            else:
                messagebox.showerror("Error", 'Conexion no estable')
        except requests.exceptions.ConnectionError as error:
            messagebox.showerror("Error", 'Conexion no estable')

    def list_update(self, rows):
        self.my_tree_cate.delete(*self.my_tree_cate.get_children())
        for i in rows:
            self.my_tree_cate.insert('', 'end', values=i)

    def list_get(self, event):
        row_id = self.my_tree_cate.identify_row(event.y)
        item = self.my_tree_cate.item(self.my_tree_cate.focus())
        try:
            self.isbn_13.set(item['values'][0])
            self.title.set(item['values'][1])
            self.subtitle.set(item['values'][2])
            self.price.set(item['price'][3])
            self.url.set(item['values'][5])
        except AttributeError as error:
            pass

    def view_books(self):
        try:
            self.my_tree_cate.item(self.my_tree_cate.selection())['values'][0]
            self.view_book = tk.Toplevel()
            self.view_book.title('Libro')
            self.view_book.geometry("1000x450")
            self.view_book.update_idletasks()
            width = self.view_book.winfo_width()
            frm_width = self.view_book.winfo_rootx() - self.view_book.winfo_x()
            win_width = width + 2 * frm_width
            height = self.view_book.winfo_height()
            titlebar_height = self.view_book.winfo_rooty() - self.view_book.winfo_y()
            win_height = height + titlebar_height + frm_width
            x = self.view_book.winfo_screenwidth() // 2 - win_width // 2
            y = self.view_book.winfo_screenheight() // 2 - win_height // 2
            self.view_book.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            self.view_book.deiconify()

            self.isbn_13 = tk.StringVar()
            self.title = tk.StringVar()
            self.subtitle = tk.StringVar()
            self.price = tk.StringVar()
            self.url = tk.StringVar()

            self.isbn_13.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][0])
            self.title.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][1])
            self.subtitle.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][2])
            self.price.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][3])
            self.url.set(self.my_tree_cate.item(self.my_tree_cate.selection())['values'][5])

            label_title = tk.Label(self.view_book, font=("Arial", 15), textvariable=self.title).place(x=150, y=0)
            label_isbn13 = tk.Label(self.view_book, font=("Arial", 12), textvariable=self.isbn_13).place(x=20, y=90)
            label_price = tk.Label(self.view_book, font=("Arial", 12), textvariable=self.price).place(x=20, y=30)
            label_subtitle = tk.Label(self.view_book, font=("Arial", 12), textvariable=self.subtitle,
                                      justify=tk.LEFT).place(x=20, y=50)
            open_url = tk.Button(self.view_book, text='url de libro', command=lambda: self.open_url(
                self.my_tree_cate.item(self.my_tree_cate.selection())['values'][5])).place(x=20, y=200)
            self.open_img()
        except IndexError as e:
            messagebox.showerror("Error", 'Error! seleciona un libro')

    @staticmethod
    def open_url(url):
        webbrowser.open(url)

    def dowloand_img(self):
        try:
            url_imagen = self.my_tree_cate.item(self.my_tree_cate.selection())['values'][4]
            nombre_local_imagen = "image/default.png"
            imagen = requests.get(url_imagen).content
            with open(nombre_local_imagen, 'wb') as handler:
                handler.write(imagen)
        except requests.exceptions.ConnectionError as error:
            messagebox.showerror("Error", 'No se pudo descargar la imagen')

    def open_img(self):
        self.dowloand_img()

        img = ImageTk.PhotoImage(file="image/default.png")
        panel = tk.Label(self.view_book, image=img)
        panel.image = img
        panel.pack(side="right")


if __name__ == '__main__':
    main = tk.Tk()
    window = MainWindow(main)
    main.mainloop()
