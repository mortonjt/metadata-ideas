# ----------------------------------------------------------------------------
# Copyright (c) 2023--, dynomics development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from abc import ABC, abstractmethod
from typing import List, Union, Dict, Optional, Tuple
import yaml


def _validate_float(values, null_values):
    for v in values:
        if v not in null_values:
            float(v)


def _cast_float(values, null_values):
    res = []
    for v in values:
        if v in null_values:
            res.append(None)
        else:
            res.append(float(v))
    return res


class DataColumn(ABC):
    def __init__(
        self, name: str, description: str, null_values: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        if null_values:
            self.null_values = null_values
        else:
            self.null_values = [
                "not_applicable",
                "not_collected",
                "not_provided",
                "restricted_access",
            ]

    @abstractmethod
    def data_type(self):
        pass

    @abstractmethod
    def validate(self, values):
        pass

    def cast(self, values):
        self.validate(values)
        return values


class BooleanDataColumn(DataColumn):
    @property
    def data_type(self):
        return "Boolean"

    def validate(self, values: List[Union[str, bool]]):
        for v in values:
            if v not in self.null_values:
                if v not in {"True", "False", "Yes", "No", "0", "1", True, False, 0, 1}:
                    raise ValueError(
                        f"Invalid value {v} for boolean column " f"{self.name}."
                    )

    def cast(self, values: List[Union[str, bool]]) -> List[bool]:
        self.validate(values)
        res = []
        for v in values:
            if v in self.null_values:
                res.append(None)
            else:
                res.append(True if v in {"True", "Yes", "1", True, 1} else False)
        return res


class ContinuousDataColumn(DataColumn):
    def __init__(
        self,
        name: str,
        description: str,
        unit: str,
        null_values: Optional[List[str]] = None,
    ):
        super().__init__(name, description, null_values)
        # TODO : need to add unit types
        self.unit = unit

    @property
    def data_type(self):
        return "Continuous"

    def validate(self, values: List[Union[str, float, int]]):
        try:
            _validate_float(values, self.null_values)
        except ValueError:
            raise ValueError(f"Invalid values for continuous column " f"{self.name}.")

    def cast(self, values: List[Union[str, float, int]]) -> List[float]:
        self.validate(values)
        res = _cast_float(values, self.null_values)
        return res


class CategoricalDataColumn(DataColumn):
    def __init__(
        self,
        name: str,
        description: str,
        categories: List[str],
        null_values: Optional[List[str]] = None,
    ):
        super().__init__(name, description, null_values)
        self.categories = categories

    @property
    def data_type(self):
        return "Categorical"

    def validate(self, values: List[Union[str, int]]):
        for v in values:
            if v not in self.null_values:
                if v not in self.categories:
                    raise ValueError(
                        f"Invalid value {v} for categorical " f"column {self.name}."
                    )

    def cast(self, values: List[Union[str, int]]) -> List[int]:
        self.validate(values)
        res = []
        for v in values:
            if v in self.null_values:
                res.append(None)
            else:
                res.append(self.categories.index(v))
        return res

    def rename(self, new_categories: dict, values: List[Union[str, int]]):
        """Rename categories in a categorical column."""
        res = []
        for v in values:
            res.append(new_categories[self.categories[v]])

        self.categories = [new_categories[c] for c in self.categories]

        return res


class OrdinalDataColumn(CategoricalDataColumn):
    def __init__(
        self,
        name: str,
        description: str,
        categories: List[str],
        null_values: Optional[List[str]] = None,
    ):
        super().__init__(name, description, null_values)
        self.categories = categories
        # TODO : need to figure out how to enforce ordering

    @property
    def data_type(self):
        return "Ordinal"


class FreeTextDataColumn(DataColumn):
    def __init__(
        self,
        name: str,
        description: str,
        text: str,
        null_values: Optional[List[str]] = None,
    ):
        super().__init__(name, description, null_values)

    @property
    def data_type(self):
        return "FreeText"

    def validate(self, values: str):
        for v in values:
            if not isinstance(values, str):
                raise ValueError(
                    f"Invalid value {v} for free text column " f"column {self.name}."
                )


class IdentifierDataColumn(DataColumn):
    def __init__(self, name: str, description: str):
        super().__init__(name, description, None)

    @property
    def data_type(self):
        return "Identifier"

    def validate(self, values: List[Union[int, str]]):
        for v in values:
            if not isinstance(v, str):
                if not isinstance(v, int):
                    raise ValueError(
                        f"Invalid value {v} for identifier column "
                        f"column {self.name}."
                    )


class BiospecimenDataColumn(DataColumn):
    def __init__(
        self, name: str, description: str, null_values: Optional[List[str]] = None
    ):
        super().__init__(name, description, null_values)

    @property
    def data_type(self):
        return "Biospecimen"

    def validate(self, values: List[Union[int, str]]):
        for v in values:
            if not isinstance(v, str):
                if not isinstance(v, int):
                    raise ValueError(
                        f"Invalid value {v} for identifier column "
                        f"column {self.name}."
                    )


class TemporalDataColumn(DataColumn):
    def __init__(self, name: str, description: str):
        super().__init__(name, description, None)

    @property
    def data_type(self):
        return "Temporal"

    def validate(self, values: List[Union[int, float]]):
        _validate_float(values, self.null_values)

    def cast(self, values: List[Union[int, float]]) -> List[float]:
        self.validate(values)
        res = _cast_float(values, self.null_values)
        return res

    def time(self, values: List[str], unit: str):
        # convert time stamps to a specific unit
        x = pd.to_datetime(values)
        return getattr(x, unit)


class Spatial1dDataColumn(DataColumn):
    def __init__(self, name: str, description: str):
        super().__init__(name, description, None)

    @property
    def data_type(self):
        return "Spatial1d"

    def validate(self, values: List[Union[int, float]]):
        # Q : how should time stamps be handled?
        _validate_float(values, self.null_values)

    def cast(self, values: List[Union[int, float]]) -> List[float]:
        self.validate(values)
        res = _cast_float(values, self.null_values)
        return res


class Spatial2dDataColumn(DataColumn):
    def __init__(self, name: str, description: str):
        super().__init__(name, description, None)

    @property
    def data_type(self):
        return "Spatial2d"

    def validate(self, values: List[Tuple[Union[int, float], Union[int, float]]]):
        # Q : how should time stamps be handled?
        x, y = zip(*values)
        _validate_float(x, self.null_values)
        _validate_float(y, self.null_values)

    def cast(self, values: List[Union[int, float]]) -> List[Tuple[float, float]]:
        self.validate(values)
        x, y = zip(*values)
        x = _cast_float(x, self.null_values)
        y = _cast_float(y, self.null_values)
        return list(zip(x, y))


class Spatial3dDataColumn(DataColumn):
    def __init__(self, name: str, description: str):
        super().__init__(name, description, None)

    @property
    def data_type(self):
        return "Spatial3d"

    def validate(
        self,
        values: List[Tuple[Union[int, float], Union[int, float], Union[int, float]]],
    ):
        # Q : how should time stamps be handled?
        x, y, z = zip(*values)
        _validate_float(x, self.null_values)
        _validate_float(y, self.null_values)
        _validate_float(z, self.null_values)

    def cast(self, values: List[Union[int, float]]) -> List[Tuple[float, float]]:
        self.validate(values)
        x, y, z = zip(*values)
        x = _cast_float(x, self.null_values)
        y = _cast_float(y, self.null_values)
        z = _cast_float(z, self.null_values)
        return list(zip(x, y, z))


class DataDictionary(dict):
    # TODO : we need to revisit this.
    # I think the safest bet is to have
    # 3 columns, the name, the description, and the data type
    def read(self, filename: str):
        res = yaml.safe_load(filename)
        # TODO : validate

        for k, v in res.items():
            self.__setitem__(k, v)

    def write(self, filename: str):
        with open(filname, "w") as f:
            yaml.dump(self, f)
