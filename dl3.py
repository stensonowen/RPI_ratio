#!/usr/bin/python3
import requests, bs4, re
import sys, random, datetime
from fractions import Fraction

def get_by_index(n):
    #Download RPI Directory page by index
    #Note: entries span n = 1 .. 10532
    #Note: generated 9703 the first time
    #requests session object must be used to preserve session info 
    url = "http://prod3.server.rpi.edu/peopledirectory/entry.do?datasetName=directory&key=" + str(n)
    s = requests.Session()
    return s.get(url)

def parse(html):
    #Convert RPI Directory html into dictionary of fields and values
    #It's a little wonky, but the page formatting doesn't really lend itself to parsing
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
    #extract relevant info from dictionary of directory data
    #If the page is a student's, should return [name, 1, Major, Year]
    #Otherwise, should return [name, 0, Position, Department]
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
    #Get list of details based only on the index
    r = get_by_index(n)
    data = parse(r.text)
    details = extract(data)
    return details

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

def names_to_probs(years, folder=''):
    #calculates gender breakdown for each first name based on SSA data
    #arg 1 is a list of the filenames for to search (e.g. "yob1946.txt")
    #arg 2 is an optional folder these filenames reside in (including a slash)
    #more data from https://www.ssa.gov/oact/babynames/names.zip
    #wget https://www.ssa.gov/oact/babynames/names.zip && unzip names.zip -d ss_names
    #1980-1999 returns 58k name records
    m_ = {} #overall averages
    f_ = {}
    t_ = 0
    for y in years:
        #yearly data
        (f, m, t) = names_dict(folder + str(y))
        for i,j in f.items():
            prev = f_.get(i) or 0
            f_[i] = prev + Fraction(j,t)
        for i,j in m.items():
            prev = m_.get(i) or 0
            m_[i] = prev + Fraction(j,t)
        t_ += t
    print('Total records: ', t_)
    p_female = {}
    for name in set(list(m_) + list(f_)):
        m = (m_.get(name) or 0) #P(name|Man)
        f = (f_.get(name) or 0)
        p_female[name] = float(f / (m+f))
    return p_female


def names_dict(fn):
    #ss data source
    #returns dictionaries of {name:count} for males and females, as well as total people 
    m = {}
    f = {}
    total = 0
    for l in open(fn, 'r'):
        line = l.split(',')
        name = line[0].upper()
        count= int(line[2])
        sex  = line[1].upper()
        if sex == 'F':
            f[name] = count
            total += count
        elif sex == 'M':
            m[name] = count
            total += count
        else:
            print('ERROR: UNKNWON LINE: <' + l + '>')
    return (f, m, total)


def lookup_sex(people, names):
    #calculate probability someone with a given name is female; populate dictionary of probabilities
    #names not found were also tracked for testing purposes
    #probabilities expressed as ratio of Women:All (i.e. P(random person in this category is female))
    #0 = male-dominated, 1 = female-dominated, .5 = even
    #return value is a tuple of the probability dictionary and the list of absent names
    d = {}
        #d = dictionary of gender probabilities
        #   key = field (e.g. 'Math' or 'Administrator' or 'Sophomore')
        #   val = list: [probability, number of data points (i.e. names found in the database)]
    not_found = []
    for person in people:
        first_name = person[0].split()[0]
        sex_p = names.get(first_name.upper())
        if sex_p == None:
            not_found.append((first_name, person[0]))
            continue
        for x in person[1:]:
            old = d.get(x) or [0,0]
            old[0] += sex_p
            old[1] += 1
            d[x] = old
    return (d, not_found)

def main():
    start = datetime.datetime.now()
    people = []
    for n in range(1,10532):
    #for n in [random.randint(1,10532) for i in range(100)]:
        #people.append(fetch(n))
        result = fetch(n)
        if result[0]:   #only append results with a name
            people.append(result)
    print("Time Elapsed: ", datetime.datetime.now() - start)
    print("People found: ", len(people))
    files = ['yob'+str(i)+'.txt' for i in range(1993,1998)] #name files pertinent to undergrads
    names = names_to_probs(files, 'ss_names/')
    print('Names on record: ', len(names))
    ratios = lookup_sex(people, names)
    print('Names not found: ', len(ratios[1]))
    write_data(ratios[0], 'results.csv')
    #return (people, names, ratios[0], ratios[1])


if __name__ == "__main__":
    main()
