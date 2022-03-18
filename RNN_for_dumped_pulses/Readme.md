### A toy Recurrent Neural Network for dumped pulses. 
 
#### WHAT IT DOES:
This is an experiment to see if an RNN can learn an algorithm 
where the effect of the input propagates for a while in the future. 
This aims to replicate the behaviour of a large number of real life physical models.

For example, consider a man standing on a road and hearing cars passing by.
We can ask ourselves how intense is the noise he hears, depending on the cars he sees.
When a car is at the nearest point from him, the noise is maximum. More the car gets far, 
more the noise is dumped. If we imagine the flux of cars as a flux of inputs, 
each one of them fading out with distance, this can represent a sample of the algortithm intended to be
modelled.

In the script presented here, the toy scenario is that of a little boy seeing different animals and going out to the sun or rain.
The output of the algorithm is the feeling of the boy at a certain instant. 
In this simulation, each time step is a day. In each day the boy sees a bunch of animals.
Each animal has a positive or negative effect on the boy's emotions, depending on its nature.
The next day, the boy still fills the emotion related to the animals he saw the day before, but all diminished a bit.
This continues day by day, in a cumulative process.
The graph provided when running the code shows the timeseries of the emotions in the simulation.
The decay of the effect of single emotion is modelled as a negative exponential.
The emotions are mapped to integer numbers.
Exactly the same way as the animal-input-type works, another parameter to influence emotions is added to the model: 
this is the less or more presence of sun. This is intended to raise the dimensionality of the problem, and see
if the RNN can handle it.
The metric chosen so far is the MAPE.





#### INSTRUCTIONS TO RUN THIS EXPERIMENT:

1. This code has been written using the python 3.8.0 interpreter. 
Ensure you have this version (best is to use a virtual env). 
Alternatively, you can try a more recent interpreter, although the compatibility will not be 100% ensured.
2. Dowload the files in this subfolder to test only this particular experiment,
or clone the entire REPO if you are also interested in other projects and to have them on GIT.
3. Be sure to be in this particular experiment subfolder ("/experiments/RNN_for_dumped_pulses). 
Then run from CLI the command "python -m pip install -r requirements.txt". This will install 
the packages/modules required for this particular experiment. 
4. Go to settings.py and configure the parameters there for your local machine.
Read how to do it directly from the settings.py comments.
5. Run the file. You will see a graph first, showing the input to the model. 
To proceed with the computations, close the plot window.
