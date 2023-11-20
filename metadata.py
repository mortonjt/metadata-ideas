from qiime2.metadata import Metadata
from data_dictionary import DataDictionary


class SampleMetadata(Metadata):
    """ For now we will subclass, but eventually this will directly
    implement an expanded version of the qiime2.Metadata object
    """
    def __init__(self, metadata : pd.DataFrame,
                 data_dictionary : DataDictionary):
        self.data_dictionary = data_dictionary
        # some validation needs to be done here to make sure that
        # each metadata column has corresponding entries in the
        # data_dictionary object
        super().__init__(self, metadata)

    def rename_columns(self, namings : dict) -> SampleMetadata:
        """ Creates a new dataframe with renamed columns.
        Keys represent old column name, and values represent new column name.
        This is very similar to the pd.DataFrame.rename function.
        """
        return new_obj

    def rename_column_values(self, column_name : str, namings : dict) -> SampleMetadata:
        """ Creates a new dataframe with renamed column values.
        Keys represent old values, and values represent new values.

        The logic is similar to `df[column_name].apply(lambda x: namings[x])`

        The main contribution here is that edge cases are more elegantly handled
        (i.e. missing values in the column, or missing values in the `namings` object).
        """
        return new_obj

    def column_semantic_distance(other_metadata : SampleMetadata) -> DistanceMatrix:
        return DistanceMatrix()

    def column_value_distance(other_metadata: SampleMetadata) -> DistanceMatrix:
        return DistanceMatrix()


    def nearest_column_matching(other_metadata : SampleMetadata,
                                mode : str) -> dict :
        """ Matches columns from `self` to columns in `other_metadata`
        by leveraging semantic similarity of descriptions in the data dictionary.
        We can leverage SentenceTransformers available in huggingface to
        cast sentences to vectors and infer sentence similarity.

        https://huggingface.co/tasks/sentence-similarity

        Parameters
        ----------
        other_metadata : SampleMetadata

        mode : str
           Specifies to use column values ('value'),
           or column descriptions in data_dictionary ('description')

        Returns
        -------
        dict : mapping column names from `self` to `other_metadata`
        """
