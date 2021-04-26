# Queries to perform
import re
batches = {
    "simple" : ["activitiesResearch-simple"],
    "single-lucene" : [
        "lucene-creatininewhite"
    ],
    "5x-lucene" : [
        "lucene-creatininewhite",
        "lucene-arrcreatininewhite",
        "lucene-whiteteal_neurodegenerative",
        "lucene-Interleukin-10hypothyroidism_violet",
        "lucene-cholesterol18F-fluoromisonidazole"
    ],
    "6x-stringindex" : [
        "Interleukin-10hypothyroidism_violet-ary",
        "2-term_Interleukin-10-ary",
        "3-term_Interleukin-10-ary",
        "Interleukin-10hypothyroidism_violet-txt",
        "2-term_Interleukin-10-txt",
        "3-term_Interleukin-10-txt"
        ]
}

lexicon = [
    "red", "purple", "violet", "rose", 'pink', "black", "white", "navy",
    "blue", "aqua", "periwinkle", "blk", "grey", 'mauve', "taupe", "charcoal",
    "yellow", "green", "teal", "sand", "brown", "orchre", "sienna", "umber",
    "bronchovascular", "supraclavicular", "lymphadenopathy", "Oropharynx", "auscultation", "Creatinine", "hypercoaguability", "M2-haplotype", "Annexin-A5",
    "myocardial", "hyperlipidemia", "cholesterol", "Glucovance", "homocysteine", "cytogenetic", "IL10RA", "IL10RB", "leukemia", "epigenetic", "mononuclear",
    "neurodegenerative", "microcephaly", "dysmorphism", "Interleukin-10", "hypothyroidism", "Duchene muscular dystrophy", "prostatetic", "serotonin", "tri-amide",
    "pancreatobiliary", "anemia", "thyromegaly", "2-carbonyl","cyanosis","3-methylcrotonyl-coa_carboxylase_deficiency",
    "hydrochlorothiazide", "hepatosplenomegaly", "carcinoma", "invasive","2-methoxyestradiol","18F-fluoromisonidazole"
]

terms = {
    "Creatininewhite" : ["Creatinine","white","dysmorphism"],
    "myocardialanemia" : ["myocardial","anemia","2-methoxyestradiol"],
    "Interleukin-10" : ["Interleukin-10","purple","auscultation"],
    "neurodegenerative" : ["neurodegenerative","2-carbonyl","invasive"],
    "M2-haplotype" : ["M2-haplotype","prostatetic","cholesterol"]
}

fillers = ["investment", "citizen", "couple", "management", "husband", "various", "reveal", "without", "continue"]

