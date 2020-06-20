import json
import time
import sys
import os
import random
import math
import shutil



# File Names and locatons
path= os.getcwd()+ '/'

data_file_path= f'{path}data/'
readable_file_path= f'{path}Account Files/'

name_list = f'{data_file_path}name_list.txt'
username= f'{data_file_path}username.json'
accounts= readable_file_path
raw_balance_files= f'{data_file_path}'
tax= f'{data_file_path}tax.json'
taxed_accounts= f'{data_file_path}poor.txt'
tax_collectors= f'{data_file_path}rich.txt'
rb_file_suffix= '\'s r_b.txt'
# Global Variables
''' This Chunk Creates The Bank From Scratch. It gets skipped if the text files are already there'''

def run():
    greet()

def test():
    print('Test :D')
    # Function to test

'''Start Up Functions'''

def greet():
    first_time= False
    try:
        with open(username) as user:
            finance_officer= json.load(user)
    except FileNotFoundError:
        first_time= True
        if not os.path.isdir(data_file_path):
            os.mkdir(data_file_path)
        if not os.path.isdir(readable_file_path):
            os.mkdir(readable_file_path)
        drama('This seems to be your first time running this.')
        finance_officer= input('\nWhat would you like me to call you: ')
        with open(username, 'w') as user:
            json.dump(finance_officer, user)
            print(f'Nice to meet you {finance_officer.title()}. :D')
    else:
        print(f'Welcome back {finance_officer.title()}')
    try:
        listed_names()
    except FileNotFoundError:
        print('There seems to be no records saved.')
        print('Making new ones.')
        create_pc_names()
    if first_time:
        tax_options_menu(True)
        return main_menu()
    else:
        return main_menu()

def create_pc_names():
    print('Name each player or group fund you want to track. Including a name for your group fund.')
    with open(name_list, 'w'):
        print('New name file created. This is where all names will be stored')
    log_names()
    print('\nEnteties we are fiscally tracking:')
    display_names()
    print('\nIs this ok or would you like to:')
    reset_check = True
    while reset_check:
        print('\t(1) Continue')
        print('\t(2) Start Over')
        print('\t(3) Add Another Name')
        do_what = input()
        choice= menu_navigate(do_what, 3)
        if choice== 0:
            continue
        elif choice== 1:
            lname= listed_names()
            create_blank_accounts()
            update_accounts(lname)
            for x in lname:
                print(f'{x.title()}\'s Balance Updated')
            return
        elif choice == 2:
            return create_pc_names()
        elif choice == 3:
            log_names()
            print('Enteties we are fiscally tracking:')
            display_names()

def log_names():
    logging = True
    with open(name_list, 'a') as nlist:
        while logging:
            name_player = input('Type a name and hit enter. Or (d) for done: ')
            name_player = name_player.lower()
            if name_player == 'd':
                logging = False
            else:
                nlist.write(name_player + '\n')
    nlist.close()

def create_blank_accounts(who= None):
    if who== None:
        lname= listed_names()
        for x in lname:
            if x == '':
                break
            else:
                x= x.title()
                pc_name= x
                x+= '\'s r_b.txt'
                with open(f'{raw_balance_files}{x}', 'w') as balance:
                    balance.write(pc_name+ '\n')
                    for _ in range(0, 5): # pp, gp, sp, cp, ep
                        balance.write('0\n')
    else:
        name= who.title()
        pc_name= name
        name+= '\'s r_b.txt'
        with open(f'{raw_balance_files}{name}', 'w') as balance:
            balance.write(pc_name+ '\n')
            for _ in range(0, 5): # pp, gp, sp, cp, ep
                balance.write('0\n')
        print(f'Created blank balance files for {pc_name}')
        return
    print('Created blank balance files for:')
    display_names()


''' Utility Functions'''
# Lists Every Name
# A little outdated, made at the start.. Lists all names.
# Only used in startup functions
def display_names():
    lname= listed_names()
    for x in lname:
        x = x.rstrip()
        print(f'\t-{x.title()}')

# Just a easy way to have a universal pause.
def dramatic_pause():
    time.sleep(2)

# Give it a message and it adds teenage pausing to it!!!
def drama(message):
    print(message, end='', flush=True)
    time.sleep(.4)
    for _ in range(1, 5):
        print('.', end='', flush=True)
        time.sleep(.4)

# Returns a clean list of every name in the name_list.txt file
def listed_names():
    lname= []
    with open(name_list) as nlist:
        list_bank = nlist.readlines()
        for x in list_bank:
            x = x.rstrip()
            lname.append(x)
    return lname

