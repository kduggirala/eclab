import pandas as pd
import re
import os

products = pd.concat([pd.read_csv(f"products_data/part_{i}.csv") for i in range(1, 11)]).drop_duplicates().reset_index(drop = True)

process = products.query("weight == 'None'")
process['name'] = process['name'].astype("str").apply(lambda s : s.replace("pcs", "").replace("pc", ""))
excluding = "(?!\s*THC|\s*CBD|\s*CBN|\s*CBG|\s*\+?Caff(ei|ie)ne|\s*CBC|\s*Melatonin|\s*CAF|\s*MEL)"
products.loc[process.index, "weight"] = process['name'].astype("str").apply(lambda s : re.search(f"(\d+x|\d+\s*x)*\s*\d*\.*\d+\s*m*[gl]{excluding}", s)).apply(lambda o : o.group() if o else "None")
products['weight'] = products['weight'].apply(lambda s : s.replace("..", "."))

fraction = products[products['weight'].str.contains("/")]
defractioned = fraction['weight'].apply(lambda s : f'{int(s.split(" ")[0].split("/")[0]) / int(s.split(" ")[0].split("/")[1])}{s.split(" ")[1]}')
products.loc[fraction.index, "weight"] = defractioned

process = products.query("weight != 'None'")
multiply = process[process['weight'].str.match("\d+\s*x\s*\d*\.?\d+")]
multiply['num'] = multiply['weight'].apply(lambda s : re.search("\d+\s*x\s*\.?\d+", s).group()).apply(lambda s : int(int(s.split('x')[0]) * float(s.split('x')[1])))
multiply['weight'] = multiply['num'].astype("str") + multiply['weight'].apply(lambda s : re.search("m*[gl]", s).group())
products.loc[multiply.index, "weight"] = multiply['weight']
products = products[products['name'].notnull()]
products[products['name'].str.contains("indoor")]
rescale = products[products['weight'].str.contains("\d*\.?\d+\s*g")]
products.loc[rescale.index, "weight"] = rescale['weight'].apply(lambda s : int(1000 * float(re.search('\d*\.*\d+', s).group()))).apply(lambda s : f"{s}mg")

units_change = products[products['weight'].str.contains("oz")]
rescale = units_change[units_change['weight'].str.match("\d*\.?\d+\s*oz")]
products.loc[rescale.index, "weight"] = rescale['weight'].apply(lambda s : int(28000 * float(re.search('\d*\.*\d+', s).group()))).apply(lambda s : f"{s}mg")
products.loc[326627, 'weight'] = f"{71 * 350}mg"
products.loc[783088, 'name'] = f"{5*500}mg"

products['thc'] = products['cbd'].apply(lambda s : s.split(" | ")).apply(lambda l : next((s for s in l if "THC" in s), "None"))
products['cbd'] = products['cbd'].apply(lambda s : s.split(" | ")).apply(lambda l : next((s for s in l if "CBD" in s), "None"))
products = products.query("name == name")[['category', 'name', 'thc', 'cbd', 'price', 'weight', 'url']]
thc = products[products['name'].str.contains("\d+\s*mg\s*THC")].query("thc == 'None'")
products.loc[thc.index, "thc"] = thc['name'].apply(lambda s : re.search("\d+\s*mg\s*THC", s).group())
cbd = products[products['name'].str.contains("\d+\s*mg\s*CBD")].query("cbd == 'None'")
products.loc[cbd.index, "cbd"] = cbd['name'].apply(lambda s : re.search("\d+\s*mg\s*CBD", s).group())

# Specify the input CSV file and the output directory for the parts
output_directory = 'products_data_cleaned/'
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
