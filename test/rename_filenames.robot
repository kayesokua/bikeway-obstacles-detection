*** Settings ***
Documentation    This suite demonstrates the usage of the Rename Filenames keyword.
Library          OperatingSystem

*** Variables ***
${input_dir}     ./test/input
${TEMPDIR}       ${OUTPUTDIR}/temp

*** Keywords ***
Setup
    [Arguments]    ${input_directory}
    [Documentation]    Creates test files in the input directory.
    Create Directory    ${input_directory}/test_rename_filenames
    Create File     ${input_directory}/test_rename_filenames/1.png
    Create File     ${input_directory}/test_rename_filenames/2.png
    Create File     ${input_directory}/test_rename_filenames/3.heic
    Create File     ${input_directory}/test_rename_filenames/4.HEIC

*** Test Cases ***
Test rename_filenames Function
    Setup    ${input_dir}
    # Test that the function correctly renames all the files in the input directory.
    rename_filenames    ${TEMPDIR}/test_rename_filenames    1
    ${files}    List Directory    ${TEMPDIR}/test_rename_filenames
    Should Be Equal As Integers    ${files.__len__()}    4

    # Test that the function adds the start number to the beginning of each filename.
    ${new_files}    Remove String Prefix    ${files}    0
    FOR    ${file}    IN    @{new_files}
        ${start_number}    Evaluate    ${file.split('.')[0]}
        Should Be True    ${start_number} >= 1
        Should Be True    ${start_number} <= 4
    END

    # Test that the function adds a leading zero to the filename if the start number is less than 10000.
    rename_filenames    ${TEMPDIR}/test_rename_filenames    5
    ${files}    List Directory    ${TEMPDIR}/test_rename_filenames
    ${new_files}    Remove String Prefix    ${files}    0
    FOR    ${file}    IN    @{new_files}
        ${start_number}    Evaluate    ${file.split('.')[0]}
        ${filename_length}    Evaluate    len(${file.split('.')[0]})
        Run Keyword If    ${start_number} < 10000    Should Be Equal As Strings    ${filename_length}    9
    END

    # Test that the function does not rename files that already have a filename with the same name in the directory.
    rename_filenames    ${TEMPDIR}/test_rename_filenames    1
    rename_filenames    ${TEMPDIR}/test_rename_filenames    1
    ${files}    List Directory    ${TEMPDIR}/test_rename_filenames
    Should Be Equal As Integers    ${files.__len__()}    4