from data_scraper import fetch_skater_data

# Run scraper
skaters=fetch_skater_data()

# Export to csv
skaters.to_csv("skaters.csv", index=False)