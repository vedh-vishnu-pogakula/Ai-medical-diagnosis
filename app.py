import tkinter as tk
from tkinter import messagebox, scrolledtext
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


try:
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
except Exception as e:
    raise RuntimeError(f"Gemini model init failed: {e}")


def get_diagnosis():
    symptoms = symptoms_input.get("1.0", tk.END).strip()
    history = history_input.get("1.0", tk.END).strip()

    if not symptoms:
        messagebox.showwarning("Missing Info", "Please enter your symptoms.")
        return

    prompt = (
        f"You are a medical assistant. Based on the following symptoms and medical history, "
        f"provide a possible diagnosis or suggestions.The output should be consise and give in bullet points. Also mention if the user should visit a doctor.\n\n"
        f"Give description if the disease or diagnosis is not common.\n\n"
        f"Symptoms: {symptoms}\nMedical History: {history}"
    )

    try:
        response = model.generate_content(prompt)
        diagnosis_output.config(state="normal")
        diagnosis_output.delete("1.0", tk.END)
        diagnosis_output.insert(tk.END, response.text)
        diagnosis_output.config(state="disabled")
    except Exception as e:
        messagebox.showerror("API Error", f"Something went wrong:\n{e}")

#  GUI
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
os.system('defaults write -g NSRequiresAquaSystemAppearance -bool No')
app = tk.Tk()
app.title("🧠 Medical Diagnosis Assistant (Gemini)")
app.geometry("750x650")
app.configure(bg="white")  # Force bright background


label_font = ("Arial", 14, "bold")
text_font = ("Arial", 12)
button_font = ("Arial", 13, "bold")


tk.Label(app, text="📝 Enter Symptoms:", font=label_font, bg="white", fg="#1a1a1a").pack(pady=(15, 5))
symptoms_input = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=80, height=6, font=text_font,
                                           bg="#f0f0f0", fg="black", bd=2, relief="solid", insertbackground="black")
symptoms_input.pack(pady=5)

# Medical History Input
tk.Label(app, text="📋 Medical History (optional):", font=label_font, bg="white", fg="#1a1a1a").pack(pady=(15, 5))
history_input = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=80, height=4, font=text_font,
                                          bg="#f0f0f0", fg="black", bd=2, relief="solid", insertbackground="black")
history_input.pack(pady=5)


tk.Button(app, text="🩺 Get Diagnosis", command=get_diagnosis, font=button_font,
          bg="#007acc", fg="white", activebackground="#005b99", activeforeground="white",
          width=25, height=2, bd=3, relief="raised").pack(pady=25)

# Diagnosis Result Output
tk.Label(app, text="🔍 Diagnosis Result:", font=label_font, bg="white", fg="#1a1a1a").pack(pady=(0, 5))
diagnosis_output = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=80, height=10, font=text_font,
                                             bg="#f9f9f9", fg="black", bd=2, relief="sunken", insertbackground="black")
diagnosis_output.pack(pady=10)
diagnosis_output.config(state="disabled")

app.mainloop()