# Makes sure user input correct format.
# If correct, returns False
# If theres an error, prints format tips and returns True.
def coin_format_check(incoming_user_input_already_listed):
    coin_types= ['pp', 'gp', 'ep', 'sp', 'cp']
    # coin_names= ['blank', 'platinum', 'gold', 'electrum', 'silver', 'copper']
    profit= incoming_user_input_already_listed
    try: # Check if first value is a number. Pass= Good
        profit[0]= int(profit[0])
    except ValueError:
        print(f'If you followed the correct format. {profit[0]} should have a number in front of it.')
        coin_format_tips()
        return True
    # Check if last value is a str. Fail= Good
    try:
        last_value= len(profit)-1
        profit[last_value]= int(profit[last_value])
        print('You forgot to type a coin type on your last value.')
        return True
    except ValueError:
        pass
    # Check if they typed the coin type correct.
    for p in profit:
        try:
            p= int(p)
            if p < 0:
                print(f'Looks like you typed a negative, this only uses positives.')
                coin_format_tips()
                return True
            continue
        except ValueError:
            if p in coin_types:
                continue
            else:
                print(f'{p} is not in the accepted coin type format.')
                coin_format_tips()
                return True
    return False
    
# Just prints out format tips    
def coin_format_tips():
    coin_types= ['pp', 'gp', 'sp', 'cp', 'ep']
    coin_names= ['blank', 'platinum', 'gold', 'silver', 'copper', 'electrum']
    print(f'Stick to the following format, sans quotation marks:')
    for x in range(0, 5):
        z= random.randint(1, 100)
        print(f'\t-"{z} {coin_types[x]}" for {z} {coin_names[x+1]}')
    print('You can string them together like:')
    print('5 gp 2 ep 35 pp')

# Turns a file into a clean list.
# R_B files format into a standard wallet with this
def listify(file_to_list):
    just_a_list= []
    with open(file_to_list) as f:
        list_bank = f.readlines()
        for x in list_bank:
            x = x.rstrip()
            just_a_list.append(x)
    f.close()
    return just_a_list

# Gets raw value for the r_b txt file and turns it into a readable text file ___'s balance.txt
def update_accounts(who= 'all'):
    lname= listed_names()
    if who== 'all': # This might be insane, it just seemed the easiest way to do it... Had to work with lname no longer being global
        return update_accounts(lname)
    if(type(who)== list):
        for name in who:
            name= name.title()
            pc_account= name
            pc_account+= '\'s balance.txt'
            name+= '\'s r_b.txt'
            coins= []
            with open(f'{raw_balance_files}{name}') as balance:
                cbalance= balance.readlines()
                for x in cbalance:
                    x= x.rstrip()
                    coins.append(x)
            balance.close()
            coins= coins[:6]
            with open(f'{accounts}{pc_account}', 'w') as balance_update:
                balance_update.write(f'{coins[0]}\'s monetary value:\n')
                balance_update.write(f'\t- {coins[1]} in platinum\n')
                balance_update.write(f'\t- {coins[2]} in gold\n')
                balance_update.write(f'\t- {coins[5]} in electrum\n')
                balance_update.write(f'\t- {coins[3]} in silver\n')
                balance_update.write(f'\t- {coins[4]} in copper')
            balance_update.close()
    else:
        name= who.title()
        pc_account= name
        pc_account+= '\'s balance.txt'
        name+= '\'s r_b.txt'
        coins= []
        with open(f'{raw_balance_files}{name}') as balance:
            cbalance= balance.readlines()
            for x in cbalance:
                x= x.rstrip()
                coins.append(x)
        balance.close()
        coins= coins[:6]
        with open(f'{accounts}{pc_account}', 'w') as balance_update:
            balance_update.write(f'{coins[0]}\'s monetary value:\n')
            balance_update.write(f'\t- {coins[1]} in platinum\n')
            balance_update.write(f'\t- {coins[2]} in gold\n')
            balance_update.write(f'\t- {coins[5]} in electrum\n')
            balance_update.write(f'\t- {coins[3]} in silver\n')
            balance_update.write(f'\t- {coins[4]} in copper')
        balance_update.close()

# Displays the ___'s balance.txt into the terminal.
def display_account(who= None):
    print('\n')
    lname= listed_names()
    if who== None:
        for x in lname:
            update_accounts(x)
            pc= x.title()
            pc+= '\'s balance.txt'
            print('\n')
            with open(f'{accounts}{pc}') as account:
                print_account= account.read()
                print(print_account)
            account.close()
    else:
        update_accounts(who)
        pc= who.title()
        pc+= '\'s balance.txt'
        with open(f'{accounts}{pc}') as account:
            print_account= account.read()
            print(print_account)
        account.close()

# Format a user input into a standard wallet format.
# wallet= [name, pp, gp, sp, cp, ep]
# wish I thought of this sooner
def wallify_this_shiiii(wallet_to_standerdize):
    formated_wallet=['blank', 0, 0, 0, 0, 0]
    check_range= len(wallet_to_standerdize)
    for x in range((check_range- 1), 0, -1):
        money= x-1
        if wallet_to_standerdize[x]== 'cp':
            try:
                formated_wallet[4]= int(wallet_to_standerdize[money])
            except ValueError:
                print(f'You skipped a number. There should be a value in front of {wallet_to_standerdize[x]}')
                return 0
        elif wallet_to_standerdize[x]== 'sp':
            try:
                formated_wallet[3]= int(wallet_to_standerdize[money])
            except ValueError:
                print(f'You skipped a number. There should be a value in front of {wallet_to_standerdize[x]}')
        elif wallet_to_standerdize[x]== 'ep':
            try:
                formated_wallet[5]= int(wallet_to_standerdize[money])
            except ValueError:
                print(f'You skipped a number. There should be a value in front of {wallet_to_standerdize[x]}')        
        elif wallet_to_standerdize[x]== 'gp':
            try:
                formated_wallet[2]= int(wallet_to_standerdize[money])
            except ValueError:
                print(f'You skipped a number. There should be a value in front of {wallet_to_standerdize[x]}')
        elif wallet_to_standerdize[x]== 'pp':
            try:
                formated_wallet[1]= int(wallet_to_standerdize[money])
            except ValueError:
                print(f'You skipped a number. There should be a value in front of {wallet_to_standerdize[x]}')
    return formated_wallet

