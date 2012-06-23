import json, math

def roundUpToPowerOfTwo(num):
    return math.pow(2, math.ceil(math.log(num)/math.log(2)))

def generate_brackets(team_list, match_list=None):
    num_teams = len(team_list)
    power = int(roundUpToPowerOfTwo(num_teams))
    num_rounds = int(math.ceil(math.log(num_teams, 2)))
    t_height = 1 + power/4
    # if num_teams%4:
    #     t_height += 1
    t_width = (4 * num_rounds) - 1
    #Build a matrix of our table for later use.
    table = []
    table_trs = []
    for i in range(0,t_height):
        table.append(['' for j in range(0,t_width)])
        table_trs.append('<tr class="match-row">|</tr>')
    table_trs[0] = '<tr class="header-row">|</tr>'

    #Let's start generating code; we are just going to toss TD's into the matrix, and worry about rows later I guess

    #First row is headers only
    middle = t_width/2
    table[0][middle] = '<td class="middle"></td>'
    # table[0][middle+1] = '<td class="round%s>Round %s</td>' % (num_rounds, num_rounds)
    # table[0][middle-1] = '<td class="round%s>Round %s</td>' % (num_rounds, num_rounds)
    ctr=0
    #
    for i in range(middle-1,-1, -2):
        table[0][i] = '<td class="round%s">Round %s</td>' % (num_rounds, num_rounds-ctr)
        table[0][t_width-1-i] = '<td class="round%s">Round %s</td>' % (num_rounds, num_rounds-ctr)
        ctr = ctr + 1
    for i in range(middle-2, -1, -2):
        table[0][i] = '<td></td>'
        table[0][t_width-1-i] = '<td></td>'
    numgames = 1
    #Build the tourney grid
    cur_rd = num_rounds
    match_id = 1
    for i in range(middle-1,-1, -2):
        col_h = pow(2, cur_rd-1)
        # print 'col_h: ', col_h
        num_elements = pow(2, num_rounds-1) / col_h
        # print 'num_elements: ',num_elements
        for j in range(1, len(table), col_h):
            # table[j][column] will place us in the expected cell
            # Build the cell here, with all the knockout junk thrown in
            left_cell = ''
            right_cell = ''
            #Add a span for team 1
            left_cell += '<span id="left-r%s-match%s-team1" data-bind="ms.%s.team1"></span>' % (cur_rd, match_id, match_id)
            left_cell += '<span id="left-r%s-match%s-team2" data-bind="ms.%s.team2"></span>' % (cur_rd, match_id, match_id)
            match_id +=1
            right_cell += '<span id="right-r%s-match%s-team1" data-bind="ms.%s.team1"></span>' % (cur_rd, match_id, match_id)
            right_cell += '<span id="right-r%s-match%s-team2" data-bind="ms.%s.team2"></span>' % (cur_rd, match_id, match_id)
            if cur_rd == num_rounds:
                #Need to build special cells for this one
                table[j][i] = '<td rowspan=%s>%s</td>' % (col_h, left_cell)
                table[j][t_width-1-i] = '<td rowspan=%s>%s</td>' % (col_h, right_cell)
            else col_h == 1:
                table[j][i] = '<td>MATCH</td>'
                table[j][t_width-1-i] = '<td>MATCH</td>'
            else:
                table[j][i] = '<td rowspan=%s>MATCH</td>' % col_h
                table[j][t_width-1-i] = '<td rowspan=%s>MATCH</td>' % col_h
        cur_rd = cur_rd-1
    cur_rd = num_rounds
    #Build the spaces/lines that connect each round/bracket
    for i in range(middle-2, -1, -2):
        col_h = pow(2, cur_rd-1)
        num_elements = pow(2, num_rounds-1) / col_h
        for j in range(1, len(table), col_h):
            if col_h == 1:
                table[j][i] = '<td></td>'
                table[j][t_width-1-i] = '<td></td>'
            else:
                table[j][i] = '<td rowspan=%s></td>' % col_h
                table[j][t_width-1-i] = '<td rowspan=%s></td>' % col_h
        cur_rd = cur_rd-1
    #Middle row
    col_h = pow(2, num_rounds-1)
    for j in range(1, len(table), col_h):
        table[j][middle] = '<td rowspan=%s></td>' % col_h


    print_table = ''
    for i in range(0,t_height):
        print_table = print_table + table_trs[i].split('|')[0] + ' '.join(table[i]) + table_trs[i].split('|')[1]




    return print_table#, table_trs

def test():
    from pprint import pprint
    pprint (generate_brackets(['aaa','bbb','ccc','ddd','eee','fff','ggg','hhh']))




if __name__ == "__main__":
    test()