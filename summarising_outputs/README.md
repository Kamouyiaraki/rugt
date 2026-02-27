### summarising BUSCO outputs

A short python script to summarise all BUSCO outputs nested directory. 

**Example usage**
```
python summarise_busco.py --input_dir busco_out/ --output busco_summary.csv
```

### Summarising fastp outputs from JSON

A tool for summarising fastp outputs - originally written for the pipeline https://github.com/museomics/its-fun-2-map but useful as a standalone script!  

**Example usage:** 
```
json2csv(json_dir= "fastp_outdir", out_name = "json2csv_output.csv")
```
