setwd("~/Desktop/rawData")

base_dir <- "02.vector/remove-duplicate"
filename <- "test.csv"

infile <- paste(base_dir, filename, sep = "/")
data <- read.csv(infile, header = TRUE) 

# Remove meta-data column in data frame
data$ID <- NULL
data$File <- NULL
data$Directory <- NULL

library(arules)
rules <- apriori(data, parameter=list(support=0.9, confidence=1))
rules.sorted <- sort(rules, by="lift")