<h1> Automatic Speaker Independent Dysarthric Speech Intelligibility Assessment System </h1>

This repository contains the code (selection of 14 words, identifying the optimal set of words) for our Computer Speech and Language paper (2021).
> [Tripathi A, Bhosale S, Kopparapu SK. Automatic speaker independent dysarthric speech intelligibility assessment system. Computer Speech & Language. 2021 Sep 1;69:101213.](https://www.sciencedirect.com/science/article/pii/S0885230821000206)

<h2> Dependencies </h2>

  - Python 3.x

<h2> Setup instructions</h2>

- Install python modules,

```
pip install -r requirements.txt
```

- Intelligibility scores

[csv_dir](csv_dir) contains intelligibility scores for each word using all four proposed approaches. These scores are later used to select an optimal (small) number of utterances that need to be spoken by the dysarthric patient.


<h2> Prune words</h2>

- Based on number of syllables and distance between formants F1 and F2, (_please refer section 5.2_)

```
python prune_words.py --dir csv_dir --ns <num_syllables> --dist <formant_distance>
```
(the intelligibility scores corresponding to the pruned subset are saved as separate csv files in [csv_dir](csv_dir))

- In our experiments we used **ns**=_4_ and **dist**=_2400_, which yields the following pruned set of 14 words:
  - NATURALIZATION
  - AUTOBIOGRAPHY
  - EXACTITUDE
  - IRRESOLUTE
  - INALIENABLE
  - LEGISLATURE
  - OVERSHADOWED
  - PSYCHOLOGICAL
  - DISSATISFACTION
  - AGRICULTURAL
  - APOTHECARY
  - AUTHORITATIVE
  - EXAGGERATE
  - INEXHAUSTIBLE

<h2> Computing the optimal set</h2>

```
python main.py --csv csv_dir/<csv_of_pruned_set> --a1 <a1_value> --a2 <a2_value> --a3 <a3_value>
```
where, <csv_of_pruned_set>: {[csv_dir/I_os_pruned.csv](csv_dir/I_os_pruned.csv), [csv_dir/I_unk_pruned.csv](csv_dir/I_unk_pruned.csv), [csv_dir/I_sm_pruned.csv](csv_dir/I_sm_pruned.csv), [csv_dir/I_ld_pruned.csv](csv_dir/I_ld_pruned.csv)}

_(for a deeper understanding of a1, a2, a3 please refer to Eq. 9)_
 
 - For example, using a1=a2=a3=1 we obtained,

| Method | csv | Pc | optimal words |
| ------ | ------ | ------ | ------ |
| I_os | [csv_dir/I_os_pruned.csv](csv_dir/I_os_pruned.csv) |-0.86 | Autobiography, Overshadowed, Psychological, Dissatisfaction, Agricultural, Inexhaustible |
| DeepSpeech + I_unk | [csv_dir/I_unk_pruned.csv](csv_dir/I_unk_pruned.csv) | 0.94 | Naturalization, Psychological, Dissatisfaction, Agricultural, Apothecary, Authoritative, Inexhaustible |
| DeepSpeech + I_sm | [csv_dir/I_sm_pruned.csv](csv_dir/I_sm_pruned.csv) | 0.94 | Naturalization, Authoritative,Overshadowed, Exactitude, Psychological, Dissatisfaction, Agricultural, Apothecary, Inexhaustible|
| DeepSpeech + I_ld | [csv_dir/I_ld_pruned.csv](csv_dir/I_ld_pruned.csv) | 0.91 | Inexhaustible, Authoritative, Apothecary, Agricultural, Dissatisfaction, Naturalization|

where **Method** denoted the type of intelligibility assessment system, **csv** denotes the name of csv used from [csv_dir](csv_dir) (generated as an output of [prune_words.py](scripts/prune_words.py)), **Pc** stands for Pearson correlation, and the **optimal words** shows the selected subset of words (among the pruned set).
<h2> Citation</h2>

- If you use any of the material in this repository as part of your work, please cite:

```
@article{tripathi2021automatic,
  title={Automatic speaker independent dysarthric speech intelligibility assessment system},
  author={Tripathi, Ayush and Bhosale, Swapnil and Kopparapu, Sunil Kumar},
  journal={Computer Speech \& Language},
  volume={69},
  pages={101213},
  year={2021},
  publisher={Elsevier}
}
```
Last updated: May 03, 2021.


