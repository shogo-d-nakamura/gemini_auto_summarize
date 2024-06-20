qiita https://qiita.com/Shoelife2022/items/f69def09a6a272b42d16
claudeで生成したREADME↓

# Gemini Auto Summarize

This repository contains a Python script that automatically summarizes academic papers using the Gemini large language model. The script reads a PDF file of a research paper, feeds it to the Gemini model, and generates responses to a set of predefined prompts. The generated summaries provide an in-depth explanation of the paper's content, experiments, results, and conclusions.

## Features

- Automatically reads a PDF file of a research paper
- Utilizes the Gemini-1.5-Flash or Gemini-1.5-Pro model for text generation
- Generates detailed summaries based on a set of predefined prompts
- Supports single file processing or batch processing of multiple files
- Handles request limits and server errors by switching between Flash and Pro models
- Generates a markdown file with the summarized content

## Requirements

- Python 3.x
- tqdm
- google-generativeai
- argparse
- pypdf

## Usage

1. Clone the repository:

```
git clone git@github.com:shogo-d-nakamura/gemini_auto_summarize.git
```

2. Install the required dependencies:

```
conda env create -f env.yml
```

3. Set up your Gemini API key:

- Create a file named `gemini_api` in the project directory.
- Paste your Gemini API key into the file and save it.

4. Run the script:

- To process a single PDF file:

```
python main.py --input <filename>
```

- To process multiple PDF files in a batch:

```
python main.py --batch <dirname>
```

- To use the Gemini-1.5-Pro model (default is Gemini-1.5-Flash):

```
python main.py --input <filename> --pro
```

5. The script will generate a markdown file with the same name as the input PDF file, containing the summarized content.

## Prompts

The script uses a set of predefined prompts to generate summaries for different sections of the research paper. The prompts cover the following aspects:

- Overall content of the paper
- Introduction
- Important cited papers
- Datasets used
- Experiments and their results
- Proposed methods
- Conclusion
- Related work
- Novelty of the paper
- Advantages over existing research
- Challenges and limitations

## Limitations

- The script relies on the availability and performance of the Gemini language model. Request limits or server issues may affect the summarization process.
- The quality of the generated summaries depends on the quality and clarity of the input PDF file.
- The script assumes the PDF file contains a single research paper. Processing multiple papers in a single PDF file may lead to unexpected results.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- This project utilizes the Gemini language model developed by Google.
- The script is built using various open-source libraries and tools.
