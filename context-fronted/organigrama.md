//////////////////////////////////////////////////
// MÓDULO COMERCIAL: PROSPECTOS Y CLIENTES
//////////////////////////////////////////////////

Table prospecto {
id bigserial [pk]
nombre varchar(255)
tipo varchar(50) // persona, empresa
telefono varchar(50)
email varchar(255)
direccion text
ubicacion text
estado varchar(50) // nuevo, en_evaluacion, aprobado, denegado
factibilidad_tecnica varchar(50) // aprobada, rechazada, pendiente
factibilidad_comercial varchar(50) // aprobada, rechazada, pendiente
notas text
created_at timestamp
updated_at timestamp
}

Table cliente {
id bigserial [pk]
prospecto_id bigint [ref: > prospecto.id] // puede ser null si no viene de prospecto
nombre varchar(255)
tipo varchar(50) // natural, juridico
rif_ci varchar(50)
telefono varchar(50)
email varchar(255)
direccion text
datos_fiscales text
created_at timestamp
updated_at timestamp
}

//////////////////////////////////////////////////
// MÓDULO SERVICIOS: PLANES Y PAQUETES
//////////////////////////////////////////////////

Table plan {
id bigserial [pk]
nombre varchar(255)
descripcion text
precio_base numeric(12,2)
tipo varchar(50) // residencial, corporativo, etc.
velocidad_down_mbps int
velocidad_up_mbps int
es_activo boolean
created_at timestamp
updated_at timestamp
}

Table paquete_mega {
id bigserial [pk]
plan_id bigint [ref: > plan.id]
nombre varchar(255)
megas_extra int // megas adicionales
costo_extra numeric(12,2)
es_activo boolean
created_at timestamp
updated_at timestamp
}

//////////////////////////////////////////////////
// MÓDULO EQUIPOS / SMARTOLT
//////////////////////////////////////////////////

Table equipo {
id bigserial [pk]
serial varchar(255)
modelo varchar(255)
tipo varchar(100) // ONU, router, etc.
mac_address varchar(50)
olt_id varchar(100) // id en SmartOLT
puerto_olt varchar(50) // slot/pon/onu
estado varchar(50) // disponible, asignado, en_reparacion, de_baja
created_at timestamp
updated_at timestamp
}

Table equipo_historial {
id bigserial [pk]
equipo_id bigint [ref: > equipo.id]
contrato_id bigint [ref: > contrato.id] // se define más abajo
accion varchar(50) // asignado, desasignado, reemplazado
detalle text
created_at timestamp
}

//////////////////////////////////////////////////
// MÓDULO CONTRATOS
//////////////////////////////////////////////////

Table contrato {
id bigserial [pk]
cliente_id bigint [ref: > cliente.id]
plan_id bigint [ref: > plan.id]
equipo_id bigint [ref: > equipo.id, null] // puede no tener equipo al inicio

codigo_contrato varchar(100) // código interno visible al cliente
tipo_facturacion varchar(50) // prepago, pospago
estado varchar(50) // por_instalar, activo, cortado, exonerado

fecha_creacion date
fecha_instalacion date
dia_facturacion smallint // día del mes para facturación si aplica
saldo_actual numeric(12,2) // cache del saldo según ledger

direccion_servicio text
notas text

created_at timestamp
updated_at timestamp
}

Table historial_estado_contrato {
id bigserial [pk]
contrato_id bigint [ref: > contrato.id]
estado_anterior varchar(50)
estado_nuevo varchar(50)
motivo text
origen varchar(50) // manual, sistema, automatizacion
usuario_ref varchar(100) // opcional: usuario que hizo el cambio
created_at timestamp
}

Table prorroga {
id bigserial [pk]
contrato_id bigint [ref: > contrato.id]
fecha_inicio date
fecha_fin date
dias_extender int
motivo text
estado varchar(50) // activa, vencida, cancelada
created_at timestamp
}

