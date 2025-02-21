class ANSI_COLORS:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREY = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    
#Whether this CPU supports SMT
SMT = True

#P/E denomer is used interchangeably with CCDs, where P is CCD0 and E is CCD1
#Ryzen 9 7900 var.
P_CORES = range(0,12) 
E_CORES = range(12,24)

#Ryzen 5 8500G var.
#P_CORES = [0,1,8,9] 
#E_CORES = [2,3,4,5,6,7,10,11]

#Ryzen AI 9 365 var.
#P_CORES = range(0,8)
E_CORES = range(8,20)

