#results <- read.delim("results.csv")
annotated_barplot <- function(fields, title, fields_opt=fields, width=20){
  #args: "fields" = vector of rows which data in results.csv to use
  #      "title"  = title of the graph
  #  "fields_opt" = optional vector containing list of shorter labels for fields
  #       "width" = width to wrap field labels
  fields_opt = gsub(" ", "\n", fields_opt)
  counts <- c()
  f_pcts <- m_pcts <- c()
  field_labels <- value_labels <- c()
  for(i in 1:length(fields)){
    row <- results[ results$Field == fields[i], ]
    f_pcts <- append(f_pcts, row[,4])
    m_pcts <- append(m_pcts, 1-row[,4])
    counts <- append(counts, paste("n=", row[,3], sep=""))
    value_labels <- append(value_labels, paste(round(row[,4]*100,1), "%", sep=""))
    fields_opt[i] = paste(strwrap(fields_opt[i], width), collapse="\n")
  }
  mtx <- rbind(f_pcts, m_pcts)
  bp = barplot(mtx, names.arg = fields_opt, main=paste("Percent Female:", title, sep="\n"), col=c("pink","light blue"), las=1)
  for(i in 1:length(value_labels)){
    text(x=bp[i], y=mtx[1,i], pos=3, labels=value_labels[i], xpd=TRUE)
    text(x=bp[i], y=mtx[1,i], pos=1, labels=counts[i], xpd=TRUE)
  }
  return(bp)
}



data_years <- c("First-Year Student", "Sophomore", "Junior", "Senior", "Graduate Student")
data_years_<- c("Freshmen", "Sophomore", "Junior", "Senior", "Grad Student")
plot_years <- annotated_barplot(data_years, "Year", data_years_)

data_eng <- c('Mechanical Engineering', 'Biomedical Engineering', 'Chemical Engineering', 'Aeronautical Engineering', 'Electrical Engineering', 'Computer and Systems Engineering', 'Civil Engineering', 'Industrial and Management Engr', 'Undeclared Engineering', 'Materials Engineering', 'Nuclear Engineering', 'Environmental Engineering')
data_eng_<- gsub(" Engineering|Engr", "", data_eng)
plot_eng <-annotated_barplot(data_eng, "School of Engineering", data_eng_)

data_sci <- c('Computer Science', 'Biology', 'Mathematics', 'Physics', 'Chemistry', 'Biochemistry and Biophysics', 'Information Tech and Web Science', 'Geology', 'Bioinformatics and Molec Biology', 'Applied Physics', 'Environmental Science')
data_sci_<- c('Computer Science', 'Biology', 'Mathematics', 'Physics', 'Chemistry', 'Biochemistry and Biophysics', 'ITWS', 'Geology', 'Bioinformatics & Molec Biology', 'Applied Physics', 'Environmental Science')
plot_sci <- annotated_barplot(data_sci, "School of Science", data_sci_)

data_sciu <- c('Mechanical, Aerospace & Nuclear Eng', 'Physics,Applied Physics & Astronomy', 'Engineering Science', 'Mathematical Sciences', 'Chemistry and Chemical Biology', 'Architectural Sciences', 'Decision Sciences and Engr Syst', 'Science, Tech and Society', 'Science and Technology Studies', 'Information Technologies Infrastructure', 'Applied Mathematics')
plot_sciu <-annotated_barplot(data_sciu, "Misc Science Majors", width=19) #render @ 1080p

data_hass <- c('Games and Simulation Arts and Sci', 'Design, Innovation and Society', 'Cognitive Science', 'Elect Media, Arts, and Comm', 'Electronic Arts', 'Economics', 'Psychology', 'Science, Tech and Society', 'School of Humanities, Arts and  Social Sciences', 'Sustainability Studies', 'Communication')
data_hass_<- c('GSAS', 'Design, Innovation & Society', 'Cognitive Science', 'Elect Media, Arts, and Comm', 'Electronic Arts', 'Economics', 'Psychology', 'Science, Tech & Society', 'School of HASS', 'Sustainability Studies', 'Communication')
plot_hass <-annotated_barplot(data_hass, "Humanities and Social Sciences", data_hass_, width=17)

data_bm <- c('Business and Management', 'Industrial and Management Engr', 'Management', 'Lally School of Management')
plot_bm <-annotated_barplot(data_bm, "Business/Management")

data_rsch <- c('Postdoc Research Associate', 'Lighting Research Center', 'Research Administration & Finance', 'Visiting Researcher', 'Research Scientist', 'Research Scientist, Sr.', 'Research Assistant')
plot_rsch <- annotated_barplot(data_rsch, "Research", width=25)

data_prof <- c('Professor', 'Associate Professor', 'Lecturer', 'Assistant Professor', 'Adjunct', 'Visiting Scholar/Adjunct', 'Professor & Department Head')
plot_prof <-annotated_barplot(data_prof, "Teaching Positions")

data_misc <- c('Architecture', 'Communication and Rhetoric', 'Undeclared', 'Arts', 'Technical Communication', 'Communication and Media', 'Undeclared Major', 'Advancement Strategy, Services and Infrastructure')
plot_misc <- annotated_barplot(data_msc, "Misc Majors", width=20)

data_union <- c('Rensselaer Union', 'Rensselaer Union Club Staff')
plot_union <-annotated_barplot(data_unin, "Union Staff", width=30)

data_admn <- c('Physical Plant', 'Administrative Coordinator', 'Administrative Specialist', 'Center for Biotechnology and Interdisciplinary Studies', 'Operations Associate', 'Operations Specialist', 'Auxiliary, Parking and Transportation Services', 'Administrative Associate', 'Research Administration & Finance', 'Health Center', 'Human Resources', 'Registrar', 'Enrollment Operations')
plot_admn <-annotated_barplot(data_admn, "Administration") #render @ 1080p

data_empl <- c('Environmental & Site Services', 'Environmental Specialist, Sr.', 'Department of Athletics', 'Public Safety', 'MultiMedia Services', 'Public Safety Officer II', 'Driver, Shuttle', 'Groundskeeper, Sr.', 'Integrated Admn Computing Services')
plot_empl <-annotated_barplot(data_empl, "School Employees", width=20)
