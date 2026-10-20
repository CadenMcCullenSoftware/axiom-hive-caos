"""Tests for the coherence of the catalogue's class-to-category mapping.

The catalogue declares, for each countermeasure class, the adversary
categories it principally addresses. The taxonomy declares the categories.
The mapping between them is the join that lets an operator go from "this
technique" to "what addresses it", and a join that has drifted is a join that
misleads.
"""

from __future__ import annotations

import unittest

from caos.countermeasures import CATALOGUE, by_class
from caos.taxonomy import CATEGORIES, categories_for_countermeasure_class


class ClassCategoryMappingTests(unittest.TestCase):
    def test_every_class_has_a_mapping(self) -> None:
        for cm_class in {c.cm_class for c in CATALOGUE}:
            mapped = categories_for_countermeasure_class(cm_class)
            self.assertTrue(mapped, f"{cm_class} maps to no category")
            for category in mapped:
                self.assertIn(category, CATEGORIES)

    def test_every_countermeasure_binds_at_least_one_of_its_class_s_categories(self) -> None:
        """A countermeasure must act on something its own class addresses.

        The catalogue binds each entry to the adversary categories it is
        written against. The class mapping says which categories each class
        principally addresses. An entry that binds only outside its class's
        mapping is an entry whose class label and whose bindings disagree,
        and a reader would be misled by one of the two.
        """
        for cm in CATALOGUE:
            mapped = categories_for_countermeasure_class(cm.cm_class)
            self.assertTrue(
                cm.techniques & mapped,
                f"{cm.identifier} binds {sorted(cm.techniques)} and its class "
                f"{cm.cm_class.value} addresses {sorted(mapped)}",
            )

    def test_each_class_has_entries(self) -> None:
        for cm_class in {c.cm_class for c in CATALOGUE}:
            self.assertTrue(by_class(cm_class))

    def test_the_mapping_covers_every_category_the_catalogue_binds(self) -> None:
        bound = {category for cm in CATALOGUE for category in cm.techniques}
        mapped = set()
        for cm_class in {c.cm_class for c in CATALOGUE}:
            mapped |= categories_for_countermeasure_class(cm_class)
        self.assertTrue(
            bound <= mapped,
            f"categories bound but not mapped: {sorted(bound - mapped)}",
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
