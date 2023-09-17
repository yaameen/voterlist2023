# Voter's list extractor from PDF

This Python script is designed to extract voter's list information from a PDF file. It utilizes concurrent processing to efficiently handle multiple PDF files.

## Prerequisites

Before running this script, ensure you have the following Python packages installed:

- `concurrent.futures`

- `os`

You can install these packages using `pip`:

```bash
pip install -r requirements.txt
```

This will install all the listed packages and their specified versions.

## Usage

1\. Set the working directory and worker count:

```python
WORKING_DIRECTORY = os.getcwd() + '/data'
WORKER_COUNT = 10
```

- `WORKING_DIRECTORY`: This variable defines the working directory where files will be downloaded and processed.

- `WORKER_COUNT`: This variable sets the maximum number of workers in the ThreadPoolExecutor.

2\. Run the script:

```bash
python app.py
```

## Details

- `download(url)`: This function downloads a given URL.
  This file contains links to all other files https://storage.googleapis.com/gazette.gov.mv/docs/iulaan/142302.pdf
- `download_and_process_curried(url)`: This function downloads and processes a given URL.

- `signal_handler(sig, frame)`: This function handles the `Ctrl+C` signal for graceful shutdown.

- `main()`: This is the main function. It downloads a PDF file, extracts links, and processes them concurrently using a ThreadPoolExecutor.

- `if __name__ == "__main__":`: This statement ensures that `main()` is executed only if the script is run directly (not imported as a module).

## Exiting the Script

To exit the script, press `Ctrl+C`. This will trigger the `KeyboardInterrupt` exception, which will be caught in the `except KeyboardInterrupt` block, allowing for a graceful shutdown.
