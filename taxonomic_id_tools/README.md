
### Function to pull gbif metadata based on input name from csv file
Input csv: requires header "Current_Accepted_Name"
Output csv: "taxa", "gbif_id", "accepted_name", "authorship", "kingdom", "phylum", "order", "family", "genus", "species", "gbif_link", "reference"

Example useage: 
```
source(taxid_registration_tools.R)

get_gbifid_out_verboselin2(csv_file = "new_tax_names_checked.csv", out_file = "new_tax_names_checked.csv")
```

### Function to create taxID registration file for ENA
Input csv: requires headers "accepted_name", "gbif_id", "gbif_link", "reference" (all generated using get_gbifid_out_verboselin2()
Input args: csv_file input filepath, project.name (code as registered with ENA, e.g., PRJEBXXXX), csv_out output filepath 

```
source(taxid_registration_tools.R)

Example usage: create_ena_sheet("new_tax_names_checked.csv", "PRJEBXXXX", "taxid_registration_form.csv") 
```

### Function to create taxID registration file for ENA
Input csv: requires headers "accepted_name", "gbif_id", "gbif_link", "reference" (all generated using get_gbifid_out_verboselin2()
Input args: csv_file input filepath, project.name (code as registered with ENA, e.g., PRJEBXXXX), csv_out output filepath 

Example useage: 
python get_taxids.py -i taxids2check.csv -c Current_Name`

Output: 
(1) csv of Taxonomic_name and taxID only 
(2) csv of null taxIDs (i.e., taxonomic_name with no tax IDs)
(3) csv of original input spreadsheet with taxIDs (where found) added as a new column. 
