Results:
Interesting behavior using Python 2 and Python 3 under different conditions.  
The significative test is the last one (Python 3.6 with 'lockcontrol=True') where all rounds returned consistent results.  

EDIT: Despite the results for test 'Python 3.6 with 'lockcontrol=True' that's still unsafe. After searching for the subject (threading), and python's "Global Interpreter Lock" and accordingly some instruction in Freenode's #python channel it seems that the satisfactory result from the last test cannot be guaranteed for different situations, for any python version.  
If the objective is achieve thread safe operations and secure access of shared data/objects it's necessary to use python specific locking resources. The same example (but using thread locks) is exemplified in threadingspree2.py archive.
Reference: http://effbot.org/zone/thread-synchronization.htm  


* Python 2.7 with variable 'lockcontrol = False'. 1000 threads fired in each round.

round 1:  
[0, 0] = 270 | [1, 0] = 242 | [0, 1] = 264 | [1, 1] = 224  
Total processed: 1000  

round 2:  
[0, 0] = 237 | [1, 0] = 265 | [0, 1] = 255 | [1, 1] = 242  
Total processed: 999  

round 3:  
[0, 0] = 246 | [1, 0] = 247 | [0, 1] = 235 | [1, 1] = 273  
Total processed: 1001  

round 4:  
[0, 0] = 253 | [1, 0] = 240 | [0, 1] = 265 | [1, 1] = 236  
Total processed: 994  

round 5:  
[0, 0] = 244 | [1, 0] = 237 | [0, 1] = 255 | [1, 1] = 261  
Total processed: 997  


* Python 2.7 with variable 'lockcontrol = True'. 1000 threads fired in each round.

round 1:  
[0, 0] = 64 | [1, 0] = 436 | [0, 1] = 436 | [1, 1] = 64  
Total processed: 1000  

round 2:  
[0, 0] = 204 | [1, 0] = 296 | [0, 1] = 300 | [1, 1] = 201  
Total processed: 1001  

round 3:  
[0, 0] = 345 | [1, 0] = 156 | [0, 1] = 150 | [1, 1] = 349  
Total processed: 1000  

round 4:  
[0, 0] = 159 | [1, 0] = 341 | [0, 1] = 340 | [1, 1] = 160  
Total processed: 1000  

round 5:  
[0, 0] = 215 | [1, 0] = 285 | [0, 1] = 286 | [1, 1] = 214  
Total processed: 1000  


* Python 3.6 with variable 'lockcontrol = False'. 1000 threads fired in each round.

round 1:  
[0, 0] = 179 | [1, 0] = 291 | [0, 1] = 200 | [1, 1] = 330  
Total processed: 1000  

round 2:  
[0, 0] = 282 | [1, 0] = 217 | [0, 1] = 273 | [1, 1] = 228  
Total processed: 1000  

round 3:  
[0, 0] = 200 | [1, 0] = 262 | [0, 1] = 224 | [1, 1] = 314  
Total processed: 1000  

round 4:  
[0, 0] = 205 | [1, 0] = 276 | [0, 1] = 206 | [1, 1] = 313  
Total processed: 1000  

round 5:  
[0, 0] = 226 | [1, 0] = 271 | [0, 1] = 211 | [1, 1] = 292  
Total processed: 1000  


* Python 3.6 with variable 'lockcontrol = True'. 1000 threads fired in each round.

round 1:  
[0, 0] = 500 | [1, 0] = 0 | [0, 1] = 0 | [1, 1] = 500  
Total processed: 1000  

round 2:  
[0, 0] = 500 | [1, 0] = 0 | [0, 1] = 0 | [1, 1] = 500  
Total processed: 1000  

round 3:  
[0, 0] = 500 | [1, 0] = 0 | [0, 1] = 0 | [1, 1] = 500  
Total processed: 1000  

round 4:  
[0, 0] = 500 | [1, 0] = 0 | [0, 1] = 0 | [1, 1] = 500  
Total processed: 1000  

round 5:  
[0, 0] = 500 | [1, 0] = 0 | [0, 1] = 0 | [1, 1] = 500  
Total processed: 1000  




