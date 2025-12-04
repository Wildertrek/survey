# A Survey and Computational Atlas of Personality Models

This repository contains the datasets, embeddings, and visualizations associated with the paper "A Survey and Computational Atlas of Personality Models". It serves as a comprehensive resource for researchers in psychometrics, personality psychology, and computational social science.

## Repository Structure

The repository is organized into three main directories:

*   **`datasets/`**: Contains CSV files for various personality models and inventories. Each file typically includes factors/scales and their associated descriptors (adjectives, synonyms, verbs, nouns).
*   **`Embeddings/`**: Contains the computational representations of the models.
    *   `*_embeddings.csv`: The dataset with an added `Embedding` column containing vector representations.
    *   `*_clustered_embeddings.csv`: Embeddings with cluster assignments.
    *   `*_confusion_matrix.csv`: Confusion matrices representing the relationships or overlaps between different constructs.
*   **`graphs/`**: High-resolution visualizations (`.png`) of the personality models, generated using neo4j based on the datasets.

## Included Models

The atlas covers a wide range of personality models, including but not limited to:

*   **OCEAN** (Big Five Personality Traits)
*   **MBTI** (Myers-Briggs Type Indicator)
*   **MMPI** (Minnesota Multiphasic Personality Inventory)
*   **DISC** (Dominance, Influence, Steadiness, Conscientiousness)
*   **HEX** (HEXACO model)
*   **NPI** (Narcissistic Personality Inventory)
*   **BDI** (Beck Depression Inventory)
*   **GAD7** (Generalized Anxiety Disorder 7)
*   And many others (e.g., RIASEC, Enneagram, etc.)

## Usage

This data can be used to:
*   Analyze the semantic relationships between different personality constructs.
*   Visualize the "landscape" of personality models.
*   Develop or benchmark computational models of personality.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Supplementary Material

For detailed methodology and analysis, please refer to the `Supplementary_Appendices_for_A_Survey_and_Computational_Atlas_of_Personality_Models.pdf` file included in this repository.
