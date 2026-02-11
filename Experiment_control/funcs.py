#functions for the 2kHz program
import math
import random
import csv


def strgen (BF, BDC, PBD, TF, TDC, PuF, amp, TF_LuT):
    #print('BF:')
    #print(BF)
    #print('BDC:')
    #print(BDC)
    if (TF_LuT == 'on'):
        TF_dir = TF_LuT(BF, BDC)
        TF_list= TF_dir["TF"]
        TF= closest(TF_list, TF)
    #print('TF:')
    #print(TF)
    MaxNP = round (TF/BF)
    NP = round(TF/BF*BDC/100)
    #print('NP:')
    #print(NP)
    MaxNs = round (PuF/TF)
    NS = math.ceil(MaxNs*TDC/100)
    #print('NS:')
    #print(NS)
    IPD = MaxNs-NS
    #print('IPD:')
    #print(IPD)
    NB = math.ceil(BF/2)
    #print('NB:')
    #print(NB)
    MaxNx = round(PuF/BF)
    IBD= MaxNx - NP*MaxNs
    #print('IBD:')
    #print(IBD)
    SPW = math.ceil(100000/(4*PuF))
    PePD = math.ceil(100000/(2*PuF))-SPW
    return ['stack', 1, 'CH', 1,  'SPW', SPW, 'PePD' , PePD, 'NS', NS,  'IPD', IPD, 'NP', NP, 'NB', NB, 'IBD', IBD, 'PBD', PBD, 'word_amp', amp]

def stacked_strgen (stack, BF, BDC, PBD, TF, TDC, PuF, amp, length, TF_LuT):
    #print('BF:')
    #print(BF)
    #print('BDC:')
    #print(BDC)
    if (TF_LuT == 'on'):
        TF_dir = TF_LuT(BF, BDC)
        TF_list= TF_dir["TF"]
        TF= closest(TF_list, TF)
    #print('TF:')
    #print(TF)
    #MaxNP = round (TF/BF*length/500)
    NP = math.ceil(TF/BF*length/1000*BDC/100)
    #print('NP:')
    #print(NP)
    MaxNs = round (PuF/TF)
    NS = math.ceil(MaxNs*TDC/100)
    #print('NS:')
    #print(NS)
    IPD = MaxNs-NS
    #print('IPD:')
    #print(IPD)
    #NB = math.ceil(BF/2)
    NB = 1
    #print('NB:')
    #print(NB)
    MaxNx = round(PuF/BF*length/1000)
    IBD= MaxNx - NP*MaxNs
    #print('IBD:')
    #print(IBD)
    SPW = math.ceil(100000/(4*PuF))
    PePD = math.ceil(100000/(2*PuF))-SPW
    return ['stack', stack, 'CH', 1,  'SPW', SPW, 'PePD' , PePD, 'NS', NS,  'IPD', IPD, 'NP', NP, 'NB', NB, 'IBD', IBD, 'PBD', PBD, 'word_amp', amp]

def runfile (title, PBD, PuF, amp, rand):
    output = [
    ['reset', 'prefix_off'],
    ]
    with open(title) as csv_file:
        my_list = csv.reader(csv_file, delimiter=',')
        for row in my_list:
            #print(row)
            if row[0] != 'number':
                if (row[2]=='1'):
                    #print(row[2])
                    #print('not stacked')
                    output += not_stacked_str(row, PBD, PuF, amp)
                else:
                    print(row[2])
                    print('stacked')
                    for stack_nu in range(1,int(row[2])+1):
                        temp_num = [stack_nu]
                        template = row[0:3]+temp_num+row[5*stack_nu-2:5*stack_nu+3]
                        print(template)
                        output += stacked_str(template, PBD, PuF, amp, stack_nu, int(row[2]))
                if row[1] == 'comp':
                    output += ['stream', 'prompt']
                else:
                    output += ['stream']
    print(output)
    return output
                 
def not_stacked_str(row, PBD, PuF, amp):
    output = [ strgen (int(row[3]), int(row[5]), PBD, int(row[4]), int(row[6]), PuF, amp, 'off')]
    return output

