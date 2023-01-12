import pickle
import PIL.Image, PIL.ImageTk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from client import Client
from fill import gen_invoice

class Page(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.clients = []

    def show(self):

        "Reloads client list and displays frame"
        self.clients = client_loader()
        self.tkraise()

    def error_message(self, phrase=None):
        messagebox.showerror(message=phrase, title="Error")

    def enable_client_tree(self, frame, tree_select_func):
        client_tree_columns = ("name", "email", "phone")
        self.client_tree = ttk.Treeview(frame, columns=client_tree_columns, show="headings", selectmode="browse")
        self.client_tree.heading("name", text="Name")
        self.client_tree.heading("email", text="Email")
        self.client_tree.heading("phone", text="Phone")
        self.client_tree.grid(column=0, row=0)
        self.client_tree.bind("<<TreeviewSelect>>", tree_select_func)

        scroll = ttk.Scrollbar(frame, orient=VERTICAL, command=self.client_tree.yview)
        self.client_tree.configure(yscrollcommand=scroll.set)
        scroll.grid(column=1, row=0, sticky=(N, S))

    def destroy_and_release(self, window):

        """Destroy top level window and release to parent frame"""
        window.destroy()
        window.grab_release()

    def clear_entry_fields(self, frame):

        """Clear all entry (including text) fields within a frame"""
        for widget in frame.winfo_children():
            if widget.winfo_class() == "TEntry":
                widget.delete(0, END)
            elif widget.winfo_class() == "Text":
                widget.delete("1.0", END)


class PageGenInvoice(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        client_frame = ttk.Frame(self, padding="10")
        client_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        """Enable client tree"""
        self.enable_client_tree(client_frame, self.set_client)

        field_frame = ttk.Frame(self)
        field_frame.grid(column=0, row=1, sticky=(N, W, E, S))
        field_frame.columnconfigure(tuple(range(2)), weight=1)
        field_frame.rowconfigure(tuple(range(10)), weight=1)

        gen_frame = ttk.Frame(self, padding="0 15")
        gen_frame.grid(column=0, row=2, sticky=(N, S))

        ttk.Label(field_frame, text="Invoice Date").grid(column=0, row=0, sticky=(W, E))
        ttk.Label(field_frame, text="Invoice Number").grid(column=0, row=1, sticky=(W, E))
        ttk.Label(field_frame, text="Services Selected").grid(column=0, row=2, sticky=(W, E))
        ttk.Label(field_frame, text="Description of Work").grid(column=0, row=3, sticky=(W, E))
        ttk.Label(field_frame, text="Item Price").grid(column=0, row=4, sticky=(W, E))
        ttk.Label(field_frame, text="Item Quantity").grid(column=0, row=5, sticky=(W, E))
        ttk.Label(field_frame, text="Item Total").grid(column=0, row=6, sticky=(W, E))
        ttk.Label(field_frame, text="Deposit Paid").grid(column=0, row=7, sticky=(W, E))
        ttk.Label(field_frame, text="Paid Via").grid(column=0, row=8, sticky=(W, E))
        ttk.Label(field_frame, text="Balance").grid(column=0, row=9, sticky=(W, E))

        self.invoice_date = StringVar()
        invoice_date_entry = ttk.Entry(field_frame, width=64, textvariable=self.invoice_date)
        invoice_date_entry.grid(column=1, row=0)

        self.invoice_num = StringVar()
        invoice_num_entry = ttk.Entry(field_frame, width=64, textvariable=self.invoice_num)
        invoice_num_entry.grid(column=1, row=1)

        self.services = StringVar()
        services_entry = ttk.Entry(field_frame, width=64, textvariable=self.services)
        services_entry.grid(column=1, row=2)

        self.description = Text(field_frame, width=48, height=3, wrap="none")
        self.description.grid(column=1, row=3)

        self.item_price = StringVar()
        item_price_entry = ttk.Entry(field_frame, width=64, textvariable=self.item_price)
        item_price_entry.grid(column=1, row=4)

        self.item_quantity = StringVar()
        item_quantity_entry = ttk.Entry(field_frame, width=64, textvariable=self.item_quantity)
        item_quantity_entry.grid(column=1, row=5)

        self.item_total = StringVar()
        item_total_entry = ttk.Entry(field_frame, width=64, textvariable=self.item_total)
        item_total_entry.grid(column=1, row=6)

        self.deposit = StringVar()
        deposit_entry = ttk.Entry(field_frame, width=64, textvariable=self.deposit)
        deposit_entry.grid(column=1, row=7)

        self.paid_via = StringVar()
        paid_via_entry = ttk.Entry(field_frame, width=64, textvariable=self.paid_via)
        paid_via_entry.grid(column=1, row=8)

        self.balance = StringVar()
        balance_entry = ttk.Entry(field_frame, width=64, textvariable=self.balance)
        balance_entry.grid(column=1, row=9)

        gen_btn = ttk.Button(gen_frame, text="Generate", padding="0 5", command=self.generate_invoice)
        gen_btn.grid(column=0, row=0, sticky=(N, S), padx=10)

        clear_form_btn = ttk.Button(gen_frame, text="Clear Form", padding="0 5", command=lambda: self.clear_form(field_frame))
        clear_form_btn.grid(column=1, row=0, sticky=(N, S), padx=10)

        for child in field_frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)


    def show(self):
        super().show()

        """Delete all previous tree entries and reload updated client info"""
        entries = self.client_tree.get_children()
        for entry in entries:
            self.client_tree.delete(entry)
        for client in self.clients:
            self.client_tree.insert("", "end", values=(client.name, client.email, client.phone_number))


    def set_client(self, *args):

        client_selected = self.client_tree.item(self.client_tree.selection())

        """Work around a ValueError produced by an empty row selection when clearing the tree"""
        if len(client_selected["values"]) == 3:

            self.name, self.email, self.phone = client_selected["values"]


    def clear_form(self, frame, *arg):

        self.client_tree.selection_remove(self.client_tree.selection())
        self.clear_entry_fields(frame)


    def generate_invoice(self):

        """Throw an error message if no client has been selected"""
        if len(self.client_tree.selection()) == 0:
            return self.error_message("No client has been selected")

        gen_invoice(self.name,
            self.email,
            self.phone,
            self.invoice_date.get(),
            self.invoice_num.get(),
            self.services.get(),
            self.description.get("1.0", "end-1c"),
            self.item_price.get(),
            self.item_quantity.get(),
            self.item_total.get(),
            self.deposit.get(),
            self.paid_via.get(),
            self.balance.get(),)


class PageAddClient(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        self.field_frame = ttk.Frame(self, padding="0 15")
        self.field_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.save_frame = ttk.Frame(self)
        self.save_frame.grid(column=0, row=1, sticky=(N, S))

        ttk.Label(self.field_frame, text="Name").grid(column=0, row=0, sticky=(W, E))
        ttk.Label(self.field_frame, text="Email").grid(column=0, row=1, sticky=(W, E))
        ttk.Label(self.field_frame, text="Phone").grid(column=0, row=2, sticky=(W, E))

        self.name = StringVar()
        name_entry = ttk.Entry(self.field_frame, width=48, textvariable=self.name)
        name_entry.grid(column=1, row=0, sticky=W)

        self.email = StringVar()
        email_entry = ttk.Entry(self.field_frame, width=48, textvariable=self.email)
        email_entry.grid(column=1, row=1, sticky=W)

        self.phone = StringVar()
        phone_entry = ttk.Entry(self.field_frame, width=48, textvariable=self.phone)
        phone_entry.grid(column=1, row=2, sticky=W)

        self.save = ttk.Button(self.save_frame, text="Save", padding="0 5", command=self.save_and_reset)
        self.save.grid(column=0, row=0, sticky=(N, S))

        for child in self.field_frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def show(self):
        super().show()

        self.clear_entry_fields(self.field_frame)


    def save_and_reset(self):
        name = self.name.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        for client in self.clients:
            if client.name == name:
                return self.error_message("Name has already been assigned to an existing client")
        try:
            add_client(Client(name, email, phone))
        except ValueError:
            return self.error_message("One or more fields are missing")
        self.show()


class PageEditClient(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)

        client_frame = ttk.Frame(self, padding="10")
        client_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        """Enable client tree"""
        self.enable_client_tree(client_frame, self.set_client)

        self.field_frame = ttk.Frame(self, padding="0 15")
        self.field_frame.grid(column=0, row=1, sticky=(N, W, E, S))

        button_frame = ttk.Frame(self, padding="0 8")
        button_frame.grid(column=0, row=2, sticky=(N, S))

        ttk.Label(self.field_frame, text="Name").grid(column=0, row=0, sticky=(W, E))
        ttk.Label(self.field_frame, text="Email").grid(column=0, row=1, sticky=(W, E))
        ttk.Label(self.field_frame, text="Phone").grid(column=0, row=2, sticky=(W, E))

        self.name_var = StringVar()
        self.name_entry = ttk.Entry(self.field_frame, width=48, textvariable=self.name_var)
        self.name_entry.grid(column=1, row=0, sticky=W)

        self.email_var = StringVar()
        self.email_entry = ttk.Entry(self.field_frame, width=48, textvariable=self.email_var)
        self.email_entry.grid(column=1, row=1, sticky=W)

        self.phone_var = StringVar()
        self.phone_entry = ttk.Entry(self.field_frame, width=48, textvariable=self.phone_var)
        self.phone_entry.grid(column=1, row=2, sticky=W)

        self.save = ttk.Button(button_frame, text="Save", padding="0 5", command=self.save_and_reset)
        self.save.grid(column=0, row=0, sticky=(N, S), padx=10)

        self.delete = ttk.Button(button_frame, text="Delete Client", padding="0 5", command=self.are_you_sure_delete)
        self.delete.grid(column=1, row=0, sticky=(N, S), padx=10)

        for child in self.field_frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def set_client(self, *args):

        """Clear all entry fields"""
        self.clear_entry_fields(self.field_frame)

        client_selected = self.client_tree.item(self.client_tree.selection())

        """Work around a ValueError produced by an empty row selection when clearing the tree"""
        if len(client_selected["values"]) == 3:

            self.name, self.email, self.phone = client_selected["values"]

            self.name_entry.insert(0, self.name)
            self.email_entry.insert(0, self.email)
            self.phone_entry.insert(0, self.phone)
        else:
            return

    def show(self):
        super().show()

        """Clear all entry fields"""
        self.clear_entry_fields(self.field_frame)

        """Delete all previous tree entries and reload updated client info"""
        entries = self.client_tree.get_children()
        for entry in entries:
            self.client_tree.delete(entry)
        for client in self.clients:
            self.client_tree.insert("", "end", values=(client.name, client.email, client.phone_number))

    def save_and_reset(self):

        """Throw an error message if no client has been selected"""
        if len(self.client_tree.selection()) == 0:
            return self.error_message("No client has been selected")

        selected_client_index = self.find_client_by_name()

        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()

        """Check if the the new name matches to any other of an already existing client"""
        for client in (self.clients[:selected_client_index] + self.clients[selected_client_index + 1:]):
            if client.name == name:
                return self.error_message("Name has already been assigned to an existing client")

        try:
            self.clients[selected_client_index].edit(name, email, phone)
        except ValueError:
            return self.error_message("One or more fields are missing")

        update_clients(self.clients)
        self.show()

    def are_you_sure_delete(self):

        """Throw an error message if no client has been selected"""
        if len(self.client_tree.selection()) == 0:
            return self.error_message("No client has been selected")

        window = messagebox.askyesno(
            message=f"Are you sure you want to delete {self.name}?",
            icon="question",
            title="Delete")
        
        if window == True:
            self.delete_and_reset()

    def delete_and_reset(self):
        selected_client_index = self.find_client_by_name()
        del self.clients[selected_client_index]

        update_clients(self.clients)
        self.show()

    def find_client_by_name(self):

        """Find the location of the client that has been selected by name"""
        for i in range(len(self.clients)):
            if self.clients[i].name == self.name:
                return i


class MainView:
    def __init__(self, root):

        self.main_menu = ttk.Frame(root)
        self.main_menu.grid(column=0, row=0, sticky=(N, W, E, S))
        self.main_menu.columnconfigure(0, weight=1)
        self.main_menu.rowconfigure(tuple(range(4)), weight=1)

        self.page_container = ttk.Frame(root, padding="10")
        self.page_container.grid(column=0, row=0, sticky=(N, W, E, S))
        self.page_container.columnconfigure(0, weight=1)
        self.page_container.rowconfigure(tuple(range(2)), weight=1)

        btn_to_menu = ttk.Button(self.page_container, text="Return to Main Menu", padding="5 2", command=self.main_menu.tkraise)
        btn_to_menu.grid(column=0, row=0, sticky=W)

        p1 = PageGenInvoice(self.page_container)
        p1.grid(column=0, row=1, sticky=(N, W, E, S))

        p2 = PageAddClient(self.page_container)
        p2.grid(column=0, row=1, sticky=(N, W, E, S))

        p3 = PageEditClient(self.page_container)
        p3.grid(column=0, row=1, sticky=(N, W, E, S))

        """Main menu widgets"""

        image1 = PIL.Image.open("MGlogo2.png")
        self.logo = PIL.ImageTk.PhotoImage(image1)
        ttk.Label(self.main_menu, image=self.logo).grid(column=0, row=0)

        btn_gen_invoice = Button(self.main_menu,
            text="Generate Invoice",
            height=3,
            width=20,
            command=lambda: self.show_page(p1))
        btn_gen_invoice.grid(column=0, row=1, sticky=S)

        btn_add_client = Button(self.main_menu, 
            text="Add Client", 
            height=3,
            width=20,
            command=lambda: self.show_page(p2))
        btn_add_client.grid(column=0, row=2)

        btn_edit_client = Button(self.main_menu, 
            text="Edit Client",
            height=3,
            width=20,
            command=lambda: self.show_page(p3))
        btn_edit_client.grid(column=0, row=3, sticky=N)

        self.main_menu.tkraise()


    def show_page(self, page):
        self.page_container.tkraise()
        page.show()


def client_loader():

    """Load clients from a pickle file"""
    clients_file = "clients.pkl"
    clients = []
    try:
        file =  open(clients_file, "rb")
    except FileNotFoundError:
        return clients
    else:
        with file:
            while True:
                try:
                    clients.append(pickle.load(file))
                except EOFError:
                    return clients


def add_client(client):

    """Append a new client to clients file"""
    clients_file = "clients.pkl"
    with open(clients_file, "ab") as file:
        pickle.dump(client, file)


def update_clients(clients):

    """Update clients file"""
    clients_file = "clients.pkl"
    with open(clients_file, "wb") as file:
        for client in clients:
            pickle.dump(client, file)

def main():
    root = Tk()
    root.title("MenGar PR HQ")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    MainView(root)
    root.mainloop()


if __name__ == "__main__":
    main()