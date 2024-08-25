import tkinter as tk

window = tk.Tk()

window.title("집가고싶다")
window.geometry("800x450+100+100")

frame = tk.Frame(window)
frame.pack(fill=tk.BOTH, expand=True)

label1 = tk.Label(frame, text="평문")

inoutput1 = tk.Text(frame, width=20, height=5)

button1 = tk.Button(frame, text="암호화")

label_input1 = tk.Label(frame, text="시프트 수")

input1 = tk.Entry(frame, width=5)

button2 = tk.Button(frame, text="복호화")

label2 = tk.Label(frame, text="암호문")

inoutput2 = tk.Text(frame, width=20, height=5)



label1.grid(row=0, column=0, padx=5, pady=5, sticky="n")
inoutput1.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
button1.grid(row=1, column=1, padx=5, pady=5)
label_input1.grid(row=0, column=2, padx=5, pady=5, sticky="n")
input1.grid(row=1, column=2, padx=5, pady=5)
button2.grid(row=1, column=3, padx=5, pady=5)
label2.grid(row=0, column=4, padx=5, pady=5, sticky="n")
inoutput2.grid(row=1, column=4, padx=5, pady=5, sticky="nsew")


frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(4, weight=1)

window.mainloop()