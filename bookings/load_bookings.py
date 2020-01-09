#!/usr/bin/env python3
##
# Script to load booking information
##
import sys
import random
import time
import datetime
import random
import pymongo
import multiprocessing
import faker
import json
import uuid
import bbhelper as bb
from bson.objectid import ObjectId
from collections import OrderedDict
from faker import Faker
#from datetime import datetime
from pymongo import MongoClient

fake = Faker()
VERSION = "1.0"
mongodb_url = "mongodb://localhost:27017/test" #sys.argv[3].strip()
#mongodb_url = "mongodb+srv://main_admin:<password>@m10basicagain-vmwqj.mongodb.net/test?retryWrites=true&w=majority"
retry = False
database_name = "amadata"
print(f'Connecting to:\n {mongodb_url}\n')
client = MongoClient(mongodb_url)
mdb = client[database_name]


'''
Booking Model
    Account
        People
    Booking
        Snapshots
    Event - BookingEvent
    RoomBlock
        RoomNight
'''

####
# create and insert a event object
####
def create_booking():
    doc = OrderedDict()
    events_array = []
    rb_array = []
    doc["_id"] = ObjectId()
    doc["version"] = VERSION
    doc["app_module"] = "BookingModuleService"
    doc["app_object"] = "Booking"
    name = random.choice(["Wedding","Corp Party","Wake","Convention","Annual Meeting","50th Birthday","Rails Camp","4H Show","Toga Party"])
    doc["name"] = name
    ntrim = name.replace(" ","")
    doc["abbreviation"] = ntrim[0:4]
    doc["agency"] = {"agency_name" : "agency1", "agency_id" : "abcde", "agent" : "Barney Rubble"}
    doc["comments"] = fake.sentence()
    doc["arrival_date"] = fake.date_time_this_decade()
    doc["booked_date"] = fake.date_time_this_decade()
    doc["booking_end_date"] = fake.date_time_this_decade()
    doc["booking_start_date"] = fake.date_time_this_decade()
    doc["booking_category"] = random.choice(["Wedding","Convention","Corp Event"])
    doc["status"] = random.choice(["Initial","Verified","Booked","Lost","Complete","Archived"])
    acct = create_account()
    print(f'Creating: {doc["name"]}')
    doc["catering_manager"] = acct["contacts"][random.randint(0,9)]
    doc["account"] = {"account_id": acct["_id"], "account_name" : acct["account_name"],"phone" : acct["phone"], "primary_contact": acct["primary_contact_fullname"]}

    try:
        mdb["bookings"].insert_one(doc)

    except Exception as e:
        print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM(account): '
              f'{str(e)}')
        connect_problem = True
    return(doc)

# create and insert a customer object
####
def create_account():
    try:
        doc = OrderedDict()
        conts_array = []
        cont_docs = []
        doc["_id"] = ObjectId()
        doc["version"] = VERSION
        doc["app_module"] = "BookingModuleService"
        doc["app_object"] = "Account"
        doc["account_name"] = fake.company()
        doc["abbreviation"] = doc["account_name"][0:4]
        doc["account_type"] = "customer"
        doc["industry_code_description"] = random.choice(["Hotel","Resort","Condominium","Conference Center","Campground"])
        doc["phone"] = fake.msisdn()
        doc["primary_contact_fullname"] = fake.name()
        doc["website_url"] = fake.url()
        doc["preferred_operating_currency_code"] = random.choice(["USD","CAD","EUR","GBP"])
        doc["addresses"] = []
        doc["addresses"].append(create_address("main"))
        doc["addresses"].append(create_address("alternate"))
        doc["addresses"].append(create_address("shipping"))

        # create 10 contacts per account
        for x in range(0, 10):
            ans = create_contact(doc)
            conts_array.append(ans)
        doc["contacts"] = conts_array
        mdb["accounts"].insert_one(doc)

    except Exception as e:
        print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM(account): '
              f'{str(e)}')
        connect_problem = True
    return(doc)

