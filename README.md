# mongodb_util #

## Demo/POC and Utility Code for working with MongoDB

### Bookings
*Generates synthetic data for a hospitality booking system*

### Clinical
*Generates synthetic data and performance queries for clinical/EMR data*
The loader uses the faker library to generate a synthetic document that represents a simplified EMR document.  The document has some attributes and 3 large text fields (illness_history, assessment and mentions).  Each one contains a paragraph of random sentences (mentions is actually an array of sentences).  This generates about a 1-2k document.  Then there are arrays of medical terms (in clinical_queries).  Medical terms are randomly mixed in groups of three to make a fake disease, for the frequency of 1/dilution_factor, the 'disease' and fragments of the disease will be sprinkled into the the paragraph text.  This will create a dataset where the frequency of disease terms can be controlled to measure full-text searching efficiency.

There are 4 files in the system:
  bbutil.py - utility module for logging and file handling etc
  clinical_setting.json - settings credentials etc to run the loader
  clinical_queries.py - MongoDB queries and aggregations to run for performance testing
  clinical_loader.py - data generation and query code

#### Personalizing:
  Change the uri, username/password, database and collection in the settings file to point to your Atlas database.

#### Loader Parameters:
  process_count - the number of parallel process threads to run
  batch_size - the number of records for each bulk insert
  batches - yep, the number of batches
  
  *The total documents loaded will be batch_size * batches * process_count*
  dilution_factor - adds disease terms every xx documents

#### Run parameters:
You can run the loader like this, there are several different optional parameters:

  `python3 clinical_loader.py action=emr_data wait=12000 file=yes label=60mload`
In this invocation, its running emr_data (the loader), its going to wait 12000 seconds to start, log output to a file and add a field called label with the value 60mload.  Alternatively, it could have been:

  `python3 clinical_loader.py action=emr_data`

#### Performing Queries:
Build queries to be performed in the clinical_queries file, then add the queries as batches in the 'batches' variable.  To invoke the queries:

  `python3 clinical_loader.py action=perf batch=5x-lucene`
this will run all the queries in the batch entry called 5x-lucene. There are some other optional parameters to enter as well:

  `python3 clinical_loader.py action=perf batch=5x-lucene iters=3, preference=secondaryPreferred`
this will run the batch queries 3 times and will use secondary nodes for the analytic work.
