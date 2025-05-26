#coding:utf-8

from tkinter import *
from PIL import Image, ImageTk #Image
import matplotlib.pyplot as plt #Get the matplotlib library
from matplotlib.figure import Figure #Graphique
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Pour Canva qui affiche le graphique
from openpyxl import load_workbook #sauvegarde sur plusieur sheets (peut être pas nécessaire)
import datetime # date sous forme m/j/a h:m:s
import pandas as pd
import matplotlib.dates as mdates


# Page Accueil
window = Tk()
height = window.winfo_screenheight()
width = window.winfo_screenwidth()
window.geometry("%ix%i" %(width, height))
window.title("Buddget")
window.iconbitmap('coins.ico')

def verify(window2, ID_entry, PS_entry):
    identifiant = ID_entry.get() #récupère info entrée
    password = PS_entry.get()
    document = pd.read_excel('Database.xlsx', sheet_name="Compte") #lit le doc
    if identifiant in document['Identifiant'].values: #search if identifiant is in the document
        ligne = document[document['Identifiant']==identifiant] # lit la ligne qu'il faut 
        Info = ligne.to_dict('records')[0] # Info : toute la ligne d'information sur le compte 
        PS_ligne = str(Info['Mot de Passe']) # récupère le mot de passe de la ligne Info 
        if PS_ligne==password:
            #PAGE 3
            numeroCompte = int(Info['Numéro de compte']) #pas utile
            window2.destroy()
            open_secondary_window(identifiant)
        else:
            ID_entry.delete(0,END)
            PS_entry.delete(0,END) 
            false_=Label(window2, text="Identifiant ou mot de passe incorrect.", fg="red", font=("Verdana", 8))
            false_.place(x=width/2+50, y=350)
    else :
        ID_entry.delete(0,END)
        PS_entry.delete(0,END)
        false_=Label(window2, text="Identifiant ou mot de passe incorrect.", fg="red", font=("Verdana", 8))
        false_.place(x=width/2+50, y=350)

def connection():

    window.destroy()

    window2 = Tk()
    height = window2.winfo_screenheight()
    width = window2.winfo_screenwidth()
    window2.geometry("%ix%i" %(width, height))
    window2.title("Buddget")
    window2.iconbitmap('coins.ico')

    #rectangle
    canvas = Canvas(window2, width=width, height=150)
    canvas.pack()
    rectangle = canvas.create_rectangle(0, 0, width, 150, outline="orange", fill="orange")

    #titre
    titre = canvas.create_text(width/2, 70, text="Connection :", fill="white", font=("Verdana", 30, "bold"))
    canvas.pack()

    #image
    img = PhotoImage(file="famille2Orange.gif")
    image = Label(window2, image=img)
    image.place(x=width/4-275, y=200)

    #Contact
    contact = Label(window2, text= "Pour nous contacter : 07 64 83 21 55\nBuddget.cont@unilasalle.fr", justify="center")
    contact.place(x=3*width/4-100, y=600)

    #Nom d'utilisateur
    ID_label = Label(window2, text="Nom d'utilisateur : ", fg="black", font=("Verdana", 16, "bold"))
    ID_label.place(x=(width/2)+50, y=250)
    ID_entry = Entry(window2, width=40)
    ID_entry.place(x=width/2+300, y=259)

    #Mot de passe
    PS_label = Label(window2, text="Mot de Passe : ", fg="black", font=("Verdana", 16, "bold"))
    PS_label.place(x=(width/2)+100, y=300)
    PS_entry = Entry(window2, width=40, show="*")
    PS_entry.place(x=width/2+300, y=309)

    #Valider
    valider = Button(window2, text="Valider", font=("Noto Sans CJK KR", 15, "bold"), bd=0, bg="orange", fg="white", activebackground="white", activeforeground="orange", command=lambda :[verify(window2, ID_entry, PS_entry)])
    valider.place(x=width/1.355, y=400)

    window2.mainloop()

