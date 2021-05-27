import tkinter as tk
from tkinter import ttk
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn.utils import shuffle


data = pd.read_csv(os.getcwd() + "/csv/data.csv",',',error_bad_lines=False)
data.dropna(inplace=True)

data = shuffle(data)
data.reset_index(drop=True,inplace=True)

X = data['password']

def words_to_char(inputs):
    characters=[]
    for i in inputs:
        characters.append(i)
    return characters

vectorizer=TfidfVectorizer(tokenizer=words_to_char)
vectorizer.fit_transform(X)

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.title_text = tk.Label(self, text="Gimme some text!")
        self.title_text.pack(pady=10)

        self.pass_text = tk.Label(self, text="Enter your text here")
        self.pass_text.pack(pady=10)

        self.pass_area = tk.Text(self, width= 18, height= 1, font=("Helvetica",16))
        self.pass_area.pack(pady=10)
        
        self.get_input = tk.Button(self, text= "OK", width=9, command = self.retrieve_input)
        self.get_input.pack(side="left",padx=35)

        self.quit = tk.Button(self, text="Cancel", width=9, command=self.master.destroy)
        self.quit.pack(side="right",padx=35, pady=10)

        self.out_area = tk.Text(self, width= 18, height= 1, font=("Helvetica",14),border=0,background="#F5F5F5")
        self.out_area.pack(pady=10)

    def retrieve_input(self):
        password = self.pass_area.get("1.0","end-1c")
        strength_map = {
            0: 'Weak',
            1: 'Moderate',
            2: 'Strong'
        }
        with open('model.pkl', 'rb') as f: 
            log_class = pickle.load(f)
        strength = log_class.predict(vectorizer.transform(np.array([password])))
        self.out_area.delete("1.0", tk.END)
        self.out_area.insert(tk.END, strength_map[strength[0]])

        
root = tk.Tk()
app = Application(master=root)
root.wm_title("Password Checking")
root.geometry("400x400")
root.configure(bg = '#696969')
app.mainloop() 