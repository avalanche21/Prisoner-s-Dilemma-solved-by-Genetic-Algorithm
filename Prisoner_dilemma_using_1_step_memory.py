import random
from random import seed
import pandas as pd
import numpy as np

seed(7)

# This Prisoners Dilemma program use 1-step memory
# Each game consists of 10 steps


######### INITIALIZATION SUB ####################################################
#################################################################################


# Create the first geration parents (P1 and P2)
P1 = {'Memory': ["CC", "CD", "DC", "DD"], 'Decision': ["D", "C","D","C"]}
Database1 = pd.DataFrame(data=P1)
print("All D strategy")
print(Database1)

P2 = {'Memory': ["CC", "CD", "DC", "DD"], 'Decision': ["D", "D","D","D"]}
Database2 = pd.DataFrame(data=P2)
print("Tit-for_Tat strategy")
print(Database2)


######### FUNCTION SUBS #########################################################
#################################################################################



# MAKE A DECISION
# This function search the case in the database that match with the memory to make a decision
def make_decision(DB,memory):
    decision = DB["Decision"][DB["Memory"] == memory]
    return decision

# CALCULATE SCORE
# This function calculates an individual score for each step, to be used in finding "total game score"
# and then we will find maximum "total game score" leter in the play_and_get_score function
def calculate_score(memory):
    if memory == "CC":
        score = (15-1)
        #score = 14+14
    elif memory == "CD":
        score = 15-15
        #score = 0+15
    elif memory == "DC":
        score = 15-0
        #score = 15+0
    elif memory == "DD":
        score = (15-5)
        #score = 10+10
    return score

# PLAY AND GET SCORES
# This function calculates Total game score, and individual scores for each player
def play_and_get_score(Database1,Database2):
    # Initiate Parent 1
    # At the firt roung of each play, the decision will be randomly generated
    # 50% chance of getting "C", 50% chance of getting "D"
    Player_1 = []
    n = random.uniform(0, 1)
    if n < 0.5:
        Player_1.append("C")
    else:
        Player_1.append("D")

    # Initiate Parent 2
    Player_2 = []
    n = random.uniform(0, 1)
    if n < 0.5:
        Player_2.append("C")
    else:
        Player_2.append("D")

    #Keep the 1-step memory by concatenating two string together, for example, Meory = "C"+"D" = "CD"
    Mem1 = Player_1[0] + Player_2[0]
    #print(Mem1)

    Mem2 = Player_2[0] + Player_1[0]
    #print(Mem1)

    # Calculate the score from the first step of Player 1 and Player 2
    Player_1_score = calculate_score(Mem1)
    Player_2_score = calculate_score(Mem2)
    # Calculate the rest 9 steps of Player 1 and Player 2
    for i in range(1, 10):
        Player_1.append(make_decision(Database1, Mem1).iloc[0])
        Player_2.append(make_decision(Database2, Mem2).iloc[0])
        # print("the index %d:" % i)
        Mem1 = Player_1[i] + Player_2[i]
        Mem2 = Player_2[i] + Player_1[i]
        Player_1_score = Player_1_score + calculate_score(Mem1)
        Player_2_score = Player_2_score + calculate_score(Mem2)
        Total_score  = Player_1_score+Player_2_score
    return(Player_1,Player_2,Player_1_score,Player_2_score, Total_score)
    # This fuction returns 4 values
    # 1) all the steps that player 1 played
    # 2) all the steps that player 2 played
    # 3) Player 1 Score
    # 4) Player 2 Score
    # 5) Total score


