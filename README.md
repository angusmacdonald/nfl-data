# NFL Receiver Data Scraper / Parser

Utility to scrape data on receptions of NFL players from the internet and add it to a local MongoDB instance.

## Example Queries
Once the data is stored in the database it can be queried. For example:
    db.receiving.find( { $and: [ { Team: "GB" }, { Year: 2015 } ] } )

