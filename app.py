from concurrent.futures import ThreadPoolExecutor
import os
from utils import download, extract_links, download_and_process


WORKING_DIRECTORY = os.getcwd() + '/data'
WORKER_COUNT = 10


def download_and_process_curried(url):
    download_and_process(url, WORKING_DIRECTORY)


def signal_handler(sig, frame):
    print("\nCtrl+C received. Exiting...")
    exit(0)


def main():
    try:
        download("https://storage.googleapis.com/gazette.gov.mv/docs/iulaan/142302.pdf",
                 WORKING_DIRECTORY)
        dhaairas = [x for x in extract_links(
            WORKING_DIRECTORY + '/142302.pdf') if x.endswith('.pdf')]
        number_of_dhaairas = len(dhaairas)
        with ThreadPoolExecutor(
                max_workers=min(number_of_dhaairas, WORKER_COUNT)) as executor:
            executor.map(download_and_process_curried, dhaairas)
    except KeyboardInterrupt:
        print("Received Ctrl+C. Shutting down...")


if __name__ == "__main__":
    main()
