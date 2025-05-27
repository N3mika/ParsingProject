# Parsing the Switch: LLM-Based UD Annotation for Complex Code-Switched and Low-Resource Languages
Code-switching presents a complex challenge for syntactic analysis, especially in low-resource language settings where annotated data is scarce. While recent work has explored the use of large language models (LLMs) for sequence-level tagging, few approaches systematically investigate how well these models capture syntactic structure in code-switched contexts. Moreover, existing parsers trained on monolingual treebanks often fail to generalize to multilingual and mixed-language input. To address this gap, we introduce the \textit{BiLingua Parser}, an LLM-based annotation pipeline designed to produce Universal Dependencies (UD) annotations for code-switched text. First, we develop a prompt-based framework for Spanish-English and Spanish-Guaraní data, combining few-shot LLM prompting with expert review. Second, we release two annotated datasets, including the first Spanish-Guaraní UD-parsed corpus. Third, we conduct a detailed syntactic analysis of switch points across language pairs and communicative contexts. Experimental results show that BiLingua Parser achieves up to \textbf{95.29\%} LAS after expert revision, significantly outperforming prior baselines and multilingual parsers. These results show that LLMs, when carefully guided, can serve as practical tools for bootstrapping syntactic resources in under-resourced, code-switched environments

![teaserimage](./data/figure.png)

## 📦 Requirements

Install the required Python packages via the provided `requirements.txt` file.

---

## 🛠 Installation

1. Clone the repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
2. Install the dependencies using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your OpenAI API Key:
   - You should add your OpenAI API key to your environment variables. For example:
     - On Linux/macOS:
       ```bash
       export OPENAI_API_KEY="your-api-key-here"
       ```
     - On Windows (CMD):
       ```bash
       set OPENAI_API_KEY="your-api-key-here"
       ```

---

## 🚀 Usage

1. **To run the Spanish-English tagging script:**
     ```bash
     python spaeng.py
     ```

2. **To run the Spanish-Guarani tagging script**
     ```bash
     python spagua.py
     ```
   - Make sure to update the file paths within the script to point to your local data files.
