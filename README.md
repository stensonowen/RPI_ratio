# RPI_ratio
Estimating the RPI gender ratio by major/year via names in the RPI directory

Data is scraped from the ["Rensselaer Directories"](http://rpinfo.rpi.edu/directories.html), which has data on students (their major and year) and administration (their title, field, etc.). It doesn't seem to have an api, so it has to be downloaded a page at a time; fortunately pages are indexed, meaning it is easy to get the nth page with a parameter (e.g. http://prod3.server.rpi.edu/peopledirectory/entry.do?datasetName=directory&key=9953).
There are roughly 10k valid entries, of which 75% are records of students.

I then looked up the probability of gender by first name [here](https://github.com/organisciak/names/blob/master/data/us-likelihood-of-gender-by-name-in-2014.csv) to get preliminary results, but the data is from 2014 and there's no license on the repo, so I think I'll have to do my own analysis. (The probability for all male names was subtracted from 1, so that the corresponding field was 'probability that someone with this name is female'.) I took the average of all corresponding probabilities for everyone in each field (major, year, department, etc.) to get the ratio of women:all for each category.

There are about 5000 total records (3700 student records), meaning a fair portion of the student body was excluded because they weren't on the list of names (the list doesn't include double names or non-US names).  
The student population is supposedly 34% female, which seems accurate and in line with the official numbers.
Majors with poor ratios (with at least 100 data points) include CS/CSE (17%/16%) and Physics (18%); majors with good ratios include Bio (58%), Architecture (58%), and Biomedical Engineering (55%).  
