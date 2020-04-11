from Tkinter import *
import tkinter as tk
from tkinter import messagebox
import mysql.connector


# Global variables
selected_index = 0
notes_ids = [] # store the ids because of listbox limitation :(


def onselect(evt):
    global selected_index
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    selected_index = index
    display_note(index, value)

# GUI CODES
window = tk.Tk()
window.title("Note Taking")

top_left = tk.Frame(window)
top_right = tk.Frame(window)


list_notes = Listbox(top_left, height=35, width=25, font = "Helvetica 14")
list_notes.bind('<<ListboxSelect>>', onselect)
list_notes.pack(side=tk.TOP, fill=tk.Y, padx=(10, 0), pady=(10, 10))

scroll_list = tk.Scrollbar(top_left)
scroll_list.pack(side=tk.RIGHT, fill=tk.Y)
scroll_list.config(command=list_notes.yview)
list_notes.config(yscrollcommand=scroll_list.set, cursor="hand2", background="#fff5e6", highlightbackground="grey", bd=0, selectbackground="#c9b922")

text_frame = tk.Frame(top_right)
note_title = tk.Entry(text_frame, width=52, font = "Helvetica 13")
note_title.insert(tk.END, "Title")
note_title.config(background="#F4F6F7", highlightbackground="grey")
note_title.pack(side=tk.TOP, pady=(0, 5), padx=(0, 10))


scroll_text = tk.Scrollbar(text_frame)
scroll_text.pack(side=tk.RIGHT, fill=tk.Y)
note_text = tk.Text(text_frame, height=34, width=53, font = "Helvetica 13")
note_text.pack(side=tk.TOP, fill=tk.Y, padx=(5, 0), pady=(0, 5))
note_text.tag_config("tag_your_message", foreground="blue")
note_text.insert(tk.END, "Notes")
scroll_text.config(command=note_text.yview)
note_text.config(yscrollcommand=scroll_text.set, background="#F4F6F7", highlightbackground="grey")

text_frame.pack(side=tk.TOP)

button_frame = tk.Frame(top_right)
photo_add = PhotoImage(file="add.gif")
photo_edit = PhotoImage(file="edit.gif")
photo_delete = PhotoImage(file="delete.gif")

btn_save = tk.Button(button_frame, text="Add", command=lambda : save_note(), image=photo_add)
btn_edit = tk.Button(button_frame, text="Update", command=lambda : update_note(), state=tk.DISABLED, image=photo_edit)
btn_delete = tk.Button(button_frame, text="Delete", command=lambda : delete_note(), state=tk.DISABLED, image=photo_delete)

btn_save.grid(row=0, column=1)
btn_edit.grid(row=0, column=2)
btn_delete.grid(row=0, column=3)

button_frame.pack(side=tk.TOP)


top_left.pack(side=tk.LEFT)
top_right.pack(side=tk.RIGHT)

# DATABASE FUNCTIONS STARTS
conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="")


def db_create_db(conn):
    mycursor = conn.cursor()
    query = "CREATE DATABASE IF NOT EXISTS db_notes"
    mycursor.execute(query)


def db_create_table(conn):
    db_create_db(conn)
    conn.database = "db_notes"
    mycursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS tb_notes (" \
          "note_id INT AUTO_INCREMENT PRIMARY KEY, " \
          "title VARCHAR(255) NOT NULL, " \
          "note VARCHAR(2000) NOT NULL)"
    mycursor.execute(query)


def db_insert_note(conn, title, note):
    conn.database = "db_notes"
    mycursor = conn.cursor()
    query = "INSERT INTO tb_notes (title, note) VALUES (%s, %s)"
    val = (title, note)
    mycursor.execute(query, val)
    conn.commit()
    return mycursor.lastrowid


def db_select_all_notes(conn):
    conn.database = "db_notes"
    query = "SELECT * from tb_notes"
    mycursor = conn.cursor()
    mycursor.execute(query)
    return mycursor.fetchall()


def db_select_specific_note(conn, note_id):
    conn.database = "db_notes"
    mycursor = conn.cursor()
    mycursor.execute("SELECT title, note FROM tb_notes WHERE note_id = " + str(note_id))
    return mycursor.fetchone()


def db_update_note(conn, title, note, note_id):
    conn.database = "db_notes"
    mycursor = conn.cursor()
    query = "UPDATE tb_notes SET title = %s, note = %s WHERE note_id = %s"
    val = (title, note, note_id)
    mycursor.execute(query, val)
    conn.commit()


def db_delete_note(conn, note_id):
    conn.database = "db_notes"
    mycursor = conn.cursor()
    query = "DELETE FROM tb_notes WHERE note_id = %s"
    adr = (note_id,)
    mycursor.execute(query, adr)
    conn.commit()


def init(conn):
    db_create_db(conn)  # create database if not exist
    db_create_table(conn)  # create table if not exist

    # select data
    notes = db_select_all_notes(conn)

    for note in notes:
        list_notes.insert(tk.END, note[1])
        notes_ids.append(note[0])  # save the id

init(conn)

def save_note():
    global conn
    title = note_title.get()

    if len(title) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the note title")
        return

    note = note_text.get("1.0", tk.END)
    if len(note.rstrip()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the notes")
        return

    # Check if title exist
    title_exist = False
    existing_titles = list_notes.get(0, tk.END)

    for t in existing_titles:
        if t == title:
            title_exist = True
            break

    if title_exist is True:
        tk.messagebox.showerror(title="ERROR!!!", message="Note title already exist. Please choose a new title")
        return

    # save in database
    inserted_id = db_insert_note(conn, title, note)
    print("Last inserted id is: " + str(inserted_id))

    # insert into the listbox
    list_notes.insert(tk.END, title)

    notes_ids.append(inserted_id)  # save notes id

    # clear UI
    note_title.delete(0, tk.END)
    note_text.delete('1.0', tk.END)


def update_note():
    global selected_index, conn

    title = note_title.get()

    if len(title) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the note title")
        return

    note = note_text.get("1.0", tk.END)
    if len(note.rstrip()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter the notes")
        return

    note_id = notes_ids[selected_index]  # get the id of the selected note

    # save in database
    db_update_note(conn, title, note, note_id)

    # update list_note
    list_notes.delete(selected_index)
    list_notes.insert(selected_index, title)

    # clear UI
    note_title.delete(0, tk.END)
    note_text.delete('1.0', tk.END)


def delete_note():
    global selected_index, conn, notes_ids
    title = note_title.get()
    notes = note_text.get("1.0", tk.END)

    print("Selected note is: " + str(selected_index))

    if len(title) < 1 or len(notes.rstrip()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="Please select a note to delete")
        return

    result = tk.messagebox.askquestion("Delete", "Are you sure you want to delete?", icon='warning')

    if result == 'yes':
        # remove notes from db
        note_id = notes_ids[selected_index]
        db_delete_note(conn, note_id)
        del notes_ids[selected_index]

        # remove from UI
        note_title.delete(0, tk.END)
        note_text.delete('1.0', tk.END)
        list_notes.delete(selected_index)


def display_note(index, value):
    global notes_ids, conn
    # clear the fields
    note_title.delete(0, tk.END)
    note_text.delete('1.0', tk.END)

    note = db_select_specific_note(conn, notes_ids[index])

    # insert data
    note_title.insert(tk.END, note[0])
    note_text.insert(tk.END, note[1])

    btn_delete.config(state=tk.NORMAL)
    btn_edit.config(state=tk.NORMAL)

window.mainloop()