//////////////////////////////////////////////////
// MÓDULO FACTURACIÓN
//////////////////////////////////////////////////

Table ciclo_facturacion {
id bigserial [pk]
nombre varchar(255) // ciclo general, empresarial, etc.
tipo varchar(50) // mensual, semanal, etc. (principalmente mensual)
dia_generacion smallint // día del mes para generar facturas
hora_generacion time // hora aproximada del proceso
es_activo boolean
created_at timestamp
updated_at timestamp
}

Table factura {
id bigserial [pk]
contrato_id bigint [ref: > contrato.id]
ciclo_facturacion_id bigint [ref: > ciclo_facturacion.id, null]

numero varchar(100) [unique] // número de factura
fecha_emision date
fecha_vencimiento date

total_bruto numeric(12,2)
total_descuento numeric(12,2)
total_neto numeric(12,2)

estado varchar(50) // pendiente, pagada, vencida, anulada
tipo varchar(50) // mensual, prorrateo, ajuste, material

notas text
created_at timestamp
updated_at timestamp
}

Table detalle_factura {
id bigserial [pk]
factura_id bigint [ref: > factura.id]

tipo_item varchar(50) // PLAN, PAQUETE, MATERIAL, AJUSTE, OTRO
descripcion text
cantidad numeric(10,2)
precio_unitario numeric(12,2)
subtotal numeric(12,2)

created_at timestamp
}

//////////////////////////////////////////////////
// MÓDULO PAGOS
//////////////////////////////////////////////////

Table pago {
id bigserial [pk]
contrato_id bigint [ref: > contrato.id]
factura_id bigint [ref: > factura.id, null] // puede ser pago a cuenta

metodo_pago varchar(50) // EFECTIVO, TRANSFERENCIA, TDC, ZELLE, etc.
referencia_pago varchar(255)
monto numeric(12,2)
fecha_pago timestamp

observacion text
created_at timestamp
}

//////////////////////////////////////////////////
// MÓDULO LEDGER: MOVIMIENTOS DE SALDO
//////////////////////////////////////////////////

Table movimiento_saldo {
id bigserial [pk]
contrato_id bigint [ref: > contrato.id]

factura_id bigint [ref: > factura.id, null]
pago_id bigint [ref: > pago.id, null]

tipo varchar(50) // FACTURA, PAGO, ABONO, DESCUENTO, AJUSTE, DEUDA_MATERIAL
operador varchar(1) // "+", "-"
monto numeric(12,2) // siempre positivo
saldo_final numeric(12,2) // saldo del contrato tras este movimiento

referencia_id bigint // id genérico extra (equipo, orden, etc.)
referencia_tipo varchar(50) // FACTURA, PAGO, EQUIPO, MATERIAL, OTRO

descripcion text
created_at timestamp
}

//////////////////////////////////////////////////
// MÓDULO AUTOMATIZACIONES / OLT
//////////////////////////////////////////////////

Table log_olt {
id bigserial [pk]
contrato_id bigint [ref: > contrato.id]
equipo_id bigint [ref: > equipo.id, null]

accion varchar(50) // CORTE, RECONEXION, CONFIGURACION
resultado varchar(50) // OK, ERROR
mensaje text

payload_request json // opcional: request enviado a SmartOLT
payload_response json // opcional: respuesta de SmartOLT

created_at timestamp
}

Table log_automatizacion {
id bigserial [pk]
contrato_id bigint [ref: > contrato.id, null]

tipo_proceso varchar(100) // CORTE_AUTOMATICO, RECONEXION_AUTOMATICA, GENERACION_FACTURA, AVISO_PAGO
estado varchar(50) // EJECUTADO, ERROR, PENDIENTE
detalle text

created_at timestamp
}

Ref: "log_automatizacion"."id" < "log_automatizacion"."estado"

Ref: "log_automatizacion"."id" < "log_automatizacion"."detalle"

Ref: "factura"."id" < "factura"."total_bruto"
