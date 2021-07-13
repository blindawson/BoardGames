---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.11.3
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

```python
import pandas as pd
from pandas_highcharts.display import display_charts



time_played = pd.DataFrame([{'Name': 'Twilight Imperium', 'Time Played': 40},
                            {'Name': 'Dominion', 'Time Played': 20},
                            {'Name': 'The Quacks of \nQuedlinburg', 'Time Played': 14},
                            {'Name': 'The Crew', 'Time Played': 12},
                            {'Name': 'War of the Ring', 'Time Played': 9},
                            {'Name': 'Wavelength', 'Time Played': 8},
                            {'Name': 'A Few Acres \nof Snow', 'Time Played': 8}])

display_charts(time_played, kind='bubble')
```

```python
from pandas_highcharts.core import serialize

chart = serialize(time_played, render_to="my-chart", title="Test", kind="bar")

```
