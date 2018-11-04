
##################
# Import libraries
##################

import pandas as pd
import numpy as np
import math


###########
# Load data
###########

iris = pd.read_csv('iris.csv', header=None)
iris.columns = ['sepal_length', 'sepal_width',
                'petal_length', 'petal_width', 'target_class']


###############################################
# Merging rows based on least chi square values 
###############################################

def merge_rows(df,feature):

    tdf = df[:-1]
    distinct_values = sorted(set(tdf['chi2']), reverse=False)

    col_names =  [feature,'Iris-setosa', 'Iris-versicolor', 
                  'Iris-virginica','chi2']
    #new dataframe to send back
    updated_df  = pd.DataFrame(columns = col_names) 
    
    updated_df_index=0
    for index, row in df.iterrows(): #iterating over old dataframe
        if(index==0):
            updated_df.loc[len(updated_df)] = df.loc[index]
            updated_df_index+=1
        else:
            if(df.loc[index-1]['chi2']==distinct_values[0]): #merge
                updated_df.loc[updated_df_index-1]['Iris-setosa']+=df.loc[index]['Iris-setosa']
                updated_df.loc[updated_df_index-1]['Iris-versicolor']+=df.loc[index]['Iris-versicolor']
                updated_df.loc[updated_df_index-1]['Iris-virginica']+=df.loc[index]['Iris-virginica']
            else:
                updated_df.loc[len(updated_df)] = df.loc[index]
                updated_df_index+=1
                
    updated_df['chi2'] = 0.   #clearing old chi square values

    return updated_df
        

#####################
# Chi square function
#####################

def calc_chi2(array):
    shape = array.shape
    n = float(array.sum()) #total number of entries
    row={}
    column={}
    
    #find row-wise summations
    for i in range(shape[0]):
        row[i] = array[i].sum()
    
    #find column-wise summations
    for j in range(shape[1]):
        column[j] = array[:,j].sum()

    chi2 = 0
    
    #using the chi square formula
    for i in range(shape[0]):
        for j in range(shape[1]):
            eij = row[i]*column[j] / n 
            oij = array[i,j]  
            if eij==0.:
                chi2 += 0. #making sure nan doesnt bother us
            else: 
                chi2 += math.pow((oij - eij),2) / float(eij)
  
    return chi2
    
    
##################################################################
# This function calculates the chi square values for each row pair
##################################################################

def update_chi2_column(contingency_table,feature):
    
    for index, row in contingency_table.iterrows():
        #we dont wanna work with the very last row alone
        if(index!=contingency_table.shape[0]-1): 
            
            # prepare an array with two rows of data at a time
            list1=[]
            list2=[]
            list1.append(contingency_table.loc[index]['Iris-setosa'])
            list1.append(contingency_table.loc[index]['Iris-versicolor'])
            list1.append(contingency_table.loc[index]['Iris-virginica'])
            list2.append(contingency_table.loc[index+1]['Iris-setosa'])
            list2.append(contingency_table.loc[index+1]['Iris-versicolor'])
            list2.append(contingency_table.loc[index+1]['Iris-virginica'])
            prep_chi2 = np.array([np.array(list1),np.array(list2)])
            
            #actually compute the chi square values
            c2 = calc_chi2(prep_chi2)
            
            #update dataframe
            contingency_table.loc[index]['chi2'] = c2
    return contingency_table


##############################################
# This function calculates the frequency table
##############################################

def create_contingency_table(dataframe,feature):
    distinct_values = sorted(set(dataframe[feature]), reverse=False)
    col_names =  [feature,'Iris-setosa', 'Iris-versicolor','Iris-virginica','chi2']
    my_contingency  = pd.DataFrame(columns = col_names)
    
    #these are the distinct attribute values
    for i in range(len(distinct_values)): 
        temp_df=dataframe.loc[dataframe[feature]==distinct_values[i]]
        count_dict = temp_df["target_class"].value_counts().to_dict()

        #initialize with zero frequencies
        setosa_count = 0
        versicolor_count = 0
        virginica_count = 0
        
        #update if necessary
        if 'Iris-setosa' in count_dict:
            setosa_count = count_dict['Iris-setosa']
        if 'Iris-versicolor' in count_dict:
            versicolor_count = count_dict['Iris-versicolor']
        if 'Iris-virginica' in count_dict:
            virginica_count = count_dict['Iris-virginica']

        new_row = [distinct_values[i],setosa_count,versicolor_count,virginica_count,0]
        my_contingency.loc[len(my_contingency)] = new_row

    return my_contingency


####################
# Chi Merge function
####################

def chimerge(feature, data, max_interval):
    df = data.sort_values(by=[feature],ascending=True).reset_index()
    
    #generate frequency table
    contingency_table = create_contingency_table(df,feature)

    #calculate initial number of intervals. #initially, all entries
    #are intervals on their own
    num_intervals= contingency_table.shape[0] 

    # keep looping till max-interval condition satisfied
    while num_intervals > max_interval: 
        #compute chi square for adjacent row pairs
        chi2_df = update_chi2_column(contingency_table,feature) 
        
        #merge rows based on lowest chi square values
        contingency_table = merge_rows(chi2_df,feature)
        
        #update number of intervals
        num_intervals= contingency_table.shape[0]               

    # Print results
    print('The split points for '+feature+' are:')
    for index, row in contingency_table.iterrows():
        print(contingency_table.loc[index][feature])
    
    print('The final intervals for '+feature+' are:')
    for index, row in contingency_table.iterrows():
        if(index!=contingency_table.shape[0]-1):
            for index2, row2 in df.iterrows():
                if df.loc[index2][feature]<contingency_table.loc[index+1][feature]:
                    temp = df.loc[index2][feature]
        else:
            temp = df[feature].iloc[-1]
        print("["+str(contingency_table.loc[index][feature])+","+str(temp)+"]")
    print(" ")

    
######
# Init
######
if __name__=='__main__':
	for feature in ['sepal_length', 'sepal_width', 'petal_length','petal_width']:
		chimerge(feature=feature, data=iris, max_interval=6)