# Get a list and update a wallet to its value.
def refresh_wallet(who, incoming_wallet_list):
    with open(raw_balance_files+ who, 'w') as wallet:
        for x in incoming_wallet_list:
            wallet.write(f'{x}\n')
        wallet.close()


''' Math Functions'''
# Sorted the add and withdraws into two seperate functions
# I just wanted on function for asking who and how much
# And a second function actually doing the work
def ask_how_much_to_add(whom= None, in_coin= None):
    lname= listed_names()
    if whom== 'all':
        if in_coin== None:
            in_coin= input('How much to each account? ')
        listed_names()
        for x in lname:
            add_to_raw_balance(x, in_coin)
        return
    elif whom== 'poor':
        in_coin= input('How much to each account? ')
        poor= listify(taxed_accounts)
        for x in poor:
            add_to_raw_balance(x, in_coin)
        return
    elif whom== None:
        listed_names()
        numerical= len(lname)
        print('Who are we adding to?')
        for x in range(0, numerical):
            order_spot= x+ 1
            print(f'\t({order_spot}) {lname[x].title()}')
        back_to_menu=  numerical+ 1
        print(f'\t({back_to_menu}) Back to Main Menu')
        add_to_who= input()
        try:
            add_to_who= int(add_to_who)
        except ValueError:
            print('Use numbers to navigate the menu.')
            ask_how_much_to_add()
        if add_to_who > back_to_menu or add_to_who< 1:
            print('That is not an option.')
            ask_how_much_to_add()
        elif add_to_who== back_to_menu:
            main_menu()
        else:
            add_to_who-= 1
            whom= (lname[add_to_who])
    if in_coin== None:
        in_coin= input('How much money are you adding? ')
    add_to_raw_balance(whom, in_coin)

def add_to_raw_balance(who, incoming_money):
    whomst= who.title()
    whomst+= '\'s r_b.txt'
    account= raw_balance_files+ whomst
    coins= listify(account)
    if isinstance(incoming_money, list):
        ammount_to_add= incoming_money
    else:
        incoming_money= incoming_money.lower()
        profit= incoming_money.split()
        # list_check_range= len(profit)
        is_you_dumb= coin_format_check(profit)
        if is_you_dumb:
            return ask_how_much_to_add(who)
        else:
            ammount_to_add= wallify_this_shiiii(profit)
            if ammount_to_add== 0:
                return ask_how_much_to_add(who)
    for x in range(1, 6):
        coins[x]= int(coins[x])+ int(ammount_to_add[x])
    with open(f'{raw_balance_files}{whomst}', 'w') as balance:
        for x in coins:
            balance.write(f'{x}\n')
    balance.close()
    update_accounts(who)
    print(f'{who.title()}\'s Balance Updated')

def ask_how_much_to_pull(whom= None, out_coin= None):
    lname= listed_names()
    if whom== 'all':
        if out_coin== None:
            out_coin= input('How much from each account? ')
        for x in lname:
            withdraw_from_raw_balance(x, out_coin)
        return
    elif whom== 'poor':
        in_coin= input('How much to each account? ')
        poor= listify(taxed_accounts)
        for x in poor:
            withdraw_from_raw_balance(x, in_coin)
        return
    elif whom== None:
        listed_names()
        numerical= len(lname)
        print('Who are we withdrawing from?')
        for x in range(0, numerical):
            order_spot= x+ 1
            print(f'\t({order_spot}) {lname[x].title()}')
        all_=  numerical+ 1
        back_to_menu= all_+ 1
        print(f'\t({back_to_menu}) Back to Main Menu')
        pull_from= input()
        pull_from_who= menu_navigate(pull_from, back_to_menu)
        if pull_from_who== 0:
            ask_how_much_to_pull()
        elif pull_from_who== all_:
            ask_how_much_to_pull(lname)
        elif pull_from_who== back_to_menu:
            main_menu()
        else:
            pull_from_who-= 1
            whom= (lname[pull_from_who])
    if out_coin== None:
        out_coin= input('And how much? ')
    withdraw_from_raw_balance(whom, out_coin)

