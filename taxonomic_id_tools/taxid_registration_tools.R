### Function to pull gbif metadata based on input name from csv file
### Input csv: requires header "Current_Accepted_Name"
### Output csv: "taxa", "gbif_id", "accepted_name", "authorship", "kingdom", "phylum", "order", "family", "genus", "species", "gbif_link", "reference"

library(taxize)

get_gbifid_out_verboselin2 <- function(csv_file, out_file){
  
  df<- read.csv(csv_file, header = T)
  taxa <- as.vector(df$Current_Accepted_Name)
  
  gbiftaxID <- data.frame(taxa=taxa, gbif_id=rep(NA,length(taxa)),
                          authorship=rep(NA,length(taxa)),
                          accepted_name=rep(NA,length(taxa)),
                          kingdom=rep(NA,length(taxa)),
                          phylum=rep(NA,length(taxa)),
                          order=rep(NA,length(taxa)),
                          family=rep(NA,length(taxa)),
                          genus=rep(NA,length(taxa)),
                          species=rep(NA,length(taxa)),
                          gbif_link=rep(NA,length(taxa)))
  i<-1
  for(i in 1:length(taxa)){
    
    if(length(gbif_name_usage(name = gbiftaxID$taxa[i])$results) > 0 && length(gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$species) > 0){
      gbiftaxID$gbif_id[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$taxonID
      gbiftaxID$authorship[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$authorship
      gbiftaxID$accepted_name[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$species
      gbiftaxID$kingdom[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$kingdom
      gbiftaxID$phylum[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$phylum
      gbiftaxID$order[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$order
      gbiftaxID$family[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$family
      gbiftaxID$genus[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$genus
      gbiftaxID$species[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$species
      gbiftaxID$gbif_link[i] <- paste0("https://www.gbif.org/species/", gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$key)
    }else{
      gbiftaxID$gbif_id[i] <- NA
      gbiftaxID$accepted_name[i] <- NA
      gbiftaxID$authorship[i] <- NA
      gbiftaxID$kingdom[i] <- NA
      gbiftaxID$phylum[i] <- NA
      gbiftaxID$order[i] <- NA
      gbiftaxID$family[i] <- NA
      gbiftaxID$genus[i] <- NA
      gbiftaxID$species[i] <- NA
      gbiftaxID$gbif_link[i] <- NA
    }
  }
  if(length(gbif_name_usage(name = gbiftaxID$taxa[i])$results) >0 && length(gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$publishedIn)>0) {
    gbiftaxID$reference[i] <- gbif_name_usage(name = gbiftaxID$taxa[i])$results[[1]]$publishedIn
  }else{
    gbiftaxID$reference[i] <- NA
  }
  
  write.csv(unique(gbiftaxID), out_file)
  
}
#Example useage: get_gbifid_out_verboselin2(csv_file = "new_tax_names_checked.csv", out_file = "new_tax_names_checked.csv")


### Function to create taxID registration file for ENA
### Input csv: requires headers "accepted_name", "gbif_id", "gbif_link", "reference" (all generated using get_gbifid_out_verboselin2()
### Input args: csv_file input filepath, project.name (code as registered with ENA, e.g., PRJEBXXXX), csv_out output filepath 

create_ena_sheet() <- function(csv_file, project.name, csv_out){
  df <- read.csv(csv_file, header=T)
  
  f1df <- data.frame(proposed_name = df$accepted_name, 
                     names_type=rep("Published Name", nrow(df)), 
                     host=rep(NA, nrow(df)), 
                     project_id = rep(project.name, nrow(df)),
                     description = paste(df$gbif_link, df$gbif_id, df$reference, sep="; ")
  )
  
  write.csv(f1df, csv_out, row.names = F)
}

#Example usage: create_ena_sheet("new_tax_names_checked.csv", "PRJEBXXXX", "taxid_registration_form.csv") 
