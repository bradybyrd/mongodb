#----------------------------------------------------------#
#      README for Load Script
#----------------------------------------------------------#
# 1/6/2020 BJB

#### Introduction:
    This script loads data for bookings, accounts and events.
    It makes use of the faker library to generate synthetic data

#### Model:
The model is intended to represent an event booking at a hotel.
The components are:
```
Booking Model
    Account
        People
    Booking
        Snapshots
    Event - BookingEvent
    RoomBlock
        RoomNight
```

#### Use:
The script has help on the invocation in the _main_ block. Its basically like this:
```
python3 load_bookings.py action=test_data count=100
```
This will create 100 booking documents, 100 accounts and 1000 people.


Now add some events:
```
python3 load_bookings.py action=add_events
```
This will create one of each of these types of events:
["Welcome Reception","Keynote Speech","Monday Breakfast","Monday Dinner"]


Now add some room blocks to the booking:
```
python3 load_bookings.py action=add_rooms
```
This will a single room_block for each booking with 3 different room_night subdocuments.


The model makes use of the calculated fields pattern to summarize information into the booking document.  Those totals are added like this:
```
python3 load_bookings.py action=room_totals
python3 load_bookings.py action=revenue_totals
```
This will create a revenue_totals subdocument for the booking.  The totals are calculated using an aggregation.  This is a good example of using the aggregation framework as well as a simple de-normalization that provides important at-a-glance information.
