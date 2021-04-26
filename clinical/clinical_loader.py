import sys
import os
import csv
#import vcf
from collections import OrderedDict
import json
import datetime
import random
import time
import re
import multiprocessing
import pprint
import getopt
import bson
from bson.objectid import ObjectId
from bbutil import Util
import clinical_queries as cc
#import pysam
from pymongo import MongoClient
from faker import Faker

fake = Faker()
settings_file = "loader_settings.json"

def synth_data_load():
    # read settings and echo back
    bb.message_box("Loading Data", "title")
    bb.logit(f'# Settings from: {settings_file}')
    # Spawn processes
    num_procs = settings["process_count"]
    bb.logit(f'# Launching: {num_procs} processes')
    jobs = []
    inc = 0
    multiprocessing.set_start_method("fork", force=True)
    for item in range(num_procs):
        p = multiprocessing.Process(target=worker_emr_sample, args = (item,))
        jobs.append(p)
        p.start()
        time.sleep(1)
        inc += 1

    main_process = multiprocessing.current_process()
    bb.logit('Main process is %s %s' % (main_process.name, main_process.pid))
    for i in jobs:
        i.join()

def worker_emr_sample(ipos):
    #  Reads EMR sample file and finds values
    conn = client_connection()
    bb.message_box("Loading Synth EMR Data", "title")
    batch_size = settings["batch_size"]
    batches = settings["batches"]
    dilution_factor = settings["dilution_factor"]
    cur_process = multiprocessing.current_process()
    bb.logit('Current process is %s %s' % (cur_process.name, cur_process.pid))
    file_log(f'New process {cur_process.name}')
    start_time = datetime.datetime.now()
    collection = settings["collection"]
    db = conn[settings["database"]]
    id_num = settings["base_counter"] + (ipos * batch_size * batches)
    add_disease = True
    if "clean" in ARGS:
        add_disease = False
    bulk_docs = []
    cnt = 0
    tot = 0
    for batch in range(batches):
        somethini = "ooo"
        cycler = 0
        for inc in range(batch_size):
            #print(record.FORMAT)
            if not "clean" in ARGS:
                if cycler == 0:
                    add_disease = True
                elif cycler == dilution_factor:
                    cycler = -1
                else:
                    add_disease = False
            year = random.randint(2017,2020)
            month = random.randint(1,12)
            day = random.randint(1,28)
            patient_id = f"emr-{ipos}-{id_num}"
            name = fake.name()
            dr = fake.name()
            age = random.randint(28,84)
            doc = OrderedDict()
            doc['patient_id'] = patient_id
            doc['consultation_date'] = datetime.datetime(year,month,day, 10, 45)
            doc['referring_physician'] = dr
            doc['patient'] = name
            doc["age"] = age
            if add_disease:
                dogma = instant_history(name, age)
            else:
                dogma = instant_clean(name, age)
            doc["disease"] = dogma["disease"]
            doc['illness_history'] = dogma["history"]
            doc['mentions'] = dogma["mentions"]
            doc['assessment'] = dogma["assessment"]
            doc['version'] = "1.0"
            if "label" in ARGS:
                doc["label"] = ARGS["label"]
            #pprint.pprint(doc)
            bulk_docs.append(doc)
            cnt += 1
            tot += 1
            id_num += 1
            cycler += 1

        db[collection].insert_many(bulk_docs)
        bulk_docs = []
        cnt = 0
        bb.logit(f"{cur_process.name} Inserting Bulk, Total:{tot}")
        file_log(f"{cur_process.name} Inserting Bulk, Total:{tot}")
        #oktogo = checkfile()
        #if not oktogo:
        #    bb.logit("Received stop signal")
        #    break
    end_time = datetime.datetime.now()
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds()
    conn.close()
    file_log(f"{cur_process.name} - Bulk Load took {execution_time} seconds")
    bb.logit(f"{cur_process.name} - Bulk Load took {execution_time} seconds")

