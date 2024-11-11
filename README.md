```markdown
# TikZ Figure Generator

This project is designed to generate custom TikZ figures based on user inputs provided through a simple UI. The project leverages OpenAI’s language model API to interpret user descriptions and generate appropriate LaTeX TikZ code that can be compiled into various output formats, such as PDF, PNG, JPEG, and SVG.

This is a collaborative project between:
- **Dr. Jair Wuilloud**
- **Professor Stephan Lauermann**

## Project Overview

- **Main File**: `generative_tikz_figures.py`
- **Configuration File**: `config.yaml` (contains the OpenAI API key)
- **Requirements**: `requirements.txt` (for dependencies)

## Requirements

Install the dependencies using:

```bash
pip install -r requirements.txt
```

The OpenAI API key must be specified in `config.yaml` as follows:

```yaml
openai_api_key: "your_openai_key_here"
```

## How It Works

The application offers a user interface (UI) to collect inputs and generates the LaTeX code for TikZ figures based on these parameters. The application processes four key input parameters provided by the user and outputs the generated TikZ figure in the desired format.

## Input Parameters

1. **code_description**: A textual description of what the figure should represent, such as the type of function, integral, plot area, etc.
2. **plot_description**: Specifications for the plot’s appearance, including colors, styles, and any labels.
3. **file_name**: The desired name for the output file, without file extension.
4. **file_format**: The preferred file format for the output (PDF, PNG, JPEG, SVG).

## Usage

1. **Prepare the Environment**: Make sure all dependencies are installed via `requirements.txt`.
   
2. **Update API Key**: Place your OpenAI API key in `config.yaml`.

3. **Run the Application**:
   Execute the `generative_tikz_figures.py` script to launch the UI. Enter values for the required inputs in the fields provided. 
   
4. **Generating the Figure**: Click "Submit" in the UI, and the application will use the provided descriptions to generate LaTeX TikZ code and compile it to the specified file format. The output file will be saved with the specified name and format.

## Example

```bash
python generative_tikz_figures.py
```

- **code_description**: "I want a TikZ code that shows a parabola."
- **plot_description**: "Plot the function in blue with a labeled x-axis and y-axis."
- **file_name**: "parabola_plot"
- **file_format**: "PDF"

The application will generate a file named `parabola_plot.pdf` (or in the specified format) in the same directory.

## File Structure

- `generative_tikz_figures.py`: Main file with code to gather inputs and generate TikZ figures.
- `config.yaml`: Configuration file storing API key.
- `requirements.txt`: Lists all dependencies for the project.

## Troubleshooting

If you encounter any issues with LaTeX compilation, ensure `pdflatex` is installed and accessible via your system's PATH.

## License

This project is open source and freely available for educational and non-commercial use. Please attribute appropriately when using or modifying.
```
