For Hidden layer 1 in Network 1, below is how each node is calculated:
$$
\overrightarrow{a}^{(2)}=W^{(2)}a^{(1)}+\overrightarrow{b}^{(2)}
$$
For Hidden layer 2 in Network 1, below is how each node is calculated:
$$
\overrightarrow{a}^{(3)}=W^{(3)}a^{(2)}+\overrightarrow{b}^{(3)}
$$
So, as examplified in [d2l.ai Chapter 4.1](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html), we can just collapse out the hidden layers, thus:
$$
\overrightarrow{a}^{(3)}=W^{(3)}(W^{(2)}a^{(1)}+\overrightarrow{b}^{(2)})+\overrightarrow{b}^{(3)}=\overset{\sim}{W}X+\overset{\sim}{b}
$$
Therefore, 
$$
\left\{  
\begin{array}\\
\overset{\sim}{W}=\overrightarrow{W}^{(2)}\overrightarrow{W}^{(3)}\\
\overset{\sim}{b}=\overrightarrow{b}^{(2)}\overrightarrow{b}^{(3)}+\overrightarrow{W}^{(3)}\overrightarrow{b}^{(2)}\
\end{array}
\right.
$$
This feature allows us to continue to stack layers in MLP to build more expressive models.

**References:** 

- ["4.1. Multilayer Perceptrons — Dive into Deep Learning 0.16.1 documentation"](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html). *d2l.ai*. Retrieved 2021-03-02. (and its Chinese version at https://zh.d2l.ai/chapter_deep-learning-basics/mlp.html, which has illustrated almost the same problem, with and without an activation function) 

- [3Blue1Brown's Youtube video on neural network](https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) (very useful to understand why this layer structure)
- LaTeX/Advanced Mathematics. (2020, September 20). *Wikibooks, The Free Textbook Project*. Retrieved 06:56, March 3, 2021 from https://en.wikibooks.org/w/index.php?title=LaTeX/Advanced_Mathematics&oldid=3741965. (I am not good at writing maths XD)