def creationUser(window3, Identifiant_entry, Password_entry, Solde_entry): 
    document = pd.read_excel('Database.xlsx', sheet_name="Compte") #lit l'excel
    previousNumber= document['Numéro de compte'].iloc[-1]#récupère la valeur de la dernière case
    numero = previousNumber +1 # Peut-être pas nécessaire 
    identifiant= str(Identifiant_entry.get())
    password = str(Password_entry.get())
    solde= float(Solde_entry.get())
    if not password:
        PS_empty = Label(window3, text="Tout les champs doivent être renseigné.", fg="red", font=("Noto Sans CJK KR", 8))
        PS_empty.place(x=width/2-150, y=490)
    else :
        if identifiant in document['Identifiant'].values : 
            ID_False = Label(window3, text = "Identifiant déjà prit.", fg="red", font=("Noto Sans CJK KR", 8))
            ID_False.place(x=width/2-150, y=520)
            Identifiant_entry.delete(0,END)
            Password_entry.delete(0,END)
            Solde_entry.delete(0,END)
        else :
            date = datetime.datetime.now()
            #Excel
            documentData = pd.read_excel('Database.xlsx', sheet_name="Data")
            DataCompte = pd.DataFrame({'Numéro de compte': [numero], 'Identifiant': [identifiant], 'Mot de Passe' :[password]}) #valeur à enregistrer 
            DataDonnes = pd.DataFrame({'Utilisateur':[identifiant], 'Dépenses':[0], 'Revenues':[0], 'Solde':[solde], 'Légende':['Initial'], 'Date':[date]})
            df_combined = document._append(DataCompte) #enregistre une nouvelle ligne 
            df_combined2 = documentData._append(DataDonnes)
            with pd.ExcelWriter('Database.xlsx') as writer :
                df_combined.to_excel(writer, sheet_name= "Compte", index=False)#nouvelle ligne sur la sheet Compte
                df_combined2.to_excel(writer, sheet_name= "Data", index = False)# Nouvelle ligne sur la sheet Data
            window3.destroy()
            open_secondary_window(identifiant)

def compteCreation():

    window.destroy()

    window3 = Tk()
    height = window3.winfo_screenheight()
    width = window3.winfo_screenwidth()
    window3.geometry("%ix%i" %(width, height))
    window3.title("Buddget")
    window3.iconbitmap('coins.ico')

    #Background
    canvabg = Canvas(window3, width=width, height = height, bd=0)
    canvabg.place(x=0, y=0)
    wbg=int(width*1)
    hbg = int(height*0.97)
    bg= Image.open("Background création compte.gif")
    resizedBG = bg.resize((wbg, hbg))
    newBG = ImageTk.PhotoImage(resizedBG)
    canvabg.create_image(0, 0, anchor=NW, image= newBG)
    
    #rectangle
    canvas = Canvas(window3, width=width, height=150, bd=0, bg="orange")
    canvas.place(x=0, y=0)
    
    #titre
    titre = canvas.create_text(width/2, 70, text="Créer un compte :", fill="white", font=("Verdana", 30, "bold"))
    canvas.pack()
        
    #Center rectangle
    canvaCenter = Canvas(window3, width=width/3, height=height-150)
    canvaCenter.place(x=width/3, y=152)

    #Identifiant
    Identifiant_label = Label(window3, text="Identifiant :", fg="black", font=("Noto Sans CJK KR", 20, "bold"))
    Identifiant_label.place(x=width/2-80, y=200)
    Identifiant_entry= Entry(window3, width=40)
    Identifiant_entry.place(x=width/2-130, y=250)

    #Mot de passe
    Password_label = Label(window3, text="Mot de passe :", fg="black", font=("Noto Sans CJK KR", 20, "bold"))
    Password_label.place(x=width/2-100, y=300)
    Password_entry = Entry(window3, width=40)
    Password_entry.place(x=width/2-130, y=350)

    #Solde
    Solde_label = Label(window3, text="Montant total :", fg="black", font=("Noto Sans CJK KR", 20, "bold"))
    Solde_label.place(x=width/2-100, y=400)
    Solde_entry = Entry(window3, width=40)
    Solde_entry.place(x=width/2-130, y=450)

    #Valider
    valider=Button(window3, text="Valider", fg="white", bg = "orange", activebackground="white", activeforeground="orange", font=("Noto Sans CJK KR", 15, "bold"), command=lambda :[creationUser(window3, Identifiant_entry, Password_entry, Solde_entry)], bd=0)
    valider.place(x=width/2-40, y=550)

    #Contact
    contact = Label(window3, text= "Pour nous contacter : 07 64 83 21 55\nBuddget.cont@unilasalle.fr", justify="center")
    contact.place(x=width/2-100, y=650)
    
    window3.mainloop()

