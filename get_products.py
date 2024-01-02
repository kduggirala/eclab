import subprocess
import pandas as pd
import os

#run spiders in parallel using scrapyd library
with open("../eclab/links.csv", "r") as f:
    links = f.read().split("\n")
    for link in links:
        subprocess.run(f'curl http://localhost:6800/schedule.json -d project=weed -d spider=weed -d start_url="{link}"')

# Split the data from 1 big jsonl file to 10 csvs
        
products = pd.read_json("../eclab/weed/products_data.jsonl", orient = "records", dtype = {"category" : str, "name" : str, "cbd" : str, "price" : str, "weight" : str, "url" : str}, lines=True)
output_directory = 'products_data/'
os.mkdir(output_directory)

# Calculate the number of rows per part
num_rows = len(products)
rows_per_part = num_rows // 10



# Split the CSV into 10 parts
for i in range(10):
    start_idx = i * rows_per_part
    end_idx = start_idx + rows_per_part
    if i == 9:
        end_idx = num_rows
    part_df = products.iloc[start_idx:end_idx]
    
    # Save each part to a separate CSV file
    output_file = os.path.join(output_directory, f'part_{i+1}.csv')
    part_df.to_csv(output_file, index=False)
