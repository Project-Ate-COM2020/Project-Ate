# Consistent Terminology Rules

I have noticed we are all using different terms to refer to users, buyers, sellers, postings, listings and bundles

To resolve this theoretically I am making this doc - no need to implement retroactively unless to fix breaking changes, but from monday meeting on try and keep variable names, paths and json messages in the following naming convention

## Users

User refers to anyone who uses the site, there are three types of users: buyer, seller, maintainer

Therefore when refering to a specific one always use exact the terminology of 'buyer' rather than user

## Bundles

Consistent terminology for bundle related terms

 -A Bundle refers to a singular bundle of food

 -A Posting refers to a collection of bundles on the marketplace - this is what a seller is able to create and post

 -A Listing refers to a single bundle inside a Posting - this is what a buyer is able to reserve

 -A Reservation refers to a single bundle reserved by a buyer

 -A Collection refers to a single bundle collected by a buyer

## Any more / Problems

If there are any more ambiguous terms please add them here, if any of the terms I've listed here are incorrect, or would be too hard to retroactively implement let me know as son as possible and we can sort out a different term
