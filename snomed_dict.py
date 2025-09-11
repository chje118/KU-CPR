import pandas as pd
import re

# Path to SNOMED codes (all codes with code history)
# snomed_path = "D:/DATA/patoSnoMed_2025-04.xlsx"
snomed_path = "C:/Users/chris/OneDrive/Dokumenter/SDU/Master's Thesis Project/patoSnoMed_2025-04.xlsx"

# Load the Excel file
xls_snomed = pd.read_excel(snomed_path)

# Check column names
# print(f"Columns: {xls_snomed.columns.tolist()}")

# Data Frame with relevant columns
df_snomed = pd.DataFrame(xls_snomed, columns=['SKSkode', 'DatoFra', 'DatoÆndring', 'DatoTil', 'Kodetekst', 'Fuldtekst'])

# print("Shape of data frame: ", df_snomed.shape)
# print("\nHead of data frame: \n", df_snomed.head())

SNOMED_patterns = {
    "Topografi ukendt": r"T0000\d", 
    "Multiple lokalisationer": r"T000\d{2}",
    "Resektionsrand": r"T001\d{2}",
    "Hud, hår og negle": r"T0[123].*",
    "Cytologi, hud": r"T0Y200|T0Y5.*",
    "Mamma": r"T04.*",
    "Cytologi, mamma": r"T0Y4.*",
    "Hæmatopoietisk og retikuloendotelialt system": r"T0[56].*|T0X.*",
    "Milt" : r"T07.*",
    "Lymfeknuder og det lymfatiske system": r"T0[89].*",
    "Knoglesystem": r"T1[012].*|T1X5.*",
    "Skeletmuskulatur": r"T1[34].*",
    "Bursa, sener og ligamenter": r"T1[678].*",
    "Bløddelsvæv": r"T1X[02].*",
    "Glat muskulatur": r"T1X3.*",
    "Bruskvæv": r"T1X7.*",
    "Cytologi, synovialvæske": r"T1Y.*",
    "Næse og bihuler": r"T2[012].*",
    "Pharynx": r"T23.*|T60.*",
    "Larynx": r"T24.*",
    "Trachea": r"T25.*",
    "Bronkier og lunger": r"T2[6789].*",
    "Cytologi, luftveje": r"T2[XY].*",
    "Hjerte": r"T3.*",
    "Blodkar": r"T4.*",
    "Mundhule": r"T5[1234].*",
    "Spytkirtler": r"T55.*",
    "Lever": r"T56.*",
    "Galdeveje": r"T5[78].*",
    "Pancreas": r"T59.*|T99000",
    "Cytologi, fordøjelsessystem": r"T5[XY].*",
    "Tonsiller og adenoider": r"T61.*",
    "Esophagus": r"T62.*",
    "Ventrikel": r"T63.*",
    "Tarmsystem": r"T6[4-9].*|T50000|T50100|T50500|T6[X].*",
    "Fæces": r"T6Y.*",
    "Urogenitale system, NOS": r"T70000",
    "Nyrer": r"T7[12].*",
    "Ureter": r"T73.*",
    "Urinblære": r"T74.*",
    "Urethra": r"T75.*",
    "Penis": r"T76.*",
    "Prostata og vesicula seminalis": r"T77.*",
    "Testis og epididymis": r"T7[89].*",
    "Cytologi, urogenitale system": r"T7[XY].*",
    "Kvindelige kønsorganer": r"T8[01].*",
    "Uterus": r"T8[2,4-5].*",
    "Cervix uteri": r"T83.*",
    "Tuba uterina og ovarier": r"T8[67].*",
    "Placenta, fosterhinder og navlestreng": r"T88.*",
    "Foster og fostervand": r"T89.*",
    "Cytologi, kvindelige kønsorganer": r"T8[XY].*",
    "Endokrine system": r"T90.*",
    "Hypofyse": r"T91.*",
    "Epifyse": r"T92.*",
    "Binyre": r"T93.*",
    "Glomus caroticum": r"T94.*",
    "Paraganglie": r"T95.*",
    "Thyroidea": r"T96.*",
    "Parathyroidea": r"T97.*",
    "Thymus": r"T98.*",
    "Cilium": r"TE.*",
    "Rekonstruerede organer": r"TN.*",
    "Nervesystem": r"TX[0-9].*",
    "Øje": r"TXX.*",
    "Øre": r"TXY.*",
    "Hoved og hals": r"TY0.*",
    "Truncus (krop)": r"TY1.*",
    "Thorax": r"TY[23].*",
    "Abdomen": r"TY[45].*",
    "Pelvis, lysken": r"TY[67].*",
    "Overekstremitet": r"TY8.*",
    "Underekstremitet": r"TY9.*",
    "Øvrige": r"TY[XY].*|T00[1-9X].*",
}

class SNOMED: 
    """ Class to handle SNOMED codes. """
    def __init__(self, dataframe: pd.DataFrame, snomed_dict: dict = SNOMED_patterns):
        self.dataframe = dataframe
        self.snomed_dict = snomed_dict

    def get_unique_first_letters(self) -> set:
        """ Get unique first letters of SNOMED codes. """
        return {code[0] for code in self.dataframe['SKSkode'].dropna().unique() if code}
    
    def print_first_letters(self) -> None:
        first_letters = self.get_unique_first_letters()
        print('SNOMED letters:', first_letters)

    def get_codes_by_letter(self, letter: str) -> pd.DataFrame:
        """ Get SNOMED codes starting with a specific letter. """
        return self.dataframe[self.dataframe['SKSkode'].str.startswith(letter)].copy()
    
def categorize_snomed(code):
    for category, pattern in SNOMED_patterns.items():
        if re.match(pattern, code):
            return category
    return "Udefineret"


if __name__ == "__main__":
    snomed = SNOMED(df_snomed)
    snomed.print_first_letters()
    tcodes = snomed.get_codes_by_letter('T')
    tcodes["Category"] = tcodes["SKSkode"].apply(categorize_snomed)
    print(tcodes.sample(5))