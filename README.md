### It's a simple class to convert Python dict or JSON string into a pandas dataframe.

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

#### The main class is JSONToDataframe
##### Example:
```python
from json2df.json2df import JSONToDataframe
from json2df.json2df import LoadInfo


json_file = 'data/svg_example.json'

info_ = LoadInfo(file=json_file).get_data()
j2df = JSONToDataframe(json_data=info_).convert_to_df()
print(j2df.head())

   menu_header menu_items_id menu_items_label menu_items
0   SVG Viewer          Open              NaN        NaN
1   SVG Viewer       OpenNew         Open New        NaN
2   SVG Viewer           NaN              NaN       None
3   SVG Viewer        ZoomIn          Zoom In        NaN
4   SVG Viewer       ZoomOut         Zoom Out        NaN
5   SVG Viewer  OriginalView    Original View        NaN
6   SVG Viewer           NaN              NaN       None
7   SVG Viewer       Quality              NaN        NaN
8   SVG Viewer         Pause              NaN        NaN
9   SVG Viewer          Mute              NaN        NaN
10  SVG Viewer           NaN              NaN       None
11  SVG Viewer          Find          Find...        NaN
12  SVG Viewer     FindAgain       Find Again        NaN
13  SVG Viewer          Copy              NaN        NaN
14  SVG Viewer     CopyAgain       Copy Again        NaN
```

