parent_cols_to_discard = ['KEY', 'SET-OF-ind_group']

columns_and_value_labels_for_replacement = \
    {'status-mask': {'0':'No mask', '1':'Non-mask face covering', '6':'Any Mask - PROPERLY', '7':'Any Mask - IMPROPERLY'},
    'status-distance': {'1':"Someone within arm's length", '0':"Someone within arm's length"},
    'status-gender': {'1':"Male", '2':"Female"},
    'status-agegroup': {'1':"Young (below 30)", '2':"Middle-age (30-50)", '3':"Old (50+)"}
    }

intro_group_area_replacements_dict = \
    {1:"Gabtali bus terminal", 2:"Mohammadpur town hall", 3:"Mohammadpur bus stand",
    4:"Mohammadpur Shia Mosque", 5:"Farmgate area", 6:"Badda and notun market areas",
    7:"Mirpur-1 Golchottor, Shah Ali Market", 8:"Mirpur-10 Golchottor",
    9:"Bashundhara City Shopping Mall", 10:"Jamuna Future Park Shopping Mall",
    11:"Uttara Muscat Plaza Shopping Mall", 12:"Uttara Rajalakshi Shopping Mall",
    13:"Mohakhali bus terminal"}

upazila_replacement_dict = \
        {"Gabtali bus terminal":"Darus Salam", "Mohammadpur town hall":"Mohammadpur", "Mohammadpur bus stand":"Mohammadpur",
        "Mohammadpur Shia Mosque":"Mohammadpur", "Farmgate area":"Tejgaon", "Badda and notun market areas":"Badda",
        "Mirpur-1 Golchottor, Shah Ali Market":"Mirpur", "Mirpur-10 Golchottor":"Mirpur",
        "Bashundhara City Shopping Mall":"Sher-E-Bangla Nagar", "Jamuna Future Park Shopping Mall":"Khilkhet",
        "Uttara Muscat Plaza Shopping Mall":"Uttara", "Uttara Rajalakshi Shopping Mall":"Uttara",
        "Mohakhali bus terminal":"Tejgaon"}

union_replacement_dict = \
        {"Gabtali bus terminal":"Ward No-10", "Mohammadpur town hall":"Ward No-31", "Mohammadpur bus stand":"Ward No-33",
        "Mohammadpur Shia Mosque":"Ward No-33", "Farmgate area":"Ward No-27", "Badda and notun market areas":"Ward No-21",
        "Mirpur-1 Golchottor, Shah Ali Market":"Ward No-8", "Mirpur-10 Golchottor":"Ward No-3",
        "Bashundhara City Shopping Mall":"Ward No-27", "Jamuna Future Park Shopping Mall":"Ward No-17",
        "Uttara Muscat Plaza Shopping Mall":"Ward No-1", "Uttara Rajalakshi Shopping Mall":"Ward No-1",
        "Mohakhali bus terminal":"Ward No-20"}

district_replacement_dict = \
        {"Gabtali bus terminal":"Dhaka", "Mohammadpur town hall":"Dhaka", "Mohammadpur bus stand":"Dhaka",
        "Mohammadpur Shia Mosque":"Dhaka", "Farmgate area":"Dhaka", "Badda and notun market areas":"Dhaka",
        "Mirpur-1 Golchottor, Shah Ali Market":"Dhaka", "Mirpur-10 Golchottor":"Dhaka",
        "Bashundhara City Shopping Mall":"Dhaka", "Jamuna Future Park Shopping Mall":"Dhaka",
        "Uttara Muscat Plaza Shopping Mall":"Dhaka", "Uttara Rajalakshi Shopping Mall":"Dhaka",
        "Mohakhali bus terminal":"Dhaka"}

division_replacement_dict = \
        {"Gabtali bus terminal":"Dhaka", "Mohammadpur town hall":"Dhaka", "Mohammadpur bus stand":"Dhaka",
        "Mohammadpur Shia Mosque":"Dhaka", "Farmgate area":"Dhaka", "Badda and notun market areas":"Dhaka",
        "Mirpur-1 Golchottor, Shah Ali Market":"Dhaka", "Mirpur-10 Golchottor":"Dhaka",
        "Bashundhara City Shopping Mall":"Dhaka", "Jamuna Future Park Shopping Mall":"Dhaka",
        "Uttara Muscat Plaza Shopping Mall":"Dhaka", "Uttara Rajalakshi Shopping Mall":"Dhaka",
        "Mohakhali bus terminal":"Dhaka"}

replacements = {
    'intro_group_area_replacements_dict':intro_group_area_replacements_dict,
    'upazila_replacement_dict':upazila_replacement_dict,
    'union_replacement_dict':union_replacement_dict,
    'district_replacement_dict':district_replacement_dict,
    'division_replacement_dict':division_replacement_dict
}
