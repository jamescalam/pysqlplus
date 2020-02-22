# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:31:01 2019

@author: jamesbriggs
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""
Manual bucketing code for quick and easy visualising. User must have data
ready for input within a Pandas Dataframe.
"""

class manual:
    def __init__(self, data, column):
        self.data = data
        self.column = column
        
        # column summary
        print("{} Summary\n\nmaximum:\t{}\nminimum:\t{}\nmean:\t\t{}\nstandard deviation:\t{}".format(
                    column,
                    data[column].max(),
                    data[column].min(),
                    data[column].mean(),
                    data[column].std()))

    def see(self, buckets, measure="On_Bal_Exp", method="sum"):
        
        def bucket(x):
            # 'x' is the individual sample value, 'buckets' the list of integers
            # that will act as our boundaries
            for i in range(len(buckets)+1):
                # create custom 00X, 0XX, XXX numbering system to keep columns in
                # line for visuals
                _i = "000"[:-len(str(i))] + str(i)
                if i == 0:
                    if x < buckets[i]:
                        # for first range bucket
                        return "{})         < {}".format(_i, buckets[i])
                elif i == 1:
                    # for normal range bucket
                    if x >= buckets[i-1] and x <= buckets[i]:
                        return "{})      {} - {}".format(_i, buckets[i-1], buckets[i])
                elif i == len(buckets):
                    # for final bucket
                    if x > buckets[i-1]:
                        return "{})      > {}".format(_i, buckets[i-1])
                else:
                    if x > buckets[i-1] and x <= buckets[i]:
                        return "{})      {} - {}".format(_i, buckets[i-1], buckets[i])


        # this vectorises (makes fast) the function above
        vbucket = np.vectorize(bucket)

        # applying the bucketing function
        self.data[self.column+"_grp"] = self.data[self.column].apply(vbucket)
        
        # aggregating data ready for visualisation
        if method == "count":
            buck = self.data.groupby([self.column+"_grp"])[measure].count().reset_index()
        else:
            buck = self.data.groupby([self.column+"_grp"])[measure].sum().reset_index()
            
        # plot the figure so we can see the distribution
        # set size
        plt.figure(figsize=(10,8))
        # setting colour scheme
        dt_colour = ['#E3E48D', '#009A44', '#DDEFE8', '#9DD4CF', '#6FC2B4',
                     '#00ABAB', '#007680', '#004F59', '#A0DCFF', '#005587',
                     '#041E42', '#A7A8AA', '#63666A']
        sns.set_palette(dt_colour)
        # creating the barplot
        sns.barplot(data=buck, x=self.column+"_grp", y=measure)
        # making it pretty
        plt.xticks(rotation='vertical')
        # plotting
        plt.show()

        # print the SQL output
        # initialise our bytes object (starts with 'a', then increases the
        # value in bytes per iteration to get next unicode letter)
        n = bytes('a', 'utf-8')[0]
        print("CASE\n")
        for i in range(len(buckets)+1):
            letter = str(bytes([n]))[2]  # pull string letter from bytes
            if i == 0:
                print("\t\tWHEN {} < {}".format(self.column, buckets[i]) +
                      "\t\t\t\t\t\tTHEN '{}. < {}'".format(letter, buckets[i]))
            elif i == 1:
                print("\t\tWHEN {} >= {} and {} <= {}\t\tTHEN '{} - {}'".format(self.column,
                                                                            buckets[i-1],
                                                                            self.column,
                                                                            buckets[i],
                                                                            buckets[i-1],
                                                                            buckets[i]))
            elif i == len(buckets):
                print("\t\tWHEN {} > {}".format(self.column, buckets[i-1]) +
                      "\t\t\t\t\t\tTHEN '{}. > {}'".format(letter,
                                         buckets[i-1]))
            else:
                print("\t\tWHEN {} > {} and {} <= {}\t\tTHEN '{} - {}'".format(self.column,
                                                                            buckets[i-1],
                                                                            self.column,
                                                                            buckets[i],
                                                                            buckets[i-1],
                                                                            buckets[i]))            
        print("\t\t\t\t\t\t\t\t\t\tELSE 'N/A' \n")
        print("END AS {}".format(self.column+'_grp'))
        n += 1  # increment byte value of n


"""
Autobucketer for automatically generating bucket ranges for data based on
multiple 'attractive' bucketing distributions such as;

    - Normal Distribution
    - Right skewed (feed into flat)
    - Left skewed (feed into flat)
    - Flat
    - U-shaped

