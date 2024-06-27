# This code aims to check if the functions set.pop(), randrange(), and choice() do actually produce random selections of elements from a set.

More specifically, we will select 5 random cards from a full deck (52 cards) using each of the aforementioned methods 
and check if these 5 cards form a straight.

Now, the possible straights of 5 cards from a 52-card deck are x = 10,240, while the possible combinations of 5 cards
from a 52-card deck are y = 2,598,960. Therefore the probability of having a straight is x / y = 0.00394 or 0.394%.

So, we will run several thousand rounds and see if all three functions produce a straight with a probability close
to 0.394%.
