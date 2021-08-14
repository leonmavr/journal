# diary
## Description
This repository contains reference notes on different topics such as computer vision, machine learnig etc. Explaining things to yourself is the best way to learn, plus I want to use these as reference without having to google stuff.

## Repository structure
Each topic is readable from one pdf and its Latex source is provided.
```
[topic1]
|
+--+ [sub-topic1]
|    |
|    +--+ [sub-sub-topic1]
|         |
|         +--+ Latex files +---+ src
|         |                |
|         +--+ pdf         +---+ img
|                          |
|                          +---+ tikz
|
+--+ [sub-topic2]
|
...
|
[topic2]
...
```

## Instructions
Each topic can be read from its pdf file. Notes follow the note-taking template. For Latex, the bibliography backend is `bibtex` and they should be able to be compiled by:
```
$ python compile.py <file_name_without_extension>
```
If warnings should be ignored, then the following can be used:
```
$ yes "" | python compile.py <file_name_without_extension>
```
