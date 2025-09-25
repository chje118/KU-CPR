import pandas as pd

class SNOMED: 
    """ Class to handle SNOMED codes. """
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self.first_letters = self.unique_first_letters()

    def unique_first_letters(self) -> set:
        """ Get unique first letters of SNOMED codes. """
        return {code[0] for code in self.dataframe['SKSkode'].dropna().unique() if code}
    
    def get_first_letters(self) -> None:
        print('SNOMED letters:', self.first_letters)

    def get_letter_counts(self) -> None:
        prefixes = self.dataframe['SKSkode'].str[0].value_counts()
        print("Unique code prefixes in SKSkode: \n", prefixes)

    def get_codes_by_letter(self, letter: str) -> pd.DataFrame:
        """ Get SNOMED codes starting with a specific letter. """
        return self.dataframe[self.dataframe['SKSkode'].str.startswith(letter)].copy()

class SNOMEDHierarchy:
    def __init__(self, codes: pd.DataFrame, main_len: int = 3, sub_len: int = 4):
        self.codes = codes
        self.main_len = main_len
        self.sub_len = sub_len
        self.code_to_region = {}
        self.code_to_subregion = {}
        self.hierarchy = self._build_hierarchy()

    def _build_hierarchy(self):
        hierarchy = {}
        for _, row in self.codes.iterrows():
            code = row['SKSkode']
            text = row['Kodetekst']
            if len(code) < self.main_len:
                print(f"Skipping invalid code: {code}")
                continue

            main = code[:self.main_len]
            sub = code[:self.sub_len]
            
            if main not in hierarchy:
                hierarchy[main] = {
                    "name": text,
                    "subregions": {}
                }
            if sub not in hierarchy[main]["subregions"]:
                hierarchy[main]["subregions"][sub] = {
                    "name": text,
                    "codes": []
                }
            # Always append the code to the subregion
            hierarchy[main]["subregions"][sub]["codes"].append({"code": code, "text": text})
            self.code_to_region[code] = main
            self.code_to_subregion[code] = sub
        return hierarchy

    def get_sub_dict(self, code_prefix):
        """Return a dict by prefix. """
        # Main region 
        if len(code_prefix) == self.main_len:
            return self.hierarchy.get(code_prefix)
        
        # Subregion
        elif len(code_prefix) == self.sub_len:
            main = code_prefix[:self.main_len]
            return (
                self.hierarchy.get(main, {})
                .get("subregions", {})
                .get(code_prefix)
            )
        else: 
            raise ValueError(
                f"Prefix must be {self.main_len} (main region) or {self.sub_len} (subregion) characters long"
            )

    def get_regions(self, code):
        """ Get main region code, main region name, and subregion name for a given code."""
        region = self.code_to_region.get(code)
        region_name = self.hierarchy[region]["name"]

        subregion = self.code_to_subregion.get(code)
        subregion_name = self.hierarchy[region]["subregions"].get(subregion, {}).get("name")

        codes_list = self.hierarchy[region]["subregions"].get(subregion, {}).get("codes", [])
        code_name = next((c["text"] for c in codes_list if c["code"] == code), "")

        return region, region_name, subregion_name, code_name
   
    def list_regions(self):
        for region in sorted(self.hierarchy.keys()):
            # Count all codes in all subregions
            count = sum(len(sub["codes"]) for sub in self.hierarchy[region]["subregions"].values())
            region_name = self.hierarchy[region]["name"] if self.hierarchy[region] else "Unknown"
            print(f"{region}: {region_name} ({count} codes)")

    def list_subregions(self, region, max_examples=None):
        """Print subregions (TXXX) for a given main region (TXX) in a readable format."""
        if region not in self.hierarchy:
            print(f"Region {region} not found.")
            return

        subregions = self.hierarchy[region]["subregions"]
        for subregion in sorted(subregions.keys()):
            codes = subregions[subregion]["codes"]
            subregion_name = codes[0]["text"] if codes else "Unknown"
            print(f"\n{subregion}: {subregion_name} ({len(codes)} codes)")
            for i, code_info in enumerate(codes):
                if max_examples is not None and i >= max_examples:
                    print(f"    ... and {len(codes) - max_examples} more codes")
                    break
                print(f"    {code_info['code']}: {code_info['text']}")


if __name__ == "__main__":
    snomed_path = "C:/Users/chris/OneDrive/Dokumenter/SDU/Master's Thesis Project/SNOMED/patoSnoMed_2025-04.xlsx"
    xls_snomed = pd.read_excel(snomed_path)
    df_snomed = pd.DataFrame(xls_snomed, columns=['SKSkode', 'DatoFra', 'DatoÆndring', 'DatoTil', 'Kodetekst', 'Fuldtekst'])
    
    # Get SNOMED code overview
    snomed = SNOMED(df_snomed)
    snomed.get_letter_counts()

    # Focus on T-codes (topography)
    t_codes = snomed.get_codes_by_letter('T')
    t_hierarchy = SNOMEDHierarchy(t_codes)

    print("\nExample lookup for T1884A:")
    print(t_hierarchy.get_regions('T1884A'))
    
    print("\nSubregions of T00:")
    t_hierarchy.list_subregions('T00')