regex_filler = [
    {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*1\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : 'mccd,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*2\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : 'mccd,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : '\bmgca1', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : '\bmgca3', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : '3[-\s]*methylglutaconic\s+aciduria,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
    {"regex" : {"query" : '\bmgca4', "path" : "mentions", "allowAnalyzedField": True}}
]

# Create Queries to be executed in the performance tests
queries = {
    "base_query": {"type" : "agg","query" :
        [
          {"$search": {
            "compound" : {
              "should" : [
                  {"regex" : {"query" : "__TERM__", "path" : "illness_history", "allowAnalyzedField": True}},
                ]
            }
          }},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "creatininewhite", "illness_history": 1}}
        ]
        },
    "lucene-creatininewhite": {"type" : "agg", "query" :
        [
          {"$search": {
            "compound" : {
              "should" : [
                  {"regex" : {"query" : "Creatinine(\s|-)+white", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "white(\s|_)+dysmorphism", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "white_dysmorphism", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*1\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*2\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca1', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca3', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*methylglutaconic\s+aciduria,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca4', "path" : "mentions", "allowAnalyzedField": True}}
                ]
            }
          }},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "creatininewhite", "illness_history": 1}},
          {"$count": "numrecords"}
        ]
        },
    "lucene-arrcreatininewhite": {"type" : "agg", "query" :
        [
          {"$search": {
            "compound" : {
              "should" : [
                  {"regex" : {"query" : "Creatinine(\s|-)+white", "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "white(\s|_)+dysmorphism", "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "white_dysmorphism", "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*1\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*2\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca1', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca3', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*methylglutaconic\s+aciduria,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca4', "path" : "mentions", "allowAnalyzedField": True}}
                ]
            }
          }},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "creatininewhite", "illness_history": 1}},
          {"$count": "numrecords"}
        ]
        },
    "index-creatininewhite" : {"type" : "agg", "query" :
        [
          {"$match": {"mentions" : {"$in":
            [
                re.compile("Creatinine(\s|-)+white"),
                re.compile("white(\s|_)+dysmorphism"),
                re.compile("white_dysmorphism")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "hyromegaly_2-methoxyestradio", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "lucene-cholesterol18F-fluoromisonidazole": {"type" : "agg", "query" :
        [
          {"$search": {
            "compound" : {
              "should" : [
                  {"regex" : {"query" : "cholesterol18F(\s|-)+fluoromisonidazole", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "fluoromisonidazole(\s|_)+ochre", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "fluoromisonidazole_orchre", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*1\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*2\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca1', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca3', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*methylglutaconic\s+aciduria,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca4', "path" : "mentions", "allowAnalyzedField": True}}
                ]
            }
          }},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "cholesterol18F-fluoromisonidazole", "illness_history": 1}},
          {"$count": "numrecords"}
        ]},
    "lucene-Interleukin-10hypothyroidism_violet": {"type" : "agg", "query" :
        [
          {"$search": {
            "compound" : {
              "should" : [
                  {"regex" : {"query" : "Interleukin-10(\s|-)+hypothyroidism", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "hypothyroidism(\s|_)+violet", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "hypothyroidism_violet", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*1\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*2\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca1', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca3', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*methylglutaconic\s+aciduria,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca4', "path" : "mentions", "allowAnalyzedField": True}}
                ]
            }
          }},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "illness_history": 1}},
          {"$count": "numrecords"}
        ]},
    "lucene-whiteteal_neurodegenerative": {"type" : "agg", "query" :
        [
          {"$search": {
            "compound" : {
              "should" : [
                  {"regex" : {"query" : "white(\s|-)+teal", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "teal(\s|_)+neurodegenerative", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : "teal_neurodegenerative", "path" : "illness_history", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*1\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '(3[-\s]*)?methylcrotonyl[-\s]*coa\s+carboxylase\s*2\s+deficiency', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'mccd,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : 'methylcrotonylglycinuria,?\s*type\s*(2|ii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca1', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(1|i)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca3', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*methylglutaconic\s+aciduria,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '3[-\s]*mgca,?\s*type\s*(3|iii)\b', "path" : "mentions", "allowAnalyzedField": True}},
                  {"regex" : {"query" : '\bmgca4', "path" : "mentions", "allowAnalyzedField": True}}
                ]
            }
          }},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "whiteteal_neurodegenerative", "illness_history": 1}},
          {"$count": "numrecords"}
        ]},
    "txt-creatininewhite" : {"type" : "agg", "query" :
        [
          {"$match": {"illness_history" : {"$in":
            [
                re.compile("Creatinine(\s|-)+white"),
                re.compile("white(\s|_)+dysmorphism"),
                re.compile("white_dysmorphism")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "hyromegaly_2-methoxyestradio", "illness_history": 1}},
          {"$count": "numrecords"}
        ]},
    "Interleukin-10hypothyroidism_violet-ary" : {"type" : "agg", "query" :
        [
          {"$match": {"mentions" : {"$in":
            [
                re.compile("Interleukin-10hypothyroidism(\s|_)+violet")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "2-term_Interleukin-10-ary" : {"type" : "agg", "query" :
        [
          {"$match": {"mentions" : {"$in":
            [
                re.compile("Interleukin-10hypothyroidism_violet"),
                re.compile("Interleukin-10hypothyroidism")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "3-term_Interleukin-10-ary" : {"type" : "agg", "query" :
        [
          {"$match": {"mentions" : {"$in":
            [
                re.compile("Interleukin-10hypothyroidism_violet"),
                re.compile("Interleukin-10hypothyroidism"),
                re.compile("hypothyroidism(\s|_)+violet")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "Interleukin-10hypothyroidism_violet-txt" : {"type" : "agg", "query" :
        [
          {"$match": {"illness_history" : {"$in":
            [
                re.compile("Interleukin-10hypothyroidism(\s|_)+violet")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "2-term_Interleukin-10-txt" : {"type" : "agg", "query" :
        [
          {"$match": {"illness_history" : {"$in":
            [
                re.compile("Interleukin-10hypothyroidism_violet"),
                re.compile("Interleukin-10hypothyroidism")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "3-term_Interleukin-10-txt" : {"type" : "agg", "query" :
        [
          {"$match": {"illness_history" : {"$in":
            [
                re.compile("Interleukin-10hypothyroidism_violet"),
                re.compile("Interleukin-10hypothyroidism"),
                re.compile("hypothyroidism(\s|_)+violet")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "regex_fragment" : {"type" : "agg", "query" :
        [
          {"$match": {"illness_history" : {"$in":
            [
                re.compile("Interleukin-10hypothyroidism_violet"),
                re.compile("Interleukin-10hypothyroidism"),
                re.compile("hypothyroidism(\s|_)+violet")
              ]
          }}},
          {"$project": {"patient_id": 1, "referring_physician": 1, "age": 1, "term": "Interleukin-10hypothyroidism_violet", "mentions": 1}},
          {"$count": "numrecords"}
        ]},
    "update-mention" : {"type" : "update", "query" :
        {"mentions": re.compile('^Support\saffect')}, "update" : {"$set" : {"version" : "1.1"}}
    },
    "escapeslash" : {"type" : "agg", "query" :
    [
    {"$search": {
      "compound" : {
        "should" : [
            {"regex" : {"query" : "Creatinine(\\s|-)+white", "path" : "illness_history", "allowAnalyzedField": True}},
          ]
      }
    }},
    {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "creatininewhite", "illness_history": 1}},
    {"$count": "numrecords"}
    ]},
#    Find me all the patients with hypertention and a total cholesterol greater than 190 who are over 55 years old
    "emr_sample": {"type" : "agg", "query" :
        [
          {"$match": {"version" : "1.2","medications.name" : "Lipitor"}},
          {"$project": {"score": {"$meta": "searchScore"},"patient_id": 1, "referring_physician": 1, "age": 1, "term": "whiteteal_neurodegenerative", "illness_history": 1}},
          {"$count": "numrecords"}
        ]}
}
