import os
import json
import time
from random import randint
from datetime import datetime
import requests
import json

start = time.time()
record = []

is_posix = False
if os.name == 'posix':
    is_posix = True

is_hard = True;

CEND      = '\33[0m' if is_posix else ''
CBOLD     = '\33[1m' if is_posix else ''
CBLINK    = '\33[5m' if is_posix else ''
CRED    = '\33[31m' if is_posix else ''
CGREEN  = '\33[32m' if is_posix else ''
CYELLOW = '\33[33m' if is_posix else ''
CREDBG    = '\33[41m' if is_posix else ''
CBLUEBG   = '\33[44m' if is_posix else ''
CBEIGE  = '\33[36m' if is_posix else ''
CGREY    = '\33[90m' if is_posix else ''

def send_slack(timestamp, name, total, correct, wrong, score, duration):
    #webhook_url = 'https://hooks.slack.com/services/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'
    #webhook_url = 'https://hooks.slack.com/services/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'
    # {\"channel\": \"#general\", \"username\": \"webhookbot\", \"text\": \"This is posted to #general and comes from a bot named webhookbot.\", \"icon_emoji\": \":ghost:\"}"
    with open("webhook.json") as webhook:
        webhook_data = json.load(webhook)
        webhook_url = webhook_data.get('slack_webhook')


    slack_data = {
        'channel': '#exercise',
        'username': name,
        'text': 
                '\n ----------------------------------'  + '\n' +
                '    *%s* ' % timestamp + '\n' +
                '----------------------------------'  + '\n' +
                ' *Name*: %s' % str(name) + '\n' +
                ' *Score*: %s' % str(score) + '\n' +
                ' *Problem Number*: %s' % str(total) + '\n' +
                ' *Correct*: %s' % str(correct) + '\n' +
                ' *Wrong*: %s' % str(wrong) + '\n' +
                ' *Spent Time*: %s' % str(duration) + '\n \n'
    }

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        print('Not sent')
        print(response.status_code)
        print(response.content)        
    

ops = ['+', '-', 'x']

print('')
name = input('Please input your name:')

number = input('Please input the number of problems you want to play:')

while True:
    if number.isdigit() and int(number) != 0:
        break

    if not number.isdigit():
        msg = 'Please input the number of problems you want to play:'
    elif int(number) == 0:
        msg = 'Please input a non-zero number :'

    number = input(msg)
    
print('')
for i in range(int(number)):
    op = ops[randint(0, 2)]    
    
    if op == '+':
        a = randint(1, 10)
        b = randint(1,10)
        exp = a + b

        if is_hard == True:
            whole = randint(1, 20)
            part1 = randint(1, 10)
            if whole < part1:
                t = whole
                whole = part1
                part1 = whole
            exp = whole - part1
        
    elif op == '-':
        a = randint(1, 20)
        b = randint(1,10)
        if a < b:
            t = a
            a = b
            b = a
        exp = a - b
        
    elif op == 'x':
        a = randint(1, 10)
        b = randint(1, 10)
        exp = a * b

           
    
    
    if op == '+' and is_hard == True:
        c = input('%s)   (    ) %s %s = %s  ' % (i+1, op, part1, whole))
    else:
        c = input('%s)   %s %s %s = ' % (i+1, a, op, b))
        
    while not c.isdigit():                
        print('Please input a number')
        
        if op == '+' and is_hard == True:
            c = input('%s)   (    ) %s %s = %s  ' % (i+1, op, part1,whole))
        else:
            c = input('%s)   %s %s %s = ' % (i+1, a, op, b))
                    
    if int(c) == exp:
        # print('You answer is ' +  CGREEN + 'correct' + CEND)
        r = 0
    else:
        # print('You answer is ' +  CRED + 'wrong' + CEND)
        r = 1
    if op == '+' and is_hard == True:
        record.append((op, whole, part1, c, r, i+1))
    else:
        record.append((op, a, b, c, r, i+1))
    print('')
end = time.time()
duration = int(end - start)
#print('%s seconds' % str(duration))

correct = 0
wrong = 0
for r in record: 
    if r[4] == 0:
        correct = correct + 1
    else:
        wrong = wrong + 1


print('--------------------------------------------')
min, sec = divmod(duration, 60)
print('You spent ' + CBOLD + CYELLOW + str(min) + CEND + ' minutes ' +  CBOLD + CYELLOW + str(sec) + CEND + ' seconds completing %s problems' % str(len(record)))
print('You have ' +  CBOLD + CYELLOW + str(correct) + CEND + ' correct and ' + CBOLD + CYELLOW + str(wrong) + CEND + ' wrong answers')
score = int(correct*100/(correct+wrong))
print('Your score is ' + CBLINK + CBOLD + CYELLOW + str(score) + CEND)
if score == 100:
    print('Good job, %s!' % name)
elif score > 80 and score < 99:
    print('You can do it better, %s!' % name)
elif score < 80:
    print(CRED + 'Shame of you!!!' + CEND)

print('')
input('Type any key to review problems and your answers ... ')
print('')
for r in record: 
    result =  CGREEN + 'Correct' + CEND if r[4] == 0 else CRED + 'Wrong' + CEND
    if r[0] == '+' and is_hard == True:
    #if r[0] == '+':
        print('%s)   (%s) %s %s = %s (%s)' % (r[5], r[3], r[0], r[1], r[2], result))
    else:
        print('%s)   %s %s %s = %s (%s)' % (r[5], r[1], r[0], r[2], r[3], result))
        
print('')


if not name:
    name = 'unknown'

# put result files in to the folder with the local machine name
machine_name = os.uname()[1].lower().split('.')[0].replace('-', '').replace('_', '')
result_folder = './result/%s' % machine_name
if not os.path.exists(result_folder):
    os.makedirs(result_folder, 0o755)
result_file = os.path.join(result_folder, name.lower() + '.txt')
with open(result_file, 'a') as f:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    f.write('%s %s %s %s \n' % (timestamp, str(duration), str(correct), str(wrong)))


send_slack(timestamp, name, len(record), correct, wrong, score, '%s:%s' %(min, sec))
