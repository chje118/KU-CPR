import pandas as pd

# Paths to Metadata
snomed_path = "C:/Users/chris/OneDrive/Dokumenter/KU CPR/patoSnoMed_2025-04.xlsx"

# Check available sheet names
xls_snomed = pd.read_excel(snomed_path)

# Check column names
print(f"Columns: {xls_snomed.columns.tolist()}")

# Data Frame with relevant columns
df_snomed = pd.DataFrame(xls_snomed, columns=['SKSkode', 'Kodetekst', 'Fuldtekst'])

# Function to get first letters of SNOMED codes
def get_first_letters(codes):
    """ Given a list of SNOMED codes, return a list of unique first letters. """
    return {code[0] for code in codes if code}

# Get unique first letters
first_letters = get_first_letters(df_snomed['SKSkode'].dropna().unique())
print('SNOMED letters:', first_letters)
