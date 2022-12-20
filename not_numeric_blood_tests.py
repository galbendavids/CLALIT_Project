#this script helps in classifcation of blood test resuts using basic search

#this script get not numeric datasets and creates a dataset for a patient
import pandas as pd
import re
df=pd.read_csv("/Users/galbd/Desktop/clalit/csvs/icds/blood_test_relevant_not_numeric_2.csv",low_memory=True)

print(df)
can="ֿבוטל|נכון|מתוקנת|מספיק|לבדיקה|חומר|פעמים|מדבקה|לחזור|יש|טכניות|קודמת|זיהוי|לפי בקשת|הסליחה|טעות|עקב|פסל|קטנה|ֿאינו|פסול|בעבודה|קיימת|ריקה|נפסל|קודמת|שנית|לבדוק|לא|מבוטל"

canceld=df[df['res'].str.contains(can)==True]
not_canceld=df[df['res'].str.contains(can)==False]


neg="שלילי|קטן|Negative|NEGATIVE|negative"
negative=not_canceld[not_canceld['res'].str.contains(neg)==True]
prob_not_negative=not_canceld[not_canceld['res'].str.contains(neg)==False]
small="<"
smaller=prob_not_negative[prob_not_negative['res'].str.contains(small)==True]
not_negative=prob_not_negative[prob_not_negative['res'].str.contains(small)==False]

negative_overall=pd.concat([negative,smaller])
#not_negative=not_canceld[not_canceld['res'].str.contains(neg)==False]




#pos="אעאעאע|ֿחיובי |גדול|Positive|POSITIVE|positive"
pos="חיובי|positive|POSITIVE|Positive"
positive=not_negative[not_negative['res'].str.contains(pos)==True]
prob_nor_postive_nor_negative=not_negative[not_negative['res'].str.contains(pos)==False]

big=">"
bigger=prob_nor_postive_nor_negative[prob_nor_postive_nor_negative['res'].str.contains(big)==True]
nor_postive_nor_negative=prob_nor_postive_nor_negative[prob_nor_postive_nor_negative['res'].str.contains(big)==False]

positive_overall=pd.concat([positive,bigger])




lst_numerric = []
lst_not_numeric=[]
for index, row in nor_postive_nor_negative.iterrows():
    try:
        float(row["res"])
        lst_numerric.append(index)
    except:
        lst_not_numeric.append(index)



#this does nothing..
shit_happens=nor_postive_nor_negative.loc[lst_not_numeric]


#negative_overall
#todo hold binaric feature for a patient if it happens once or more
df_negative=negative_overall.groupby(['PID','test'])['res'].last()
df_negative=df_negative.to_frame()
df_negative.loc[:,'res']=True
df_negative.reset_index(inplace=True)
df_negative['test']=(df_negative['test']).astype(str)
df_negative['test']=(df_negative['test'])+'_negative'
df_negative_pivot=df_negative.pivot(index='PID', columns='test', values='res')
df_negative_pivot=df_negative_pivot.fillna(False)
#todo after joining - dot forget to fll nan with 0s

#positive_overall
#todo hold binaric feature for a patient if it happens once or more

df_positive=positive_overall.groupby(['PID','test'])['res'].last()
df_positive=df_positive.to_frame()
df_positive.loc[:,'res']=True
df_positive.reset_index(inplace=True)
df_positive['test']=(df_positive['test']).astype(str)
df_positive['test']=(df_positive['test'])+'_positive'
df_positive_pivot=df_positive.pivot(index='PID', columns='test', values='res')
df_positive_pivot=df_positive_pivot.fillna(False)

#todo after joining - dot forget to fll nan with 0s

df_numeric=nor_postive_nor_negative.loc[lst_numerric]
#todo get last, and max value for a patient


df_negative_pivot.reset_index(inplace=True)
df_positive_pivot.reset_index(inplace=True)
result=df_negative_pivot.merge(df_positive_pivot, how='cross')



