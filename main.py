import io
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tkinter import filedialog

df=None

def load_csv():
    global df
    try:
        file_path = filedialog.askopenfilename(title="Sélectionner un fichier")
        df=pd.read_csv(file_path)
        # Create a StringIO buffer to capture the output of df.info()
        buffer = io.StringIO()
        df.info(buf=buffer)
        info = buffer.getvalue()
        
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace('^Col\d+', '', regex=True).str.strip()
        combobox1['values'] = df.columns.tolist()
        combobox2['values'] = df.columns.tolist()
        
        
        return f"File loaded successfully!\n\n{info}"
    except Exception as e:
        return f"Error: {e}"
    
#Titanic-Dataset.csv

def visualization():
    global df
    try :
        if df is None:
            raise ValueError("No CSV file loaded")
        
        var1=combobox1.get()
        var2=combobox2.get()
        chart=combobox3.get()
        
        if (df[var1].isnull().sum()!=0):
            df[var1]=df[var1].fillna(df[var1].mean())
            df[var1]=df[var1].round().astype(int)
            
        if (df[var2].isnull().sum()!=0):
            df[var2]=df[var2].fillna(df[var2].mean())
            df[var2]=df[var2].round().astype(int)
            
        df.drop_duplicates()
        
        if chart=='Line Plot': #Visualizing continuous data over an interval
            plt.plot(df[var1], df[var2])
        elif chart=='Bar Chart': #Comparing categorical data 
            df.groupby(var1)[var2].mean().plot(kind='bar',color='pink')
            #df.plot(x=var2, y=var1, kind='bar')
        
        elif chart=='Histogram': #Showing the distribution of a numerical variable.
            df.groupby(var1)[var2].plot(kind='hist', alpha=0.5, label=var1, bins=5)
            #df[var2].plot(kind='hist', alpha=0.5, label=var2, bins=5)
            
        elif chart=='Scatter Plot' : #Visualizing the relationship between two continuous variables.
            df.plot(x=var1, y=var2, kind='scatter')
            
        elif chart=='Pie Chart': #Showing proportions of a whole.
            df.plot(kind='pie', y=var1)
            #df.groupby('AgeGroup')['Survived'].mean().plot(kind='pie')
            
        elif chart=='Box Plot': #Distribution of continuous data with quartiles and outliers.
            df.select_dtypes(include=['numbers']).plot(kind='box')
            
        else:
            raise ValueError("Unknown chart type selected")
         
        '''   
        elif chart=='Heatmap' : #Displaying matrix-like data where the individual values are represented as colors.
            sns.heatmap(df.corr(), annot=True)
        '''
            
        plt.title(var2+" selon "+var1)
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.xticks(rotation=45)
        plt.legend() 
        plt.show()

    except Exception as e:
        showinfo(title='Error', message=f"Error: {e}")
       
def corrolation():
    global df
    try:
        if df is None:
            raise ValueError("No CSV file loaded")

        correlation_matrix = df.select_dtypes(include=['number']).corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title("Correlation Heatmap")
        plt.show()

    except Exception as e:
        showinfo(title='Error', message=f"Error: {e}")
        
def button_clicked():
    msg=load_csv()
    showinfo(title='Information', message=msg)
    
def button_visualization_clicked():
    visualization()
    
def button_corrolation_clicked():
    corrolation()
    
    
win=tk.Tk()
win.geometry("350x400")
win.title("data analysis dashboard")
label1=tk.Label(win,text="analysis of dataset varaiables : ")
label1.pack()
label2=tk.Label(win,text="enter csv file : ")
label2.pack()
button1=ttk.Button(win,text="load csv file",command=button_clicked)
button1.pack()
button4=ttk.Button(win,text="show corrolation",command=button_corrolation_clicked)
button4.pack(pady=20)
label3=tk.Label(win,text="choose two variables to analyse : ")
label3.pack()
combobox1=ttk.Combobox(win,values=[])
combobox1.pack()
combobox2=ttk.Combobox(win,values=[])
combobox2.pack()
label4=tk.Label(win,text="choose chart type : ")
label4.pack()
combobox3=ttk.Combobox(win,values=['Line Plot','Bar Chart','Histogram','Scatter Plot','Pie Chart','Box Plot'])
combobox3.pack()
button2=ttk.Button(win,text="visualize",command=button_visualization_clicked)
button2.pack(pady=20)
try:
    win.mainloop()
except Exception as e:
    print(f"Error starting Tkinter: {e}")


