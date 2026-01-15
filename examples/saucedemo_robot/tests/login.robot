*** Settings ***
Library    ../keywords/SauceKeywords.py

*** Variables ***
${USERNAME}    standard_user
${PASSWORD}    secret_sauce

*** Test Cases ***
Successful Login
    Open Browser
    Login    ${USERNAME}    ${PASSWORD}
    Page Should Contain Text    Products
    [Teardown]    Close Browser
