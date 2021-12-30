
from datetime import time
from tkinter import *
from tkinter.font import ITALIC, Font



def clickSearchButton(event):
    searched_text = searchText.get()
    # the text entered in search bar goes to searched_text

    ################## where time_taken = str(end-start) #############
    time_taken = float
    time_taken = 5.24
    #time_taken = str(end - start)

    frame3 = Frame(window, background="black") 
    
    frame3.pack()

    timeTaken_msg = Label(frame3, text="Time taken for search in seconds = ", font=("Helvetica", 12, ITALIC), background="black", foreground="#00FFC0")
    timeTaken_msg.pack(side=LEFT)

    timeTaken_secs = Label(frame3, text = time_taken, font=("Helvetica", 12, ITALIC), foreground="white", background="black")
    timeTaken_secs.pack(side=RIGHT)

    frame3.place(relx=0.5, rely=0.7, anchor=CENTER)

    string_list= ["a bit more", "hullo", "just", "do", "it", "Hello", "this is a link", "hullo shishter","CHECK","SCROLL","Also very", "nice weather", "out here", "very cold"]

    result.delete(0.0, END)

    ############### this displays the result #######################
    try:
        for x in range(len(docIDs[rankedDocs])):
            result.insert(END, docIDs[rankedDoc[i][0]])
            result.insert(END, "\n")

    except:
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

searchButton = Button(frame, text="Search", font=("Helvetica", 10), width=6, command=clickSearchButton)
searchButton.pack(side=RIGHT)

frame.place(relx=0.5, rely=0.33, anchor=CENTER)

scroll = Scrollbar(window)
scroll.pack(side=RIGHT, fill=Y)

result = Text(window, width=100, height=10, foreground="black", background="#00FFC0", font=("Helvetica", 14), yscrollcommand=scroll.set)
result.place(relx=0.5, rely=0.52, anchor=CENTER)

scroll.config(command=result.yview)

addButton = Button(window, text="Insert Data", font=("Helvetica", 10), width=11, command=clickInsertDataButton )
addButton.place(relx=0.5, rely=0.77, anchor=CENTER)

window.mainloop()