import sys
import os

sys.path.append(os.path.dirname(__file__))
import dncc_cleaning_values
import brac_cleaning_values
import default_cleaning_values

def merge_dicts(dict_a, dict_b):
    dict_a.update(dict_b)
    return dict_a

#replacements
replacements = {
    'bdmaskrct_mask_monitoring_form_bn': \
        merge_dicts(dncc_cleaning_values.replacements, default_cleaning_values.replacements),

    'bdmaskrct_mask_monitoring_form_brac': \
        merge_dicts(brac_cleaning_values.replacements, default_cleaning_values.replacements)
}

# keys_to_drop
keys_to_drop = {
    'bdmaskrct_mask_monitoring_form_bn':dncc_cleaning_values.keys_to_drop,
    'bdmaskrct_mask_monitoring_form_brac':brac_cleaning_values.keys_to_drop
}

#parent_cols_to_discard
parent_cols_to_discard = {
    'bdmaskrct_mask_monitoring_form_bn': default_cleaning_values.parent_cols_to_discard,
    'bdmaskrct_mask_monitoring_form_brac': default_cleaning_values.parent_cols_to_discard
}

#columns_and_value_labels_for_replacement
columns_and_value_labels_for_replacement = {
    'bdmaskrct_mask_monitoring_form_bn': default_cleaning_values.columns_and_value_labels_for_replacement,
    'bdmaskrct_mask_monitoring_form_brac': default_cleaning_values.columns_and_value_labels_for_replacement
}
