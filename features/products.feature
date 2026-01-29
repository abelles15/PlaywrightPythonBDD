Feature: Products

  Scenario Outline: View products after logging in
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then should be able to see the products list

    Examples:
      | username                | password       |
      | standard_user           | secret_sauce   |
      | problem_user            | secret_sauce   |
      | performance_glitch_user | secret_sauce   |
      | error_user              | secret_sauce   |
      | visual_user             | secret_sauce   |