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

  Scenario Outline: Order products by price low to high
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then order the products by price low to high

    Examples:
      | username                | password       |
      | standard_user           | secret_sauce   |
      | performance_glitch_user | secret_sauce   |

  Scenario Outline: Order products by price high to low
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then order the products by price high to low

    Examples:
      | username                | password       |
      | standard_user           | secret_sauce   |
      | performance_glitch_user | secret_sauce   |

  Scenario Outline: Order products by name A to Z
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then order the products by name A to Z

    Examples:
      | username                | password       |
      | standard_user           | secret_sauce   |
      | performance_glitch_user | secret_sauce   |

  Scenario Outline: Order products by name Z to A
    Given the user is on the login page
    When the user logs in with <username> and <password>
    Then order the products by name Z to A

    Examples:
      | username                | password       |
      | standard_user           | secret_sauce   |
      | performance_glitch_user | secret_sauce   |