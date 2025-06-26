*** Settings ***
Resource  step_defs.resource
Suite Setup  Start Parking system at port ${parkingport}
Suite Teardown  Stop the parking system

*** Variables ***
${parkingport}  3001

*** Test Cases ***
do some parking
    Given it is safe to park
    Then the car parks
