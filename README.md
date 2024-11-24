
# 🤖 MHTR-Agent: A Novel Paradigm for Heat Treatment Research Based on Multimodal Analysis and LLMs

MHTR-Agent is a multimodal analysis and intelligent optimization framework for the heat treatment field. It leverages large language models (LLMs) and advanced multimodal data integration techniques to accelerate scientific discoveries and process optimization.

This repository includes the implementation of the following key modules:

- **llm_tracker**: For data mining and trend analysis in the heat treatment field.
- **llm_predictor**: Implements multimodal data integration and builds quantitative relationships between composition, microstructure, and properties.
- **llm_advisor**: An intelligent assistant for process optimization and decision-making.

---

## Features

- **Data Mining and Trend Analysis (`llm_tracker`)**:
  - Extracts critical features from unstructured data, such as research papers, production reports, and experiment logs.
  - Analyzes research trends and identifies key technical challenges.

- **Multimodal Data Integration and Performance Prediction (`llm_predictor`)**:
  - Integrates multimodal data, including microstructure images, processing parameters, and material composition.
  - Builds high-precision quantitative models using advanced vision-language frameworks.

- **Intelligent Process Optimization (`llm_advisor`)**:
  - Provides actionable recommendations for process optimization.
  - Combines finite element simulation and physics-informed neural networks to optimize heat treatment workflows.

---

## Installation Guide

1. Clone this repository:
   ```bash
   git clone https://github.com/NotUrNeighborMrWang/MHTR-Agent.git
   cd MHTR-Agent
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. Configure the API key for LLM integrations (e.g., OpenAI API) in the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

---

## Usage Instructions

### 1. Data Mining with `llm_tracker`

Run `llm_tracker` to extract and analyze data trends:

```bash
python llm_tracker/main.py --input data/research_papers.json
```

The output includes research trends and key technical domains.

### 2. Multimodal Prediction with `llm_predictor`

Train and test predictive models using multimodal datasets:

```bash
python llm_predictor/main.py --config config/predictor_config.yaml
```

The output includes high-accuracy predictions for material properties.

### 3. Intelligent Advising with `llm_advisor`

Use the intelligent assistant to optimize heat treatment processes:

```bash
python llm_advisor/main.py --process carburizing --parameters parameters.json
```

The output includes optimized process parameters and detailed insights.

---

## Examples

- **Data Mining**: Analyze research trends in the heat treatment field.
- **Performance Prediction**: Build a "composition-microstructure-property" model for Cr13 martensitic stainless steel.
- **Process Optimization**: Optimize carburizing temperature and atmosphere composition.

---

## Project Structure

```
MHTR-Agent/
├── llm_tracker/         # Data mining and trend analysis
├── llm_predictor/       # Multimodal data integration and prediction
├── llm_advisor/         # Intelligent process optimization assistant
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements

This project uses the following libraries and frameworks:
- OpenAI GPT
- Hugging Face Transformers
- PyTorch
- Scikit-learn

For more details, please refer to the [References](#) section in the documentation.