#   FONCTIONS

    # Sauvegarde excel
def save_to_excel(expenses, benefits, previousSolde, description, identifiant):
    document = pd.read_excel('Database.xlsx', sheet_name="Data")
    date = datetime.datetime.now()# date sous forme m/j/a h:m:s
    new_data =pd.DataFrame({'Utilisateur':[identifiant], 'Dépenses': [expenses], 'Revenues': [benefits], 'Solde': [previousSolde], 'Légende':[description],  'Date':[date] })
    updatedDocument = pd.concat([document, new_data], ignore_index=True)
    with pd.ExcelWriter('Database.xlsx',engine='openpyxl', mode="a", if_sheet_exists='replace') as writer :
        updatedDocument.to_excel(writer, sheet_name= "Data", index=False)#nouvelle ligne sur la sheet data

    #Additionne des revenues

def revenue(description_entry_rev, revenue_ent, addi_label, solde_1, fina, listbox, identifiant):
    global previousSolde
    description = str(description_entry_rev.get())
    description_entry_rev.delete(0, END)
    addi = float(revenue_ent.get())
    if addi >= 0:    
        previousSolde = float(previousSolde + addi)
        addi_label['text'] = addi
        solde_1.config(text="{}".format(previousSolde))
        revenue_ent.delete(0, END)
        fina['text'] = "Votre solde est maintenant : {} €".format(previousSolde)
        save_to_excel(0, addi, previousSolde, description, identifiant)  # Save revenue to Excel
        listbox.insert(END, f"Revenu: {addi} € - {description}") # Display on the bos too
    else : 
        addi_label['text'] = "Entrer une valeur numérique"
        revenue_ent.delete(0, END)

    #Calcul pour les dépenses

def depense(description_entry_dep, depense_ent, minus_label, solde_1, fina, listbox, identifiant):
    global previousSolde
    description = str(description_entry_dep.get())
    description_entry_dep.delete(0, END)
    try:  
        minus = float(depense_ent.get())
        previousSolde -= minus
        minus_label['text'] = minus
        solde_1.config(text="{}".format(previousSolde))
        depense_ent.delete(0,END)
        fina['text'] = "Votre solde est maintenant : {} €".format(previousSolde)
        save_to_excel(minus, 0, previousSolde, description, identifiant)  # Save expense to Excel
        listbox.insert(END, f"Dépense: {minus} € - {description}") # Display on the box
    except ValueError:
        minus_label['text'] = "Entrer une valeur numérique"
        depense_ent.delete(0, END)
        
#Modification de la solde 
def valider(solde_entry, solde_1, fina, listbox, identifiant):
    global previousSolde
    previousSolde = float(solde_entry.get())
    try:
        legende = str('Modification de la solde')
        solde_1['text'] = previousSolde
        solde_entry.delete(0, END)
        fina['text'] = "Votre solde est maintenant : {} €".format(previousSolde)
        save_to_excel(0, 0, previousSolde, legende, identifiant)  # Save new total to Excel
        listbox.delete(0, END)
    except ValueError:
        solde_1['text'] = "Entrer une valeur numérique"
        solde_entry.delete(0, END)

#   FUNCTION EDIT

    #Supprime la ligne séléctionner
def delete_selected(identifiant, listbox, fina):
    global previousSolde
    selected_index = listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        selected_item = listbox.get(selected_index)
        data = pd.read_excel("Database.xlsx", sheet_name="Data")
        for i, column in data.iterrows():
            formatted_column = f"Dépense: {float(column['Dépenses'])} € - {column['Légende']}"
            if identifiant == column['Utilisateur']:
                if formatted_column == selected_item:
                    expense = float(column['Dépenses'])
                    data = data.drop(i)
                    previousSolde += expense
                    break
        for i, column in data.iterrows():
            formatted_column = f"Revenu: {float(column['Revenues'])} € - {column['Légende']}"
            if formatted_column == selected_item:
                benefit = float(column['Revenues'])
                data = data.drop(i)
                previousSolde -= benefit
                break
            
        data = data.reset_index(drop=True)
        with pd.ExcelWriter('Database.xlsx',engine='openpyxl', mode="a", if_sheet_exists='replace') as writer :
            data.to_excel(writer, sheet_name= "Data", index=False)#Remets à jour la sheet data
        listbox.delete(selected_index)
        fina['text'] = "Votre solde est maintenant : {} €".format(previousSolde)

