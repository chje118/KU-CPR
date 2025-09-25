import pandas as pd
from snomed_dict import SNOMED, SNOMEDHierarchy

if __name__ == "__main__":
    # Load SNOMED data
    snomed_path = "C:/Users/chris/OneDrive/Dokumenter/SDU/Master's Thesis Project/SNOMED/patoSnoMed_2025-04.xlsx"
    xls_snomed = pd.read_excel(snomed_path)
    df_snomed = pd.DataFrame(xls_snomed, columns=['SKSkode', 'DatoFra', 'DatoÆndring', 'DatoTil', 'Kodetekst', 'Fuldtekst'])
    snomed = SNOMED(df_snomed)
    
    # Focus on T-codes (topography)
    t_codes = snomed.get_codes_by_letter('T')
    t_hierarchy = SNOMEDHierarchy(t_codes)

    # Get main regions
    t_hierarchy.list_regions()


    # print("\nExample lookup for T1884A:")
    # print(t_hierarchy.get_regions('T1884A'))
    
    # print("\nSubregions of T00:")
    # t_hierarchy.list_subregions('T00')

    # # Manually editing the dictionary to ensure correctness/clarity
    # t_dict = t_hierarchy.hierarchy
    # t_dict['General/Unknown Topography'] = t_dict.pop('T00')
    # skin_codes = t_dict['T01'] + t_dict['T02'] + t_dict['T03'] + t_hierarchy.get_sub_dict('T0Y2') + t_hierarchy.get_sub_dict('T0Y5')
    # t_dict['Skin, hair and nails'] = skin_codes
    # del t_dict['T01']
    # del t_dict['T02']
    # del t_dict['T03']
    # mamma_codes = t_dict['T04'] + t_hierarchy.get_sub_dict('T0Y4')
    # t_dict['Mammae'] = mamma_codes
    # del t_dict['T04']
    # blood_codes = t_dict['T05'] + t_dict['T06'] + t_dict['T0X']
    # t_dict['Hæmatopoietic and reticuloendothelial system'] = blood_codes
    # del t_dict['T05']
    # del t_dict['T06']
    # del t_dict['T0X']
    # t_dict['Spleen'] = t_dict.pop('T07')
    # lymph_codes = t_dict['T08'] + t_dict['T09']
    # t_dict['Lymphatic System'] = lymph_codes
    # del t_dict['T08']
    # del t_dict['T09']
    # del t_dict['T0Y']
    # skelet_codes = t_dict['T10'] + t_dict['T11'] + t_dict['T12'] + t_hierarchy.get_sub_dict('T1X5')
    # t_dict['Skeletal System'] = skelet_codes
    # del t_dict['T10']
    # del t_dict['T11']
    # del t_dict['T12']
    # muscle_codes = t_dict['T13'] + t_dict['T14'] + t_dict['T16'] + t_dict['T17'] + t_dict['T18']
    # t_dict['Muscular System'] = muscle_codes
    # del t_dict['T13']
    # del t_dict['T14']
    # del t_dict['T16']
    # del t_dict['T17']
    # del t_dict['T18']
    # other_tissue_codes = t_hierarchy.get_sub_dict('T1X0') + t_hierarchy.get_sub_dict('T1X2') + t_hierarchy.get_sub_dict('T1X3') + t_hierarchy.get_sub_dict('T1X7') + t_dict['T1Y'] 
    # t_dict['Other connective and soft tissues'] = other_tissue_codes
    # del t_dict['T1X']
    # del t_dict['T1Y']
    # respiratory_codes = t_dict['T20'] + t_dict['T21'] + t_dict['T22'] + t_dict['T23'] 
    # t_dict['Respiratory System'] = respiratory_codes
    # del t_dict['T20']
    # del t_dict['T21']
    # del t_dict['T22']
    # del t_dict['T23']

# T24: (30 codes)
# T25: (5 codes)
# T26: (17 codes)
# T27: (2 codes)
# T28: (13 codes)
# T29: (9 codes)
# T2X: (3 codes)
# T2Y: (15 codes)
# T30: (1 codes)
# T31: (3 codes)
# T32: (23 codes)
# T33: (15 codes)
# T34: (1 codes)
# T35: (2 codes)
# T36: (3 codes)
# T37: (2 codes)
# T38: (3 codes)
# T39: (2 codes)
# T3X: (4 codes)
# T40: (7 codes)
# T41: (5 codes)
# T42: (7 codes)
# T43: (5 codes)
# T44: (2 codes)
# T45: (23 codes)
# T46: (14 codes)
# T47: (7 codes)
# T48: (20 codes)
# T49: (13 codes)
# T50: (3 codes)
# T51: (15 codes)
# T52: (15 codes)
# T53: (13 codes)
# T54: (5 codes)
# T55: (17 codes)
# T56: (35 codes)
# T57: (6 codes)
# T58: (9 codes)
# T59: (5 codes)
# T5X: (1 codes)
# T5Y: (4 codes)
# T60: (10 codes)
# T61: (27 codes)
# T62: (10 codes)
# T63: (31 codes)
# T64: (17 codes)
# T65: (16 codes)
# T66: (4 codes)
# T67: (43 codes)
# T68: (10 codes)
# T69: (5 codes)
# T6X: (10 codes)
# T6Y: (1 codes)
# T70: (1 codes)
# T71: (39 codes)
# T72: (6 codes)
# T73: (22 codes)
# T74: (19 codes)
# T75: (7 codes)
# T76: (9 codes)
# T77: (12 codes)
# T78: (24 codes)
# T79: (26 codes)
# T7X: (12 codes)
# T7Y: (2 codes)
# T80: (24 codes)
# T81: (8 codes)
# T82: (13 codes)
# T83: (13 codes)
# T84: (1 codes)
# T85: (1 codes)
# T86: (28 codes)
# T87: (16 codes)
# T88: (27 codes)
# T89: (18 codes)
# T8X: (15 codes)
# T8Y: (1 codes)
# T90: (5 codes)
# T91: (5 codes)
# T92: (1 codes)
# T93: (11 codes)
# T94: (1 codes)
# T95: (1 codes)
# T96: (8 codes)
# T97: (6 codes)
# T98: (1 codes)
# T99: (1 codes)
# TE0: (1 codes)
# TN2: (1 codes)
# TN6: (7 codes)
# TN7: (2 codes)
# TX0: (10 codes)
# TX1: (28 codes)
# TX2: (22 codes)
# TX3: (15 codes)
# TX4: (6 codes)
# TX5: (10 codes)
# TX6: (11 codes)
# TX7: (6 codes)
# TX8: (10 codes)
# TX9: (7 codes)
# TXX: (101 codes)
# TXY: (48 codes)
# TY0: (74 codes)
# TY1: (25 codes)
# TY2: (7 codes)
# TY3: (1 codes)
# TY4: (21 codes)
# TY5: (1 codes)
# TY6: (7 codes)
# TY7: (6 codes)
# TY8: (44 codes)
# TY9: (39 codes)
# TYX: (3 codes)
# TYY: (18 codes)


