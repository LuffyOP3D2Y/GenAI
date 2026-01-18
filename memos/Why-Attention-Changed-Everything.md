**Why Attention Changed everything?**

**Summary: "Attention allowed models to decide which parts of the input
matter most for each prediction, instead of forcing all information
through a single bottleneck"**

**Let me explain:**

1.  **What limitations attention removed.**

Before attention took centerstage, LLMs relied heavily on RNNs which
would arrive at the output sequentially working on tokens one by one in
their order of arrival. Although RNNs provided mechanisms for backward
propagation, the tokens themselves were not able to get compared with
each other and hence the LLM would not be able to form a meaningful
context of the inputs specified. Also since, sequential processing was
inherent to RNNs, scaling them would mean huge processing and
computation costs.

With Attention, both problems got solved to an extent. Attention
architecture focused on deriving meaningful context based on how two
tokens in an input sequence interact with each other to build that
context, irrespective of their position in the sequence. Hence tokens
that were far apart would also be able to add to the vectors of other
terms which wasn't previously possible with RNNs. Also because there
could be multiple attention blocks that could be used to derive a
specific part of the context; they could be run parallelly, independent
of each other giving scaling and cost efficiency.

2.  **Why Parallelism Mattered?**

With increasing parameters and improvements in hardware architecture
with advent of GPUs, it was the sequential processing that was inherent
in RNNs that was holding back LLMs from scaling and was proving to be a
huge bottleneck. Parallelism unlocked the power of GPUs to process
multiple threads simultaneously that ran independently which is what
Attention architecture facilitated with multiple attention blocks
running at the same time on same embeddings without waiting for output
from the previous block.

3.  **Why this enabled scale?**

Since attention blocks could now be processed independently to represent
embeddings in a more contextually meaningful vector space, it made
scaling feasible because now researchers could stack multiple attention
blocks without worrying about time constraints caused by sequential
processing and it gave rise to huge number of different ways of
attention giving rise to total number of parameters. The parameters were
not only dependent on embeddings but also on attention queries, their
keys and value scalers.

4.  **Conclusion:**

Attention basically changed the lay of the land entirely by unlocking
parallel processing, better information flow and increase in parameters.
It also enabled tokens to affect weights of other tokens irrespective of
their distance in the sequence making gains on contextual meaning.
