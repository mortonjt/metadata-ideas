Here we will be revisiting and expanding upon the [qiime2.Metadata](https://github.com/qiime2/qiime2/blob/dev/qiime2/metadata/metadata.py) object.

Requirements
We want to be able to enable users to more easily annotate their metadata files.  This means providing easy ways to
1. Search for similar metadata columns based on descriptions and types
2. Renaming metadata column names
3. Relabeling metadata column values with validation
4. Creating automated / semi-automated workflows for metadata curation

To do this, we need to have new software abstractions that not only contain more relevant information, but allows for querying and manipulating these data objects.
Defining appropriate types is going to be very important in order to force standards across studies to enable interoperability.


For the metadata object, we need at least 2 (possibly 3) distinct classes, `DataDictionary` and the `SampleMetadata`.


The role of the `DataDictionary` object is to make it easier to keep track of types.
The `DataDictionary` itself is a dictionary, but the values within the `DataDictionary` class itself are typed.



At a high level, we can formulate the following structure

1. Consider a base class `DataColumn` that represents column types within the metadata, and the values that are allowed within a given column
2. A `DataDictionary` object that is really a dictionary of `str`, `DataColumn` pairs
3. The SampleMetadata contains both a `pd.DataFrame` and a `DataDictionary`


```
DataColumn
 - CategoricalDataColumn
 - ContinuousDataColumn

DataDictionary[Str, DataColumn]

SampleMetadata(pd.DataFrame, DataDictionary)
```



