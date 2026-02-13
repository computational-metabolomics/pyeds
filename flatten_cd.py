import os
import sys

import pandas as pd
import pyeds

path_to_project = "X:\\data\\PrecisionTox\\Studies\\02_Phase2"

match_status_dictionary = {
    7: "Not the top hit",
    5: "Invalid mass",
    4: "Full match",
    3: "Partial match",
    2: "No match",
    1: "No results",
}

mzvault_match_status_dictionary = {
    2: "Multiple matches found",
    1: "Single match found",
    0: "No matches found",
}

level_2_headers = [
    "L2 Calc. MW",
    "L2 Reference Ion",
    "L2 RT [min]",
    "L2 FWHM [min]",
    "L2 Max. # MI",
    "L2 Polarity",
    "L2 # Adducts",
    "L2 Area (All Ions)",
    "L2 Area Ref. Ion",
    "L2 Study File ID",
]

level_3_headers = [
    "L3 Ion",
    "L3 Charge",
    "L3 Molecular Weight",
    "L3 m/z",
    "L3 RT [min]",
    "L3 FWHM [min]",
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

mzcloud_headers = [
    "mzCloud Structure",
    "mzCloud Name",
    "mzCloud Formula",
    "mzCloud Molecular Weight",
    "mzCloud Best Match",
    "mzCloud mzCloud ID",
    "mzCloud IUPAC Name",
    "mzCloud KEGG ID",
    "mzCloud CAS Number",
    "mzCloud SMILES",
    "mzCloud InChI",
    "mzCloud InChIKey",
    "mzCloud HMDB ID",
    "mzCloud PubChem CID",
    "mzCloud Compound Class",
    "mzCloud DeltaMass [Da]",
    "mzCloud DeltaMass [ppm]",
    "mzCloud Match",
    "mzCloud Confidence",
    "mzCloud Compound Match",
]

# define connection paths
input_files_path = ["Input Files"]
main_path = ["Compounds", "Compounds per File", "Features per File"]
comp_path = ["Compounds", "mzCloud Results"]


def extract_data(output_file_directory: str, path_to_cd_result: str, output_file_name: str) -> None:
    """Extract data from a Thermo Fisher .cdResult file into two Excel spreadsheets.

    Args:
        output_file_directory: The directory to store the output Excel spreadsheets.
        path_to_cd_result: The full path to the Thermo Fisher .cdResult file.
        output_file_name: The basis of the output file name. Usually "HILIC_POS_5ppm" or "LIPIDS_POS_5ppm".
    """
    with pyeds.EDS(path_to_cd_result) as eds:
        # extract names of input files
        input_files_iter = eds.ReadHierarchy(input_files_path)
        input_files_names = []
        for input_file_item in input_files_iter:
            if input_file_item.SampleType == "Sample":
                input_files_names.append(
                    f"{os.path.basename(input_file_item.FileName)} ({input_file_item.StudyFileID})"
                )

        # extract data for main file
        main_items_iter = eds.ReadHierarchy(main_path)
        main_rows = []
        for level_1_item in main_items_iter:
            if level_1_item.AnnotationMatchStatus.GetLevel(1).Name in (
                "Partial match",
                "Full match",
                "Not the top hit",
            ):  # Filter based on mzCloud Search
                for level_2_item in level_1_item.Children:
                    for level_3_item in level_2_item.Children:
                        main_rows.append(
                            [
                                level_1_item.ID,
                                level_1_item.Name,
                                level_1_item.Formula,
                                *[
                                    level_1_item.AnnotationMatchStatus.GetLevel(box_number).Name
                                    for box_number in range(len(level_1_item.AnnotationMatchStatus))
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
                                *[
                                    level_1_item.mzVaultLibraryMatches.GetLevel(box_number).Name
                                    for box_number in range(len(level_1_item.mzVaultLibraryMatches))
                                ],
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

        # extract data for comp file
        comp_items_iter = eds.ReadHierarchy(comp_path)
        comp_rows = []
        for level_1_item in comp_items_iter:
            if level_1_item.AnnotationMatchStatus[1] in (3, 4, 7):  # Filter based on mzCloud Search
                for mz_cloud_item in level_1_item.Children:
                    comp_rows.append(
                        [
                            level_1_item.ID,
                            level_1_item.Name,
                            level_1_item.Formula,
                            *[
                                level_1_item.AnnotationMatchStatus.GetLevel(box_number).Name
                                for box_number in range(len(level_1_item.AnnotationMatchStatus))
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
                            *[
                                level_1_item.mzVaultLibraryMatches.GetLevel(box_number).Name
                                for box_number in range(len(level_1_item.mzVaultLibraryMatches))
                            ],
                            level_1_item.Polarity,
                            level_1_item.MSnStatus,
                            level_1_item.IsolationPurity,
                            *level_1_item.Area,
                            level_1_item.PeakRatingMax,
                            *level_1_item.PeakRating,
                            mz_cloud_item.MolStructure,
                            mz_cloud_item.Name,
                            mz_cloud_item.Formula,
                            mz_cloud_item.Mass,
                            mz_cloud_item.MaxMatchFactor,
                            mz_cloud_item.MzCloudId,
                            mz_cloud_item.IUPAC,
                            mz_cloud_item.KeggId,
                            mz_cloud_item.CASNumber,
                            mz_cloud_item.SMILES,
                            mz_cloud_item.InChI,
                            mz_cloud_item.InChIKey,
                            mz_cloud_item.HMDB,
                            mz_cloud_item.PubChemId,
                            mz_cloud_item.CompoundClassNames,
                            mz_cloud_item.DeltaMassInDa,
                            mz_cloud_item.DeltaMassInPPM,
                            mz_cloud_item.MzLibraryMatchFactor,
                            mz_cloud_item.Confidence,
                            mz_cloud_item.CompoundMatchStatus,
                        ]
                    )

    level_1_headers = [
        "L1 ID",
        "L1 Name",
        "L1 Formula",
        "L1 Annot. Source: Predicted Compositions",
        "L1 Annot. Source: mzCloud Search",
        "L1 Annot. Source: mzVault Search",
        "L1 Annot. DeltaMass [ppm]",
        "L1 Calc. MW",
        "L1 m/z",
        "L1 Reference Ion",
        "L1 RT [min]",
        "L1 Area (Max.)",
        "L1 mzCloud Results",
        "L1 # mzVault Results",
        "L1 mzCloud Best Match",
        "L1 mzCloud Best Match Confidence",
        "L1 mzVault Best Match",
        "L1 mzVault Library Match: Bamba lab 34 lipid mediators library stepped NCE 10 30 45",
        "L1 mzVault Library Match: Bamba lab 598 polar metabolites stepped NCE 10 30 45",
        "L1 Polarity",
        "L1 MS2",
        "L1 MS2 Purity [%]",
        *[f"L1 Area {input_file_name}" for input_file_name in input_files_names],
        "L1 Peak Rating (Max.)",
        *[f"L1 Peak Rating {input_file_name}" for input_file_name in input_files_names],
    ]

    main_df = pd.DataFrame(data=main_rows, columns=level_1_headers + level_2_headers + level_3_headers)
    main_df.to_excel(os.path.join(output_file_directory, f"{output_file_name}_flattened.xlsx"), index=False)
    print(f"Output generated: {os.path.join(output_file_directory, output_file_name)}_flattened.xlsx")

    comp_df = pd.DataFrame(data=comp_rows, columns=level_1_headers + mzcloud_headers)
    comp_df.to_excel(os.path.join(output_file_directory, f"{output_file_name}_flattened_comp.xlsx"), index=False)
    print(f"Output generated: {os.path.join(output_file_directory, output_file_name)}_flattened_comp.xlsx")

    return None


if __name__ == "__main__":

    try:
        if sys.argv[1] == "all":
            batches = [
                os.path.basename(species_dir) + "_" + batch_dir.rsplit("_", 1)[1]
                for species_dir in os.scandir(path_to_project)
                if os.path.basename(species_dir).startswith("00")
                for batch_dir in os.listdir(species_dir)
                if batch_dir.startswith(os.path.basename(species_dir).split("_")[1])
            ]
        else:
            batches = [sys.argv[1]]

        if sys.argv[2] == "all":
            assays = ["HILIC_POS_5ppm", "LIPIDS_POS_5ppm"]
        else:
            assays = [sys.argv[2]]

        for batch in batches:
            species_directory = batch.rsplit("_", 1)[0]
            batch_directory = batch.split("_", 1)[1]
            cd_directory = os.path.join(
                path_to_project, species_directory, batch_directory, "results", "annotations", "CD_33"
            )
            for assay in assays:
                cd_result_file = os.path.join(
                    cd_directory,
                    batch_directory,
                    f"{assay}.cdResult",
                )
                try:
                    extract_data(cd_directory, cd_result_file, assay)
                except KeyError:
                    print(
                        f"{cd_result_file} is not analysed because it was generated from a different version of Compound Discoverer."
                    )

    except IndexError:  # No command line arguments
        print(
            "Batch and assay not specified. Extracting data from the first .cdResult file in the current directory instead."
        )
        current_directory = os.getcwd()
        cd_result_file = [filename for filename in os.listdir(current_directory) if filename.endswith(".cdResult")][0]
        assay = os.path.splitext(os.path.basename(cd_result_file))[0]
        extract_data(current_directory, cd_result_file, assay)
