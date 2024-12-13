from neo4j import GraphDatabase
import pandas as pd

# Load the CSV data
file_path = 'Updated_Diets.csv'
diet_data = pd.read_csv(file_path)

# Connect to Neo4j
uri = "bolt://localhost:7687"  # Adjust if your Neo4j is running elsewhere
username = "neo4j"
password = "12341234"  # Replace with your Neo4j password

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_graph(tx, diet_type, recipe_name, properties):
    # Create or match DietType node and set its name
    tx.run("""
        MERGE (d:DietType {type: $diet_type}) //Uniqueness
        SET d.name = $diet_type
    """, diet_type=diet_type)
    
    # Create or match Recipe node and set its properties
    tx.run("""
        MERGE (r:Recipe {name: $recipe_name})
        ON CREATE SET r += $properties
    """, recipe_name=recipe_name, properties=properties)
    
    # Create or match the relationship
    tx.run("""
        MATCH (d:DietType {type: $diet_type})
        MATCH (r:Recipe {name: $recipe_name})
        MERGE (d)-[:HAS_RECIPE]->(r)
    """, diet_type=diet_type, recipe_name=recipe_name)

# Insert data into Neo4j
with driver.session() as session:
    for _, row in diet_data.iterrows():
        diet_type = row["Diet_type"]
        recipe_name = row["Recipe_name"]
        properties = {
            "Cuisine_type": row["Cuisine_type"],
            "Protein(g)": row["Protein(g)"],
            "Carbs(g)": row["Carbs(g)"],
            "Fat(g)": row["Fat(g)"],
            "Extraction_day": row["Extraction_day"],
            "Calories": row["Calories"],
            "Skinny": row["Skinny"],
            "Healthy": row["Healthy"],
            "Overweight": row["Overweight"],
            "Cardiovascular": row["Cardiovascular"],
        }
        session.write_transaction(create_graph, diet_type, recipe_name, properties)

print("Data successfully inserted into Neo4j!")
