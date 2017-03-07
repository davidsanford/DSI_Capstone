import pandas as pd

def get_proper_name_dict(freq_cut = 0.0):
    proper_names_df = pd.read_csv("proper_name_replacement.csv")
    if freq_cut < 1:
        proper_names_df = \
            proper_names_df[proper_names_df["Frequency"] >= freq_cut]
    else:
        proper_names_df = \
            proper_names_df.sort_values("Frequency",
                                        ascending=False).head(int(freq_cut))
        
    proper_names_dict = \
        {proper_names_df["Name"].loc[i]:proper_names_df["Replacement"].loc[i] \
         for i in proper_names_df.index}
    
    return proper_names_dict
