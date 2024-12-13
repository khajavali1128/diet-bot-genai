import pandas as pd

# Reading CSV file for All Diets
original = pd.read_csv("data/All_Diets.csv", index_col=0)

# Taking necessary columns into df
df = pd.DataFrame(original,
                  columns=['Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)', 'Extraction_day'])

# Convert object type columns to string type
object_columns = df.select_dtypes(include='object').columns
df[object_columns] = df[object_columns].astype(pd.StringDtype())

# The 4-4-9 system uses the average values of 4 kcal/g for protein, 4 kcal/g for carbohydrates, and 9 kcal/g for fat
df['Calories'] = (df['Protein(g)'] * 4) + (df['Carbs(g)'] * 4) + (df['Fat(g)'] * 9)


# Add Yes/No columns for suitability
def suitability(row):
    # Initialize suitability columns
    skinny = "No"
    healthy = "No"
    overweight = "No"
    cardiovascular = "No"

    # Logic for Skinny
    if row['Calories'] > 350 and row['Protein(g)'] > 20:
        skinny = "Yes"

    # Logic for Healthy
    if 200 <= row['Calories'] <= 500 and row['Protein(g)'] > 10 and 10 <= row['Fat(g)'] <= 20:
        healthy = "Yes"
    elif row['Calories'] < 200 and row['Protein(g)'] > 10 and row['Fat(g)'] < 10:
        healthy = "Yes"

    # Logic for Overweight
    if row['Calories'] < 300 and row['Fat(g)'] < 10 and row['Protein(g)'] > 10:
        overweight = "Yes"

    # Logic for Cardiovascular Health
    if row['Fat(g)'] <= 15 and row['Carbs(g)'] <= 50 and row['Protein(g)'] >= 10:
        cardiovascular = "Yes"

    return skinny, healthy, overweight, cardiovascular


# Apply suitability logic to each row and create new columns
df[['Suitable for Skinny', 'Suitable for Healthy', 'Suitable for Overweight',
    'Suitable for Cardiovascular']] = df.apply(
    lambda row: pd.Series(suitability(row)), axis=1
)

# Display the updated DataFrame
print(df.head())

# Save the updated DataFrame to a new CSV file
df.to_csv("All_Diets_With_Suitability_CVD_YesNo.csv")
print("Updated data saved to 'All_Diets_With_Suitability_CVD_YesNo.csv'.")