def instant_history(person, age):
    result = {}
    parts = disease_maker()
    disease = f'{parts[0]}{parts[1]}_{parts[2]}'
    result["disease"] = disease
    result["mentions"] = [paragraph_sprinkle(parts,2),paragraph_sprinkle(parts,2),paragraph_sprinkle(parts,2), paragraph_sprinkle(parts,3)]
    result["history"] = f"The patient ({person}) is a ({age})-year-old who was recently diagnosed with {disease} {paragraph_sprinkle(parts, 6)}"
    result["assessment"] = f"Continue therapies with {person} for {paragraph_sprinkle(parts,6)}"
    return result

def instant_clean(person, age):
    result = {}
    result["disease"] = "no disease"
    result["mentions"] = [fake.paragraph(2),fake.paragraph(2),fake.paragraph(2), fake.paragraph(3)]
    result["history"] = f"The patient ({person}) is a ({age})-year-old who was recently diagnosed with nothing {fake.paragraph(6)}"
    result["assessment"] = f"Continue therapies with {person} for {fake.paragraph(6)}"
    return result

def disease_maker():
    part1 = random.choice(cc.lexicon)
    part2 = random.choice(cc.lexicon)
    part3 = random.choice(cc.lexicon)
    return([part1,part2,part3])

def paragraph_sprinkle(items,numtodo):
    para = fake.paragraph(numtodo)
    words = para.split(" ")
    size = len(words)
    items.append(f'{items[0]}{items[1]}')
    items.append(f'{items[1]}_{items[2]}')
    for k in range(4):
        ipos = random.randint(0,size)
        words.insert(ipos, random.choice(items))
    newpara = " ".join(words)
    return(newpara)

def emr_annotate():
    bb.message_box("Loading EMR Annotations", "title")
    batch_size = settings["batch_size"]
    start_time = datetime.datetime.now()
    collection = settings["collection"]
    conn = client_connection()
    db = conn[settings["database"]]
    inc = 0
    interval = 20
    pipe = [
        { "$sample": { "size": 10000}}
    ]
    cursor = db[collection].aggregate(pipe)
    for adoc in cursor:
        notes = []
        fname = adoc["patient"].split(" ")[0]
        lname = adoc["patient"].split(" ")[1]
        addr = {}
        addr["address1"] = fake.street_address()
        addr["address2"] = ""
        addr["city"] = fake.city()
        addr["state"] = fake.state()
        addr["zipcode"] = fake.zipcode()
        year = 2021 - adoc["age"]
        month = random.randint(1,12)
        day = random.randint(1,28)
        patient_details = {
            "first_name" : fname,
            "last_name" : lname,
            "email" : f'{fname}.{lname}@xfinity.com',
            "phone" : fake.phone_number(),
            "address" : addr,
            "birth_date" : datetime.datetime(year,month,day, 10, 45),
            "marital_status" : random.choice(["married", "single","widowed"]),
            "gender" : random.choice(["male","female"]),
            "language" : random.choice(["English", "Spanish","French","Farsi","English","Portugese","English","English"])
        }
        problems = [
            "DIABETES MELLITUS (ICD-250.)",
            "HYPERTENSION, BENIGN ESSENTIAL (ICD-401.1)",
            "DEPRESSION (ICD-311)",
            "RETINOPATHY, DIABETIC (ICD-362.0)",
            "POLYNEUROPATHY IN DIABETES (ICD-357.2)"
        ]
        medications = [
            {"name" : "HYTRIN CAP 5MG (TERAZOSIN HCL) 1 po qd", "last_refill" : "#30 x 2", "provider" : fake.name()},
            {"name" : "Metaprolol 5MG 1 po qd", "last_refill" : "#60 x 1", "provider" : fake.name()},
            {"name" : "Lipitor 20MG (Atorvastatin) 1 po qd", "last_refill" : "#30 x 2", "provider" : fake.name()},
            {"name" : "Apririn 85MG 1 po qd", "last_refill" : "N/A", "provider" : "N/A"}
        ]
        review = {
            "General" : "denies fatigue, malaise, fever, weight loss",
            "Eyes" : "denies blurring, diplopia, irritation, discharge",
            "Ear_nose_throat" : "denies ear pain or discharge, nasal obstruction or discharge, sore throat",
            "Cardiovascular" : "denies chest pain, palpitations, paroxysmal nocturnal dyspnea, orthopnea, edema Respiratory: denies coughing, wheezing, dyspnea, hemoptysis",
            "Gastrointestinal" : "denies abdominal pain, dysphagia, nausea, vomiting, diarrhea, constipation",
            "Genitourinary" : "denies hematuria, frequency, urgency, dysuria, discharge, impotence, incontinence",
            "Musculoskelital" : "denies back pain, joint swelling, joint stiffness, joint pain",
            "Psychiatric" : "denies depression, anxiety, mental disturbance, difficulty sleeping, suicidal ideation, hallucinations",
            "Skin" : "denies rashes, itching, lumps, sores, lesions, color change",
            "Neurologic" : "denies syncope, seizures, transient paralysis, weakness, paresthesias",
            "Allergic" : "denies urticaria, hay fever, frequent UTIs; denies HIV high risk behaviors"
        }
        db[collection].update_one({"_id": adoc["_id"]},{"$set": {"version" : "1.2", "patient_details" : patient_details, "problems" : problems, "medications" : medications, "review_of_symptoms" : review}})
        if inc % interval == 0:
            bb.logit(f"Updating: {inc} completed")
        inc += 1
    bb.logit(f"All done - {inc} completed")

