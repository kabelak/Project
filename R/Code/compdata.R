compdata = function(data1, data2){
	N = nrow(data1)
	N2 = nrow(data2)
	if (N2 < N){ N = N2 }
	i = 0

	# set a window of allowable difference
	w = 20

	# create a dataframe to store data
	result.df = data.frame(t(rep(NA,3)))
	names(result.df) = c("Nucleotide", "Mean1", "Mean2")

	while ((i+50) <= N){
		mean1 = mean(data1$For[i:(i+50)])
		mean2 = mean(data2$For[i:(i+50)])
		if (mean1 < (mean2-w) || mean1 > (mean2+w)){
			result.df = rbind(result.df,c(i, mean1, mean2))
		}
		i = i + 10
	}

	# Remove NA's from first line
	result.df = result.df[-1,]

	return(result.df)
}


# Function to create empty df with colnames
# nodata <- as.data.frame(setNames(replicate(5,numeric(0), simplify = F), letters[1:5]))

