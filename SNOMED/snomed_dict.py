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

    def merge_main_regions(self, new_region, regions_to_merge, new_name=None):
        """
        Concatenate two or more main regions into one new main region.
        - new_region: str, the code for the new main region (e.g. 'T99')
        - regions_to_merge: list of str, the main region codes to merge (e.g. ['T00', 'T01'])
        - new_name: str, optional name for the new region (default: name from first region merged)
        """
        merged_subregions = {}
        for region in regions_to_merge:
            if region not in self.hierarchy:
                print(f"Region {region} not found, skipping.")
                continue
            for subregion, sub_dict in self.hierarchy[region]["subregions"].items():
                if subregion not in merged_subregions:
                    merged_subregions[subregion] = {
                        "name": sub_dict["name"],
                        "codes": []
                    }
                merged_subregions[subregion]["codes"].extend(sub_dict["codes"])
        # Set new region name
        if not new_name:
            # Use name from first region, or "Merged Region"
            new_name = self.hierarchy[regions_to_merge[0]]["name"] if regions_to_merge else "Merged Region"
        # Overwrite hierarchy
        self.hierarchy[new_region] = {
            "name": new_name,
            "subregions": merged_subregions
        }
        # Remove old regions
        for region in regions_to_merge:
            if region in self.hierarchy:
                del self.hierarchy[region]

    def update_region(self, region, new_name):
        """
        Update the name of a main region.
        - region: str, the main region code (e.g. 'T00')
        - new_name: str, the new name for the region
        """
        if region in self.hierarchy:
            self.hierarchy[region]["name"] = new_name
        else:
            print(f"Region {region} not found.")

    def split_main_region(self, original_region, subregion_map):
        """
        Split a main region into multiple new main regions.
        - original_region: str, the main region code to split (e.g. 'T00')
        - subregion_map: dict, mapping new region codes to lists of subregion codes to move.
          Example: {'T00A': ['T000', 'T001'], 'T00B': ['T002']}
        """
        if original_region not in self.hierarchy:
            print(f"Region {original_region} not found.")
            return
    
        original_subregions = self.hierarchy[original_region]["subregions"]
    
        for new_region, subregion_list in subregion_map.items():
            new_subregions = {}
            for subregion in subregion_list:
                if subregion in original_subregions:
                    new_subregions[subregion] = original_subregions[subregion]
            # Use the name of the first subregion as the new region name, or "Split Region"
            new_name = (
                next(iter(new_subregions.values()))["name"]
                if new_subregions else "Split Region"
            )
            self.hierarchy[new_region] = {
                "name": new_name,
                "subregions": new_subregions
            }
    
        # Remove moved subregions from the original region
        for subregion_list in subregion_map.values():
            for subregion in subregion_list:
                if subregion in original_subregions:
                    del original_subregions[subregion]
        
        # Remove the original region if no subregions left
        if not original_subregions:
            del self.hierarchy[original_region]


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