def check_file(type = "delete"):
    #  file loader.ctl
    ctl_file = "loader.ctl"
    result = True
    with open(ctl_file, 'w', newline='') as controlfile:
        status = controlfile.read()
        if "stop" in status:
            result = False
    return(result)

def file_log(msg):
    if not "file" in ARGS:
        return("goody")
    ctl_file = "run_log.txt"
    cur_date = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    stamp = f"{cur_date}|I> "
    with open(ctl_file, 'a') as lgr:
        lgr.write(f'{stamp}{msg}\n')

#  Queries for EMR

def build_query(conn, query_params):
    pipe = query_params["query"]
    coll = settings["collection"]
    if "collection" in query_params:
        coll = query_params["collection"]
    docs = 0
    if query_params["type"] == "agg":
        cursor = conn[coll].aggregate(pipe)
    if query_params["type"] == "find":
        if "limit" in query_params:
            cursor = conn[coll].find(pipe).limit(query_params["limit"])
        elif "project" in query_params:
            bb.logit(f'Query: {pipe}')
            bb.logit(f'Project: {query_params["project"]}')
            if "limit" in query_params:
                cursor = conn[coll].find(pipe,query_params["project"]).limit(query_params["limit"])
            else:
                cursor = conn[coll].find(pipe,query_params["project"])
        elif "count" in query_params:
            cursor = conn[coll].count_documents(pipe)
        else:
            cursor = conn[coll].find(pipe)
    return(cursor)

def query_list(items, db):
    #bb.logit(f'Performing: {item}')
    for item in items:
        start = datetime.datetime.now()
        if not item in cc.queries:
            bb.logit(f"Cant find: {item} skipping")
            continue
        details = cc.queries[item]
        output = build_query(db,details)
        bulker = []
        bulk_cnt = 0
        docs = 0
        if "count" in details:
            docs = output
        else:
            for k in output:
                #print(k)
                bulker.append(k)
                if "numrecords" in k:
                    docs = k["numrecords"]
                else:
                    docs += 1
                    if (docs % 1000) == 0:
                        print(f'{docs}.', end="", flush=True)
                        if bulk_cnt > 20:
                            bb.file_log(pprint.pformat(bulker),"new")
                            bulk_cnt = 0
                        else:
                            bb.file_log(pprint.pformat(bulker))
                            bulk_cnt += 1
                        bulker = []

        end = datetime.datetime.now()
        elapsed = end - start
        secs = (elapsed.seconds) + elapsed.microseconds * .000001
        bb.logit(f"Performing {item} - Elapsed: {format(secs,'f')} - Docs: {docs}")
        bb.logit(f'Operation: {details["type"]}, Query:')
        bb.logit(details["query"])
        bb.logit("------------------------------------")

