# RPI_ratio
Estimating the RPI gender ratio by major/year via names in the RPI directory

Images also hosted [here](http://imgur.com/a/hzot3).

Data is scraped from the ["Rensselaer Directories"](http://rpinfo.rpi.edu/directories.html), which has info on students (their major and year) and administration (their title, field, etc.). It doesn't seem to have an api, so it has to be downloaded a page at a time; fortunately pages are indexed, meaning it is easy to get the nth page with a parameter (e.g. http://prod3.server.rpi.edu/peopledirectory/entry.do?datasetName=directory&key=9953).
There are roughly 10k valid entries, of which 75% are records of students.

I then looked up the probability of gender by first name. I got the data from [ssa.gov](https://www.ssa.gov/) ([here](https://www.ssa.gov/oact/babynames/names.zip) more specifically), which approximates the number of males and females born with each name each year.
To set up this data so that it can be found by the script out of the box, run `wget https://www.ssa.gov/oact/babynames/names.zip && unzip names.zip -d ss_names`; otherwise the code should be easy to change.

Estimating the sex of someone by their name can be done using [Bayes' Theorem](https://en.wikipedia.org/wiki/Bayes'_theorem). The Social Security data gives us `P(someone had a given name | their gender)`; e.g. `P('James'|Male) = 22727/3660759` and `P('James'|Female) = 57/3660759` (in 1995). Therefore `P(Female|'James') = P('James'|Female) * P(Female) / P('James') = P('James'|Female) / (P('James'|Female) + P('James'|Male))`. Thus `P(Female|'James') = 57 / (57+22727) = .25%`. 

The year range used for the names data was 1993-1997, as comparisons of undergrads (i.e. year/major) are probably the most interesting. A broader range would recognize more names, but the estimates might be less accurate (using names from 1980-1999 allows for recognition of a few dozen more names and usually alters data by less than a percent).

About 1000 of the collected names are not recognized, probably because they are uncommon in the US or are spelled uncommonly or something; this leaves about 5000 student entries and 1500 administration entries. 

The student population is supposedly 31% female, which seems accurate and in line with the official numbers.
Majors with poor ratios (excluding fields with ≤100 data points) include CS/CSE and Physics (all 16%); majors with more women include Bio and Architecture (both 56%).
