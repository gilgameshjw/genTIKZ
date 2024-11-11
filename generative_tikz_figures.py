
import os
import yaml
from openai import OpenAI
import openai

import tkinter as tk
from tkinter import ttk
import subprocess


##############################################################################
# UI for User Input
##############################################################################

class UserInputApp:
    def __init__(self, root):
        # Set up the window
        self.root = root
        self.root.title("Code Generation Inputs")

        # Code Description Entry
        tk.Label(root, text="Code Purpose:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.code_description = tk.Text(root, width=50, height=4)
        self.code_description.insert("1.0", "I want a tikz code that gives me a figure of a function and its integral.")
        self.code_description.grid(row=0, column=1, padx=10, pady=5)

        # Plot Description Entry
        tk.Label(root, text="Plot Style:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.plot_description = tk.Text(root, width=50, height=4)
        self.plot_description.insert("1.0", "function should be in green and integral in magenta")
        self.plot_description.grid(row=1, column=1, padx=10, pady=5)

        # File Name Entry
        tk.Label(root, text="File Name:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.file_name = tk.Entry(root, width=30)
        self.file_name.insert(0, "fig")
        self.file_name.grid(row=2, column=1, padx=10, pady=5)

        # File Format Dropdown
        tk.Label(root, text="File Format:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.file_format = ttk.Combobox(root, values=["PDF", "PNG", "JPEG", "SVG"], width=10)
        self.file_format.set("PDF")
        self.file_format.grid(row=3, column=1, padx=10, pady=5)

        # Submit Button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=1, pady=10)

    def submit(self):
        # Get values from the fields
        self.code_description = self.code_description.get("1.0", "end-1c").strip()
        self.plot_description = self.plot_description.get("1.0", "end-1c").strip()
        self.file_name = self.file_name.get().strip()
        self.file_format = self.file_format.get().lower()

        # Display the user input in console (or handle further processing here)
        print("\nUser Input:")
        print(f"Code Purpose: {self.code_description}")
        print(f"Plot Style: {self.plot_description}")
        print(f"File Name: {self.file_name}")
        print(f"File Format: {self.file_format}")

        # Optional: Close the window after submitting
        self.root.destroy()


##############################################################################
# Code for generating TikZ code
##############################################################################

def load_api_key(config_path="config.yaml"):
    """Load the OpenAI API key from a configuration file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config.get("openai_api_key")

def initialize_openai_client(api_key):
    """Initialize the OpenAI client with the API key."""
    os.environ["OPENAI_API_KEY"] = api_key
    openai.api_key = api_key
    return OpenAI()

def construct_prompt(code_description, plot_description):
    """Construct the system and user prompts for generating TikZ code."""
    prompt_system = """
    You are generating TikZ code that can be executed in LaTeX.
    
    ***Instructions:***
    * Return the latex code.
    * Code should start with ```latex and end with ```.
    * Use \\documentclass[tikz,border=2mm]{standalone}.
    * Import the TikZ package.
    """
    prompt_code = f"""
    I want a TikZ code that gives me a: 
    
    Code description:
    {code_description}

    Plot description:
    {plot_description}
    """
    return prompt_system, prompt_code

def generate_tikz_code(client, code_description, plot_description):
    """Generate TikZ code from OpenAI based on the provided descriptions."""
    prompt_system, prompt_code = construct_prompt(code_description, plot_description)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_code}
        ]
    )
    return response.choices[0].message.content

def extract_latex(latex_text):
    """Extract the LaTeX code block from the response."""
    id_start = latex_text.find("```latex")
    id_end = latex_text.find("```", id_start + 1)
    return latex_text[id_start + 8:id_end] if id_start != -1 and id_end != -1 else None

def generate_tikz_figure(code_description, plot_description, config_path="config.yaml"):
    """Main function to load config, initialize client, and generate TikZ code."""
    api_key = load_api_key(config_path)
    client = initialize_openai_client(api_key)
    latex_response = generate_tikz_code(client, code_description, plot_description)
    latex_code = extract_latex(latex_response)
    if latex_code:
        print("Generated TikZ LaTeX Code:\n", latex_code)
        return latex_code
    else:
        print("Failed to extract LaTeX code from the response.")
        None


##############################################################################
# latex execution to a file in different formats
##############################################################################

def tikz_to_format(tikz_code, output_filename="output", format="pdf"):
    """Generate a LaTeX file from TikZ code and compile it to the desired format."""    
    # File names
    tex_filename = f"{output_filename}.tex"
    pdf_filename = f"{output_filename}.pdf"

    # Write LaTeX content to .tex file
    with open(tex_filename, 'w') as tex_file:
        tex_file.write(tikz_code)

    # Compile LaTeX file to PDF using pdflatex
    try:
        result = subprocess.run(["pdflatex", tex_filename], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"PDF generated successfully: {pdf_filename}")
    except subprocess.CalledProcessError as e:
        print("Error during PDF generation:", e)
        print(e.stderr.decode())  # Show detailed error message
        return

    # Convert PDF to the desired format if needed
    if format.lower() == "pdf":
        print(f"File generated in PDF format: {pdf_filename}")
    elif format.lower() == "png":
        subprocess.run(["pdftoppm", "-png", pdf_filename, output_filename], check=True)
        print(f"PNG generated successfully: {output_filename}-1.png")
    elif format.lower() == "jpeg":
        subprocess.run(["pdftoppm", "-jpeg", pdf_filename, output_filename], check=True)
        print(f"JPEG generated successfully: {output_filename}-1.jpg")
    elif format.lower() == "svg":
        subprocess.run(["pdf2svg", pdf_filename, f"{output_filename}.svg"], check=True)
        print(f"SVG generated successfully: {output_filename}.svg")
    else:
        print(f"Unsupported format: {format}")

    # Clean up auxiliary files except PDF if requested format is "pdf"
    for ext in [".aux", ".log", ".tex"]:
        try:
            os.remove(f"{output_filename}{ext}")
        except FileNotFoundError:
            pass




# Create and run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = UserInputApp(root)
    root.mainloop()
    
    tikz_code = generate_tikz_figure(app.code_description, app.plot_description)
    if tikz_code:
        tikz_to_format(tikz_code, app.file_name, app.file_format)
        
        