def perf_stats():
    iters = 1
    bb.message_box("Query Performance", "title")
    ctype = "uri"
    pref = "secondaryPreferred"
    items = [
        "simple"
    ]
    if "batch" in ARGS:
        batch = ARGS["batch"]
        items = cc.batches[batch]
    if "iters" in ARGS:
        iters = int(ARGS["iters"])
    if "url" in ARGS:
        ctype = ARGS["url"]
    if "preference" in ARGS:
        pref = ARGS["preference"]
    conn = client_connection(ctype, {"readPreference" : pref})
    db = conn[settings["database"]]
    for k in range(iters):
        query_list(items, db)
    bb.logit("-- Complete --")

def load_query():
    # read settings and echo back
    bb.message_box("Performing 10000 queries in 7 processes", "title")
    num_procs = 7
    jobs = []
    inc = 0
    multiprocessing.set_start_method("fork", force=True)
    for item in range(num_procs):
        p = multiprocessing.Process(target=run_query)
        jobs.append(p)
        p.start()
        time.sleep(1)
        inc += 1

    main_process = multiprocessing.current_process()
    for i in jobs:
        i.join()

def run_query():
    cur_process = multiprocessing.current_process()
    bb.logit('Current process is %s %s' % (cur_process.name, cur_process.pid))
    bb.logit("Performing 5000 queries")
    conn = client_connection()
    db = conn[settings["database"]]
    num = len(cc.lexicon)
    cnt = 0
    for k in range(int(5000/num)):
        for term in cc.lexicon:
            start = datetime.datetime.now()
            output = db.emr.find({"disease" : {"$regex" : f'^{term}.*'}}).count()
            if cnt % 100 == 0:
                end = datetime.datetime.now()
                elapsed = end - start
                secs = (elapsed.seconds) + elapsed.microseconds * .000001
                bb.logit(f"{cur_process.name} - Query: Disease: {term} - Elapsed: {format(secs,'f')} recs: {output} - cnt: {cnt}")
            cnt += 1
            #time.sleep(.5)

def client_connection(type = "uri", details = {}):
    mdb_conn = settings[type]
    username = settings["username"]
    password = settings["password"]
    if "username" in details:
        username = details["username"]
        password = details["password"]
    mdb_conn = mdb_conn.replace("//", f'//{username}:{password}@')
    bb.logit(f'Connecting: {mdb_conn}')
    if "readPreference" in details:
        client = MongoClient(mdb_conn, readPreference=details["readPreference"]) #&w=majority
    else:
        client = MongoClient(mdb_conn)
    return client

#------------------------------------------------------------------#
#     MAIN
#------------------------------------------------------------------#
if __name__ == "__main__":
    bb = Util()
    ARGS = bb.process_args(sys.argv)
    settings = bb.read_json(settings_file)
    if "wait" in ARGS:
        interval = int(ARGS["wait"])
        if interval > 10:
            bb.logit(f'Delay start, waiting: {interval} seconds')
            time.sleep(interval)
    #conn = client_connection()
    if "action" not in ARGS:
        print("Send action= argument")
        sys.exit(1)
    elif ARGS["action"] == "emr_annotate":
        emr_annotate()
    elif ARGS["action"] == "emr_data":
        synth_data_load()
    elif ARGS["action"] == "perf":
        perf_stats()
    elif ARGS["action"] == "queries":
        load_query()
    else:
        print(f'{ARGS["action"]} not found')
    #conn.close()
