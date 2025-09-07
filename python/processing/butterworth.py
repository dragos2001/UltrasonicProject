from utils import FileHandler
import pandas as pd 
from plot.plot_signal import plot_signal


class MultiBiquadFloat:
            default_coefs =[ [ 5.49496377e-04, -1.09899275e-03,  5.49496377e-04,  1.00000000e+00, 7.75752801e-01,  5.82317689e-01],
                [ 1.00000000e+00, -2.00000000e+00,  1.00000000e+00,  1.00000000e+00, 5.54213901e-01,  6.30454831e-01],
                [ 1.00000000e+00,  0.00000000e+00, -1.00000000e+00,  1.00000000e+00, 1.03575406e+00,  6.80934131e-01],
                [ 1.00000000e+00,  2.00000000e+00,  1.00000000e+00,  1.00000000e+00, 4.52443546e-01,  8.39682131e-01],
                [ 1.00000000e+00,  2.00000000e+00,  1.00000000e+00,  1.00000000e+00, 1.26801640e+00,  8.75731512e-01]]
            

         
            def __init__(self, coefs = default_coefs):
                self.original_coefs = coefs
                self.num_sections = len(self.original_coefs)
                #self.coeffs = array('f' , [])
                #self.state = array('f' , [0]*(self.num_sections*2))
                self.coeffs=[]
                self.state = [0]*(self.num_sections*2)
                for s, section in enumerate(self.original_coefs):
                    b0, b1, b2, a0, a1, a2 = section
                    self.coeffs.extend([b0,b1,b2,a1,a2])

           
            def process_sample (self, x):
                    
                    x_float = (x-32658)/32658
                    for s in range(self.num_sections):
                        #---------------------------
                        ci = s*5
                        si = s*2
                        #--------------------------
                        b0 = self.coeffs[ci+0]
                        b1 = self.coeffs[ci+1]
                        b2 = self.coeffs[ci+2]
                        #---------------------------
                        #a0_inv = self.coeffs[ci+3]
                        a1 = self.coeffs[ci+3]
                        a2 = self.coeffs[ci+4]
                        #---------------------------
                        yn = b0 * x_float + self.state[si] 
                        self.state[si+0] =  b1 * x_float - a1 * yn + self.state[si+1] 
                        self.state[si+1] =  b2 * x_float - a2 * yn 
                        x_float = yn
                      
                        #---------------------------
                    return yn
         
            
            def apply_filter(self, data):

                output = [self.process_sample(x) for x in data]

                return output

if __name__ =="__main__":
    #file handler obj
    fh = FileHandler()
    th_order_coeffs4 =[ [0.00245139, -0.00490278,  0.00245139, 1, 0.62705842, 0.59315217],
                        [1, -2,  1, 1, 0.93918031, 0.62993437],
                        [1, 2, 1, 1,0.45639616, 0.80515434],
                        [1, 2, 1, 1,1.2414353 , 0.84737342]]
    th_order_coeffs2 = [[ 0.04828833, -0.09657667,  0.04828833 , 1.,          0.51495245,  0.6680828 ],
                        [ 1.,          2.,          1,          1.,          1.09773868,  0.7223506 ]]
    #butter filter object
    butter_filter = MultiBiquadFloat(th_order_coeffs2)
    #read path
    path = fh.select_file()
    #read a dataframe
    data_frame = pd.read_csv(path)
    #extract signal
    timestamps = data_frame.iloc[:,0]
    signal = data_frame.iloc[:,1]
    #apply filtering
    filtered_signal = butter_filter.apply_filter(signal)
    
    #plot original
    plot_signal(timestamps,signal,'Original')
    
    #plot filtered
    plot_signal(timestamps,filtered_signal,title="Filtered")
    
    






























