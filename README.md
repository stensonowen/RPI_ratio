# RPI_ratio
Estimating the RPI gender ratio by major/year via names in the RPI directory

Data is scraped from the ["Rensselaer Directories"](http://rpinfo.rpi.edu/directories.html), which has info on students (their major and year) and administration (their title, field, etc.). It doesn't seem to have an api, so it has to be downloaded a page at a time; fortunately pages are indexed, meaning it is easy to get the nth page with a parameter (e.g. http://prod3.server.rpi.edu/peopledirectory/entry.do?datasetName=directory&key=9953).
There are roughly 10k valid entries, of which 75% are records of students.

I then looked up the probability of gender by first name. I got the data from [ssa.gov](https://www.ssa.gov/) ([here](https://www.ssa.gov/oact/babynames/names.zip) more specifically), which approximates the number of males and females born with each name each year.

Estimating the sex of someone by their name can be done using Bayes' Theorem. The Social Security data gives us `P(someone had a given name | their gender)`; e.g. `P('James'|Male) = 22727/3660759` and `P('James'|Female) = 57/3660759` (in 1995). Therefore `P(Female|'James') = P('James'|Female) * P(Female) / P('James') = P('James'|Female) / (P('James'|Female) + P('James'|Male))`. Thus `P(Female|'James') = 57 / (57+22727) = .25%`. 

About 1000 of the collected names are not recognized, because they are uncommon in the US or are spelled uncommonly or whatever. 

The student population is supposedly 34% female, which seems accurate and in line with the official numbers.
Majors with poor ratios (with at least 100 data points) include CS/CSE (17%/16%) and Physics (18%); majors with more women include Bio (58%), Architecture (58%), and Biomedical Engineering (55%).  