def analyse_value(value):
    parts = value.split('€ - ', 1)
    if len(parts) == 2:
        amount_str = parts[0].split(': ')[1].strip()
        description = parts[1].strip()
        amount = float(amount_str)
        if "Dépense" in value:
            return "Dépense", amount, description
        else:
            return "Revenu", amount, description
    return None, None, None
   
def format_column(column):
    description = column['Légende'] if not pd.isna(column['Légende']) else ''
    if not pd.isna(column['Dépenses']):
        return f"Dépense: {float(column['Dépenses'])} € - {description}"
    else:
        return f"Revenu: {float(column['Revenues'])} € - {description}"

def format_column2(column):
    description = column['Légende'] if not pd.isna(column['Légende']) else ''
    if not pd.isna(column['Revenues']):
        return f"Revenu: {float(column['Revenues'])} € - {description}"

def update_selected(index, new_value, listbox, identifiant, fina):
    global previousSolde
    index = index[0]
    old_value = listbox.get(index)
    old_type, old_amount, old_description = analyse_value(old_value)
    listbox.delete(index)
    listbox.insert(index, new_value)
    new_type, new_amount, new_description = analyse_value(new_value)
    df = pd.read_excel("Database.xlsx", sheet_name='Data')
    row_to_update = None
    for i, column in df.iterrows():
        formatted_column = format_column(column) # formatted_column : ligne du excel étudié une par une 
        if formatted_column == old_value:
            row_to_update = i
            break

    for i, column in df.iterrows():
        formatted_column = format_column2(column)
        if formatted_column == old_value:
            row_to_update = i
            break

    if row_to_update is not None:
        if new_type == "Dépense":
            df.at[row_to_update, 'Dépenses'] = new_amount
            df.at[row_to_update, 'Revenues'] = 0
            if old_type == "Revenu":
                previousSolde-=old_amount
                previousSolde-=new_amount
            if old_type == "Dépense":
                previousSolde += old_amount
                previousSolde -= new_amount
            df.at[row_to_update, 'Solde']=previousSolde
        if new_type == "Revenu":
            df.at[row_to_update, 'Dépenses'] = 0
            df.at[row_to_update, 'Revenues'] = new_amount
            if old_type == "Revenu":
                previousSolde -=old_amount
                previousSolde +=new_amount
            if old_type == "Dépense":
                previousSolde += old_amount
                previousSolde += new_amount
            df.at[row_to_update, 'Solde']=previousSolde
                
        df.at[row_to_update, 'Légende'] = new_description
            
        with pd.ExcelWriter('Database.xlsx',engine='openpyxl', mode="a", if_sheet_exists='replace') as writer :
            df.to_excel(writer, sheet_name= "Data", index=False)#Remets à jour la sheet data

    fina['text'] = "Votre solde est maintenant : {} €".format(previousSolde)

def edit_selected(listbox, compte, identifiant, fina):
    selected_index = listbox.curselection()
    if selected_index:
        new_value_entry = Entry(compte)
        new_value_entry.place(x=width/3+70, y=height-75)
        new_value_button= Button(compte, text="Valider", command=lambda: update_selected(selected_index, new_value_entry.get(), listbox, identifiant, fina), bd=0, bg="sandy brown", fg="white", font=("verdana", 10, "bold"))
        new_value_button.place(x=width/3+200, y=height-75)
        old_value = listbox.get(selected_index)
        new_value_entry.insert(0, old_value)
    

#   FONCTION GRAPHIQUE

    #Annuel
