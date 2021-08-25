# -*- coding: utf-8 -*-
"""
Main file.
"""
import argparse
import configparser
import csv
import logging
import multiprocessing
import os


from coreference.document import Document
from coreference.multipass_resolution import MultiPassResolution
from coreference.sieves.exact_match_sieve import ExactMatchSieve
from coreference.sieves.precise_construct_sieve import PreciseConstructsSieve
from coreference.sieves.relax_modifiers_sieve import StrictHeadRelaxModifiers
from coreference.sieves.relax_inclusion_sieve import StrictHeadRelaxInclusion
from coreference.sieves.strict_head_match_sieve import StrictHeadMatchSieve

# Make sure local files are found even if main.py is
# not executed from root directory of project.
ROOT = os.path.dirname(os.path.abspath(__file__))

# Map config names to sieve classes.
SIEVE_DICT = {"exact_match_sieve": ExactMatchSieve,
              "precise_constructs_sieve": PreciseConstructsSieve,
              "strict_head_match_sieve": StrictHeadMatchSieve,
              "strict_head_relax_modifiers": StrictHeadRelaxModifiers,
              "strict_head_relax_inclusion": StrictHeadRelaxInclusion}

logging.basicConfig(filename=os.path.join(ROOT, "main.log"),
                    level=logging.DEBUG)


def find_language_dir(path, language="english"):
    for root, dirs, files in os.walk(path):
        if language in dirs:
            lang_dir = os.path.join(root, language)
            break
    else:
        logging.error(f"No dir '{language}' found in {path}")
        raise OSError(f"Language Directory {language} not found.")
    return lang_dir


def extract_files(path, ext="gold_conll"):
    file_paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                file_paths.append(os.path.join(root, file))
    if not file_paths:
        logging.warning(f"No files with extension '{ext}' found in {path}.")
    return file_paths


def get_sieves(config_file):
    sieve_key = "Sieves"
    sieves = []
    config = configparser.ConfigParser()
    config.read(config_file)
    if sieve_key not in config.sections():
        raise OSError(f"Invalid config file: Need key '{sieve_key}'")
    for key in config[sieve_key]:
        try:
            sieve = SIEVE_DICT[key]
        except KeyError:
            logging.warning(f"Unknown sieve '{key}' in config file.")
            continue
        else:
            position = config["Sieves"].getint(key)
            if position == -1:
                continue
            sieves.append((sieve(), position))
    sieves.sort(key=lambda x: x[1])
    return list(map(lambda x: x[0], sieves))


def write_eval_summary(path, eval_list):
    if not eval_list:
        return
    sum_doc = len(eval_list)
    avg_recall = sum(recall for _, _, recall, _ in eval_list)/sum_doc
    avg_precision = sum(prec for _, prec, _, _ in eval_list)/sum_doc
    avg_f1 = sum(f1 for _, _, _, f1 in eval_list)/sum_doc
    with open(path, "w", encoding="utf-8", newline="") as file:
        csv_writer = csv.writer(file, delimiter=";")
        csv_writer.writerow(["file", "precision", "recall", "f1-score"])
        csv_writer.writerow(["average", avg_precision, avg_recall, avg_f1])
        for filename, prec, rec, f1 in eval_list:
            csv_writer.writerow([filename, prec, rec, f1])
    logging.info(f"Summary file written to {path}")


def coreference_resolution(file, sieves, path_out):
    doc = Document(file)
    coref = MultiPassResolution(doc, sieves)
    coref.resolve()
    file_name = f"{doc.filename()}.csv"
    coref.to_csv(os.path.join(path_out, file_name))
    prec, rec, f1 = coref.evaluate()
    return (file_name, prec, rec, f1)


def main():
    parser = argparse.ArgumentParser(description="Coreference Resolution")
    parser.add_argument("in_dir", help="Input directory with conll files.")
    parser.add_argument("out_dir", help="Name of output directory.")
    parser.add_argument("--config", nargs="?", default="config.txt")
    parser.add_argument("--ext", nargs="?", default="conll")
    parser.add_argument("--lang", nargs="?", default=None)
    args = parser.parse_args()
    path = os.path.join(ROOT, args.in_dir)
    if args.lang:
        path = find_language_dir(path, args.lang)
    files = extract_files(path, args.ext)
    config_file = os.path.join(ROOT, args.config)
    sieves = get_sieves(config_file)
    path_out = os.path.join(ROOT, args.out_dir)
    if os.path.isdir(path_out):
        raise OSError(f"Output directory {args.out_dir} already exists")
    os.mkdir(path_out)
    eval_list = []
    with multiprocessing.Pool() as pool:
        data = [(file, sieves, path_out) for file in files]
        eval_list.extend(pool.starmap(coreference_resolution, data))
    print(f"Output files written to {path_out}")
    summary_file = os.path.join(path_out, "_summary.csv")
    write_eval_summary(summary_file, eval_list)


if __name__ == "__main__":
    try:
        main()
    except OSError as e:
        print(e)