# create and insert a customer object
####
def create_event(e_type):
    try:
        doc = OrderedDict()
        rev_array = []
        doc["_id"] = ObjectId()
        doc["version"] = VERSION
        doc["app_module"] = "BookingModuleService"
        doc["app_object"] = "Event"
        name = e_type
        #name = random.choice(["Wedding","Corp Party","Wake","Convention","Annual Meeting","50th Birthday","Rails Camp","4H Show","Toga Party"])
        doc["name"] = name
        doc["event_classification"] = random.choice(["Cool","Hip","Chill","Lame","Amazing"])
        doc["event_comments"] = fake.sentence()
        doc["event_discussion"] = fake.sentence()
        #db["accounts"].insert_one(doc)
        seed = create_event_revenue("seed")
        for item in ["Agreed","Estimated","Actual"]:
            ans = create_event_revenue(item, seed)
            rev_array.append(ans)
        doc["revenue"] = rev_array
    except Exception as e:
        print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM(account): ')
        print(f'{str(e)}')
        connect_problem = True
    return(doc)

def create_event_revenue(e_type, seed = {}):
    doc = OrderedDict()
    doc["type"] = e_type
    doc["timestamp"] = datetime.datetime.now()
    if len(seed) == 0:
        doc["AdministrativeRevenue"] = random.randint(100,500)
        doc["Attendance"] = random.randint(10,100)
        doc["AudioVisualRevenue"] = random.randint(100,500)
        doc["BeverageRevenue"] = random.randint(2000,8500)
        doc["FoodRevenue"] = random.randint(2100,6500)
        doc["FunctionRoomRentalRevenue"] = random.randint(900,2500)
        doc["OtherRevenue"] = random.randint(100,500)
        doc["ResourceRevenue"] = random.randint(100,500)
    else:
        doc["AdministrativeRevenue"] = seed["AdministrativeRevenue"]
        doc["Attendance"] = seed["Attendance"]
        doc["AudioVisualRevenue"] = seed["AudioVisualRevenue"]
        doc["BeverageRevenue"] = seed["BeverageRevenue"]
        doc["FoodRevenue"] = seed["FoodRevenue"]
        doc["FunctionRoomRentalRevenue"] = seed["FunctionRoomRentalRevenue"]
        doc["OtherRevenue"] = seed["OtherRevenue"]
        doc["ResourceRevenue"] = seed["ResourceRevenue"]
    return doc

def create_room_block(s_type = "main"):
    doc = OrderedDict()
    doc["name"] = f'Room Block {random.randint(0,9)}'
    doc["alternate_name"] = f'Room Block {random.choice(["Cool","Hip","Chill","Lame","Amazing"])}'
    doc["comments"] = fake.sentence()
    doc["timestamp"] = datetime.datetime.now()
    doc["rate_code"] = random.choice(["Full","Discount-x","IBM","AARP","Federal"])
    rn = []
    for item in ["Blocked","Agreed","Forecast"]:
        ans = create_room_night(item)
        rn.append(ans)
    doc["room_nights"] = rn
    print("Room BLock")
    print(doc)
    return(doc)

def create_room_night(s_type = "blocked"):
    doc = OrderedDict()
    doc["type"] = s_type
    doc["timestamp"] = datetime.datetime.now()
    spray = {"Single" : [34, 178], "Double" : [44,219], "Triple" : [15,265], "Quad" : [2,290]}
    for key in spray:
        doc[key] = spray[key][0]
        doc[f'{key}_rate'] = spray[key][1]

    return(doc)

def create_revenue_snapshot(s_type = "estimate"):
    doc = OrderedDict()
    doc["type"] = s_type
    doc["timestamp"] = datetime.datetime.now()
    doc["events"] = []
    for item in ["Single","Double","Triple","Quad"]:
        room = OrderedDict()
        room["type"] = item
        room["rate"] = random.randint(125,379)
        doc["rates"].append(room)
    return(doc)


