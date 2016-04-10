#!/usr/bin/python3
import requests, bs4, re
import sys, random, datetime
from fractions import Fraction

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
    print("Time Elapsed: ", datetime.datetime.now() - start)
    print("People found: ", len(people))
    names = names_to_sex_p2(['yob'+str(i)+'.txt' for i in range(1980,2000)], 'ss_names/')
    print('Names on record: ', len(names))
    ratios = lookup_sex(people, names)
    print('Names not found: ', len(ratios[1]))
    write_data(ratios[0], 'results.csv')
    #return (people, names, ratios[0], ratios[1])

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

def names_to_sex_p2(years, folder=''):
    #more data from https://www.ssa.gov/oact/babynames/names.zip
    #(m_, f_) = dl3.names_to_sex_p2(['yob'+str(i)+'.txt' for i in range(1980,2000)], 'ss_names/')
    #wget https://www.ssa.gov/oact/babynames/names.zip && unzip names.zip -d ss_names
    #1980-1999 returns 58k name records
    m_ = {} #overall averages
    f_ = {}
    t_ = 0
    for y in years:
        #yearly data
        (f, m, t) = names_dict2(folder + str(y))
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


def names_dict2(fn):
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


def names_dict_(fn):
    #data in the form "Name,frequency_percent,cumulative_freq,rank"
    freq = {}
    for line in open(fn, 'r'):
        line = line.split()
        freq[line[0]] = float(line[1])/100.
    return freq

def name_to_sex_p():
    #data from https://www.census.gov/topics/population/genealogy/data/1990_census/1990_census_namefiles.html
    (males, females) = ('dist.male.first', 'dist.female.first')
    male_names = names_dict_(males)
    female_names = names_dict_(females)
    #names = set(male_names.keys() + female_names.keys())
    names = set(list(male_names) + list(female_names))
    p_female = {}
    #generate p(female) for each name
    for name in names:
        #Bayes' theorem
        m = (male_names.get(name) or 0.)
        f = (female_names.get(name) or 0.)
        p_female[name] = f / (m + f)
    return p_female

def lookup_sex(people, names):
    #probabilities expressed as ratio of Women:All (i.e. P(random person in this category is female))
    #0 = male-dominated, 1 = female-dominated, .5 = even
    d = {}
        #d = dictionary of gender probabilities
        #   key = field (e.g. 'Math' or 'Administrator' or 'Sophomore')
        #   val = list: [probability, number of data points]
    not_found = []
    for person in people:
        first_name = person[0].split()[0]
        sex_p = names.get(first_name.upper())
        #if not sex_p:
        if sex_p == None:
            #print(' <' + first_name + '>\t\t(' + person[0] + ')') 
            not_found.append((first_name, person[0]))
            continue
        for x in person[1:]:
            old = d.get(x) or [0,0]
            old[0] += sex_p
            old[1] += 1
            d[x] = old
    return (d, not_found)

if __name__ == "__main__":
    main()
