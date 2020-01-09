
##
# Script to create a view
##
- Run this from the MongoDB CLI
- The aggregation pipeline that defines the view does this:
-  1) Joins the Books and Accounts collections via $lookup
-  2) $unwinds the full_account (all $lookup results come in as an array)
-  3) $unwinds the address array for the main address
-  4) uses $project to limit the fields and give easy access to geolocation
------------------------------
db.createView("vw_account_bookings", "bookings", [
{$lookup: {
  from: 'accounts',
  localField: 'account.account_id',
  foreignField: '_id',
  as: 'full_account'
}}, {$unwind: {
  path: "$full_account"
}}, {$unwind: {path: '$full_account.addresses'}}, {$match: {
  'full_account.addresses.type': 'main'
}}, {$project: {
  name: 1,
  booking_start_date: 1,
  status: 1,
  'account.account_name': 1,
  'full_account.addresses.location': 1
}}]
