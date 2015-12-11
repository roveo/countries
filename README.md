# What's up?

This little module can be used to convert free-form English country names into `ISO 3166-1 alpha-3` codes.

# Usage

Use interactively with `ipython` or in scripts.

```python3
from country_encoder import CountryEncoder

ce = CountryEncoder()  # init, load vocabularies

countries = ['Great Britain', 'Russia', 'The UK', 'Myanmar', 'United Kingdom', 'Burma', 'North Korea', 'Sudan', 'South Sudan', 'USSR']

print({c: ce.encode(c) for c in countries})
```

Output:
```python3
{
    'Burma': 'MMR',
    'Great Britain': 'GBR',
    'Myanmar': 'MMR',
    'North Korea': 'PRK',
    'Russia': 'RUS',
    'South Sudan': 'SSD',
    'Sudan': 'SDN',
    'The UK': 'GBR',
    'USSR': 'RUS',
    'United Kingdom': 'GBR'
}
```