def stacked_str(row, PBD, PuF, amp, stack_nu, max_stack):
    #stacked_strgen (stack, BF, BDC, PBD, TF, TDC, PuF, amp, length, TF_LuT):
    if stack_nu == max_stack:
        output = [ stacked_strgen (stack_nu, int(row[4]), int(row[6]), PBD, int(row[5]), int(row[7]), PuF, amp, int(row[8]), 'off')]
    else:
        output = [ stacked_strgen (stack_nu, int(row[4]), int(row[6]), 0, int(row[5]), int(row[7]), PuF, amp, int(row[8]), 'off')]
    return output


def BF_ranges ( BF_seed, BF_list):
    BF= BF_list[BF_seed]
    min_range = closest(BF_list, BF*1.5)
    if min_range == 1:
        min_range = 3
    max_range = closest(BF_list, BF*3)
    if max_range == 3:
        max_range = 4
    min_sweep_index = BF_list.index(min_range)
    max_sweep_index = BF_list.index(max_range)
    result= {
        "base_BF": BF,
        "min_range": min_range,
        "max_range": max_range,
        "BF_seed": BF_seed,
        "min_sweep_index": min_sweep_index,
        "max_sweep_index": max_sweep_index
        }
    return result
	
def BF_ranges_full ( BF_seed, BF_list):
    BF= BF_list[BF_seed]
    if BF==20:
        min_range= 20
    else:
        min_range = BF_list[BF_seed+1]	
    max_range = 20
    min_sweep_index = BF_list.index(min_range)
    max_sweep_index = BF_list.index(max_range)
    result={
        "base_BF": BF,
        "min_range": min_range,
        "max_range": max_range,
        "BF_seed": BF_seed,
        "min_sweep_index": min_sweep_index,
        "max_sweep_index": max_sweep_index
        }
    return result	
    
def comp_generator (base, min_sweep_index, max_sweep_index, rand_list):
    base_counter=0;
    stim_list = []
    for x in range(24):
        temp = global_seq_gen (rand_list, base, x-1)
        if temp == base :
            if (base_counter <= math.ceil(0.4*(max_sweep_index-min_sweep_index))):
                stim_list += [temp]
                base_counter += 1
        elif temp >= min_sweep_index and temp <= max_sweep_index :
            stim_list += [temp]
    return stim_list
    
def static_TF_list ():
    rows, cols = (21, 15) 
    TF_list = [[0]*cols]*rows

    TF_list[0]= [0]
    TF_list[2]= [0]
    TF_list[1]= [4,	6,	8,	12,	16,	24,	32,	40,	48,	64,	88,	112, 152, 200] #removed 2 from this list
    TF_list[3]= [6,	12,	18,	30, 36,	48,	66,	84,	114, 150, 198]
    TF_list[4]= [8,	16,	24,	32,	40,	48,	64,	88,	112, 152, 200]
    TF_list[6]= [12, 24, 36, 48, 60, 84, 108, 156, 198]
    TF_list[8]= [16, 32, 48, 64, 80, 112, 144, 200]
    TF_list[10]= [20, 40, 60, 80, 120, 160, 200]
    TF_list[12]= [24, 48, 72, 96, 120, 144, 192]
    TF_list[14]= [28, 56, 84, 112, 140, 196]
    TF_list[16]= [32, 64, 96, 128, 160, 192]
    TF_list[18]= [36, 72, 108, 144, 198]
    TF_list[20]= [40, 80, 120, 160, 200]
    
    for x in range(4,20):
        if (x% 2) == 1:
            TF_list[x]= [0]
            
    return TF_list

