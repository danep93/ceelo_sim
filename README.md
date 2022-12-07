# Ceelo_Sim the dice decision maker
### never lose (long term) at dice again
![image](https://user-images.githubusercontent.com/8129369/206088689-ea681d1e-d433-45eb-8764-8f01faadd21c.png)


   I was hooked on ceelo since I saw my first dice sack and ledger. Once I understood the rules and realized it was a solved game I needed to solve it. Is it better to keep your lower numbers over your higher numbers if you have more of the same lower number? How does the number of rounds factor into your decision? How does the number of players in your game influence your choice to roll again or stay with the dice you have?

## Object of the game
Everyone throws a dollar in the pot and winner takes all. When you roll your five dice you want to maximize concordance and value — in that order — over a max of three rolls. The person who goes first decides how many rolls that round will be — something we’ll go over in depth later — . . . You can do partial re-rolls for the dice that you don’t like, similar to Five Card Draw poker.   

## Glossary
  
  **_Concordance_**: It means “aggreeance”, if I roll [2,2,2,4,1] I have a concordance of three (twos)
  
  **_Ones target_**: What are you converting your 1s to / which dice are you keeping
  
  **_Summary_**: (4,5,1) means I got four fives in one roll
  
  **_Win-lose ratio_**:  (WLR) How many wins do you see per loss. For optimal stack growth this is the metric you want to maximize. If you have a WLR of 10.5 you’re expected to win that game with 10 other people. However, if you’re playing with 11 other people or more then the odds are that someone else will take home the pot.
  
## Questions answered on strategy

### 1. Why is it an advantage to go first
Let’s use the example of someone going first with (5,5,3) vs your  (4,6,1) 
<img width="1480" alt="Pasted Graphic 16" src="https://user-images.githubusercontent.com/8129369/206085137-d31c9820-5a64-47fc-9b89-a6061211fab8.png">
<img width="1493" alt="Pasted Graphic 17" src="https://user-images.githubusercontent.com/8129369/206085160-55c52f0f-d048-46f5-9edc-677342d48f5f.png">

(5,5,3) beats (4,6,1) even though (4,6,1) is a more “anomalously good” role. That’s because it is a better roll when you [normalize](https://en.wikipedia.org/wiki/Normalization_(statistics)) by round. So if I went first and rolled (4,6,1) I could stop there and maximize my WLR (since it only goes down from there). However, that won’t win the pot and I’m forced to keep rolling. **So in the example of a game with up to 47 people, if you go first and get (4,6,1) you are expected to win. However, if you go second and the first player gets (5,5,3), then he will most likely beat you, even in 3 rolls (85th vs 89th percentile). Even if you do get lucky and beat him you'll very likely lose to one of the other 46 people, as your WLR is now ~6**


### 2. When do you choose lower-concordance-higher-value over higher-concordance-lower-value?

If you have [1,2,2,5,6] do you keep the 2s or 6s? How does that change per round? 

https://user-images.githubusercontent.com/8129369/206085986-e2e6fb44-90f4-415e-97b3-6a1d59a60662.mov
##### As you can see, if you roll those dice and go first you maximize your WLR by keeping the 6s and rolling through round 3

Here are screenshots of the same analysis with 3s and 4s, which as you can imagine, are much closer calls to make.
<img width="1330" alt="image" src="https://user-images.githubusercontent.com/8129369/206086106-01e000fa-bc7c-4dde-9c83-3f1a4d0dd78e.png">
<img width="1342" alt="image" src="https://user-images.githubusercontent.com/8129369/206086165-4112c07e-78ba-463c-9c17-49bb204f343a.png">

So the answer is clear, depending on what my “lower value higher concordance” number is and what my stopping round is I may want to keep the higher numbers. If I have [3,3,1,5,6] and I want to maximize my 2nd round score I keep the 3s but if I want to maximize my 3rd round score I keep the 6s. 


## Frequently asked

**__Why do I see average score numbers changing?__**

I’m running over 10k simulations every time I run the program, but even then the numbers won’t be EXACTLY the same. So is the nature of random number generators, even despite the law of large numbers.


**__What are the scores__**

Since roll summaries are ordinal (5,6) > (5,5) > (4,6) . . . we can assign scores to them. This helps us compare summaries and get mean scores across multiple simulations, even though those scores might lie in the “step” between x and x+1.

**__Are percentiles and win-lose-ratios normalized by round?__**

Yes they are, let's prove this with an example.
Notice how if I have the same dice [3,3,3,2,6] but different rounds, the score in round 2 equals the score in round 3, even though their percentiles and win ratios are different.
<img width="1345" alt="Screen Shot 2022-12-06 at 11 21 32 PM" src="https://user-images.githubusercontent.com/8129369/206088325-d68d4c1f-e376-42bb-87cb-12e6ad131aa4.png">
