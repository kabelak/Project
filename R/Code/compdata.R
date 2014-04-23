# Usage: my.data.frame = compdata(dataset1, dataset2, dir=1)
# dir = column from which to take data, 1 as default


compdata = function(data1, data2, dir=1){
  N = nrow(data1)
  N2 = nrow(data2)
  
  # Prevent EOF errors by limiting to lowest row number
  if (N2 < N){ N = N2 }
  
  # create a dataframe to store data
  result.df = data.frame(t(rep(NA,3)))
  names(result.df) = c("Nuc_Posn", "Value1", "Value2")
  
  # set a window of allowable difference
  w = 20
  
  
  i = 1
  while ((i+50) <= N){
    
    # Ignore low values
    while ((data1$For[i] <= 15) && (data2$For[i] <= 15)){
      i = i+1
    }
 
    grad1 = lm(data1[i:(i+10),dir] ~ seq(1:11))$coefficients[["seq(1:11)"]]
    grad2 = lm(data2[i:(i+10),dir] ~ seq(1:11))$coefficients[["seq(1:11)"]]
    
    if (grad1 > grad2){
      
      # Condition - If previous entry in df was i-10, or a number of 10s consecutively behind, skip binding
      
      result.df = rbind(result.df,c(i, data1[i,dir], data2[i,dir]))
    }
    
    
#    mean1 = mean(data1[i:(i+50),dir])
#    mean2 = mean(data2[i:(i+50),dir])
#    if (mean1 < (mean2-w) || mean1 > (mean2+w)){
#      result.df = rbind(result.df,c(i, data1[i,dir], data2[i,dir]))
#    }
    
    i = i + 10
  }
  
  # Remove NA's from first line
  result.df = result.df[-1,]
  
  return(result.df)
}

# Instead of mean, it may be a better idea to look at gradient - if the gradient is considerably larger (more positive), it will show that a feature is starting, and that it will rise higher than the correspoding feature, if present, in the other data
# lm(dataexex$For[1:11] ~ seq(1:11))$coefficients[["seq(1:11)"]] - extracts the gradient from the
# Function to create empty df with colnames
# nodata <- as.data.frame(setNames(replicate(5,numeric(0), simplify = F), letters[1:5]))


