Feature: Login

  Scenario Outline: Login successfully
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then access the system

    Examples:
      | username                | password       |
      | standard_user           | secret_sauce   |
      | problem_user            | secret_sauce   |
      | performance_glitch_user | secret_sauce   |
      | error_user              | secret_sauce   |
      | visual_user             | secret_sauce   |

  Scenario Outline: Login invalid
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then an error message <message> is shown
    And tap on Error button of error message

    Examples:
      | username        | password       | message |
      | locked_out_user | secret_sauce   | Epic sadface: Sorry, this user has been locked out. |
      | invalid_user    | invalid_pass   | Epic sadface: Username and password do not match any user in this service |

  Scenario Outline: Logout
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then logout the system

    Examples:
      | username                | password       |
      | standard_user           | secret_sauce   |
      | problem_user            | secret_sauce   |
      | performance_glitch_user | secret_sauce   |
      | error_user              | secret_sauce   |
      | visual_user             | secret_sauce   |