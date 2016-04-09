#!/usr/bin/python3
import requests, bs4, re
import sys, random, datetime

def get_by_index(n):
    #Note: entries span n = 1 .. 10532
    #Note: generated 9703 the first time
    #requests session object must be used to preserve session info 
    url = "http://prod3.server.rpi.edu/peopledirectory/entry.do?datasetName=directory&key=" + str(n)
    s = requests.Session()
    return s.get(url)

def parse(html):
    soup = bs4.BeautifulSoup(html, "lxml")
    data = str(soup.find_all(attrs={'id': 'singleDirectoryEntry'}))
    data = data.replace('&amp;', '&')#what's the better way to do this?
    w = re.sub('<.*?>', ' ', data)  #remove tags
    x = re.split("\n | :", w)       #tokenize
    y = [i.strip() 
            for i in x 
            if len(i.strip()) > 1]  #remove garbage
    #convert to dict
    last = ''
    d = {}
    for i in y:
        if i[-1] == ':':
            last = i[:-1]
            d[last] = ''
        elif last in d:
            d[last] += (i + " ")
    for i in d:
        d[i] = d[i].strip()
    return d

def extract(data):
    result = ['?', -1, '?', '?']
    result[0] = data.get('Name')
    if 'Class' in data:
        result[1] = 1
        result[2] = data.get('Curriculum')
        result[3] = data.get('Class')
    else:
        result[1] = 0
        result[2] = data.get('Title')
        result[3] = data.get('Department')
    return result

def fetch(n):
    r = get_by_index(n)
    data = parse(r.text)
    details = extract(data)
    return details

def main():
    start = datetime.datetime.now()
    people = []
    for n in range(1,10532):
    #for n in [random.randint(1,10532) for i in range(100)]:
        #if n%200 == 0:
        #    print(n)
        #people.append(fetch(n))
        result = fetch(n)
        if result[0]:   #only append results with a name
            people.append(result)
    print("Time: ", datetime.datetime.now() - start)
    names = names_dict()
    ratios = lookup_sex(people, names)
    #return ratios
    write_data(ratios, 'results.csv')

def write_data(ratios, fout):
    #write to csv file delimited by tabs/newlines
    f = open(fout, 'w')
    f.write('Field\tRating\tEntries\tP(Woman)\n')
    rename = {0: 'Non-student', 1: 'Student'}
    skip = ['', None]
    for category, result in sorted(ratios.items(), key=lambda x: x[1][1])[::-1]:
        #iterate through dictionary, sorted by number of entries, from most to least
        if category in skip or result[1] <= 5:
            #limit entries to categories with actual data
            continue
        s =  str(rename.get(category) or category) + '\t'
        s += str(result[0]) + '\t'
        s += str(result[1]) + '\t'
        s += str(result[0]/result[1]) + '\n'
        f.write(s)
    f.close()

def names_dict():
    d = {}
    f = open('us-likelihood-of-gender-by-name-in-2014.csv', 'r')
    for i in f:
        [sex, name, p] = i.split(',')
        if sex == 'F':
            d[name] = float(p)
        elif sex == 'M':
            d[name] = 1.0 - float(p)
    f.close()
    return d 

def lookup_sex(people, names):
    #probabilities expressed as ratio of Women:All (i.e. P(random person in this category is female))
    #0 = male-dominated, 1 = female-dominated, .5 = even
    d = {}
        #d = dictionary of gender probabilities
        #   key = field (e.g. 'Math' or 'Administrator' or 'Sophomore')
        #   val = list: [probability, number of data points]
    for person in people:
        first_name = person[0].split()[0]
        sex_p = names.get(first_name)
        if not sex_p:
            continue
        for x in person[1:]:
            old = d.get(x) or [0,0]
            old[0] += sex_p
            old[1] += 1
            d[x] = old
    return d

if __name__ == "__main__":
    main()
