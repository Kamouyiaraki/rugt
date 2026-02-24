# Really Useful Genomics CheatSheet


### For dealing with directories:
#### To collapse a directory:
`find . -type f -exec mv -i '{}' . ';'`

`find /dir1 -mindepth 2 -type f -exec mv -i '{}' /dir1 ';'`

#### To delete an empty directory:
```
   files = glob.glob('/YOUR/PATH/*') 
   for f in files: 
     os.remove(f) 
```

#### To find files of a specific pattern in subdirectories and move to a designated dir
`find . -name "Sample*_fastqc.zip" -type f -exec mv {} ./fastqc_dir/ \;`

`find ./Sample* -type f -exec mv {} ./fastqc_reports/ \; `

#### To find files of a specific pattern (e.g., shell scripts) from a parent directory: 

`find ~/scratch/private -name bbmap.sh`


### For changing format to utf-u:

```
iconv -f WINDOWS-1252 -t UTF-8 script.py > tmp.py 
mv tmp.py script.py
```

### For dealing with files
#### Bulk rename pattern in file names
```
for f in *.fastq; do mv "$f" "$(echo "$f" | sed s/pattern/replacement/)"; done
To check if a zipped file is corrupted
       gzip -t output.txt.gz
       if [ $? -eq 0 ]; then
           echo "Gzip file is valid."
       else
           echo "Gzip file is corrupted or invalid."
       fi
```

### For dealing with compressed files:
####Extract only specific files from tarfile

`tar -xzf nonpareil_out.tar.gz --wildcards --no-anchored '.npo'`

#### View files in tarfile without extracting
`tar -tf filename.tar.gz`

#### For faster gzipping:
Run pigz on all files in a directory

`find . -name "*.fastq" -type f -exec pigz {} +`

#### Check if gzip is valid:
`gzip -t final.contigs.fa.gz `
