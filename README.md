# Coreference-Resolution

# How to use
Move your directory containing conll-files into this directory.
<br>
Run:<br>
```main.py [-h] [--config [CONFIG]] [--ext [EXT]] [--lang [LANG]] in_dir out_dir```<br>

+ `in_dir`: The directory containing the conll files from the Ontonotes corpus. Subdirectories will also be searched.
+ `out_dir`: A name for the directory where output files should be stored.
+ `--config`: The name of the config file where sieves are specified. This defaults to `config.txt`.
+ `--ext`: The extension files should have. This defaults to `conll`. If you only want to extract gold annotated file, set this to `gold_conll`.
+ `--lang`: A subdirectory in `in_dir` from which files should be extracted. Set this to `english` to only extract english files from nested Ontonotes corpus.

## Adjust Sieves
The sieves and their order are specified in `config.txt`. The values specify the order in which the sieves are applied.
To exclude a sieve, set its value to -1.<br>
Example:<br>
```
[Sieves]
Exact_Match_Sieve = 1
Precise_Constructs_Sieve = 2
Strict_Head_Match_Sieve = 3
Strict_Head_Relax_Modifiers = 4
Strict_Head_Relax_Inclusion = -1
```

## Interpret Output
For each document from which coreference information was extracted, there is one file in the output folder. The first line contains the path to the original file.
After that follow clusters of coreferential mentions. Clusters are seperated by `-;-`. Each line in a cluster represents a mention. The first column is a 3-tuple where the 
first element is the index of the sentence in which the mention appears in the document. The second element is the start index, the third the end index of the mention
in the respective sentence. The second column is the string of the mention.<br>
Example: <br>
```
path/to/example/file.conll
(1,2,3);man
(4,5,6);he
-;-
(7,8,9);dog
(10,11,12);it
```
<br>
Additionally, the output directory contains a file `_summary.csv` that lists the evaluation metrics precision, recall and f1 for each file.
