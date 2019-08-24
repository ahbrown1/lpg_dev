# LPG List processor


## Pre-process converted list before submitting to ID

This will divide input into bite-size chunks for import to ID  (default size is 250 records)
The input must already be in format acceptable for ID import

Each generated CSV will have no duplicate addresses, ensuring what gets exported
for ITI mailing contains the same number of records


## General Procedure

*** Join lists
To generate CSVs that will send to out of state'rs 1st

./csvcat <out_of state>.csv  <in_state.csv>   > result.csv

Or generally ./csvcat <furthest_away>.csv <next_closer>.csv .... <closest>.csv > result.csv

( or whatever priority strategy is in effect )

*** Remove duplicate owner mailing addresses
./dedup result.csv       # modifies in-place

export LPG_BACKLOG = <target directory>
./blproc result.csv      # generate importable chunks
