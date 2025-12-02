import pandas as pd
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
    main_headers = [
        # level 1 properties
        "L1 Name",
        "L1 Formula",
        "L1 Annot. Source: Predicted Compositions",
        "L1 Annot. Source: mzCloud Search",
        "L1 Annot. Source: mzVault Search",
        "L1 Annot. DeltaMass [ppm]",
        "L1 Calc. MW",
        "L1 m/z",
        "L1 Reference Ion",
        "L1 RT[min]",
        "L1 Area(Max.)",
        "L1 mzCloud Results",
        "L1 # mzVault Results",
        "L1 mzCloud Best Match",
        "L1 mzCloud Best Match Confidence",
        "L1 mzVault Best Match",
        "L1 mzVault Library Match",
        "L1 mzVault Library Match",
        "L1 Polarity",
        "L1 MS2",
        "L1 MS2 Purity [%]",
        "L1 Area file 1",
        "L1 Area file 2",
        "L1 Area file 3",
        "L1 Area file 4",
        "L1 Area file 5",
        "L1 Peak Rating (Max.)",
        "L1 Peak Rating file 1",
        "L1 Peak Rating file 2",
        "L1 Peak Rating file 3",
        "L1 Peak Rating file 4",
        "L1 Peak Rating file 5",
        # level 2 properties
        "L2 Calc. MW",
        "L2 Reference Ion",
        "L2 RT [min]",
        "L2 FWHM [min]",
        "L2 Max.  # MI",
        "L2 Polarity",
        "L2 # Adducts",
        "L2 Area (All Ions)",
        "L2 Area Ref. Ion",
        "L2 Study File ID",
        # level 3 properties
        "L3 Ion",
        "L3 Charge",
        "L3 Molecular Weight",
        "L3 m/z",
        "L3 RT[min]",
        "L3 FWHM[min]",
        "L3 # MI",
        "L3 Area",
        "L3 Parent Area [%]",
        "L3 PQF: ZZI",
        "L3 PQF: FWHM2B",
        "L3 PQF: J",
        "L3 PQF: M",
        "L3 PQF: AR",
        "L3 PQF: GR",
        "L3 PQF: NP",
        "L3 PQF: NG",
    ]
    main_rows = []
    for level_1_item in items_iter:
        if level_1_item.AnnotationMatchStatus[1] in (3, 4, 7):  # Filter based on mzCloud Search
            for level_2_item in level_1_item.Children:
                for level_3_item in level_2_item.Children:
                    main_rows.append(
                        [
                            level_1_item.Name,
                            level_1_item.Formula,
                            *[
                                match_status_dictionary[status_number]
                                for status_number in level_1_item.AnnotationMatchStatus
                            ],
                            level_1_item.AnnotationDeltaMassInPPM,
                            level_1_item.MolecularWeight,
                            level_1_item.MassOverCharge,
                            level_1_item.ReferenceIon,
                            level_1_item.RetentionTime,
                            level_1_item.MaxArea,
                            level_1_item.NumberOfmzCloudResults,
                            level_1_item.NumberOfmzVaultResults,
                            level_1_item.mzCloudBestMatch,
                            level_1_item.mzCloudBestMatchConfidence,
                            level_1_item.mzVaultBestMatch,
                            *level_1_item.mzVaultLibraryMatches,
                            level_1_item.Polarity,
                            level_1_item.MSnStatus,
                            level_1_item.IsolationPurity,
                            *level_1_item.Area,
                            level_1_item.PeakRatingMax,
                            *level_1_item.PeakRating,
                            level_2_item.MolecularWeight,
                            level_2_item.ReferenceIon,
                            level_2_item.RetentionTime,
                            level_2_item.FWHM,
                            level_2_item.NumberOfMatchedIsotopes,
                            level_2_item.Polarity,
                            level_2_item.NumberOfAdducts,
                            level_2_item.Area,
                            level_2_item.AreaReferenceIon,
                            level_2_item.StudyFileID,
                            level_3_item.IonDescription,
                            level_3_item.Charge,
                            level_3_item.MolecularWeight,
                            level_3_item.Refmz,
                            level_3_item.RetentionTime,
                            level_3_item.FWHM,
                            level_3_item.NumberOfMatchedIsotopes,
                            level_3_item.Area,
                            level_3_item.RelativeParentArea,
                            level_3_item.PQFZZI,
                            level_3_item.PQFFWHM2B,
                            level_3_item.PQFJ,
                            level_3_item.PQFM,
                            level_3_item.PQFAR,
                            level_3_item.PQFGR,
                            level_3_item.PQFNP,
                            level_3_item.PQFNG,
                        ]
                    )

main_df = pd.DataFrame(data=main_rows, columns=main_headers)
main_df.to_excel("HILIC_POS_5ppm_test.xlsx", index=False)