def graphiqueAnnuel(identifiant, compte):
    year= datetime.datetime.now().year
    document = pd.read_excel("Database.xlsx", sheet_name="Data")
    DonnéeCompte = document.loc[document['Utilisateur']==identifiant]#récupère les infos du compte 
    DonnéeGraphe =DonnéeCompte.loc[DonnéeCompte['Date'].dt.year==year]
    
    fig = Figure(figsize=(4,2), dpi=100)
    ax = fig.add_subplot(111)
        
        # Plot the balance
    ax.plot(DonnéeGraphe['Date'], DonnéeGraphe['Solde'], "y--")
    ax.set_title('Annuel')
        #ax.set_xlabel('Date')
    ax.set_ylabel('Solde(€)')
    fig.autofmt_xdate(rotation=45)  # Rotation des labels de l'axe des x pour meilleure lisibilité
    ax.yaxis.label.set_color('gray')
    ax.xaxis.label.set_color('gray')
    ax.tick_params(colors='gray')    
    ax.spines['left'].set_color('gray')       
    ax.spines['top'].set_color('gray')
    ax.spines['right'].set_color('gray')        
    ax.spines['bottom'].set_color('gray')  
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=compte)
    canvas.draw()
    canvas.get_tk_widget().place(x= width/3+330, y=280)

    # Mensuel

def graphiqueMensuel(identifiant, compte):
    month= datetime.datetime.now().month
    year = datetime.datetime.now().year
    document = pd.read_excel("Database.xlsx", sheet_name="Data")
    DonnéeCompte = document.loc[document['Utilisateur']==identifiant]#récupère les infos du compte 
    DonnéeAnnée = DonnéeCompte.loc[DonnéeCompte['Date'].dt.year==year]
    DonnéeGraphe =DonnéeAnnée.loc[DonnéeAnnée['Date'].dt.month==month]
       
    fig = Figure(figsize=(4,2), dpi=100)
    ax = fig.add_subplot(111)
        
        # Plot the balance
    ax.plot(DonnéeGraphe['Date'], DonnéeGraphe['Solde'], "y")
    ax.set_facecolor('white')
    ax.set_title('Mensuel')
    ax.set_ylabel('Solde (€)')
    fig.autofmt_xdate(rotation=45)  # Rotation des labels de l'axe des x pour meilleure lisibilité
    ax.yaxis.label.set_color('gray')
    ax.xaxis.label.set_color('gray')
    ax.tick_params(colors='gray')    
    ax.spines['left'].set_color('gray')       
    ax.spines['top'].set_color('gray')
    ax.spines['right'].set_color('gray')        
    ax.spines['bottom'].set_color('gray')  

        # Adjust the layout
    fig.tight_layout()

        # Create a canvas to display the plot
    canvas = FigureCanvasTkAgg(fig, master=compte)
    canvas.draw()

        # Add the canvas to the window
    canvas.get_tk_widget().place(x=width/3+330, y=495)