def withdraw_from_raw_balance(who, spending_money):
    whomst= who.title()
    whomst+= '\'s r_b.txt'    
    account= raw_balance_files+ whomst # Pull pc's worth from r_b file.
    wallet= listify(account)           # Turn it into a list
    coins= wallet[:]                   # Copy pc's worth so we can have an unaltered copy
    spending_money= spending_money.lower()
    cost= spending_money.split()       # Turn what you're spending into a list
    # coin_types= ['blank', 'pp', 'gp', 'sp', 'cp', 'ep']
    coin_names= ['blank', 'platinum', 'gold', 'silver', 'copper', 'electrum']
    you_dumb= coin_format_check(cost)
    if you_dumb:
        return ask_how_much_to_pull(who)
    else:
        loss= wallify_this_shiiii(cost) # Renamed the listed wallet(cost) to loss because I'm insecure
        if loss== 0:
            return ask_how_much_to_pull(who)
    cost_c= turn_it_all_into_copper(loss)
    coins_c= turn_it_all_into_copper(coins)
    if cost_c > coins_c:
        print(f'{who.title()}\'s account does not have enough to afford this.')
        print('Would you like to:')
        print('(1) Try a different ammount')
        print('(2) Return to Main Menu')
        ya_broke= input()
        ya_broke_a_f= menu_navigate(ya_broke, 2)
        if ya_broke_a_f== 0:
            return withdraw_from_raw_balance(who, spending_money)
        elif ya_broke_a_f== 1:
            ask_how_much_to_pull(who)
        else:
            main_menu()
    else:
        in_the_red= ['blank', 0, 0, 0, 0, 0]
        for x in range(1, 6):
            coins[x]= int(coins[x])- int(loss[x])
            if int(coins[x]) < 0:
                in_the_red[x]= abs(int(coins[x]))
                coins[x]= wallet[x]
    special_attention= []
    redspot= 0
    # I'm using this for loop to identify what coin types need special attention.
    for x in in_the_red:
        if x== 0 or x== 'blank':
            redspot+= 1
        else:
            special_attention.append(redspot)
            redspot+= 1
    for x in special_attention:
        short_bus= True
        while short_bus:
            print(f'You are trying to withdraw {loss[x]} {coin_names[x]}')
            print(f'{who.title()}\'s account only has {coins[x]} {coin_names[x]}')
            print('Would you like to:')
            print('\t(1) Get Change/ Convert')
            print(f'\t(2) Skip Withdrawing {coin_names[x].title()}')
            print('\t(3) Cancel Entire Operation')
            mmmm_what_u_do= menu_navigate(input(), 3)
            if mmmm_what_u_do== 0:
                continue
            elif mmmm_what_u_do== 1: # Before running coversion. Subtract what we can.
                loss[x]= int(loss[x])- int(coins[x])
                coins[x]= 0
                refresh_wallet(whomst, coins)
                coins= convert_time(who, x, loss[x])
                short_bus= False
            elif mmmm_what_u_do== 2:
                short_bus= False
            else: # Cancel operation, refresh wallet to original value.
                refresh_wallet(whomst, wallet)
                return main_menu()
    try:
        refresh_wallet(whomst, coins)
    except TypeError:
        print('Unexpected error')
        print('Setting account back to original value and returning to menu.')
        refresh_wallet(whomst, wallet)
        update_accounts(who)
        return main_menu()
    update_accounts(who)
    print(f'{who.title()}\'s Balance Updated')
    display_account(who)
    return