def global_seq_gen (rand_list, base, seq_number):
    rows, cols = (20, 24) 
    seqs = [[0]*cols]*rows
    
    seqs[0] = [ 16, 8, 10, 17, 11, 1, base, 18, 3, 14, 2, base, 13, 19, 5, 9, base, 7, base, 12, 6, 15, 4, 20]
    seqs[1] = [ 3, 4, 8, 17, 7, 11, base, 6, 13, base, 9, base, 16, 14, 5, 1, 19, 20, 18, 10, base, 12, 2, 15]
    seqs[2] = [ 14, 1, 20, 9, base, 11, base, 6, 7, base, 17, 10, 18, 3, 13, 12, 2, 8, 5, 4, base, 15, 19, 16]
    seqs[3] = [ base, 12, 11, base, 6, 7, 8, 15, 2, 10, 20, 1, 4, 9, 13, 14, 3, base, 17, 16, base, 5, 18, 19]
    seqs[4] = [ 4, 19, 12, 1, 3, 15, 20, base, base, 16, 18, base, 5, 6, 13, 8, base, 14, 7, 2, 10, 17, 11, 9]
    seqs[5] = [ base, 16, 14, 5, 8, 1, 9, 15, 10, 7, 18, 11, 4, base, 2, 12, 17, 6, base, 3, 13, base, 20, 19]
    seqs[6] = [ 4, 9, 11, 6, 18, 7, 20, base, base, 10, 15, 12, 1, 3, 17, 16, base, 8, 5, base, 2, 13, 19, 14]
    seqs[7] = [ 15, 7, 9, 3, 11, 13, 19, 14, 4, base, 12, 10, 2, 1, base, 20, 16, 5, base, 17, 8, 6, base, 18]
    seqs[8] = [ 4, 9, 13, 1, 12, 16, base, 17, base, 3, 18, 20, 19, 8, 6, 14, 2, 5, 15, base, 7, 10, base, 11]
    seqs[9] = [ 19, 5, base, 13, 18, 16, 9, 8, base, 20, 4, 6, base, 12, base, 17, 11, 14, 1, 3, 2, 7, 10, 15]
    seqs[10]= [ 8, base, 20, 17, 12, 7, 3, base, 18, 4, 15, base, 14, 16, 5, 9, 11, 19, 13, 1, base, 2, 6, 10]
    seqs[11]= [ 4, 3, 14, 13, 18, base, 20, base, 1, 10, 8, 11, 16, 9, base, 19, 5, 15, 12, 6, base, 7, 2, 17]
    seqs[12]= [ 9, 2, 10, 16, 6, 4, 19, 8, 13, base, 17, base, 3, 12, 18, 5, 14, base, 15, 20, 1, 11, base, 7]
    seqs[13]= [ 1, 8, base, 13, 7, 16, base, 2, 17, 9, 3, 12, 10, 18, 20, 19, 4, 14, 15, base, base, 11, 5, 6]    
    seqs[14]= [ 16, 14, 8, 13, 3, 19, 10, 12, 11, base, base, 15, base, 2, 9, base, 1, 5, 20, 6, 18, 4, 17, 7]
    seqs[15]= [ 11, 2, 5, 12, 9, 13, base, 4, base, 10, 14, 6, 1, 3, 15, 19, 18, 20, base, 7, 16, base, 17, 8]
    seqs[16]= [ base, 18, base, 16, 2, 13, base, 12, 14, 9, 4, 5, 7, 6, 17, 20, 8, 10, 19, 15, 1, 11, base, 3]
    seqs[17]= [ 16, 5, 4, 17, 11, 6, 7, 3, 15, 1, 18, base, base, 9, base, 12, 10, 20, 13, 19, base, 2, 14, 8]
    seqs[18]= [ 13, 12, 5, base, base, base, 4, 17, 10, 3, 20, 19, 14, 16, 6, base, 18, 7, 8, 2, 9, 15, 11, 1]
    seqs[19]= [ 1, 13, base, 8, 6, base, 10, 19, 16, 7, 3, 17, 18, 11, 5, base, base, 14, 2, 20, 15, 4, 12, 9]
    
    
    return seqs[rand_list][seq_number]

def BF_LuT (BF_seed):
    BF = [1, 3, 4, 6, 8, 10, 12, 14, 16, 18, 20]    
    return BF[BF_seed]

def TF_LuT (BF, BDC):
    temp_TF= [0]*20
    for seq in range (20):
        var= round(round(1.4998*math.exp(0.2878*(seq+1)))/round(BF*100/BDC))*round(BF*100/BDC)
        if var>0:
            if var<200:
                temp_TF[seq] = var
            else:
                temp_TF[seq] = 200
    TF= list(dict.fromkeys(temp_TF))
    TF = [i for i in TF if i != 0]
    result = {
        "TF": TF,
        "size": len(TF)
        }
         
    return result