def open_secondary_window(identifiant):
    global previousSolde

    #   NEW WINDOW
    compte = Tk()
    height = compte.winfo_screenheight()
    width = compte.winfo_screenwidth()
    compte.geometry("%ix%i" %(width, height))
    compte.title("Buddget")
    compte.iconbitmap('coins.ico')
    compte.config(bg="white")

    #   READ EXCEL

    document = pd.read_excel('Database.xlsx', sheet_name="Data") #lit les données du compte 
    InfoCompte = document.loc[document['Utilisateur']==identifiant]#récupère les infos du compte 
    previousSolde= float(InfoCompte['Solde'].iloc[-1]) #recupère la dernière ligne de InfoCompte

    #   DISPLAY WINDOW

        #Rectangle Titre
    canvas = Canvas(compte, width=width, height=150, bg="orange")
    canvas.pack()
    rectangle = canvas.create_rectangle(0, 0, width, 150, fill="orange", outline="orange")

        #titre
    titre = canvas.create_text(width/2, 70, text="Votre espace Buddget :", fill="white", font=("Verdana", 30, "bold"))
    canvas.pack()

        #Rectangle Menu
    canvaM = Canvas(compte, width = width/3, height= height-150, bg="burlywood1")
    canvaM.place(x=0, y=153)
    
        #Rectangle ListBox
    canvalist = Canvas(compte, width= width-width/3, height=height-150, bg="white")
    canvalist.place(x=width/3, y=152)
    rectangleList = canvalist.create_rectangle(50, 120, 280, 550, fill="sandy brown", outline="sandy brown")

        #Rectangle Graphe
    rectangleGraphe = canvalist.create_rectangle(320, 120, 800, 550, fill="sandy brown", outline="sandy brown")


    #   AFFICHAGE ET ENTREE

        #Affiche solde totale du compte
    fina = Label(compte, fg="orange", bg="white", font=("Verdana", 15, "bold")) #Affiche nouvelle solde 
    fina.place(x=width/2+20, y= 200)
    fina['text'] = "Votre solde est maintenant : {} €".format(previousSolde)
    
        #Dépenses
    #Entrée
    less_label = Label(compte, text = "Dépenses :",font=("Verdana", 14, "bold", "underline"), bg="burlywood1", fg="dark orange")
    less_label.place(x= 20, y=370)
    depense_ent = Entry(compte, width=30)
    depense_ent.place(x=width/6, y=375)

    #Erreur
    depense_label = Label( compte,text = "Dépenses:", bg="burlywood1", fg="orange", font=("Verdana", 7))
    depense_label.place(x=width/12-60, y= 395)
    minus_label = Label(compte,  bg="burlywood1", fg="orange", font=("verdana", 7))
    minus_label.place(x=width/12, y = 395)
    
    #Description dépense
    description_label_dep = Label(compte, text="Description:", bg="burlywood1", fg="orange", font=("Verdana", 10, "bold"))
    description_label_dep.place(x= 100, y=420)
    description_entry_dep = Entry(compte)
    description_entry_dep.place(x=width/6, y=420)

    #Bouton
    less = Button(compte, text=" - ",command= lambda : [depense(description_entry_dep, depense_ent, minus_label, solde_1, fina, listbox, identifiant)],font=("verdana", 12, "bold"), width=5, bd=0, bg="orange", fg="white")
    less.place(x=width/3 -100, y=460)
    
        #Revenu
    #Entrée
    add_label = Label(compte, text = "Revenues :",font=("Verdana", 14, "bold", "underline"), bg="burlywood1", fg="darkorange")
    add_label.place(x = 20, y=220)
    revenue_ent = Entry(compte, width=30)
    revenue_ent.place(x=width/6, y=225)

    #Erreur
    revenue_label = Label(compte, text = "Revenu:", bg="burlywood1", fg="orange", font=("Verdana", 7))
    revenue_label.place(x=width/12-60, y=245)
    addi_label = Label(compte, font=("verdana", 7), bg="burlywood1", fg="orange")
    addi_label.place(x=width/12, y=245)

    #Description revenue
    description_label_rev = Label(compte, text="Description:", bg="burlywood1", fg="orange", font=("Verdana", 10, "bold"))
    description_label_rev.place(x = 100, y= 270)
    description_entry_rev = Entry(compte)
    description_entry_rev.place(x=width/6, y=270)

    #Bouton
    add = Button(compte, text=" + ",command= lambda :[revenue(description_entry_rev, revenue_ent, addi_label, solde_1, fina, listbox, identifiant)], font=("verdana", 12, "bold"), width = 5, bd=0, bg="orange", fg="white")
    add.place(x=width/3-100, y=310)

    
        #Solde initial(dernière connection)
    pre_balance = Label(compte, text= "Votre solde initial enregistrée est : {} €".format(previousSolde), fg="orange", bg="burlywood1", font=("Verdana", 7))
    pre_balance.place(x = 20, y= 165)
    
    #    SOLDE (Affichage et changement)

        #Changer la solde/ Variable : variable3
    solde_label1 = Label(compte, text="Changer la solde:", font=("Verdana", 14, "bold", "underline"), bg="burlywood1", fg="darkorange")
    solde_label1.place(x=20, y=520)
    solde_entry = Entry(compte, width = 30)
    solde_entry.place(x=width/6, y=525)
        
        #Affiche solde 
    solde_lable_2 = Label(compte, text = "Solde:", bg="burlywood1", fg="orange", font=("Verdana", 7))
    solde_lable_2.place(x=width/12-60, y=545)
    solde_1 = Label(compte, font=("Verdana", 7), bg="burlywood1", fg="orange")
    solde_1.place(x=width/12, y=545)
    
        #Bouton
    valid2 = Button(compte, text="Valider", command=lambda : [valider(solde_entry, solde_1, fina, listbox, identifiant)], font=("verdana", 11, "bold"), width = 7, bg='orange', bd=0, fg='white')
    valid2.place(x=width/3 -100, y=570)
    

        #   GRAPHIQUE

   
    #   AFFICHAGE GRAPHIQUE

    graphiqueAnnuel(identifiant, compte)
    graphiqueMensuel(identifiant, compte)
    
    # Annuel
    plot_monthly = Button(compte, text="Initialiser", command=lambda :[graphiqueAnnuel(identifiant, compte)], font=("Verdana", 10), bg="white", fg="sandy brown", bd=0)
    plot_monthly.place(x=width-120, y=350)

    # Mensuel
    plot_yearly = Button(compte, text="Initialiser", command=lambda :[graphiqueMensuel(identifiant, compte)], font=("verdana", 10), bg="white", fg="sandy brown", bd=0)
    plot_yearly.place(x=width-120, y=570)



        #   EDIT/ LISTBOX
        # Create a Listbox
    listbox = Listbox(compte, width = 30, height= 20)
    listbox.place(x=width/3+70, y= 290)
    delete_button = Button(compte, text="Supprimer la sélection",bd=0, bg='white', fg='sandy brown', font=('verdana', 10, "bold"), command=lambda: [delete_selected(identifiant, listbox, fina)])
    delete_button.place(x=width/3+80,  y= 620)  
    edit_button = Button(compte, text="Modifier",bd=0, bg="white", fg="sandy brown", font=("verdana", 10), command=lambda :[edit_selected(listbox, compte, identifiant, fina)])
    edit_button.place(x=width/3+110, y=650)  # Adjust the position as needed

    compte.mainloop()



