#' Usage: my.data.frame = compdata(dataset1, dataset2, dir=1, lv=10, w=10, s=10)
#' dir = column from which to take data, 1 as default
#' lv = value under which data from datasets will be ignored (when both datasets have values below or equal to that number)
#' w = window of values to consider
#' s = slide for each iteration


compdata = function(data1, data2, dir=1, lv=10, w=10, s=10){
  N = nrow(data1)
  N2 = nrow(data2)
  
  # Prevent EOF errors by limiting to lowest row number
  if (N2 < N){ N = N2 }
  
  # create a dataframe to store data
  result.df = data.frame(t(rep(NA,3)))
  names(result.df) = c("Nuc_Posn", "Value1", "Value2")
  
  # set a window of allowable difference (for mean)
  # meanw = 20
  
  if (dir == 1){
    
    i = N
    run = 1:(1+w)
   # run = sort(run, decreasing = TRUE)
    
    while ((i-s) > 0){
      
      # Ignore low values
      while ((data1[i,dir] <= lv) && (data2[i,dir] <= lv)){
        i = i-1
      }
      
      grad1 = lm(data1[i:(i-w),dir] ~ run)$coefficients[["run"]]
      grad2 = lm(data2[i:(i-w),dir] ~ run)$coefficients[["run"]]
      

      # ignore until gradient next becomes positive and greater than grad2
      if ((grad1 > grad2) && (grad1 > 0)){
        
        ###### ADD: Condition - If previous entry in df was i-10, or a number of 10s consecutively behind, skip binding
        ########### if gradient is still positive, ignore; basically, ignore until gradient next becomes positive
        ###### There should be a difference between forward and reverse - reverse should look at the gradient from the otehr side of the graph
        
        result.df = rbind(result.df,c(i, data1[i,dir], data2[i,dir]))
        
        # if gradient is still positive, ignore
        while (((lm(data1[i:(i+w),dir] ~ run)$coefficients[["run"]]) > 0) && ((i-10) >= 0)){
          i = i - 10
        }
      }
      
      i = i - s
      }
      
      # Remove NA's from first line
      result.df = result.df[-1,]
    }
  
  
  
  if (dir == 2){
    
    i = 1
    run = 1:(1+w)
    
    while ((i+s) <= N){
      
      # Ignore low values
          while ((data1[i,dir] <= lv) && (data2[i,dir] <= lv)){
            i = i+1
          }
      
      grad1 = lm(data1[i:(i+w),dir] ~ run)$coefficients[["run"]]
      grad2 = lm(data2[i:(i+w),dir] ~ run)$coefficients[["run"]]
      
      # ignore until gradient next becomes positive and greater than grad2
      if ((grad1 > grad2) && (grad1 > 0)){
        
        ###### ADD: Condition - If previous entry in df was i-10, or a number of 10s consecutively behind, skip binding
        ########### if gradient is still positive, ignore; basically, ignore until gradient next becomes positive
        ###### There should be a difference between forward and reverse - reverse should look at the gradient from the otehr side of the graph
                
        result.df = rbind(result.df,c(i, data1[i,dir], data2[i,dir]))
        
        # if gradient is still positive, ignore
        while (((lm(data1[i:(i+w),dir] ~ run)$coefficients[["run"]]) > 0) && ((i+10) <= N)){
          i = i + 10
        }
                
      }
      
      
      #    mean1 = mean(data1[i:(i+w),dir])
      #    mean2 = mean(data2[i:(i+w),dir])
      #    if (mean1 < (mean2-meanw) || mean1 > (mean2+meanw)){
      #      result.df = rbind(result.df,c(i, data1[i,dir], data2[i,dir]))
      #    }
      
      i = i + s
    }
    
    # Remove NA's from first line
    result.df = result.df[-1,]
  }
  
  
  return(result.df)
}

# Instead of mean, it may be a better idea to look at gradient - if the gradient is considerably larger (more positive), it will show that a feature is starting, and that it will rise higher than the correspoding feature, if present, in the other data
# lm(dataexex$For[1:11] ~ seq(1:11))$coefficients[["seq(1:11)"]] - extracts the gradient from the
# Function to create empty df with colnames
# nodata <- as.data.frame(setNames(replicate(5,numeric(0), simplify = F), letters[1:5]))


