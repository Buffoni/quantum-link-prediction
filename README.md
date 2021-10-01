# Quantum Walk link prediction
Working repository for the science4cast competition using quantum walks

I think the best managment would be to upload the code that we have now in the main branch and then everyone does his own individual branch and pushes to the main only when major and stable stuff are made.

# L3 Method

I previously created some notes on Istvan's method:

[Istvans_method.pdf](https://github.com/Buffoni/quantum-link-prediction/files/7268290/Istvans_method.pdf)

The current implementation uses the matrix form, but that seems to be very intensive for the 2017 dataset. I think an implementation using the "single entry" form will be much quicker, since we can run it only for the competition set of unconnected nodes.
