# Script for extraction of event names from sample

This [script](#extract_event_names) can be used for extracting event names from samples of the OnionCrypter. It is IDAPython script which dumps found event names in `ndjson` format to a result file given as argument.

Script can be run from console with following command:
```
> ida.exe -A -S"path_to_script/script.py \"output_file\"" path_to_sample
```

In a case of scanning multiple samples it is recommended to create other script which will be using command above to automate scanning.
