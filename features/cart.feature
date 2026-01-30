Feature: Carrito

Scenario: Agregar producto al carrito
  Given the user is on the login page
  When agrega un producto al carrito
  Then el carrito debe tener 1 producto