#       ACCUEIL
    
    #rectangle
canvas = Canvas(window, width=width, height=150)
canvas.pack()
rectangle = canvas.create_rectangle(0, 0, width, 150, outline="orange", fill="orange")

    #titre
titre = canvas.create_text(width/2, 70, text="Bienvenue sur Buddget", fill="white", font=("Verdana", 30, "bold"))
canvas.pack()

    #image
canva = Canvas(window, width = width/2-200, height = height-300)
canva.place(x=width/2+150, y= 200)
img = Image.open("picture_page1.gif")
w=int((height-300)/1.5)
h=height-300
resizedImage=img.resize((w,h))
lastImage = ImageTk.PhotoImage(resizedImage)
canva.create_image(0,0, anchor=NW, image=lastImage)
    
    #paragraphe
titreparagraph = Label(window, text="Maitrisez votre argent, attéignez vos objectifs :\nvotre budget, notre solution!", justify="left", font=("STIXIntegralsSm", 20, "bold"))
titreparagraph.place(x=width/20, y=height/4+30)
presentation ="""Buddget est une application conçue pour vous aider à gérer un budget. Que vous souhaitiez suivre vos dépenses quotidiennes, planifier un budget mensuel ou épargner pour des objectifs spécifiques, cette application offre les fonctionnalités nécessaires pour vous aider à prendre le contrôle de vos finances. Vous pouvez choisir la somme que vous souhaitez dépenser pour une rubrique durant une période choisit. Vous pouvez lister vos dépenses en fonction de chaque catégorie. Par exemple : vous pouvez enregistrer vos dépenses quotidiennes dans différentes catégories telles que alimentation, loisirs, transport, etc. Visualisez facilement où va votre argent et identifiez les domaines où vous pourriez économiser. Pour vous aider il est possible de voir les graphiques de vos dépenses par rapport à vos périodes précédentes.\n\nNotre application est facile à utiliser et vous permet d'identifier vos dépenses facilement. Tout pour vous aider dans vos économies. """
paragraph = Label(window, text=presentation, justify="left", wraplength=width/2.5+100, font=("Noto Sans CJK TC", 10))
paragraph.place(x=width/20, y=height/3+50)
contact = Label(window, text= "Pour nous contacter : 07 64 83 21 55\nBuddget.cont@unilasalle.fr", justify="center")
contact.place(x=width/6, y=550)

    #Se connecter (button)
connect = Button(window, text="J'ai un compte", font=("Noto Sans CJK KR", 12, "bold"), bg="orange", fg='white', activebackground="white", activeforeground="orange", bd=0, command = connection)
connect.place(x=width-150, y=20, width=120, height = 22)

    # Creer un compte (button)
creation = Button(window, text="Créer un compte", font=("Noto Sans CJK KR", 12, "bold"), bg="white", fg="orange", activebackground="orange", activeforeground="white", bd=0, command = compteCreation)
creation.place(x=width-300, y=20, height = 22)

window.mainloop()