# Spit out new wallet worth.
def convert_time(who, coin_type, goal):
    account= listify(raw_balance_files+ who+ rb_file_suffix)
    account_copy= account[:]
    goal= int(goal)
    coin_type= int(coin_type)
    going_up= True
    going_down= False
    coins_used= ['blank', 0, 0, 0, 0, 0]
    coin_types= ['blank', 'pp', 'gp', 'sp', 'cp', 'ep']
    # Checks if there is still coins above this coin type to convert down from.
    if coin_type== 5:
        for x in range(2, -1, -1):
            if x== 0:
                going_up= False
                break
            elif int(account[x])> 0:
                going_up= True
                break
            else:
                continue
        if not going_up:
            going_down= True
    elif coin_type== 1:
        going_up= False
        going_down= True
    else:
        for x in range((coin_type- 1), -1, -1): 
            if int(account[5])> 0 and int(coin_type)== 4:
                going_up= True
                break
            elif int(account[5])> 0 and int(coin_type)== 3:
                going_up= True
                break                
            elif x== 0:
                going_up= False
                going_down= True
                break
            elif int(account[x])> 0:
                going_up= True
                break
            else:
                continue
    # If the going up came out True, this runs a loop giving change until goal is met.
    while going_up:
        if coin_type== 5:
            for x in range(2, -1, -1):
                if int(account[5]) >= goal: # Checks if simple subtraction will work.
                    going_up= False
                    account[5]= int(account[5])- goal
                    for x in range(1, 6):
                        if coins_used[x]== 'blank' or coins_used[x]== 0:
                            continue
                        else:
                            print(f'\t-{coins_used[x]} in {coin_types[x]}')
                    print('\n')
                    return account
                elif x== 0 and goal > 0: # Switches the direction we convert if pass plat.
                    going_down= True
                    going_up= False
                elif int(account[x])== 0: # Next coin if this type is dry.
                    continue       
                else: # Converts available coin, breaks out of loop to reset it.
                    if x== 2:
                        account[2]= int(account[2])- 1
                        coins_used[x]+= 1
                        account[5]= int(account[5])+ 2
                        break
                    elif x== 1:
                        account[1]= int(account[1])- 1
                        coins_used[x]+= 1
                        account[2]= int(account[2])+ 10
                        break
            continue
        else:
            for x in range((coin_type- 1), -1, -1):
                if int(account[coin_type]) >= goal: # Checks if simple subtraction will work.
                    going_up= False
                    account[coin_type]= int(account[coin_type])- goal
                    print('Coins Converted:')
                    for x in range(1, 6):
                        if coins_used[x]== 'blank' or coins_used[x]== 0:
                            continue
                        else:
                            print(f'\t-{coins_used[x]} in {coin_types[x]}')
                    print('\n')
                    return account
                elif x== 0 and goal > 0: # Switches the direction we convert if pass plat.
                    going_down= True
                    going_up= False
                elif x== 3 and int(account[3])== 0 and int(account[5])> 0:
                    account[5]= int(account[5])- 1
                    coins_used[5]+= 1
                    account[3]= int(account[3])+ 5
                    break
                elif int(account[x])== 0: # Next coin if this type is dry.
                    continue                    
                else: # Converts available coin, breaks out of loop to reset it.
                    account[x]= int(account[x])- 1
                    coins_used[x]+= 1
                    account[x+1]= int(account[x+1]) + 10
                    break
            continue
    while going_down:
        if coin_type== 5:
            for x in range(3, 6):
                if int(account[5]) >= goal: # Checks if simple subtraction will work.
                    going_down= False
                    account[5]= int(account[5])- goal
                    for x in range(1, 6):
                        if coins_used[x]== 'blank' or coins_used[x]== 0:
                            continue
                        else:
                            print(f'\t-{coins_used[x]} in {coin_types[x]}')
                    print('\n')
                    return account
                elif x== 5 and goal > 0: # If it hits this, not enough coin to convert
                    print('Couldn\'t afford the conversion')
                    print('Canceling this conversion and continuing')
                    return account_copy
                elif x== 3:
                    if int(account[3])>= 5:
                        account[3]= int(account[3])- 5
                        coins_used[x]+= 5
                        account[5]= int(account[5])+ 1
                        break
                    else:
                        continue
                elif x== 4:
                    if int(account[4])>= 50:
                        account[4]= int(account[4])- 50
                        coins_used[x]+= 50
                        account[3]= int(account[3])+ 5
                        break
                    else:
                        continue
            continue
        else:
            for x in range((coin_type+ 1), 6):
                if int(account[coin_type]) >= goal: # Checks if simple subtraction will work.
                    going_up= False
                    account[coin_type]= int(account[coin_type])- goal
                    print('Coins Converted:')
                    for x in range(1, 6):
                        if coins_used[x]== 'blank' or coins_used[x]== 0:
                            continue
                        else:
                            print(f'\t-{coins_used[x]} in {coin_types[x]}')
                    print('\n')
                    return account
                elif x== 5 and goal > 0: # Switches the direction we convert if pass plat.
                    print('Couldn\'t afford the conversion')
                    print('Canceling this conversion and continuing')
                    return account_copy
                elif x== 2 and int(account[2])== 0 and int(account[5])>= 2:
                    account[5]= int(account[5])- 2
                    coins_used[5]+= 2
                    account[2]= int(account[2])+ 1
                    break
                elif int(account[x])== 0: # Next coin if this type is dry.
                    continue                    
                else: # Converts available coin, breaks out of loop to reset it.
                    if int(account[x])>= 10:
                        account[x]= int(account[x])- 10
                        coins_used[x]+= 10
                        account[x-1]= int(account[x-1]) + 1
                        break
                    else:
                        continue
            continue

# This will take a listified wallet you give it and spit out the total in copper.
# Useful for seeing if you can afford something
def turn_it_all_into_copper(copper_medusa):
    for x in range(1, 6):
        copper_medusa[x]= int(copper_medusa[x])
    shit_i_looked= (copper_medusa[1]* 1000)+ (copper_medusa[2]* 100)+ (copper_medusa[5]* 50)+ (copper_medusa[3]* 10)+ copper_medusa[4]
    return shit_i_looked


''' Menu Functions'''


# Created this function to navigate menus.
# Really it's more to make sure user is putting in correct numbers
# Returns 0 if user does something wrong
# Else it should return the users menu selection
def menu_navigate(picked, max_pick):
    try:
        picked= int(picked)
    except ValueError:
        print('Use numbers to navigate the menu.')
        return 0
    if picked > max_pick or picked< 1:
        print('That is not an option on the menu.')
        return 0
    else:
        return picked

