# synapse
Small AI with synapse learning instead of traditional backprop

First off, I wouldn't design a production system like this. Rather,
its just interesting way to show how a system
can learn without explicitly specifying any cost function
or reward estimation. The learning happens implicitly.

All learning is done at the synapse level, rather than
from explicit global backpropagation of distribution errors.
Interestingly, you can view this implementation as an actor-centric
implementation of Deep Belief Networks / Stacked RBMs. The synapse network
makes greedy synapse adaptations that implicitly encourage (regularized)
consistency between the model and data distributions.
