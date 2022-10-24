# Gearing Up Py(thon)

[![Generic badge](https://img.shields.io/badge/version-0.1-green.svg)](https://shields.io/)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

# Introduction
I'm the Fleet Officer for the Harrow Cycle Hub (https://www.harrowcyclehub.org/). A lot of bikes come my way, quite a few through donations. These older, heavy, rusty bikes come from manufacturers typically outside of the more common household names e.g. Giant, Specialized etc. This repo holds some code which I will use to analyze the bikes which I get my hands on. In particular, I am interested in the choice of gearing setup. As always data is king. So my code will get better as I provide more data sets.

# Inventory Service
When the code is run, an ```/inventory``` endpoint will service requests. It does a basic lookup of manufacturer in a data file, with the Bike Index API (https://bikeindex.org/documentation/api_v3). The response will be a HTML table with the data rows and fields linking to the manufacturers website.
