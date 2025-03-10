# Protein_Data_Analyzation
## Imported the Protein Dataset of A.Thaliana from uniprot.org(Dataset of Reviewed and Unreviewed)
Labeled Protein- Protein haivng Enzyme Commission (EC) Number.
Unlabeled Protein- Protein not having the EC number.

## Imported the .tsv file into MongoDB
Queries to understand the dataset and to count labeled and unlabeled etc.
The raw data has interpro domain as one string, so using python splitting into different strings are made using Domain in One.py
and output as Domain_in_One.csv
For finding the similarity between the proteins we have used the Jaccard Similarity Function as mentioned in the project2024.pdf, Relations2.py used for output Jaccard_Data.csv
 Total 3 files were imported in MongoDB and used for retrieving the information.
 ## Graph Construction in Neo4j
 Firstly create Nodes>>Create Indices>>Link them to Attributes of Domain_in_One>>Create Relationships(Using Pthon because Time efficient---Batching.py(ctrl+c after the rows are done from Jaccard_Data ~1048567))
 Then display graph for Neighbouring proteins.
 For Annotation part, we should predict the EC number of Unlabeled Protein by the similarity analysis)
 ## GUI
 Created the website using Python, installed the packages required.
 Then app_new.py, index.html, statistics.html used to create a website integrating MongoDB and Neo4J through Python.
 
