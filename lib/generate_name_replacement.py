import pandas as pd

def single_names_dataframe(filename, colname, replacement):
    names = pd.read_csv(filename, sep="\s+",names=["Name","Frequency","Cumulative Frequency","Rank"])
    names.dropna(inplace=True)
    names["Name"] = names["Name"].apply(lambda x: x.title())
    names[colname] = names[["Frequency","Rank"]].apply(lambda x:tuple([replacement]+list(x)),axis=1)
    names.drop(["Frequency","Cumulative Frequency", "Rank"], axis=1, inplace=True)
    
    return names
    
male_names = single_names_dataframe("male_proper_names.tsv", "Male", "proper_name_male")
female_names = single_names_dataframe("female_proper_names.tsv", "Female", "proper_name_male")
surnames = single_names_dataframe("surnames.tsv", "Surnames", "proper_name_surname")

def build_names_dictionary(male, female, surnames):

    all_names = surnames.set_index("Name").join(other=[male_names.set_index("Name"),
                                                       female_names.set_index("Name")],
                                                how="outer", sort="Name")

    all_names[["Replacement","Frequency"]] = \
        all_names.apply(lambda x: pd.Series(sorted(list(x.dropna()), key=lambda tup: tup[2])[0][:2]), axis=1)
        
    all_names["Name"] = all_names.index
    all_names.index = range(all_names.shape[0])

    return all_names[["Name","Replacement","Frequency"]]

all_names_df = build_names_dictionary(male_names,female_names,surnames)

all_names_df.to_csv("proper_name_replacement.csv")
