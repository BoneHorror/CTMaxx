class ANSI_COLORS:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREY = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"

P_CORES = range(0,12) #P/E denomer is used interchangeably with CCDs, where P is CCD0 and E is CCD1
E_CORES = range(12,24)
SMT = True