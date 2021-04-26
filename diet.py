import numpy as np
import pandas as pd
from pandas._config import config

class diet():

    def __init__(self) -> None:
        pass


    def configure(self, bodyweight, maintenance):
        #Starting data
        ind = ["Week_1", "Week_2", "Week_3", "Week_4", "Week_5", "Week_6", "Week_7", "Week_8", "Week_9"]
        loss_pctg_w =  {"loss" :[(7700/7000)/bodyweight, 0.01, 0.01, 0.01, 0.0, 0.008, 0.0075, 0.006, 0.005]}
        deficit_w = [7700]
        weight = [bodyweight - (7700/7000)]
        deficit_d = [1100]

        #Creating initial missing data
        for i in range(9):
            if i != 0:
                tmp = weight[i - 1] * loss_pctg_w["loss"][i] * 1000
                deficit_d.append(tmp)
                p = tmp * 7
                deficit_w.append(p)
                weight.append(weight[i - 1] - (p / 7000))


        #Creating weekly_df dataframe
        weekly_df = pd.DataFrame(loss_pctg_w, index=ind)
        weekly_df["deficit"] = deficit_w
        weekly_df["weight"] = weight

        #Creating daily_df dataframe
        dict_deficit_d = {"deficit":deficit_d}
        daily_df = pd.DataFrame(dict_deficit_d, index=ind)
        daily_df["calories"] = maintenance - (daily_df.deficit + (0.1 * daily_df.deficit))

        prot_per_kg = [2.6, 2.4, 2.4, 2.4, 1.9, 2.3, 2.3, 2.3, 2.3]
        fats_pctg = [0.18, 0.18, 0.18, 0.18, 0.18, 0.17, 0.17, 0.17, 0.17]
        daily_df["fats_pctg"] = fats_pctg
        daily_df["protein_per_kg"] = prot_per_kg
        daily_df["protein"] = bodyweight * daily_df.protein_per_kg
        daily_df["fats"] = daily_df.calories * daily_df.fats_pctg / 9.3
        daily_df["carbs"] = (daily_df.calories - (daily_df.protein * 4.1) - (daily_df.fats * 9.3)) / 4.1 

        

        #Cleanup


        #rounding dataframes
        daily_df = daily_df.round({"loss":4, "deficit": 0, "weight": 2})
        weekly_df = weekly_df.round(1)
        print(weekly_df)
        print(daily_df)


test = diet()
test.configure(80,2800)