Normalised functions for each distribution is defined, incoming data is
bucketed (mostly randomly initially) and then normalised. An error function is
then used to calculate how 'attractive' the resulting bucketing is. This
process is then repeated wherein we use a Bayesian optimisation function to
calculate the most probable good bucket locations. After n iterations, the
lowest error function is taken to have been produced by the most attractive
figure and so we use these values moving forward.
"""

class auto:
    def __init__():
        pass

    """
    _________________________________DISTRIBUTIONS_____________________________
    
    Here we will define the distributions that we would like our figures to look
    like.
    ___________________________________________________________________________
    """
    class distributions:
        
        def __init__():
            pass
    
        def normal(x, mean, std):
            # the normal distribution
            power = -((x - mean)**2/(1 * std)**2)
            return ( 1 / (std * np.sqrt(2*np.pi)) ) * np.exp(1) ** power
        
        def flat(x):
            # here we try to flatten buckets as much as possible
            return 0.5
        
        def u(x):
            # a u-shaped distribution [not defined]
            raise ValueError("uShape distribution is not yet implemented.")
            
        # vectorising the above
        vNormal = np.vectorize(normal)
        vFlat = np.vectorize(flat)
        vU = np.vectorize(u)
        
        def find(x):
            # here we find the optimum distribution shape, 'x' is a data column
            # first we see how much of the data is within 1 std of the mean (for a
            # normally distributed dataset this will be around 68%)
            x_mean = x.mean()
            x_std = x.std()
            x_len = len(x)
            
            # how much of the data lies within the first std range?
            x_len_std = len(x) - len(x.between(x_mean - x_std,
                                                x_mean + x_std))
            
            # calculate the percentage
            x_perc = (x_len - x_len_std) / x_len
            # !!! just for testing
            print("Percentage of values within 1 std: {}".format(x_perc))
            
            # is it normal? (closeish to the 68% expected?)
            if x_perc >= 0.58 and x_perc <= 0.78:
                return "normal"
            else:
                return "flat"
        
    """
    __________________________________CALCULATIONS_____________________________
    
    Here we will define the calculations that we need throughout the process.
    ___________________________________________________________________________
    """
    
    class calculations:
        
        def __init__():
            pass
        
        def normalise(x, x_min, x_max):
            return (x - x_min)/(x_max - x_min)
        
        vNormalise = np.vectorize(normalise)
        
    """
    ___________________________________BUCKETING_______________________________
    
    Here we define all bucketing functions.
    ___________________________________________________________________________
    """
    
    class bucket:
        
        def __init__():
            pass
        
        def discrete(x, buckets):
            # create discrete bucket values, we will use this for 'display'
    
            # 'x' is the individual sample value, 'buckets' the list of integers
            # that will act as our boundaries
    
            for i in range(len(buckets)+1):
                # create custom 00X, 0XX, XXX numbering system to keep columns in
                # line for visuals
                _i = "000"[:-len(str(i))] + str(i)
                if i == 0 and x < buckets[i]:
                    # for first range bucket
                    return "{})         < {}".format(_i, buckets[i])
                elif x >= buckets[i-1] and x <= buckets[i]:
                    # for normal range bucket
                    return "{})      {} - {}".format(_i, buckets[i-1], buckets[i])
                elif i == len(buckets) and x > buckets[i-1]:
                    # for the final bucket
                    return "{})      > {}".format(_i, buckets[i-1])
                else:
                    # this shouldn't happen so raise ValueError if so
                    raise ValueError("Values do not match bucket class "
                                     "discrete function if-elif-else logic.")
            
        def continuous(x, buckets):
            # create continuous bucket values, we use this for calculation
            
            # 'x' is the individual sample value, 'buckets' the list of integers
            # that will act as our boundaries
            
            for i in range(len(buckets)+1):
                # create custom 00X, 0XX, XXX numbering system to keep columns in
                # line for visuals
                _i = "000"[:-len(str(i))] + str(i)
                if i == 0 and x < buckets[i]:
                    # for first range bucket
                    return buckets[i]
                elif x >= buckets[i-1] and x <= buckets[i]:
                    # for normal range bucket
                    return buckets[i-1]+buckets[i]*.5
                elif i == len(buckets) and x > buckets[i-1]:
                    # for the final bucket
                    return buckets[i-1]
                else:
                    # this shouldn't happen so raise ValueError if so
                    raise ValueError("Values do not match bucket class "
                                     "continuous function if-elif-else logic.")
                    
        # vectorising the two bucketing functions (increases speed)
        vDiscrete = np.vectorize(discrete)
        vContinuous = np.vectorize(continuous)
                    
    
    def run(column, measure="On_Bal_Exp"):
        pass