def create_address(addr_type = "main"):
    addr = OrderedDict()
    addr["type"] = addr_type
    addr["address1"] = fake.street_address()
    addr["address2"] = ""
    addr["address3"] = ""
    addr["city"] = fake.city()
    addr["state"] = fake.state()
    addr["zipcode"] = fake.zipcode()
    addr["location"] = {"type" : "point", "coordinates" : [float(str(fake.longitude())),float(str(fake.latitude()))]}
    return(addr)

####
# create and insert a person object
####
def create_contact(person_doc):
    try:
        doc = OrderedDict()
        doc["_id"] = ObjectId()
        doc["account_id"] = person_doc["_id"]
        doc["name"] = fake.name()
        doc["title"] = fake.job()
        doc["phone"] = fake.msisdn()
        doc["email"] = fake.email()
        doc["timestamp"] = fake.date_time_this_decade()
        #print(json.dumps(doc))
        #db["contacts"].insert_one(doc)

    except Exception as e:
        print(f'{datetime.datetime.now()} - DB-CONNECTION-PROBLEM(contact): '
              f'{str(e)}')
        connect_problem = True
    return(doc)

def add_events():
    # create several events for the booking
    cursor = mdb["bookings"].find({})
    inc = 0
    count = cursor.count()
    bb.logit("Updating Bookings - found " + str(count))
    while inc != count:
        events_array = []
        for item in ["Welcome Reception","Keynote Speech","Monday Breakfast","Monday Dinner"]:
            ans = create_event(item)
            #print("Event")
            #print(ans)
            events_array.append(ans)
            mdb["events"].insert_one(ans)
        doc = cursor[inc]
        mdb["bookings"].update_one({"_id" : doc["_id"]},{ "$set" : {"events" : events_array }})
        bb.logit(f'Updating {doc["name"]}')
        inc += 1

def add_rooms():
    # create several room block for the booking
    cursor = mdb["bookings"].find({})
    count = cursor.count()
    bb.logit("Updating Bookings - found " + str(count))
    inc = 0
    while inc != count:
        #Load country
        rb_array = []
        # create several RoomBlocks for the booking
        for item in ["Main"]:
            ans = create_room_block("main")
            rb_array.append(ans)
            bb.logit("Room Block")
        doc = cursor[inc]
        mdb["bookings"].update_one({"_id" : doc["_id"]},{ "$set" : {"room_blocks" : rb_array }})
        bb.logit(f'Updating {doc["name"]}')
        inc += 1


def revenue_totals():
    # create several room block for the booking
    cursor = mdb["bookings"].find({})
    count = cursor.count()
    bb.logit("Updating Revenue Totals - found " + str(count))
    inc = 0
    while inc != count:
        doc = cursor[inc]
        if "revenue_totals" in doc:
            totals = doc["revenue_totals"]
        else:
            totals = []
        bb.logit(f'Updating {doc["name"]}')
        inc += 1
        pipeline = [
            {"$match": {"_id" : doc["_id"] }},
            {"$unwind": {"path": "$events"}},
            {"$unwind": {"path": "$events.revenue"}},
            {"$group": {
                "_id": "$events.revenue.type",
                "Type": {"$first": "$events.revenue.type"},
                "FoodRev": {"$sum": "$events.revenue.FoodRevenue"},
                "BeverageRev": {"$sum": "$events.revenue.BeverageRevenue"},
                "AdminRev": {"$sum": "$events.revenue.AdministrativeRevenue"},
                "AVRev" : {"$sum" : "$events.revenue.AudioVisualRevenue"},
                "FRRev" : {"$sum" : "$events.revenue.FunctionRoomRentalRevenue"},
                "OtherRev" : {"$sum" : "$events.revenue.OtherRevenue"},
                "ResourceRev" : {"$sum" : "$events.revenue.ResourceRevenue"}
            }}
        ]
        agg_result = mdb["bookings"].aggregate(pipeline)
        bb.logit("Calculating Revenue Totals...")
        for adoc in agg_result:
            totrev = adoc["FoodRev"] + adoc["BeverageRev"] + adoc["AdminRev"] + adoc["AVRev"] + adoc["OtherRev"] + adoc["FRRev"] + adoc["ResourceRev"]
            totals.append({"type" : adoc["Type"], "category" : "event", "revenue" : totrev})
            bb.logit(f'Calculating {adoc["Type"]}')
        mdb["bookings"].update_one({"_id" : doc["_id"]},{ "$set" : {"revenue_totals" : totals }})