def main_menu():
    print('\nWhat would you like to do:')
    print('\t(1) Check Funds')
    print('\t(2) Add to Account')
    print('\t(3) Withdraw from Account')
    print('\t(4) Split Funds(taxed)')
    print('\t(5) Tax Options')
    print('\t(6) Advanced Options')
    print('\t(7) Save and Quit')
    menu_input= input()
    input_check= menu_navigate(menu_input, 7)
    if input_check== 0:
        return main_menu()
    elif input_check== 1:
        return check_funds_menu()
    elif input_check== 2:
        return add_to_account_menu()
    elif input_check== 3:
        return withdraw_from_account_menu()
    elif input_check== 4:
        return split_funds_menu()
    elif input_check== 5:
        return tax_options_menu()
    elif input_check== 6:
        return advanced_options()
    elif input_check== 7:
        sys.exit()

def check_funds_menu():
    lname= listed_names()
    print('\nWhat account are we checking?')
    numerical= len(lname)
    for x in range(0, numerical):
        order_spot= x+ 1
        print(f'\t({order_spot}) {lname[x].title()}')
    all_=  numerical+ 1
    back_to_menu= all_+ 1
    print(f'\t({all_}) All')
    print(f'\t({back_to_menu}) Back to Menu')
    fund_input= input()
    display_who= menu_navigate(fund_input, back_to_menu)
    if display_who== 0:
        check_funds_menu()
    elif display_who== all_:
        display_account()
        main_menu()
    elif display_who== back_to_menu:
        main_menu()
    else:
        display_who-= 1
        display_account(lname[display_who])
        main_menu()

def add_to_account_menu():
    print('\nWhat account are we adding to?')
    lname= listed_names()
    numerical= len(lname)
    for x in range(0, numerical):
        order_spot= x+ 1
        print(f'\t({order_spot}) {lname[x].title()}')
    all_= numerical+ 1
    the_poor= all_ + 1
    back_to_menu=  the_poor+ 1
    print(f'\t({all_}) All accounts (including group funds.)')
    print(f'\t({the_poor}) All players (NOT including group funds.)')
    print(f'\t({back_to_menu}) Back to Menu')
    add_to_account_input= input()
    add_to_who= menu_navigate(add_to_account_input, back_to_menu)
    if add_to_who== 0:
        return add_to_account_menu()
    elif add_to_who== back_to_menu:
        return main_menu()
    elif add_to_who== all_:
        ask_how_much_to_add('all')
        for x in lname:
            display_account(x)
        return main_menu()
    elif add_to_who== the_poor:
        ask_how_much_to_add('poor')
        poor_bitches= listify(taxed_accounts)
        for x in poor_bitches:
            display_account(x)
        return main_menu()
    else:
        add_to_who-= 1
        display_account(lname[add_to_who])
        ask_how_much_to_add(lname[add_to_who])
        display_account(lname[add_to_who])
        return main_menu()

def withdraw_from_account_menu():
    print('\nWhat account are we pulling from?')
    lname= listed_names()
    numerical= len(lname)
    for x in range(0, numerical):
        order_spot= x+ 1
        print(f'\t({order_spot}) {lname[x].title()}')
    all_= numerical+ 1
    the_poor= all_ + 1
    back_to_menu=  the_poor+ 1
    print(f'\t({all_}) All accounts (including group funds.)')
    print(f'\t({the_poor}) All players (NOT including group funds.)')
    print(f'\t({back_to_menu}) Back to Menu')
    pull_from_account_input= input()
    pull_from_who= menu_navigate(pull_from_account_input, back_to_menu)
    if pull_from_who== 0:
        withdraw_from_account_menu()
    elif pull_from_who== back_to_menu:
        return main_menu()
    elif pull_from_who== all_:
        ask_how_much_to_pull('all')
        for x in lname:
            display_account(x)
        return main_menu()
    elif pull_from_who== the_poor:
        ask_how_much_to_pull('poor')
        peasants= listify(taxed_accounts)
        for x in peasants:
            display_account(x)
        return main_menu()
    else:
        pull_from_who-= 1
        display_account(lname[pull_from_who])
        ask_how_much_to_pull(lname[pull_from_who])
        display_account(lname[pull_from_who])
        return main_menu()

