# Contropedia Recreation

This repository recreates a simplified version of **Contropedia**, a tool for analyzing controversies in Wikipedia. The original project is described on [contropedia.net](https://contropedia.net) as an "analysis and visualization of controversies within Wikipedia articles".

The included script fetches revision data from the Wikipedia API and computes
a basic controversy score based on detected revert activity. Reverts are counted when edit summaries mention reverting and when a revision's SHA1 matches an earlier version. It is inspired by the paper *Contropedia - the analysis and visualization of controversies in Wikipedia articles* (Borra et al., CHI 2015, DOI [10.1145/2641580.2641622](https://doi.org/10.1145/2641580.2641622)).

## Usage

Run the script with a Wikipedia article title:

```bash
python3 contropedia.py "Article Title"
```

The script outputs the total revision count, detected revert count, and a simple controversy score.
