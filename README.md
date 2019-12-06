# Skill Finder - Jobs In The US (Group 14)

## Team Members:
- Kevin Youssef
- Malhar Jere
- Yu Hong
- Yunzhe Hu

## File Structure:
- graphs/: all the plots generated by the data analysis
- Keywords.xlsx: skill keywords that are extracted from the job descriptions
- Skill_Finder_Analysis.ipynb: data visualization code (in case graph generated by Plotly is not shown on Github preview, please check under graphs/)
- dice_com-job_us.csv: raw dataset
- job_posting_dataset.xlsx: parsed dataset from "dice_com-job_us.csv" (extract various skills, YoE, education level from the job descriptions)
- parse_data.py: python code used to parse the raw dataset
- plot_functions.py: all the functions used to plot the data analysis graphs
- preclean_function.py: function to parse city and state from the "joblocation_address" column

## Dataset:
The dataset is extracted from Dice.com, a prominent US-based technology job board. It contains about 22,000 technology job postings.   
Refer: https://www.kaggle.com/PromptCloudHQ/us-technology-jobs-on-dicecom

## Required Third Party Modules:
- Numpy
- Pandas
- Matplotlib
- Plotly
- Seaborn

## How to Run the Code:
- Parse the raw dataset. 
```
python3 parse_data.py
```
- Open Skill_Finder_Analysis.ipynb and run all cells to plot the graphs.
