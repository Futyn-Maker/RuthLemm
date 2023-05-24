from itertools import cycle
import random
import argparse

from simpletransformers.seq2seq import Seq2SeqModel
import pandas as pd


random.seed = 42

def load_conllu_dataset(datafile, join=False):
    arr = []
    with open(datafile, encoding='utf-8') as inp:
        strings = inp.readlines()
    for s in strings:
        if (s[0] != "#" and s.strip()):
            split_string = s.split('\t')
            if split_string[1] == "(" or split_string[1] == ")" or split_string[1] == "[" or split_string[1] == "]":
                form = split_string[1]
            else:
                form = split_string[1].replace("(", "").replace(")", "").replace("[", "").replace("]", "")
            if split_string[3] != "PROPN":
                form = form.lower()
            else:
                form = form.capitalize()
            lemma = split_string[2]
            if split_string[3] == "PROPN":
                lemma = lemma.capitalize()
            if join:
                inpt = form + " " + split_string[3] + " " + split_string[5]
            else:
                inpt = form
            pos = split_string[3]
            arr.append([inpt, lemma, pos])
    return pd.DataFrame(arr, columns=["input_text", "target_text", "pos"])

def predict(in_file, out_file, join=False):
    if join:
        model_name = "Futyn-Maker/RuthLemm-morphology"
    else:
        model_name = "Futyn-Maker/RuthLemm"

    model = Seq2SeqModel(
        encoder_decoder_type="bart",
        encoder_decoder_name=model_name,
        use_cuda=False
    )

    pred_data = load_conllu_dataset(in_file, join=join)["input_text"].tolist()
    predictions = cycle(model.predict(pred_data))

    with open(in_file, encoding="utf8") as inp:
        strings = inp.readlines()
    predicted = []
    for s in strings:
        if (s[0] != "#" and s.strip()):
            split_string = s.split("\t")
            split_string[2] = next(predictions)
            joined_string = "\t".join(split_string)
            predicted.append(joined_string)
            continue
        predicted.append(s)

    with open(out_file, "w", encoding="utf8") as out:
        out.write("".join(predicted))

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Path to the input file")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    parser.add_argument("--morphology", "-m", action="store_true", help="Use morphology")

    args = parser.parse_args()
    predict(args.input_file, args.output_file, args.morphology)
    print("All done!")