def closest(lst, K): 
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
def remove_zeros (lst):
    return [i for i in lst if i != 0]

def order_element_BDC ( BF, BDC, PBD, TF, TDC, PuF, amp, base, mod):
   TF_LuT= 'off'
   element = [
        strgen (BF, base, 2000, TF, TDC, PuF, amp, TF_LuT),
        'stream',
        strgen (BF, mod, 1000, TF, TDC, PuF, amp, TF_LuT),
        'stream',
        'prompt'
        ]
   return element

def order_element_TDC ( BF, BDC, PBD, TF, TDC, PuF, amp, base, mod):
    TF_LuT= 'off'
    element = [
        strgen (BF, BDC, 2000, TF, base, PuF, amp, TF_LuT),
        'stream',
        strgen (BF, BDC, 1000, TF, mod, PuF, amp, TF_LuT),
        'stream',
        'prompt'
        ]
    return element
    
def order_element_BF ( BF, BDC, PBD, TF, TDC, PuF, amp, base, comp, random_flag):
    TF_LuT= 'on'
    if random_flag == 'random':
        if random.randrange(0, 2) == 0:
            element = [
                strgen (base, BDC, 2000, TF, TDC, PuF, amp, TF_LuT),
                'stream',
                strgen (comp, BDC, 1000, TF, TDC, PuF, amp, TF_LuT),
                'stream',
                'prompt'
                ]
        else:
            element = [
                strgen (comp, BDC, 2000, TF, TDC, PuF, amp, TF_LuT),
                'stream',
                strgen (base, BDC, 1000, TF, TDC, PuF, amp, TF_LuT),
                'stream',
                'prompt'
                ]
    else:
        element = [
                strgen (base, BDC, 2000, TF, TDC, PuF, amp, TF_LuT),
                'stream',
                strgen (comp, BDC, 1000, TF, TDC, PuF, amp, TF_LuT),
                'stream',
                'prompt'
                ]
        
    return element

def order_element_TF ( BF, BDC, PBD, TF, TDC, PuF, amp, base, comp, random_flag):
    TF_LuT= 'off'
    if random_flag == 'random':
        if random.randrange(0, 2) == 0:
            element = [
                strgen (BF, BDC, 2000, base, TDC, PuF, amp, TF_LuT),
                'stream',
                strgen (BF, BDC, 1000, comp, TDC, PuF, amp, TF_LuT),
                'stream',
                'prompt'
                ]
        else:
            element = [
                strgen (BF, BDC, 2000, comp, TDC, PuF, amp, TF_LuT),
                'stream',
                strgen (BF, BDC, 1000, base, TDC, PuF, amp, TF_LuT),
                'stream',
                'prompt'
                ]
    else:
        element = [
                strgen (BF, BDC, 2000, base, TDC, PuF, amp, TF_LuT),
                'stream',
                strgen (BF, BDC, 1000, comp, TDC, PuF, amp, TF_LuT),
                'stream',
                'prompt'
                ]
        
    return element 

def order_element_generic ( base_BF, base_BDC, base_PBD, base_TF, base_TDC, base_PuF, base_amp, comp_BF, comp_BDC, comp_PBD, comp_TF, comp_TDC, comp_PuF, comp_amp , random_flag):
    TF_LuT= 'off'
    if random_flag == 'random':
        if random.randrange(0, 2) == 0:
            element = [
                strgen (base_BF, base_BDC, 2000, base_TF, base_TDC, base_PuF, base_amp, TF_LuT),
                'stream',
                strgen (comp_BF, comp_BDC, 1000, comp_TF, comp_TDC, comp_PuF, comp_amp, TF_LuT),
                'stream',
                'prompt'
                ]
        else:
            element = [
                strgen (comp_BF, comp_BDC, 2000, comp_TF, comp_TDC, comp_PuF, comp_amp, TF_LuT),
                'stream',
                strgen (base_BF, base_BDC, 1000, base_TF, base_TDC, base_PuF, base_amp, TF_LuT),
                'stream',
                'prompt'
                ]
    else:
        element = [
                strgen (base_BF, base_BDC, 2000, base_TF, base_TDC, base_PuF, base_amp, TF_LuT),
                'stream',
                strgen (comp_BF, comp_BDC, 1000, comp_TF, comp_TDC, comp_PuF, comp_amp, TF_LuT),
                'stream',
                'prompt'
                ]
        
    return element 


    
    
