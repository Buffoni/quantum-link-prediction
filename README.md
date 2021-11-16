# Link prediction using simple network metrics
Working repository for the science4cast competition.

In the notebook full_code.ipynb there is all the code to replicate the results of the submissions of team Bacalhink. The data to run the algorithm can be found in the science4cast website https://www.iarai.ac.at/science4cast/.

These methods have been initially inspired by a relaxation of a quantum walker L3 and L2 methods but then departed in favour of other metrics like PA.

# Competition submissions

Here is what we have submitted to the leaderboard:

- Bacalhau à Brás: the L3 method - performance: 0.86238699914634
- Bacalhau com Todos: the PA method - performance: 0.8971536961553
- Bacalhau à Gomes de Sá: combines L2 and PA - performance: 0.91073543787275 (L2 alone was slightly better than L3)
- Bacalhau à Lagareiro: combines L2 and PA with time weights - performance: 0.91777075300157
