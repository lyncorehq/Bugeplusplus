# Sprint 1

El siguiente sprint se encargara de implementar la funcionalidad de los clientes - contratos, esto debera de ser un modulo o funcionalidad que se pueda integrar con el backend y el frontend, y a su vez un agente autorizado por alguna flag en el backend para realizar estas funciones.

Se necesitara un una sección unica para estas funciones.

0. Creación de Franquicia.

1. Crear un cliente
   -La creación del cliente va tener los siguientes campos:
   -Nombre / Razón Social
   -Documento de Identidad
   -Email
   -Telefono
   -Dirección
   -Tipo de Cliente
   -Fecha de Creación
   -Estado (Si es un prospecto o cliente)
   -En el momento de existir el cliente debera de contar la cantidad de contratos que le pertenece. Ya que un cliente puede tener varios contratos.
   -Agente (Quien lo creo)
   -Persona que contacto a la persona para ser cliente o prospecto.

2. Crear un contrato
   -La creación del contrato va tener los siguientes campos:
   -Cliente
   -Plan
   -Paquete de megas
   -Fecha de Instalación
   -Fecha de Creación
   -Estado (Si es un prospecto o cliente)
   -En el momento de existir el contrato debera de contar la cantidad de contratos que le pertenece. Ya que un contrato puede tener varios contratos.
   -Vendedor
   -Agente
   -Fecha de Instalación
   -Fecha de Creación

3. Inventario de contrato, cada contrato debera de tener un inventario de los equipos y materiales que se han usado en el contrato.
   -Equipo
   -Material

4. Estado de cuenta(Los contratos son indenpendientes, puede haber clientes que deban un contrato y otro no, pero se puede generar un estado de cuenta general en la interfaz de clientes para un agente pueda consultarlo. No más.)
   -Deuda
   -Abonos
   -Fecha de Creación
   -Fecha de Vencimiento
   -Fecha de Pago
   -Estado (Activo, cortado, suspendido, exonerado)
   -El estado de cuenta es independiente entra contratos.
