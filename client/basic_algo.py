    
import h5py

SUCCESS = 0
FAILED = 1
class Search_algo:
    def Search_for_user(self,username): 
        with h5py.File('user_basic.h5', 'r') as file:
            if username in file:
                return SUCCESS
            else:
                return FAILED
            
SearchAlgo = Search_algo()