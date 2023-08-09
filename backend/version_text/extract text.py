import argparse
import os
import sys
import uuid
from urllib.request import urlopen
from time import time
from dotenv import load_dotenv

import fitz  # + install PyMuPDF

import logging
from bidi.algorithm import get_display
import colorama

from text_summarizer import summarize_text
import subprocess

YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET

def printDX(string, var=""):
    print(string, var)
    sys.stdout.flush()

def getText():
    t0 = time()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    journalDirectory = "Journal"
    DatabaseDirectory = "Database"
    WebDirectory = "Web"
    files_dir = os.path.join(script_dir, "extracted_text/")
    sum_files_dir = os.path.join(script_dir, "summarized_text/")
    id_dir = os.path.join(script_dir, DatabaseDirectory, "id")

    # Create necessary directories if they don't exist
    if not os.path.exists(files_dir):
        os.makedirs(files_dir)

    if not os.path.exists(sum_files_dir):
        os.makedirs(sum_files_dir)

    if not os.path.exists(id_dir):
        os.makedirs(id_dir)

    id = uuid.uuid1()

    parser = argparse.ArgumentParser('Get pdf document from URL')

    parser.add_argument("-u", "--url",
                        default='https://plagprevent.s3.eu-west-3.amazonaws.com/EdLXsfSpi1bi00524a036.pdf',
                        type=str, help="Input: pdf document link")

    # tempo_string = 'https://plagprevent.s3.eu-west-3.amazonaws.com/EdLXsfSpi1bi00524a036.pdf'
    parser.add_argument("-p", "--public", default="private")

    args = parser.parse_args()
    Aurl = args.url
    isPublicAnalysis = args.public == "public"

    printDX('Getting Text from {} ...'.format(Aurl))

    data = urlopen(args.url).read()  # read file from link

    if args.url.endswith(".pdf"):
        doc = fitz.open(stream=data, filetype="pdf")  # open pdf file

        out = open(os.path.join(files_dir, "file{}.txt".format(id)), "wb")

        for page in doc:
            text = page.get_text()
            txt_file = text.replace("\n", " ")
            try:
                out.write(get_display(text.encode("utf8")))
            except:
                out.write(text.encode("utf8"))
            out.write(bytes((12,)))  # separate text into pages

        out.close()
        del doc
    else:
        out = open(os.path.join(files_dir, "file{}.txt".format(id)), "wb")
        out.write(data)
        out.close()

    with open(os.path.join(files_dir, "file{}.txt".format(id)), 'r', encoding="utf8") as f:
        contents = f.read()
        with open(os.path.join(sum_files_dir, "file{}.txt".format(id)), 'w+', encoding="utf8") as file:
            summarized_text = summarize_text(contents)
            # Writing to the file
            file.write("Summary: {}\n".format(summarized_text))


    print(len(contents))
    print(os.path.join(files_dir, "file{}.txt".format(id)))

    if len(contents.split()) <= 500 and not isPublicAnalysis:
        return "0000"
    else:
        # create an empty id file
        pathid = os.path.join(script_dir, DatabaseDirectory, "id", "{}.id".format(id))

        with open(pathid, 'w') as f:
            f.write(args.url)

        t1 = time()
        printDX('got text in  %f' % (t1 - t0))
        return str(id)



if __name__ == '__main__':
    # text_to_summarize = "Under the golden rays of the setting sun, the quaint village came alive with a gentle buzz of activity. Children played joyfully in the cobblestone streets, their laughter echoing through the air. The scent of freshly baked bread wafted from the local bakery, enticing passersby to stop and indulge. Colorful flowers adorned window sills, adding a touch of charm to the rustic houses. Amidst the picturesque scene, the village seemed like a time capsule, preserving the beauty of simpler days while embracing the warmth of a tight-knit community."
    printDX(f"{YELLOW}[*] Extracting:  {RESET}")
    try:
        load_dotenv()
        id = getText()
        print("iiiiiiiiiiiiiiii",id)
        if id is not None:
            printDX('$$$' + id + "$")
            # print("------------------Running script1.py")
            # summarized_text = summarize_text(text_to_summarize)
            # print("Summarized text:", summarized_text)
            # print("------------------Script1.py execution completed.")
        else:
            printDX("An error occurred during extraction.")
    except Exception as e:
        logging.exception("An error occurred during extraction:")
        printDX("An error occurred during extraction:", e)
