import json, math

def roundUpToPowerOfTwo(num):
    return math.pow(2, math.ceil(math.log(num)/math.log(2)))

def generate_brackets(team_list, match_list=None):
    num_teams = len(team_list)
    power = int(roundUpToPowerOfTwo(num_teams))
    num_rounds = int(math.ceil(math.log(num_teams, 2)))
    t_height = 3 + power/4
    # if num_teams%4:
    #     t_height += 1
    t_width = (4 * num_rounds) - 1
    #Build a matrix of our table for later use.
    table = []
    for i in range(0,t_height):
        table.append(['' for j in range(0,t_width)])

    #Let's start generating code; we are just going to toss TD's into the matrix, and worry about rows later I guess

    #First row is headers only
    middle = t_width/2
    table[0][middle] = '<tr class="middle"></tr>'
    table[0][middle+1] = '<tr class="round%s>Round %s</tr>' % (num_rounds, num_rounds)
    table[0][middle-1] = '<tr class="round%s>Round %s</tr>' % (num_rounds, num_rounds)



    return num_rounds, t_height, t_width, table