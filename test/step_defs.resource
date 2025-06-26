*** Settings ***
Library           robotnl
Resource          domain_lib/Parking.resource

*** Keywords ***
it is safe to park
    [Documentation]  *model info*
    ...    nothing?
    Send safe

the car parks
    [Documentation]  *model info*
    ...    nothing?
    ${value} = receive
    Should Be Equal  ${value}  park
