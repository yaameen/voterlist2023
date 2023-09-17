from dhivehi_unicode import DhivehiConverter as dv
import os
import pdfplumber
import pikepdf
import requests
import csv


def download(url, folder_path):
    print(f"Downloading file from '{url}'...")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name = url.split("/")[-1]

    if os.path.exists(os.path.join(folder_path, file_name)):
        print(f"File '{file_name}' already exists in '{folder_path}'.")
        return

    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(
                f"File '{file_name}' downloaded and saved in '{folder_path}'.")
        else:
            print(
                f"Failed to download the file. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")


def extract_links(file):
    pdf_file = pikepdf.Pdf.open(file)
    urls = []
    for page in pdf_file.pages:
        pages = page.get("/Annots")
        if pages is None:
            continue
        for annots in pages:
            if annots is None:
                continue
            a = annots.get("/A")
            if a is not None:
                uri = a.get("/URI")
                if uri is not None:
                    print("[+] URL Found:", uri)
                    urls.append(str(uri))

    print("[*] Total URLs extracted:", len(urls))
    return urls


def extract_list_from_pdf(file):
    print("pdf_to_csv {}".format(file))
    ofile = "{}.csv".format(file)

    box = file.split('/')[-1][:-8]

    with pdfplumber.open(file) as pdf:
        processed_lines = []
        for page in pdf.pages:
            for line in page.extract_text().split('\n'):
                parts = line.split()
                if parts[0].isnumeric():
                    processed_line = process_line(
                        ",".join(line.split()), box)
                    if processed_line is not None:
                        processed_lines.append(processed_line)
        if len(processed_lines) > 0:
            save_csv(ofile, processed_lines)
    print("Wrote {}".format(ofile))


def process_line(line, box):
    try:
        parts = line.split(',')
        atoll = parts[1]
        island = parts[2]
        address_en = parts[3]
        name = parts[4]
        gender_ix = 5
        while parts[gender_ix] not in ['F', 'M']:
            gender_ix += 1
            if gender_ix >= len(parts):
                return None
        gender = parts[gender_ix]
        id_card = parts[gender_ix+1]
        address = parts[gender_ix+2]
        name_dv = parts[gender_ix+3]

        for i in range(gender_ix+4, len(parts)):
            name_dv = name_dv + ' ' + parts[i].strip()

        address_en = " ".join(parts[3: gender_ix-len(name_dv.split(' '))])
        name = " ".join(parts[gender_ix-len(name_dv.split(' ')): gender_ix])

        return box, atoll, island, address_en, name, gender, id_card, address, dv.accent_to_unicode(name_dv)
    except Exception as e:
        return None


def save_csv(csv_file, processed_lines=[]):
    if processed_lines is None or len(processed_lines) == 0:
        return
    print("save processed csv {} with {} records.".format(
        csv_file, len(processed_lines)))
    with open(csv_file, mode='w', newline='\n') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(processed_lines)


def download_and_process(url, folder_path):
    download(url, folder_path)
    extract_list_from_pdf(os.path.join(folder_path, url.split("/")[-1]))
