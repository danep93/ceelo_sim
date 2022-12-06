# ceelo_sim the dice simulator
never lose (long term) at dice again

### Glossary
_ones-target_ --> if you get a 1 what number do you want to turn it in to  \
_round / turn_ --> a collection of rolls (up to 3)  \
_summary_ --> (x,y,z) eg. rolling three fours in one round is (3,4,1)


__First off, some context.__ Since there's a clear hierarchy of rolls  \
((3,3) > (3,2) > (2,6)) you can assign scores to summaries. If you want to see the mapping of summaries to scores look at the SCORES variable in constants.py

At first I just wanted to answer a few questions so I made a probability simulator.
How did I get my answers? Instead of figuring out the math, I ran simulations. Every time there was a decision to be made I ran thousands of simulations and picked the option that gave me the best answer.

You want to keep rolling until you get the best win:loss ratio

### An intuitive finding
Going first is an advantage because you can choose to maximize your POTENTIAL score with another round. If you rolled [1,2,3,4,6] then (2,2,1) is a horrible roll but it's your best current score. Your expected score in round 2 (3,6,2) will be in a higher percentile (normalized per number of rounds) than your current roll is in round 1 with ones-target 

### Questions I wanted to answer

### 1) Do you ever get such a bad roll you want to reroll all 5 dice?
The answer is no, as you can see, even if you get the worst roll in the game your average score goes down if you reroll all 5 vs keeping your best dice.

Here is the code
<img width="903" alt="Pasted Graphic 6" src="https://user-images.githubusercontent.com/8129369/204041816-62b9ae73-3c4a-4e7e-b4c1-13c98163b5cb.png">

And here are the results. I ran it a few times to prove the results are stable and don't change much
<img width="1103" alt="Pasted Graphic 4" src="https://user-images.githubusercontent.com/8129369/204041848-0107f2ef-b1d3-411c-b0cd-ac22892ec979.png">


### 2) What is the average score per round
In 3 rounds 17.5 A little better than (4,4,3)
In 2 rounds 13.878 . . . a little better than (3,4,2)
In 1 round 8.3265 . . . a little better than (2,4,1)

###### NOTE: If on average you will get something between (2,6) and (3,6), whose scores are 10 and 15 respectively, your average score might be ~12, which is (3,3) even though your 1s target is 6 not 3.

Here is the code for a 1s target of 6 over the next 3 rounds
<img width="889" alt="Pasted Graphic 3" src="https://user-images.githubusercontent.com/8129369/204049079-cb723455-fa91-4e21-adb8-6b36d670a18d.png">

And here are the results
<img width="903" alt="Starting with (J, in 3 pund with ones target 6 the average best score is 17 5135" src="https://user-images.githubusercontent.com/8129369/204049091-c584ea5d-1b66-4955-a697-139bb7c5b958.png">


###### NOTE: The law of large number states with big enough numbers the results trend towards the odds.

### 3) What's better, keeping (3,2) or (2,6)?
The answer depends on which round you want to roll to (which is why going first is an advantage, you get that choice). Here
you can see your best win:loss ratio results from choosing the 6s and rolling through the 2nd round
![img_1.png](images/twos_vs_sixes.png)
##### And now for a movie
https://user-images.githubusercontent.com/8129369/204049244-6e9928a4-3779-4e4a-897f-ab88df27fff1.mov

