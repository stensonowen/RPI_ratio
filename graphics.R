#results <- read.delim("results.csv")

svsa = matrix(c(0.3027334124, 0.3963599947, 0.6972665876, 0.6036400053), nrow=2, ncol=2, byrow=TRUE)
color = "Red"
bp = barplot(svsa, names.arg = c("Student\nn=4947", "Non-student\nn=1447"), main="Percent Female:\nStudent vs Non-student", col=c("pink","light blue"))
text(x=bp[1], y=svsa[1,1], pos=3, labels="30.3%")
text(x=bp[2], y=svsa[1,2], pos=3, labels="39.6%")

annotated_barplot <- function(fields, title){
  f_pcts <- m_pcts <- c()
  field_labels <- value_labels <- c()
  for(i in 1:length(fields)){
    row <- results[ results$Field == fields[i], ]
    f_pcts <- append(f_pcts, row[,4])
    m_pcts <- append(m_pcts, 1-row[,4])
    label <- paste(fields[i], "\nn=", row[,3], sep="")
    field_labels <- append(field_labels, label)
    label <- paste(round(row[,4]*100,1), "%", sep="")
    value_labels <- append(value_labels, label)
  }
  mtx <- rbind(f_pcts, m_pcts)
  bp = barplot(mtx, names.arg = field_labels, main=title, col=c("pink","light blue"))
  for(i in 1:length(value_labels)){
    text(x=bp[i], y=mtx[1,i], pos=3, labels=value_labels[i])
  }
  return(bp)
}

annotated_barplot(
  c("Student", "Non-student"), 
  "Percent Female: Student vs Non-student")

annotated_barplot(
  c("Professor", "Associate Professor", "Lecturer", "Assistant Professor", "Adjunct", "Visiting Scholar/Adjunct"), 
  "Percent Female: Teaching Positions")

annotated_barplot(
  results[grepl("Engineer", results$Field), ][,1],
  "Percent Female: Engineering Majors")
