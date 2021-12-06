# ------------------------------------------------------------------------------------------------ #
# MIT License                                                                                      #
#                                                                                                  #
# Copyright (c) 2020, Microsoft Corporation                                                        #
#                                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software    #
# and associated documentation files (the "Software"), to deal in the Software without             #
# restriction, including without limitation the rights to use, copy, modify, merge, publish,       #
# distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the    #
# Software is furnished to do so, subject to the following conditions:                             #
#                                                                                                  #
# The above copyright notice and this permission notice shall be included in all copies or         #
# substantial portions of the Software.                                                            #
#                                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING    #
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND       #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,     #
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.          #
# ------------------------------------------------------------------------------------------------ #

import haiku as hk
import jax.numpy as jnp

from .._core.base_stochastic_func_type2 import BaseStochasticFuncType2
from ..utils import jit
from ._entropy import EntropyRegularizer


class NStepEntropyRegularizer(EntropyRegularizer):
    r"""

    Policy regularization term based on the n-step entropy of the policy.

    The regularization term is to be added to the loss function:

    .. math::

        \text{loss}(\theta; s,a)\ =\ -J(\theta; s,a) - \beta\,H[\pi_\theta(.|s)]

    where :math:`J(\theta)` is the bare policy objective.

    Parameters
    ----------
    f : stochastic function approximator

        The stochastic function approximator (e.g. :class:`coax.Policy`) to regularize.

    n : tuple(int), list(int), ndarray

        Time indices of the steps (counted from the current state at time `t`)
        to include in the regularization. For example `n = [2, 3]` adds an entropy bonus for the
        policy at the states t + 2 and t + 3 to the objective.

    beta : non-negative float

        The coefficient that determines the strength of the overall regularization term.

    gamma : float between 0 and 1

        The amount by which to discount the entropy bonuses.

    """

    def __init__(self, f, n, beta=0.001, gamma=0.99):
        super().__init__(f)
        if not isinstance(n, (tuple, list, jnp.ndarray)):
            raise TypeError(f"n must be a list, an ndarray or a tuple, got: {type(n)}")
        if len(n) == 0:
            raise ValueError("n cannot be empty")
        self.n = n
        self.beta = beta
        self.gamma = gamma
        self._gammas = jnp.power(self.gamma, jnp.arange(self.n[-1] + 1))

        def entropy(dist_params, valid):
            return sum([gamma * self.f.proba_dist.entropy(p) * v
                        for p, v, gamma in zip(dist_params, valid, self._gammas)])

        def function(dist_params, beta):
            assert len(dist_params) == 2
            params, dones = dist_params
            valid = self.valid_from_done(dones)
            return -beta * entropy(params, valid)

        def metrics(dist_params, beta):
            assert len(dist_params) == 2
            params, dones = dist_params
            valid = self.valid_from_done(dones)
            return {
                'EntropyRegularizer/beta': beta,
                'EntropyRegularizer/entropy': jnp.mean(entropy(params, valid) /
                                                       sum([v for v, _ in zip(valid, self._gammas)])
                                                       )
            }

        self._function = jit(function)
        self._metrics_func = jit(metrics)

    @property
    def batch_eval(self):
        if not hasattr(self, '_batch_eval_func'):
            def batch_eval_func(params, hyperparams, state, rng, transition_batch):
                rngs = hk.PRNGSequence(rng)
                if not isinstance(transition_batch.extra_info, dict):
                    raise TypeError(
                        'TransitionBatch.extra_info has to be a dict containing "states" and' +
                        ' "dones" for the n-step entropy regularization. Make sure to set the' +
                        ' record_extra_info flag in the NStep tracer.')
                if isinstance(self.f, BaseStochasticFuncType2):
                    dist_params, _ = zip(*[self.f.function(params, state, next(rngs),
                                                           self.f.observation_preprocessor(
                        next(rngs), s_next), True)
                        for t, s_next in enumerate(transition_batch.extra_info['states'])
                        if t in self.n])
                else:
                    raise TypeError(
                        "f must be derived from BaseStochasticFuncType2")
                dist_params = (dist_params, jnp.asarray(
                    [d for t, d in enumerate(transition_batch.extra_info['dones']) if t in self.n]))
                return self.function(dist_params, **hyperparams), self.metrics_func(dist_params,
                                                                                    **hyperparams)

            self._batch_eval_func = jit(batch_eval_func)

        return self._batch_eval_func

    def valid_from_done(self, dones):
        """
        Generates a mask that filters all time steps after a done signal has been reached.

        Parameters
        ----------
        dones : ndarray

            Array of boolean entries indicating whether the episode has ended.

        Returns
        -------
        valid : ndarray

            Mask that filters all entries after a done=True has been reached.
        """
        valid = jnp.ones_like(dones, dtype=jnp.float32)
        return valid.at[1:].set(1 - jnp.clip(jnp.cumsum(dones[:-1], axis=0), a_max=1))