def room_totals():
    # create several room block for the booking
    cursor = mdb["bookings"].find({})
    count = cursor.count()
    bb.logit("Updating RoomRevenue Totals - found " + str(count))
    inc = 0
    while inc != count:
        doc = cursor[inc]
        bb.logit(f'Updating {doc["name"]}')
        if "revenue_totals" in doc:
            totals = doc["revenue_totals"]
        else:
            totals = []
        inc += 1
        pipeline = [
            {"$match": {"_id" : doc["_id"] }},
            {"$unwind": {"path": "$room_blocks"}},
            {"$unwind": {"path": "$room_blocks.room_nights"}},
            {"$group": {
                "_id": "$room_blocks.room_nights.type",
                "Type": {"$first": "$room_blocks.room_nights.type"},
                "SingleCnt": {"$sum": "$room_blocks.room_nights.Single"},
                "SingleRate": {"$sum": "$room_blocks.room_nights.Single_rate"},
                "DoubleCnt": {"$sum": "$room_blocks.room_nights.Double"},
                "DoubleRate": {"$sum": "$room_blocks.room_nights.Double_rate"},
                "TripleCnt": {"$sum": "$room_blocks.room_nights.Triple"},
                "TripleRate": {"$sum": "$room_blocks.room_nights.Triple_rate"},
                "QuadCnt": {"$sum": "$room_blocks.room_nights.Quad"},
                "QuadRate": {"$sum": "$room_blocks.room_nights.Quad_rate"}
            }}
        ]
        agg_result = mdb["bookings"].aggregate(pipeline)
        bb.logit("Calculating Revenue Totals...")
        for adoc in agg_result:
            totroom = adoc["SingleCnt"] + adoc["DoubleCnt"] + adoc["TripleCnt"] + adoc["QuadCnt"]
            totrev = adoc["SingleCnt"] * adoc["SingleRate"] + adoc["DoubleCnt"] * adoc["DoubleRate"] + adoc["TripleCnt"] * adoc["TripleRate"] + adoc["QuadCnt"] * adoc["QuadRate"]
            totals.append({"type" : adoc["Type"], "category" : "room", "revenue" : totrev})
            totals.append({"type" : adoc["Type"], "category" : "room", "count" : totroom})
            bb.logit(f'Calculating {adoc["Type"]}')
        mdb["bookings"].update_one({"_id" : doc["_id"]},{ "$set" : {"revenue_totals" : totals }})


def build_test_data():
    num_records = int(ARGS["count"])

    for k in range(num_records):
        create_booking()


####
# Main
####
if __name__ == '__main__':
    ARGS = bb.process_args(sys.argv)
    if "action" not in ARGS:
        print("Send action= argument")
        sys.exit(1)

    if ARGS["action"] == "test_data":
        # load_bookings.py action=test_data count=10
        build_test_data()
    elif ARGS["action"] == "add_events":
        # load_bookings.py action=add_events
        add_events()
    elif ARGS["action"] == "add_rooms":
        # python3 load_bookings.py action=add_rooms
        add_rooms()
    elif ARGS["action"] == "revenue_totals":
        revenue_totals()
    elif ARGS["action"] == "room_totals":
        room_totals()
    else:
        print(f'{ARGS["action"]} not found')
