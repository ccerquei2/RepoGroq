import os
import time
import csv
from crewai import Crew
from agents import ProductionOrderAgents
from tasks import AnalyzeVariationTask

# 0. Setup environment
from dotenv import load_dotenv
load_dotenv()

# 1. Create agents
agents = ProductionOrderAgents()

variation_analyzer = agents.variation_analysis_agent()

# 2. Create tasks
tasks = AnalyzeVariationTask()

analyze_variation_tasks = []

# Path to the CSV file containing production order information
csv_file_path = 'data/production_orders.csv'

# Open the CSV file
with open(csv_file_path, mode='r', newline='') as file:
    csv_reader = csv.DictReader(file)

     # Iterate over each row in the CSV file
    for row in csv_reader:
        order_details = {
            'Material_Used': row['Material_Used'],
            'Setup_Hours': row['Setup_Hours'],
            'Labor_Hours': row['Labor_Hours'],
            'Machine_Hours': row['Machine_Hours'],
            'External_Operation': row['External_Operation'],
            'Justification': row['Justification'],
            'Variation_Percentage': float(row['Variation_Percentage'])
        }

        # Create a analyze_variation task for each order
        analyze_task = tasks.analyze_variation(
            agent=variation_analyzer,
            order_details=order_details
        )

        # Add the task to the crew
        analyze_variation_tasks.append(analyze_task)

# Setup Crew
crew = Crew(
    agents=[variation_analyzer],
    tasks=analyze_variation_tasks,
    max_rpm=29
)

# Kick off the crew
start_time = time.time()

results = crew.kickoff()

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Crew kickoff took {elapsed_time} seconds.")
print("Crew usage", crew.usage_metrics)
