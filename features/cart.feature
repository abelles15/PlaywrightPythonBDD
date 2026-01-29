Feature: Carrito

Scenario: Agregar producto al carrito
  Given el usuario ha iniciado sesión correctamente
  When agrega un producto al carrito
  Then el carrito debe tener 1 producto