def split_funds_menu():
    coin_type= ['blank', 'pp', 'gp', 'sp', 'cp', 'ep']
    the_poor_listed= listify(taxed_accounts)
    the_people= len(the_poor_listed)
    the_rich_listed= listify(tax_collectors)
    print('Taxed accounts:')
    for x in the_poor_listed:
        print(f'\t{x.title()}')
    print('\n')
    print('Group fund:')
    for x in the_rich_listed:
        print(f'\t{x.title()}')
    print('\n')    
    with open(tax) as tax_value:
        show_tax= json.load(tax_value)
    print(f'Current tax: {show_tax}%')
    group_cut= ['blank', 0, 0, 0, 0, 0]
    tax_cut= ['blank', 0, 0, 0, 0, 0]
    the_round_off_cut= ['blank', 0, 0, 0, 0, 0]
    the_pre_cut= ['blank', 0, 0, 0, 0, 0]
    _input_the_treasure= input('Treasure! How much? or (m) for main menu:\n')
    _input_the_treasure= _input_the_treasure.lower()
    if _input_the_treasure== 'm':
        return main_menu()
    else:
        the_treasure= _input_the_treasure.split()
        you_dumb= coin_format_check(the_treasure)
        if you_dumb:
            return split_funds_menu()
        else:
            the_pre_cut= wallify_this_shiiii(the_treasure)
            wallet_cut= the_pre_cut[:]
            for x in range(1, 6):
                tax_cut[x]= math.ceil(int(the_pre_cut[x])* .1)
                the_pre_cut[x]= int(the_pre_cut[x])- int(tax_cut[x])
                if int(the_pre_cut[x]) >= the_people:
                    the_round_off_cut[x]= int(the_pre_cut[x])% the_people
                else:
                    the_round_off_cut[x]= int(the_pre_cut[x])
                the_pre_cut[x]= int(the_pre_cut[x])- int(the_round_off_cut[x])
                group_cut[x]= int(the_pre_cut[x])// the_people
                tax_cut[x]= int(tax_cut[x])+ int(the_round_off_cut[x])
            print('\n')
            print('Incoming Treasure:')
            for x in range(1, 6):
                if int(wallet_cut[x])== 0:
                    continue
                else:
                    print(f'{wallet_cut[x]} {coin_type[x]}, ', end='', flush=True)
            print('\n')
            print('Cut per person:')
            for x in range(1, 6):
                if int(group_cut[x])== 0:
                    continue
                else:
                    print(f'{group_cut[x]} {coin_type[x]}, ', end='', flush=True)
            print('\n')
            print('Taxed amount for group fund:')
            for x in range(1, 6):
                if int(tax_cut[x])== 0:
                    continue
                else:
                    print(f'{tax_cut[x]} {coin_type[x]}, ', end='', flush=True)
            while True:
                print('\n')
                split_decision= input('Proceed with account changes? (y) or (n)\n')
                split_decision= split_decision.lower()
                if split_decision== 'n':
                    return main_menu()
                elif split_decision== 'y':
                    for x in the_poor_listed:
                        add_to_raw_balance(x, group_cut)
                    for x in the_rich_listed:
                        add_to_raw_balance(x, tax_cut)
                    return main_menu()
                else:
                    continue
    return main_menu()

def tax_options_menu(tax_reset_check= False):
    lname= listed_names()
    if tax_reset_check:
        try:
            with open(tax) as tax_:
                tax_percent= tax_
        except FileNotFoundError:
            while not os.path.exists(tax):
                tax_percent= input('What percent would you like the default tax to be: ')
                if len(tax_percent.split())> 1:
                    print('Do not include anything but the number for the percentage you\'d like to set the tax to. ')
                    continue
                try:
                    if int(tax_percent) < 0 or int(tax_percent) > 100:
                        print('Please set tax between 0 - 100')
                        continue
                except ValueError:
                    print('Please use a number between 0-100 for the tax value.')
                    continue
                with open(tax, 'w') as tax_in:
                    json.dump(tax_percent, tax_in)
        try:
            with open(taxed_accounts) as the_poor:
                the_poor.close()
            with open(tax_collectors) as the_rich:
                the_rich.close()
        except FileNotFoundError:
            print('Lets set an account as the group funds.')
            print('\n')
            lname= listed_names()
            with open(taxed_accounts, 'w') as the_poor:
                for x in lname:
                    the_poor.write(f'{x}\n')
                the_poor.close()
            with open(tax_collectors, 'w') as the_rich:
                the_rich.close()
            numerical= len(lname)
            done= numerical+ 1
            taxing= True
            while taxing:
                the_poor_listed= listify(taxed_accounts)
                the_rich_listed= listify(tax_collectors)
                print('Player accounts:')
                for x in the_poor_listed:
                    print(f'\t{x.title()}')
                print('\n')
                print('The Group Fund:')
                for x in the_rich_listed:
                    print(f'\t{x.title()}')
                print('\n')
                print('Which one of these accounts is the group fund?')
                for x in range(0, numerical):
                    order_spot= x+ 1
                    print(f'\t({order_spot}) {lname[x].title()}')
                print(f'\t({done}) When you\'re done')
                ask_move= input()
                move= menu_navigate(ask_move, done)
                if move== 0:
                    continue
                elif move== done:
                    if len(the_rich_listed)> 1:
                        print('\n')
                        print('Please only select one as the group fund')
                        print('\n')
                        continue
                    else:
                        with open(name_list, 'w') as gf_on_bottom:
                            for x in the_poor_listed:
                                gf_on_bottom.write(x+ '\n')
                            for x in the_rich_listed:
                                gf_on_bottom.write(x+ '\n')
                        gf_on_bottom.close()
                        taxing= False
                else:
                    move-= 1
                    if lname[move] in the_poor_listed:
                        the_poor_listed.remove(lname[move])
                        the_rich_listed.append(lname[move])
                    elif lname[move] in the_rich_listed:
                        the_rich_listed.remove(lname[move])
                        the_poor_listed.append(lname[move])
                with open(taxed_accounts, 'w') as the_poor:
                    for x in the_poor_listed:
                        the_poor.write(f'{x}\n')
                    the_poor.close()
                with open(tax_collectors, 'w') as the_rich:
                    for x in the_rich_listed:
                        the_rich.write(f'{x}\n')
                    the_rich.close()
            return main_menu()
        main_menu()
    else:
        print('Tax Options:')
        print('\t(1) Change Tax Percent.')
        print('\t(2) Change who gets taxed/ What account is the group fund.')
        print('\t(3) Main Menu')
        what_u_do= input()
        jakar_does= menu_navigate(what_u_do, 3)
        if jakar_does== 0:
            tax_options_menu()
        if jakar_does== 1:
            os.remove(tax)
            return tax_options_menu(True)
        elif jakar_does== 2:
            os.remove(tax_collectors)
            os.remove(taxed_accounts)
            return tax_options_menu(True)
        elif jakar_does== 3:
            return main_menu()

