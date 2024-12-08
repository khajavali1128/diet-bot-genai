import csv
from neo4j import GraphDatabase

# Establish connection to the Neo4j database
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "12341234"

def create_nodes_and_relationships(file_path):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def create_data(tx, row):
        # Create nodes and relationships based on CSV structure
        query = """
        MERGE (recipe:Recipe {name: $recipe_name})
        SET recipe.cuisine = $cuisine_type,
            recipe.protein = $protein,
            recipe.carbs = $carbs,
            recipe.fat = $fat,
            recipe.calories = $calories,
            recipe.skinny = $skinny,
            recipe.healthy = $healthy,
            recipe.overweight = $overweight,
            recipe.cardiovascular = $cardiovascular
        """
        tx.run(query, 
               diet_type=row['Diet_type'], 
               recipe_name=row['Recipe_name'], 
               cuisine_type=row['Cuisine_type'], 
               protein=row['Protein(g)'], 
               carbs=row['Carbs(g)'], 
               fat=row['Fat(g)'], 
               calories=row['Calories'],
               skinny=row['Skinny'],
               healthy=row['Healthy'],
               overweight=row['Overweight'],
               cardiovascular=row['Cardiovascular'])

    try:
        with driver.session() as session:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    session.write_transaction(create_data, row)

    finally:
        driver.close()

# Path to your CSV file
csv_file_path = 'Updated_Diets.csv'
create_nodes_and_relationships(csv_file_path)
