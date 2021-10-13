# Quantum Walk link prediction
Working repository for the science4cast competition using quantum walks

I think the best managment would be to upload the code that we have now in the main branch and then everyone does his own individual branch and pushes to the main only when major and stable stuff are made.

# L3 Method

I previously created some notes on Istvan's method:

[Istvans_method.pdf](https://github.com/Buffoni/quantum-link-prediction/files/7268290/Istvans_method.pdf)

The current implementation uses the matrix form, but that seems to be very intensive for the 2017 dataset. I think an implementation using the "single entry" form will be much quicker, since we can run it only for the competition set of unconnected nodes. It should also be very easy to parallelize.

# Meeting 12/10

Given what we discussed in the meeting I write here a preliminary plan for the sections to include in the final report with relevant information on what to do in each case:

### 1 - Introduction

Talk a bit about network based link prediction using topological patterns, citing Istvan's method for example (and some others, I have references).

### 2 - L3 (Istvan's Method)

Explain the simple model and show the results we already have. João will work on a more optimized implementation of this computing the scores only for the specific pairs needed so that we can both go for higher powers and start doing some more complex optimizations.

### 3 - QLP (Quantum Method)

With a more optimized function to compute the powers of A we can use the first two or three relevant terms in the power series of the time evolution operator to approximate the scores obtained from the quantum method, which will require a free parameter to be trained (t, as in time of the quantum evolution). We can motivate the quantum method here and state we didn't have the time or resources to do a full simulation.

### 4 - Introducing the time stamps of the links

Each link in the network has a timestamp in days spanning a period of roughly 20 years, corresponding to the day that link was created. In order to use this information we can create a weighted adjacency matrix where each weight is some function of the time stamp of each link, which will then produce different scores when running L3 or QLP. Lorenzo will work on the function, starting by optimizing a couple of different order polynomials.

### 5 - Scoring unconnected nodes

Some pairs in the link to be ordered are between nodes with k = 0 and nodes with k > 0. Matrix powers are not able to score these links, and thus a different method must be used. Bruno will work on a type of preferential attachment model using the degree distribution of the network.

### Getting competition results and merging scores

Results from each section can be submitted to the competition independently, thus giving the report a comprehensive look at what changes to the initial simple model had the most effect on the performance.
- Section 2 was already submitted.
- Section 3 will hopefully give better results than section 2 after training the free parameter.
- Section 4 will be interesting to see whether or not we get better results than section 2/3.
- Section 5 will be scoring a completely different set of pairs, so we can include the independent results from this section for discussion purposes.

Ideally, in the end, our best submission would the one merging the results from section 5 and the best results obtained from either 2, 3 or 4. For this we would probably need to normalize all scores and add a free parameter to be trained in this final stage.

### Conclusion

Conclude that we won.

# Competition submissions

Here is what we have submitted to the leaderboard:

- Bacalhau à Brás: the simple L3 method - score: 0.86238699914634
