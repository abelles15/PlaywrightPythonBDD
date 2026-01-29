Feature: Checkout

  Scenario: Checkout exitoso
    Given el usuario ha iniciado sesión correctamente
    And tiene un producto en el carrito
    When completa el checkout
    Then debe ver el mensaje de confirmación