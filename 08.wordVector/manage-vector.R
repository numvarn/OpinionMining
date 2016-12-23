# ------------------------------------------------------------------------------
# File name : manage-vector.R
# Purpose : For checking replicated of terms in word-vector
# Author by Phisan Sookkhee
# Edited : 23 Dec 2016
# ------------------------------------------------------------------------------

setwd("~/Desktop/rawData")

base_dir <- "02.vector/raw-vector"
target_dir <- "02.vector/remove-duplicate"

list <- list.files(path = base_dir)

for (filename in list) {
     file_ext <- tools::file_ext(filename)
     if (file_ext == "csv") {
          infile <- paste(base_dir, filename, sep = "/")
          outfile <- paste(target_dir, filename, sep = "/")
          
          cat(sprintf("Processing file : %s\n", filename))
          
          # read word vector to data frame
          word_vector <- read.csv(infile, header = FALSE)
          
          # check this vector is not empty data
          if (ncol(word_vector) > 4) {
               # keep eng header
               header_en <- as.vector(as.matrix(word_vector[2, ]))
               
               # keep meta-data attibutes
               metadata <-
                    as.matrix(word_vector[3:nrow(word_vector), 1:4])
               metadata_hd <-
                    as.vector(as.matrix(word_vector[2, 1:4]))
               
               # remove header and meta-data attibutes
               vector <-
                    as.matrix(word_vector[-c(1, 2), 5:length(word_vector)])
               
               # Find replicated terms in word-vector
               terms_list <- header_en[5:length(header_en)]
               dup_lt <- list()
               
               for (i in 1:length(terms_list)) {
                    dup_vt <- c()
                    term <- as.character(terms_list[[i]])
                    
                    for (j in i:length(terms_list)) {
                         if (i != j) {
                              sub_term <- as.character(terms_list[[j]])
                              if (term == sub_term) {
                                   dup_vt <- c(dup_vt, c(i, j))
                              }
                         }
                    }
                    
                    if (length(dup_vt) != 0 &&
                        !(term %in% names(dup_lt))) {
                         dup_lt[term] <- paste(unique(dup_vt), collapse = ",")
                    }
               }
               
               # If found duplicate eng_terms
               # Manipulation Matix
               if (length(dup_lt) != 0) {
                    remove_lt <- c()
                    
                    for (value in dup_lt) {
                         index  <- unlist(strsplit(value, ","))
                         
                         # keep remove index-column of vector
                         remove_lt <-
                              c(remove_lt, as.numeric(index[2:length(index)]))
                         
                         first_index <- as.numeric(index[1])
                         result <-
                              as.numeric(as.vector(vector[, first_index]))
                         
                         for (next_i in 2:length(index)) {
                              tmp <- as.numeric(as.vector(vector[, next_i]))
                              result <- result + tmp
                         }
                         
                         vector[, first_index] <- result
                    }
                    
                    # remove replicated column
                    vector <- vector[, -remove_lt]
                    header_en <- header_en[-c(1:4)]
                    header_en <- header_en[-remove_lt]
                    
                    vector <- cbind(metadata, vector)
                    header <- c(metadata_hd, header_en)
                    
                    colnames(vector) <- header
                    
                    # Write all data to CSV
                    write.csv(vector,
                              file = outfile,
                              row.names = FALSE)
               } else {
                    word_vector <- word_vector[-c(1:2),]
                    colnames(word_vector) <- header_en
                    write.csv(
                         word_vector,
                         file = outfile,
                         row.names = FALSE
                    )
               }
          }
     }
}
