*** Settings ***
Library         OperatingSystem

*** Test Cases ***
Test Module Installation
    [Documentation]    Test that required modules are installed properly
    [Tags]             module_installation
    ${requirements} =  Create List    numpy    pyheif    Pillow    helpers    matplotlib
    FOR    ${module}    IN    @{requirements}
        Run Keyword And Ignore Error    Import Library    ${module}
        ${result} =    Run Keyword And Return Status    Should Be True    ${True}
        ...    ${module} module was imported successfully.
        Run Keyword Unless    ${result}    Fail    Could not import ${module} module.
    END