# Contropedia Recreation

This repository recreates a simplified version of **Contropedia**, a tool for analyzing controversies in Wikipedia. The original project is described on [contropedia.net](https://contropedia.net) as an "analysis and visualization of controversies within Wikipedia articles".

The included script fetches revision data from the Wikipedia API and computes a basic controversy score based on revert activity in edit summaries. It is inspired by the paper *Contropedia - the analysis and visualization of controversies in Wikipedia articles* (Borra et al., CHI 2015, DOI [10.1145/2641580.2641622](https://doi.org/10.1145/2641580.2641622)).

## Usage

Run the script with a Wikipedia article title:

```bash
python3 contropedia.py "Article Title"
```

The script outputs the total revision count, detected revert count, and a simple controversy score.

## Running Tests

Install the `pytest` package and execute the test suite from the repository root:

```bash
pip install pytest
pytest
```
