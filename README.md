python-fastpip (Segmentation Based On Turning Points)
=====================================================

The “Perceptually Important Points” algorithm
gives a method for dimensionality reduction and a mechanism to automatically extract
the most important points from a human observer perspective, favouring compression and
a good visualization of time series with high dimensionality.

Example
-------

```python
    >>> from fastpip import pip
    >>> pip([(0, 0), (1, 1), (2, 2), (3, 1), (4, 0), (5, 1), (6, 2), (7, 1), (8, 0)], 5)
    [(0, 0), (2, 2), (4, 0), (6, 2), (8, 0)]
```


References
----------
- https://github.com/intelie/fastpip-js
- http://www.academia.edu/1578716/Aplica%C3%A7%C3%A3o_do_algoritmo_Perceptually_Important_Points_em_s%C3%A9ries_temporais_de_datacenters
