from datetime import datetime
import re, json
from tkinter import *
from tkinter.font import ITALIC, Font
from nltk import stem
from searcher import searchWords
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from tkHyperLinkManager import HyperlinkManager
import webbrowser
from functools import partial

stop_words = set(stopwords.words('english'))
snow_stemmer = SnowballStemmer(language='english')

def clickSearchButton(event):
    start = datetime.now()
    
    search_text = searchText.get()
    search_words = (re.sub('[^a-zA-Z]', ' ', search_text)).lower().split()
    # if the user didnt enter anything then return
    if len(search_text) == 0:
        result.delete(0.0, END)
        result.insert(END, "You didnt enter anything")
        return 

    stemmed_words = [snow_stemmer.stem(word) for word in search_words if not word in stop_words]

    UrlFile = open('document_index.txt', 'r')
    docIndex = json.load(UrlFile)

    rankedDocuments = searchWords(stemmed_words) 
    
    
    end = datetime.now()
    time_taken = str(end - start)
    #time_taken = str(end - start)

    # Convert to hyperLinks
    hyperLink = HyperlinkManager(result)

    frame3 = Frame(window, background="black") 
    
    frame3.pack()

    timeTaken_msg = Label(frame3, text="Time taken for search in seconds = ", font=("Helvetica", 12, ITALIC), background="black", foreground="#00FFC0")
    timeTaken_msg.pack(side=LEFT)

    timeTaken_secs = Label(frame3, text = time_taken, font=("Helvetica", 12, ITALIC), foreground="white", background="black")
    timeTaken_secs.pack(side=RIGHT)

    frame3.place(relx=0.5, rely=0.7, anchor=CENTER)

    result.delete(0.0, END)

    ############### this displays the result #######################
    if len(rankedDocuments):
        for document in rankedDocuments:
            url = docIndex[document[0]]
            result.insert(END, url, hyperLink.add(partial(webbrowser.open, url)))
            result.insert(END, "\n")
    else:
        result.insert(END, "Sorry, no result found")



def clickInsertDataButton():

    def clickInsertURLButton():
        new_url = newURL.get()

        ############################################################
        # code to add "new_url" to the existing database goes here # 

        # this will close the temporary window after we have added the new url
        window2.destroy()

    window2 = Tk()
    window2.title('Insert Data')
    window2.configure(background="white")
    window2.geometry("600x100")

    frame2 = Frame(window2, background="white")
    frame2.pack()

    enterData = Label(frame2, font=("Helvetica", 14), foreground="black",background="white", text="Enter new data [URL] : ")
    enterData.pack()

    newURL = Entry(frame2, width = 50, font=("Helvetica", 14), bg="white")
    newURL.pack(side = LEFT)

    insertURLButton = Button(frame2, text="Add", font=("Helvetica", 10), width=3, command=clickInsertURLButton)
    insertURLButton.pack(side=RIGHT)

    frame2.place(relx=0.5, rely=0.5, anchor=CENTER)


window = Tk()
window.title('Search')
window.configure(background="black")
window.geometry("1920x1080")

window.bind('<Return>',clickSearchButton)

logo = PhotoImage(file="talash_png_2.png")
Label(window, image=logo, background="black").place(relx=0.5, rely=0.25, anchor=CENTER)

frame = Frame(window)
frame.pack()

searchText = Entry(frame, width = 50, font=("Helvetica", 14), bg="white")
searchText.pack(side = LEFT)

searchButton = Button(frame, text="Search", font=("Helvetica", 10), width=6)
searchButton.pack(side=RIGHT)
searchButton.bind("<Button-1>", lambda event:clickSearchButton(event))

frame.place(relx=0.5, rely=0.33, anchor=CENTER)

scroll = Scrollbar(window)
scroll.pack(side=RIGHT, fill=Y)

result = Text(window, width=100, height=10, foreground="black", background="#00FFC0", font=("Helvetica", 14), yscrollcommand=scroll.set)
result.place(relx=0.5, rely=0.52, anchor=CENTER)

scroll.config(command=result.yview) 

addButton = Button(window, text="Insert Data", font=("Helvetica", 10), width=11, command=clickInsertDataButton )
addButton.place(relx=0.5, rely=0.77, anchor=CENTER)

window.mainloop()