import pandas as pd
from flaskr.dietDB import Database
import loadConfig
import sys


def connectDB():
    try:
        config = loadConfig.Config("diet.json")

        db = Database(config=config)

        return db
    except:
        for path in sys.path:
            print(path)

def calculate_goals(bodyweight, maintenance):
    """Calculates daily nutritient and calorie goals, as well as target weight for each week

    Args:
        bodyweight (double): current bodyweight
        maintenance (int): calories needed to maintain current bodyweight
    Returns:
        dataframes: results saved in daily_df, weekly_df and macro_df
    """
    #Starting data
    ind = ["Week_1", "Week_2", "Week_3", "Week_4",
           "Week_5", "Week_6", "Week_7", "Week_8", "Week_9"]
    loss_pctg_w = {"loss": [(7700/7000)/bodyweight, 0.01,
                            0.01, 0.01, 0.0, 0.008, 0.0075, 0.006, 0.005]}
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
    dict_deficit_d = {"deficit": deficit_d}
    daily_df = pd.DataFrame(dict_deficit_d, index=ind)
    daily_df["calories"] = maintenance - \
        (daily_df.deficit + (0.1 * daily_df.deficit))

    prot_per_kg = [2.6, 2.4, 2.4, 2.4, 1.9, 2.3, 2.3, 2.3, 2.3]
    fats_pctg = [0.18, 0.18, 0.18, 0.18, 0.18, 0.17, 0.17, 0.17, 0.17]
    daily_df["fats_pctg"] = fats_pctg
    daily_df["protein_per_kg"] = prot_per_kg
    daily_df["protein"] = bodyweight * daily_df.protein_per_kg
    daily_df["fats"] = daily_df.calories * daily_df.fats_pctg / 9.3
    daily_df["carbs"] = (
        daily_df.calories - (daily_df.protein * 4.1) - (daily_df.fats * 9.3)) / 4.1

    #Creating macro_df dataframe
    indices = [1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 5.1,
               5.2, 5.3, 6.1, 6.2, 6.3, 7.1, 7.2, 7.3, 8.1, 8.2, 8.3, 9.1, 9.2, 9.3]
    macro_df = pd.DataFrame(index=indices)
    cals = [daily_df.calories[0], daily_df.calories[0], daily_df.calories[0],
            daily_df.calories[1] - 0.2 *
            daily_df.calories[1], daily_df.calories[1], daily_df.calories[1] +
            0.2 * daily_df.calories[1],
            daily_df.calories[2] - 0.2 *
            daily_df.calories[2], daily_df.calories[2], daily_df.calories[2] +
            0.2 * daily_df.calories[2],
            daily_df.calories[3] - 0.2 *
            daily_df.calories[3], daily_df.calories[3], daily_df.calories[3] +
            0.2 * daily_df.calories[3],
            daily_df.calories[4], daily_df.calories[4], daily_df.calories[4],
            daily_df.calories[5] - 0.2 *
            daily_df.calories[5], daily_df.calories[5], daily_df.calories[5] +
            0.2 * daily_df.calories[5],
            daily_df.calories[6] - 0.2 *
            daily_df.calories[6], daily_df.calories[6], daily_df.calories[6] +
            0.2 * daily_df.calories[6],
            daily_df.calories[7] - 0.2 *
            daily_df.calories[7], daily_df.calories[7], daily_df.calories[7] +
            0.2 * daily_df.calories[7],
            daily_df.calories[8] - 0.2 * daily_df.calories[8], daily_df.calories[8], daily_df.calories[8] + 0.2 * daily_df.calories[8]]

    macro_df["calories"] = cals
    macro_df["protein"] = 0
    macro_df["carbs"] = 0
    macro_df["fats"] = 0

    for i in range(len(indices)):
        if i < 4:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[0]
        elif i < 7:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[1]
        elif i < 10:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[2]
        elif i < 13:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[3]
        elif i < 16:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[4]
        elif i < 19:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[5]
        elif i < 22:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[6]
        elif i < 25:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[7]
        else:
            macro_df["protein"].iloc[i] = daily_df["protein"].iloc[8]

    for i in range(len(indices)):
        if i < 4:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[0] / 9.3 + 1
        elif i < 7:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[1] / 9.3 + 1
        elif i < 10:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[2] / 9.3 + 1
        elif i < 13:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[3] / 9.3 + 1
        elif i < 16:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[4] / 9.3 + 1
        elif i < 19:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[5] / 9.3 + 1
        elif i < 22:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[6] / 9.3 + 1
        elif i < 25:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[7] / 9.3 + 1
        else:
            macro_df["fats"].iloc[i] = macro_df.calories.iloc[i] * \
                daily_df.fats_pctg.iloc[8] / 9.3 + 1

    macro_df["carbs"] = (macro_df["calories"] - (macro_df["protein"]
                                                 * 4.1) - (macro_df["fats"] * 9.3)) / 4.1

    #Cleanup
    daily_df = daily_df.drop(["fats_pctg", "protein_per_kg"], axis=1)

    #rounding dataframes
    daily_df = daily_df.round(0)
    weekly_df = weekly_df.round({"loss": 4, "deficit": 0, "weight": 2})
    macro_df = macro_df.round(0)

    return weekly_df, daily_df, macro_df

def test_calculate(bodyweigt, maintenance):
    weekly_df, daily_df, macro_df = calculate_goals(bodyweigt, maintenance)
    
    print(weekly_df)
    print(daily_df)
    print(macro_df)
    
def test_data_creation(bodyweigt, maintenance):
    db = connectDB()
    weekly_df, daily_df, macro_df = calculate_goals(bodyweigt, maintenance)

    data = {}
    #saving into target table (except targetWeight)
    for i in range(9):
        data["week"] = i
        for j in range(3):
            x = round(1.1 + i + j * 0.1, 1)
            data["period"] = j
            data["calories"] = macro_df.loc[x, "calories"]
            data["protein"] = macro_df.loc[x, "protein"]
            data["carbs"] = macro_df.loc[x, "carbs"]
            data["fats"] = macro_df.loc[x, "fats"]

            
            db.insertTargetData(1, data)
            
            
   



def test_iteration():
    for i in range(9):
        for j in range(3):
            print(round(1.1 + i + j * 0.1, 1))
    
def main():
    test_calculate(80, 2500)
    test_data_creation(80, 2500)

if __name__ == "__main__":
    main()