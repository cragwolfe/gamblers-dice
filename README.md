### Measuring the standard deviation of frequencies of a Gambler's Fallacy Die vs. a True Random Die over a large number of rolls

For example, to start 3 experiments with random dice and another 3 experiments with gamblers fallacy dice, run:

`docker-compose up --scale exprandom=3 --scale expgambler=3`

Each "exp" container posts its experimental data to the datacollector container. The first result is posted after 10 iterations, then 20, 40, 80...

The datacollector appends results as they arrive to data/dice-results.csv.

To view the data in a jupyter notebook:

    pip install -r dice/requirements.txt
    jupyter-notebook --ip 0.0.0.0 --notebook-dir dice/jupyter_notebook/ --no-browser&


### With thanks to:

[A Python port](https://github.com/Torvaney/gamblers-dice) of [xori/gamblers-dice](https://github.com/xori/gamblers-dice):

> > The term Gambler's fallacy refers to a misconception about statistics. [...] In statistics, a random event has a certain probability of occurring. The fallacy is that if the event has occurred less frequently in the past, it will be more frequent in the future. -Wikipedia
>
> Well no longer is this a fallacy my friends, these dice are real! If you roll a 20 sided die, and you haven't seen a 20 in a while it is statistically more likely to show up in the next roll with these dice. And the best part, it's still uniformly random for large sample sets!
