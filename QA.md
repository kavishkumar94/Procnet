### LEVEL 1

#### How would you prove the code is correct?

    Answer: The correctness of the code can be checked by performing tests on it. And I created sample data to perform tests. 
    The more number of tests we perform, the more the chances are to catch bugs/errors in the program. And for the code that is 
    to be used in production environment, it should go through tests like unit testing, acceptance testing, load testing and etc.

#### How would you make this solution better?

    Answer: We can make the solution better by using classes and objects. We could also use list and dict comprehensions to make 
    our code compact and fast. However we should avoid writing long comprehensions as it can make the code difficult to understand. 
    The code should always be user friendly.

#### Is it possible for this program to miss a connection?

    Answer: Yes, it is possible for the program to miss a connection because the interval at which the program checks for the 
    connnection is 10 Seconds and generally a new connection takes milliseconds to change it's state from new connnection to 
    established or any other state. So there is a possibility that we might miss few connections in between polls.

##### If you weren't following these requirements, how would you solve the problem of logging every new connection?

    Answer: If these requirements weren't in place, I would have collected logs using netstat or SS.
