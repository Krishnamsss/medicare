import tkinter as tk
from tkinter import messagebox
import pyttsx3
import requests
import random

# Symptom-Disease Dictionary
symptom_disease_map = {
    "fever": ["Flu", "Viral Infection", "Malaria", "COVID-19", "Typhoid"],
    "cough": ["Common Cold", "Flu", "Bronchitis", "Asthma", "Pneumonia"],
    "headache": ["Migraine", "Tension Headache", "Stress", "Sinusitis", "Hypertension"],
    "fatigue": ["Anemia", "Thyroid Issues", "Diabetes", "Chronic Fatigue Syndrome", "Depression"],
    "nausea": ["Gastroenteritis", "Food Poisoning", "Pregnancy", "Motion Sickness", "Migraine"],
    "chest pain": ["Heart Disease", "Pneumonia", "Costochondritis", "Angina"],
    "diarrhea": ["Gastroenteritis", "Food Poisoning", "IBS", "Celiac Disease", "Infection"],
    "vomiting": ["Food Poisoning", "Gastroenteritis", "Pregnancy", "Migraine"],
    # Add more symptoms and diseases here
}

# Reverse mapping of diseases to symptoms
disease_symptom_map = {}
for symptom, diseases in symptom_disease_map.items():
    for disease in diseases:
        if disease not in disease_symptom_map:
            disease_symptom_map[disease] = []
        disease_symptom_map[disease].append(symptom)

# Text-to-Speech Engine
tts_engine = pyttsx3.init()

# Diagnosis logic
class DiagnosisSession:
    def __init__(self):
        self.possible_diseases = set()
        self.asked_symptoms = set()

    def start_diagnosis(self, symptoms):
        self.asked_symptoms.update(symptoms)
        for symptom in symptoms:
            diseases = set(symptom_disease_map.get(symptom.lower(), []))
            if not self.possible_diseases:
                self.possible_diseases = diseases
            else:
                self.possible_diseases &= diseases

    def refine_diagnosis(self, symptoms):
        self.asked_symptoms.update(symptoms)
        filtered_diseases = set()
        for disease in self.possible_diseases:
            if any(symptom in disease_symptom_map.get(disease, []) for symptom in symptoms):
                filtered_diseases.add(disease)
        self.possible_diseases = filtered_diseases

    def suggest_more_symptoms(self):
        all_related_symptoms = set()
        for disease in self.possible_diseases:
            all_related_symptoms.update(disease_symptom_map.get(disease, []))
        return all_related_symptoms - self.asked_symptoms

# Function to get nearby hospitals
def get_nearby_hospitals():
    # Dummy implementation for hospital suggestions
    hospitals = [
      "Shalby Hospital - 9, Race Course Rd",
      "Bombay Hospital - 9, Ujjain Road",
      "Indore Hospital & Research Centre - 15, Old Palasia",
      "Sai Hospital - 4, Hukumchand Marg",
      "Noble Hospital - 2, A B Road",
      "Arvind Hospital - 8, South Tukoganj",
      "Chirayu Hospital - 15, Bicholi Mardana",
      "Care Clinic Hospital - 12, Vijay Nagar",
      "Curewell Hospital - 3, Rajendra Nagar"
    ]
    return random.sample(hospitals, 2)


# Main GUI function
def medical_chatbot_interface():
    session = DiagnosisSession()
    enable_voice_assistant = False

    # Initialize the main window
    window = tk.Tk()
    window.title("MediSense Advanced Diagnosis")
    window.geometry("600x700")
    window.configure(bg="#f0f8ff")

    # Title label
    title_label = tk.Label(window, text="MediSense Advanced", font=("Arial", 16, "bold"), bg="#f0f8ff")
    title_label.pack(pady=10)

    # Instructions
    instruction_label = tk.Label(window, text="Enter your symptom(s) separated by commas:", font=("Arial", 12), bg="#f0f8ff")
    instruction_label.pack(pady=5)

    # Input field
    symptom_entry = tk.Entry(window, width=50, font=("Arial", 12))
    symptom_entry.pack(pady=10)

    # Output field
    output_text = tk.Text(window, height=20, width=70, font=("Arial", 12), state=tk.DISABLED, wrap=tk.WORD, bg="#ffffff")
    output_text.pack(pady=10)

    # Function to handle diagnosis
    def get_diagnosis():
        nonlocal enable_voice_assistant
        user_input = symptom_entry.get()
        symptom_entry.delete(0, tk.END)

        if not user_input.strip():
            messagebox.showinfo("Input Error", "Please enter at least one symptom.")
            return

        symptoms = [symptom.strip().lower() for symptom in user_input.split(",")]

        if not session.possible_diseases:
            session.start_diagnosis(symptoms)
        else:
            session.refine_diagnosis(symptoms)

        # Generate output
        if len(session.possible_diseases) == 1:
            result = f"The most likely condition based on your symptoms is:\n- {list(session.possible_diseases)[0]}"
            result += "\n\nPlease consult a healthcare professional for an accurate diagnosis."
        elif session.possible_diseases:
            result = "Based on your symptoms, possible conditions are:\n"
            result += "\n".join(f"- {disease}" for disease in session.possible_diseases)
            more_symptoms = session.suggest_more_symptoms()
            if more_symptoms:
                result += "\n\nTo narrow it down, can you specify if you have any of these symptoms?\n"
                result += ", ".join(more_symptoms)
            else:
                result += "\n\nPlease consult a healthcare professional for further analysis."
        else:
            result = "I'm sorry, I couldn't determine a possible disease based on the symptoms provided.\n"
            result += "Please consult a healthcare professional for an accurate diagnosis."

        # Display output
        output_text.configure(state=tk.NORMAL)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)
        output_text.configure(state=tk.DISABLED)

        if enable_voice_assistant:
            tts_engine.say(result)
            tts_engine.runAndWait()

    # Function to toggle voice assistant
    def toggle_voice_assistant():
        nonlocal enable_voice_assistant
        enable_voice_assistant = not enable_voice_assistant
        status = "enabled" if enable_voice_assistant else "disabled"
        messagebox.showinfo("Voice Assistant", f"Voice assistant is now {status}.")

    # Function to display nearby hospitals
    def show_nearby_hospitals():
        hospitals = get_nearby_hospitals()
        result = "Nearby hospitals:\n" + "\n".join(f"- {hospital}" for hospital in hospitals)

        output_text.configure(state=tk.NORMAL)
        output_text.insert(tk.END, "\n\n" + result)
        output_text.configure(state=tk.DISABLED)

        if enable_voice_assistant:
            tts_engine.say(result)
            tts_engine.runAndWait()

    # Diagnose button
    diagnose_button = tk.Button(window, text="Diagnose", font=("Arial", 12), command=get_diagnosis, bg="#4682b4", fg="white")
    diagnose_button.pack(pady=10)

    # Toggle voice assistant button
    voice_button = tk.Button(window, text="Toggle Voice Assistant", font=("Arial", 12), command=toggle_voice_assistant, bg="#4682b4", fg="white")
    voice_button.pack(pady=10)

    # Show nearby hospitals button
    hospitals_button = tk.Button(window, text="Show Nearby Hospitals", font=("Arial", 12), command=show_nearby_hospitals, bg="#4682b4", fg="white")
    hospitals_button.pack(pady=10)

    # Exit button
    exit_button = tk.Button(window, text="Exit", font=("Arial", 12), command=window.destroy, bg="#b22222", fg="white")
    exit_button.pack(pady=10)

    # Run the main event loop
    window.mainloop()

# Run the GUI
medical_chatbot_interface()
