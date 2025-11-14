import csv

import pyeds

match_status_dictionary = {
    7: "Not the top hit",
    5: "Invalid mass",
    4: "Full match",
    3: "Partial match",
    2: "No match",
    1: "No results",
}

with pyeds.EDS("HILIC_POS_5ppm.cdResult") as eds:
    # define connection path and items to keep
    path = ["Compounds", "Compounds per File", "Features per File"]

    # read data
    items_iter = eds.ReadHierarchy(path)
    with open("HILIC_POS_5ppm.csv", "w", newline="", encoding="utf_8") as csvfile:
        csv_writer = csv.writer(csvfile)
        # write level 1 header
        csv_writer.writerow(
            [
                "Name",
                "Formula",
                "Annot. Source: Predicted Compositions",
                "Annot. Source: mzCloud Search",
                "Annot. Source: mzVault Search",
                "Annot. DeltaMass [ppm]",
                "Calc. MW",
                "m/z",
                "Reference Ion",
            ]
        )
        for level_1_item in items_iter:
            # write level 1 content
            csv_writer.writerow(
                [
                    level_1_item.Name,
                    level_1_item.Formula,
                    *[match_status_dictionary[status_number] for status_number in level_1_item.AnnotationMatchStatus],
                    level_1_item.AnnotationDeltaMassInPPM,
                    level_1_item.MolecularWeight,
                    level_1_item.MassOverCharge,
                    level_1_item.ReferenceIon,
                ]
            )
            # write level 2 header
            csv_writer.writerow(
                [
                    "",
                    "Calc. MW",
                    "Reference Ion",
                    "RT [min]",
                    "FWHM [min]",
                ]
            )
            for level_2_item in level_1_item.Children:
                # write level 2 content
                csv_writer.writerow(
                    [
                        "",
                        level_2_item.MolecularWeight,
                        level_2_item.ReferenceIon,
                        level_2_item.RetentionTime,
                        level_2_item.FWHM,
                    ]
                )
                # write level 3 header
                csv_writer.writerow(["", "", "Ion", "Charge"])
                for level_3_item in level_2_item.Children:
                    # write level 3 content
                    csv_writer.writerow(["", "", level_3_item.IonDescription, level_3_item.Charge])
