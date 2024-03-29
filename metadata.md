Here we will be revisiting and expanding upon the [qiime2.Metadata](https://github.com/qiime2/qiime2/blob/dev/qiime2/metadata/metadata.py) object.

Problem : automating (or semi-automating) metadata curation
What are the biggest (or most time consuming) challenges for metadata curation?
1. Interpreting column names / units / values (due to lack of documentation)
2. Matching / syncing columns between metadata tables (quadratic runtime)
3. Data validation. Identifying if values are properly typed or have appropriate values

Possible solutions
1. Reinforce standards ahead of time via standards (i.e. MIXS or MIMARKS) or template wizards (i.e. QIIMP)
2. Lower the barrier for manual curation

Issue with QIIMP : forces the wizard to identify all of the columns to be filled out, and doesn't allow for additional columns to be added.

Requirements for metadata format
1. Identifiers that uniquely identify host_subject_id, timepoints and other contexts (i.e. geographical location)
2. Identifiers that uniquely identify biospecimens (to handle multiple omics levels)
3. Being able to handle time points with metadata (but no biospecimen information)
4. Being able to interface with QIIMP
5. Update QIIMP to be able to handle additional identifier types

Requirements for metadata manipulation
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

The `DataColumn` now has 2 functions
- `validate` which determines if the column has validate values consistent with the time
- `cast` which casts the input values to the specifie type, enabling transformations
It is important to also note that the defined `DataColumn` specifies missing values, which is often an edge case in data transformations.

Below are the DataColumn subtypes that are currently defined

```
DataColumn
 - BooleanDataColumn
 - CategoricalDataColumn
 - ContinuousDataColumn
 - OrdinalDataColumn
 - FreeTextDataColumn
 - IdentifierDataColumn
 - BiospecimenDataColumn
 - TemporalDataColumn
 - Spatial1dDataColumn
 - Spatial2dDataColumn
 - Spatial3dDataColumn
```
And these `DataColumn` objects can be fed into a `DataDictionary` object, which are then used to create `SampleMetadata` objects
```
DataDictionary[Str, DataColumn]

SampleMetadata(pd.DataFrame, DataDictionary)
```

Follow up questions

1. Should the `SampleMetadata` object directly subclass `qiime2.Metadata` and just add an extra argument for `DataDictionary`, or should it replace `qiime2.Metadata`?
2. What type of interface would best faciliate column matching between two sample metadata objects? k-nearest neighbors, bipartite matching, or both? And how should column similarity should be measured (i.e. values in the columns, semantic similarity between text, or similarity between unit descriptions?).
3. Should categories also have their own separate descriptors? For instance, one project may name one category `Control` and other project names the same category `neurotypical`. Having categorical descriptors could help with further automation.
4. If we are using ML models to match columns and categories, we also need to consider developing an interface to highlight uncertainty.
5. What are good datasets to test this on?  ASD-meta-analysis? Soil stressors project? FMT meta-analysis? American Gut Project?
6. What would best faciliate the process of inspecting elements within a spreadsheet? For instance, if one wanted to identify static vs dynamic variables, what would be a reasonable interface?
7. We should investigate other tools that could complement this approach (i.e. [OpenRefine](https://openrefine.org/) [Trelloscope](https://trelliscope.org/), Excel ). While using visualizations is key to data curation (and visualizations can be time consuming), I'm wary about defining visualization / interactive functions due to maintainence burden.  But if there is a tabular visualization library that enables scripting, that could be useful.  