# CREATE 2 OFFSPRINGS from 2 PARENTS
# This function create 2 offsprings, by using the CROSSOVER rule and MUTATION rule
# Crossover happens at the secoind and third locus
def create_offspring(Database1,Database2):
    # Crossover with probability = 0.95
    # Rule to cross over    "No Yes Yes No"
    # Mutation = 0.25
    # Offsprings Generation 1   >>>> Create 2 offsprings

    offspring_1 = Database1.copy()
    offspring_2 = Database2.copy()

    print("Cross over process start ....")
    n = random.uniform(0, 1)
    # If cross over >> execute...
    if n < 0.95:
        #print("Cross over happened !")
        for i in range(0, 4):
            k1 = offspring_1["Decision"][1]
            k2 = offspring_1["Decision"][2]

            offspring_1["Decision"][1] = offspring_2["Decision"][1]
            offspring_1["Decision"][2] = offspring_2["Decision"][2]

            offspring_2["Decision"][1] = k1
            offspring_2["Decision"][2] = k2
    #print(offspring_1)
    #print(offspring_2)
    print("Mutation process start ....")
    # Mutation for Offspring 1
    for i in range(0, 4):
        # If Mutation happens >> execute...
        n = random.uniform(0, 1)
        if n < 0.25:
            if offspring_1["Decision"][i] == "C":
                offspring_1["Decision"][i] = "D"
            elif offspring_1["Decision"][i] == "D":
                offspring_1["Decision"][i] = "C"
            print("Mutation happened at posotion %d." % i)
    #print(offspring_1)

    # Mutation for Offspring 2
    for i in range(0, 4):
        n = random.uniform(0, 1)
        if n < 0.25:
            if offspring_2["Decision"][i] == "C":
                offspring_2["Decision"][i] = "D"
            elif offspring_2["Decision"][i] == "D":
                offspring_2["Decision"][i] = "C"
            print("Mutation happened at posotion %d." % i)
    #print(offspring_2)
    return (offspring_1, offspring_2)


######### MAIN SUB (after Initialization sub) ####################################################
##################################################################################################

# Parent create offsprings
print("Try to create offspring")
Generation_1 = create_offspring(Database1,Database2)
print("Show offspring 1")
print(Generation_1[0])
print("Show offspring 2")
print(Generation_1[1])

for m in range(0,100):
    create_offspring(Database1, Database2)

    ############## Parent 1 play with Parent 2 !
    print("Show result of game1")
    Game1 = play_and_get_score(Database1,Database2)
    print("Show Player1")
    print(Game1[0])
    print("Show Player2")
    print(Game1[1])
    print("Player1 Score")
    print(Game1[2])
    print("Player2 Score")
    print(Game1[3])
    print("Total Score Score")
    print(Game1[4])

    ############## Offspring 1 play with Offspring 2
    print("O1 vs O2")
    Game2 = play_and_get_score(Generation_1[0],Generation_1[1])

    ############## Parent 1 play with Offspring 1
    print("P1 vs O1")
    Game3 = play_and_get_score(Database1,Generation_1[0])
    ############## Parent 1 play with Offspring 2
    print("P1 vs O2")
    Game4 = play_and_get_score(Database1,Generation_1[1])
    ############## Parent 2 play with Offspring 1
    print("P2 vs O1")
    Game5 = play_and_get_score(Database2,Generation_1[0])
    ############## Parent 2 play with Offspring 2
    print("P2 vs O2")
    Game6 = play_and_get_score(Database2,Generation_1[1])

    print(Game1[4],Game2[4],Game3[4],Game4[4],Game5[4],Game6[4])


    list_1 = (Game1[4],Game2[4],Game3[4],Game4[4],Game5[4],Game6[4])
    print(np.argmax(list_1))

    if np.argmax(list_1)==0:
        print("Parent 1 vs Parent 2")
        Database1 = Database1.copy()
        Database2 = Database2.copy()
        print(Game1[0])
        print(Game1[1])
    elif np.argmax(list_1)==1:
        print("select O1 vs O2")
        Database1 = Generation_1[0].copy()
        Database2 = Generation_1[1].copy()
        print(Game2[0])
        print(Game2[1])
    elif np.argmax(list_1)==2:
        print("select P1 vs O1")
        Database1 = Database1.copy()
        Database2 = Generation_1[0].copy()
        print(Game3[0])
        print(Game3[1])

    elif np.argmax(list_1)==3:
        print("select P1 vs O2")
        Database1 = Database1.copy()
        Database2 = Generation_1[1].copy()
        print(Game4[0])
        print(Game4[1])
    elif np.argmax(list_1)==4:
        print("select P2 vs O1")
        Database1 = Database2.copy()
        Database2 = Generation_1[0].copy()
        print(Game5[0])
        print(Game5[1])
    elif np.argmax(list_1)==5:
        print("select P2 vs O2")
        Database1 = Database2.copy()
        Database2 = Generation_1[1].copy()
        print(Game6[0])
        print(Game6[1])

print("Iterative process done")
print("The best 2 strategy to maximize the total score are...")
print(Database1)
print(Database2)