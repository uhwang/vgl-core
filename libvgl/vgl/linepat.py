'''
    linepat.py
    
    03/09/2023
    
'''

_pattern_name = [   "NULL", 
                    "SOLID", 
                    "DASH", 
                    "DASHDOT", 
                    "DOT", 
                    "LONGDASH", 
                    "DASHDOTDOT"
                ]

_PAT_NULL      = _pattern_name[0]
_PAT_SOLID     = _pattern_name[1]
_PAT_DASH      = _pattern_name[2]
_PAT_DASHDOT   = _pattern_name[3]
_PAT_DOT       = _pattern_name[4]
_PAT_LONGDASH  = _pattern_name[5]
_PAT_DASHDOTDOT= _pattern_name[6]

def get_pattern_names():
    return _pattern_name[1:].copy()

class LinePattern():
    def __init__(self, pat_len, pat_t):
        self.pat_len = pat_len
        self.pat_t = pat_t
        
    def __str__(self):
        return "pat_len: %f\npat_t: %s"%(self.pat_len, self.pat_t)
    
_default_pattern_length = 0.04
_pattern_length = _default_pattern_length

#_lpat_null       = LinePattern(pat_len, linepat._PAT_NULL) 
_lpat_dash       = LinePattern(_pattern_length, _PAT_DASH) 
_lpat_dashdot    = LinePattern(_pattern_length, _PAT_DASHDOT)   
_lpat_dot        = LinePattern(_pattern_length, _PAT_DOT) 
_lpat_longdash   = LinePattern(_pattern_length, _PAT_LONGDASH) 
_lpat_dashdotdot = LinePattern(_pattern_length, _PAT_DASHDOTDOT) 

def set_stock_pattern_length(pat_len): _pattern_length = pat_len
def reset_stock_pattern_length(pat_len): _pattern_length = pat_len

def _lpat(pat_len, pat_t): return LinePattern(pat_len, pat_t)

#def get_null(): return _lpat_null
def get_dash(pat_len): return LinePattern(pat_len, _PAT_DASH) 
def get_dashdot(pat_len): return LinePattern(pat_len, _PAT_DASHDOT)   
def get_dot(pat_len): return LinePattern(pat_len, _PAT_DOT) 
def get_longdash(pat_len): return LinePattern(pat_len, _PAT_LONGDASH) 
def get_dashdotdot(pat_len): return LinePattern(pat_len, _PAT_DASHDOTDOT) 

def get_stock_dash(): return LinePattern(_pattern_length, _PAT_DASH)  
def get_stock_dashdot(): return LinePattern(_pattern_length, _PAT_DASHDOT)  
def get_stock_dot(): return LinePattern(_pattern_length, _PAT_DOT)  
def get_stock_longdash(): return LinePattern(_pattern_length, _PAT_LONGDASH)  
def get_stock_dashdotdot(): return LinePattern(_pattern_length, _PAT_DASHDOTDOT)  

def get_pattern_name_dash(): return _PAT_DASH
def get_pattern_name_dashdot(): return _PAT_DASHDOT
def get_pattern_name_dot(): return _PAT_DOT
def get_pattern_name_longdash(): return _PAT_LONGDASH
def get_pattern_name_dashdotdot(): return _PAT_DASHDOTDOT