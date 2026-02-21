# Contributing

Thank you for your interest in the Personality Atlas. Contributions are welcome, especially from researchers who work with personality models not yet included in the atlas.

## How to contribute

### Reporting issues

- Use the [issue tracker](https://github.com/Wildertrek/survey/issues) to report bugs or suggest improvements
- Include the model name, dataset file, and a description of the problem
- For classification errors, include the trait entry and the expected vs. actual factor

### Adding a new personality model

The atlas currently covers 44 models. If you know of a model that should be included:

1. Open an issue describing the model (name, citation, number of factors, theoretical tradition)
2. If you have trait data, format it using the 5-column schema: `Factor`, `Adjective`, `Synonym`, `Verb`, `Noun`
3. Submit a pull request adding the CSV to the appropriate category folder under `datasets/`

See `datasets/Trait-Based/OCEAN.csv` for an example of the expected format.

### Fixing trait data

If you spot an error in an existing dataset (wrong factor assignment, missing synonym, etc.):

1. Fork the repository
2. Edit the CSV file
3. Submit a pull request with a brief explanation of the correction and its source

### Code contributions

For changes to notebooks or Python code:

1. Fork the repository
2. Create a branch (`git checkout -b fix/description`)
3. Test your changes locally
4. Submit a pull request

## Style guidelines

- Datasets: UTF-8 CSV, 5-column schema, one row per trait entry
- Notebooks: Clear markdown headers, outputs cleared before committing
- Commit messages: Plain descriptions, no conventional commit prefixes

## Questions

Open an issue or email Joseph.Raetano@gmail.com.