def seq_gen_TDC (rand_list, base, seq_number):
    rows, cols = (12, 14) 
    seqs = [[0]*cols]*rows
    base = base*10
    seqs[0] = [ 9, 1, 2, 8, base, 10, 4, base, 3, 7, base, base, 6, 5]
    seqs[1] = [ 9, 7, 4, 1, base, 10, 8, 6, base, 5, base, 2, base, 3]
    seqs[2] = [ 3, base, 2, 5, 1, 10, 7, 8, base, 4, base, 9, 6, base]
    seqs[3] = [ 9, base, 4, base, 8, 2, 1, base, 7, 6, 10, base, 5, 3]
    seqs[4] = [ 4, 5, base, 3, 10, base, 6, base, 9, 2, base, 8, 7, 1]
    seqs[5] = [ 6, 5, 3, base, 9, 2, 10, 1, base, 8, 7, base, 4, base]
    seqs[6] = [ 5, 8, 7, base, 3, base, 6, base, 10, 2, 4, 1, 9, base]
    seqs[7] = [ 4, 8, base, 3, base, 7, 5, 1, 10, 2, base, 6, 9, base]
    seqs[8] = [ 8, base, 1, base, 7, 2, 3, 6, 10, base, 9, base, 5, 4]
    seqs[9] = [ 8, 6, 10, 5, 1, base, 3, base, 9, 7, base, 4, 2, base]
    seqs[10]= [ 1, base, 7, 4, 6, base, 9, 3, base, 10, base, 8, 2, 5]
    seqs[11]= [ 10, 8, 5, 7, 1, 6, base, 4, base, 9, base, 2, 3, base]
    
    return seqs[rand_list][seq_number]/10
    
def seq_gen_20 (rand_list, base, seq_number):
    rows, cols = (12, 14) 
    seqs = [[0]*cols]*rows
    
    seqs[0] = [ 16, 8, 10, 1, base, 18, 3, 14, 2, base, 5, base, 9, base, 7, base, 12, 6, 4, 20]
    seqs[1] = [ 3, 4, 8, 7, base, 6, base, 9, base, 16, 14, 5, 1, 20, 18, 10, base, base, 12, 2]
    seqs[2] = [ 14, 1, 20, 9, base, base, base, 6, 7, base, 10, 18, 3, 12, 2, 8, 5, 4, base, 16]
    seqs[3] = [ base, 12, base, base, 6, 7, 8, 2, 10, 20, 1, 4, 9, 14, 3, base, 16, base, 5, 18]
    seqs[4] = [ 4, 12, 1, 3, 20, base, base, 16, 18, base, 5, 6, 8, base, base, 14, 7, 2, 10, 9]
    seqs[5] = [ base, 16, 14, 5, 8, 1, 9, 10, 7, 18, 4, base, base, 2, 12, 6, base, 3, base, 20]
    seqs[6] = [ 4, 9, 6, 18, 7, 20, base, base, 10, 12, 1, 3, 16, base, base, 8, 5, base, 2, 14]
    seqs[7] = [ 7, 9, 3, 14, 4, base, 12, 10, 2, 1, base, 20, 16, 5, base, base, 8, 6, base, 18]
    seqs[8] = [ 4, 9, 1, 12, 16, base, base, 3, 18, 20, 8, 6, 14, 2, 5, base, base, 7, 10, base]
    seqs[9] = [ 5, base, 18, 16, 9, 8, base, 20, 4, 6, base, base, 12, base, 14, 1, 3, 2, 7, 10]
    seqs[10]= [ 8, base, 20, 12, 7, 3, base, 18, 4, base, 14, 16, 5, 9, 1, base, base, 2, 6, 10]
    seqs[11]= [ 4, 3, 14, 18, base, 20, base, 1, base, 10, 8, 16, 9, base, 5, 12, 6, base, 7, 2]
    
    return seqs[rand_list][seq_number]