def advanced_options():
    print('\nWhat would you like to do:')
    print('\t(1) Change user name')
    print('\t(2) Wipe records and restart from scratch')
    print('\t(3) Remove Account and it\'s records')
    print('\t(4) Add new account')
    print('\t(5) Back to main menu')
    menu_selection= input()
    menu_selection= menu_navigate(menu_selection, 5)
    if menu_selection== 0:
        return advanced_options()
    elif menu_selection== 1:
        finance_officer= input('\nWhat would you like me to call you: ')
        with open(username, 'w') as user:
            json.dump(finance_officer, user)
            print(f'Nice to meet you {finance_officer.title()}. :D')
            return main_menu()
    elif menu_selection== 2:
        while True:
            print('This will completely erase all records. Are you sure?')
            print('\t(1) Yes, I want to erase everything')
            print('\t(2) No, take me back')
            torch= input()
            torch= menu_navigate(torch, 2)
            if torch== 0:
                continue
            elif torch== 1:
                shutil.rmtree(data_file_path)
                shutil.rmtree(readable_file_path)
                return greet()
            elif torch== 2:
                return advanced_options()
    elif menu_selection== 3:
        while True:
            print('Which account are we removing?')
            dead_men_walking= listed_names()
            name_list_length= len(dead_men_walking)
            for x in range(0, name_list_length):
                print(f'({x+1}) {dead_men_walking[x].title()}')
            print(f'({name_list_length+ 1}) Back to Main Menu')
            delete_account= menu_navigate(input(), (name_list_length+ 1))
            if delete_account== 0:
                continue
            elif delete_account== name_list_length+ 1:
                return main_menu()
            else:
                delete_account-= 1
                on_the_gallow= dead_men_walking[delete_account]
                print(f'Are you sure you want to delete {on_the_gallow.title()}\'s account?')
                print('(1) Yes, Delete it')
                print('(2) No, Take me back to Main Menu')
                the_lever= menu_navigate(input(), 2)
                if the_lever== 0:
                    continue
                elif the_lever== 1:
                    rich= listify(tax_collectors)
                    poor= listify(taxed_accounts)
                    if on_the_gallow in rich:
                        os.remove(tax_collectors)
                    if on_the_gallow in poor:
                        poor.remove(on_the_gallow)
                        with open(taxed_accounts, 'w') as new_poor:
                            for x in poor:
                                new_poor.write(f'{x}\n')
                            new_poor.close()
                    print(f'Removed {on_the_gallow.title()} from tax settings')
                    try:
                        os.remove(raw_balance_files+ f'{on_the_gallow}{rb_file_suffix}')
                        print(f'Removed {on_the_gallow.title()} from raw balance file')
                    except FileNotFoundError:
                        pass
                    try:
                        os.remove(accounts+ f'{on_the_gallow.title()}'+ '\'s balance.txt')
                        print(f'Removed {on_the_gallow.title()} from account file')
                    except FileNotFoundError:
                        pass
                    new_names= listed_names()
                    new_names.remove(on_the_gallow)
                    with open(name_list, 'w') as name_updated:
                        for x in new_names:
                            name_updated.write(x + '\n')
                    name_updated.close()
                    print(f'Removed {on_the_gallow.title()} from all records')
                    return main_menu()
    elif menu_selection== 4:
        logging = True
        name_repeat_check= listed_names()
        with open(name_list, 'a') as nlist:
            while logging:
                name_player = input('Type a name and hit enter. Or (d) for done: ')
                name_player = name_player.lower()
                if name_player == 'd':
                    logging = False
                elif name_player in name_repeat_check:
                    print('There is already a player named that.')
                    print('Please pick a different name.')
                    continue
                else:
                    nlist.write(name_player + '\n')
                    create_blank_accounts(name_player)
                    tax_reset= True
        nlist.close()
        update_accounts()
        if tax_reset:
            os.remove(tax_collectors)
            os.remove(taxed_accounts)
            return tax_options_menu(True)
        else:
            return main_menu()
    elif menu_selection== 5:
        return main_menu()    
    return main_menu()

run()
