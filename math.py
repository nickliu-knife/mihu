import time
from random import randint
from datetime import datetime
start = time.time()
record = []

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CBLINK    = '\33[5m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CREDBG    = '\33[41m'
CBLUEBG   = '\33[44m'
CBEIGE  = '\33[36m'
CGREY    = '\33[90m'

ops = ['+', '-']

print('')
name = raw_input('Please input your name:')
number = ''
while not number.isdigit():
    number = raw_input('Please input the number of problems you want to play:')

print('')
for  _ in range(int(number)):
    op = ops[randint(0, 1)]    
    
    if op == '+':
        a = randint(1, 10)
        b = randint(1,10)
        exp = a + b
    elif op == '-':
        a = randint(1, 20)
        b = randint(1,10)
        if a < b:
            t = a
            a = b
            b = a
            
        exp = a - b

    c = raw_input('%s %s %s = ' % (a, op, b))
    while not c.isdigit():                
        print('Please input a number')
        c = raw_input('%s %s %s = ' % (a, op, b))

    if int(c) == exp:
        # print('You answer is ' +  CGREEN + 'correct' + CEND)
        r = 0
    else:
        # print('You answer is ' +  CRED + 'wrong' + CEND)
        r = 1
    record.append((op, a, b, c, r))
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
print('You spent ' + CBLINK + CBOLD + CYELLOW + str(min) + CEND + ' minutes ' + CBLINK + CBOLD + CYELLOW + str(sec) + CEND + ' seconds')
print('You have ' +  CBLINK + CBOLD + CYELLOW + str(correct) + CEND + ' and ' + CBLINK + CBOLD + CYELLOW + str(wrong) + CEND + ' answers')
score = int(correct*100/(correct+wrong))
print('Your score is ' + CBLINK + CBOLD + CYELLOW + str(score) + CEND)
if score == 100:
    print('Good job, %s!' % name)
elif score > 80 and score < 99:
    print('You can do it better, %s!' % name)
elif score < 80:
    print(CRED + 'Shame of you!!!' + CEND)

print('')
raw_input('Type any key to review problems and your answers ... ')
print('')
for r in record: 
    result =  CGREEN + 'Correct' + CEND if r[4] == 0 else CRED + 'Wrong' + CEND
    print('%s %s %s = %s (%s)' % (r[1], r[0], r[2], r[3], result))

print('')


if not name:
    name = 'unknown'
with open(name.lower() + '.txt', 'a') as f:
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    f.write('%s %s %s %s \n' % (timestamp, str(duration), str(correct), str(wrong)))

