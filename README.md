# RuthLemm

RuthLemm is a transformer BART-based lemmatizer for Ruthenian language. With its help, you can lemmatize treebanks in the Universal Dependencies format (UD).

## Installation

1. Clone this repo: `git clone https://github.com/Futyn-Maker/RuthLemm.git`;
2. Move to the repo folder: `cd RuthLemm`;
3. Install dependencies: `pip3 install -r requirements.txt

## Usage

Ruthlemm is a command line utility. As the first argument, it takes the path to the file in the `.conllu` format, and as the second argument - the path to the output file where the lemmatized corpus will be written.

The `--morphology` (`-m`) flag is also available - set it if your data contains morphological markup and you want to improve lemmatization by using it.

## Examples

`python -m ruthlemm in.conllu out.conllu` - lemmatizes the corpus in `in.conllu` without relying on morphological markup and writes the data in `out.conllu`.

`python -m ruthlemm -m in.conllu out.conllu` - lemmatizes the corpus in `in.conllu`, using morphology information, and writes the data to 'out.conllu'.
