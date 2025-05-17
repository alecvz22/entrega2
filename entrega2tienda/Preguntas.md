¿Qué ventajas ofrece GraphQL sobre REST en este contexto?
Tiene la ventaja de que solo te da los datos que le pides ya que hay veces de que REST te da mas cosas de las que pediste o no te da todo en uno y necesitas hacer mas llamadas.

¿Cómo se definen los tipos y resolvers en una API con GraphQL?
Los tipos se definen con el nombre, precio, stock, etc y los resolvers son el como cambiar esos datos o que hacer con ellos.

¿Por qué es importante que el backend también actualice disponible y no depender solo del frontend?
Porque si solo dependiera del frontend nunca se actualizarian los datos del backend por lo tanto no se guardarian estos datos cada que se le diera refresh a la pagina 

¿Cómo garantizas que la lógica de actualización de stock y disponibilidad sea coherente?
Lo garantizo con mi backend ya que eso me garantiza no tener errores ya que esto mantiene los datos guardados ya que si llega a 0 el stock se valide que sea verdad con el backend.
