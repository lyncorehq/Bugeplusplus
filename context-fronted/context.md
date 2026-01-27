En este documento se va describir todo el contexto del proyecto (BLS) sin embargo quiero aclarar un par de cosas antes de comenzar.

1. Yo solamente voy a desarrollar el fronted de la aplicación, el backend lo va a hacer un compañero de equipo.
2. Las tecnologías que se van a usar son las siguientes:
    -React
    -Django
3. Soy novato con el tema de desarrollo a estas escalas, necesitaré ayuda de tu parte para realizar todo el tema del diagrama y demás. Se creará otro MD donde va estar el diagrama de la aplicación y demás, el cual me ayudaras a desarrollar.




# 1.1. Business Logic Specification (BLS) – ERP ISP (Módulo de Facturación)
## **1. Introducción**

El presente documento detalla la **especificación de lógica de negocio (BLS)** para el desarrollo de un ERP orientado a empresas ISP en un entorno B2B. El módulo de facturación constituye el núcleo funcional del sistema y se interrelaciona con entidades críticas como clientes, prospectos, contratos, planes, equipos y procesos operativos.


Este documento establece terminologías, entidades, reglas del negocio, flujos de operación y comportamientos esperados del sistema, sirviendo como una guía formal para el desarrollo en **Laravel + PostgreSQL (backend)** y **React (frontend)**.

  

---

  

# **2. Objetivo General del Sistema**

Crear un sistema ERP para ISPs que gestione:

- Ciclo de vida del cliente

- Creación y administración de contratos

- Facturación diaria / mensual (según el modelo definido)

- Control de estados de servicio (activo, cortado, por instalar, exonerado)

- Gestión de equipos vinculados a SmartOLT

- Movimientos de saldo y cobranza

  

---

  

# **3. Definiciones del Negocio**

### **3.1 Prospecto**

Persona o empresa evaluada para contratación del servicio. Se usa para validar factibilidad técnica y comercial antes de formalizar un contrato.

### **3.2 Cliente**

Entidad aprobada y registrada con uno o múltiples contratos activos o históricos.

### **3.3 Contrato**

Representa la relación comercial y técnica entre el cliente y el ISP. Es la **unidad principal de facturación**. Controla:

- Plan asignado

- Estado actual

- Fecha de facturación

- Saldo

- Equipo vinculado

- Tipo de facturación

- Prórrogas

### **3.4 Estados del Contrato**

- **Por Instalar**: aún no genera facturación.

- **Activo**: genera facturación diaria o mensual.

- **Cortado**: se suspende facturación y se corta el servicio.

- **Exonerado**: no genera facturación pero mantiene servicio.

- **Suspendido**: Cliente se retiro del servicio, no genera facturación y no disfruta del servicio.

### **3.5 Prórroga (Extension Shield)**

Extensión temporal de la fecha límite de pago. No cambia el estado principal del contrato.

### **3.6 Planes**

Servicio adquirido (nombre + precio base + condiciones).

### **3.7 Paquetes de Megas**

Extensiones del plan base. Relación dependiente de Planes.

### **3.8 Equipo (SmartOLT)**

Equipo asignado al cliente vía SN. Permite cortes y reconexiones automatizadas.

### **3.9 Movimientos de Saldo (Ledger)**

Cualquier operación que afecte el saldo del contrato:

- Facturas generadas (+)

- Pagos (-)

- Abonos (-)

- Deudas por materiales (+)

- Descuentos (-)

- Ajustes manuales

---

# **4. Modelo General del Sistema**

El flujo general del ciclo de vida del cliente es:

**Prospecto → Cliente → Contrato → Facturación → Estados → Cortes / Reconexiones → Historial**


---

# **5. Entidades Principales (Business Entities)**

## **5.1 Prospecto**

### **Atributos clave**
- Datos de contacto
- Ubicación
- Factibilidad técnica
- Estado (nuevo, en evaluación, aprobado, denegado)
### **Reglas**

- Un prospecto solo puede convertirse en cliente si la factibilidad es aprobada.

- No puede generar contratos sin ser cliente.

  

---
## **5.2 Cliente**
### **Atributos clave**
- Información personal o empresarial
- Datos fiscales
### **Reglas**

- Puede tener múltiples contratos.
- No tiene interacción directa con facturación; la facturación ocurre sobre contratos.


---

  

## **5.3 Contrato (Entidad principal)**

### **Atributos fundamentales**
- Cliente asociado
- Plan asignado
- Tipo de facturación (prepago/pospago)
- Estado
- Equipo asignado
- Fecha de instalación o ingreso.
- Saldo actual
### **Reglas generales**

- Solo contratos Activos pueden generar facturación.
- Solo contratos Activos o Cortados pueden recibir pagos.
- Un contrato "Por Instalar" no debe generar facturas.
- Un contrato "Exonerado" mantiene servicio sin generar facturas.

  

---
## **5.4 Estados del Contrato**
### **Transiciones válidas**

```

Por Instalar → Activo

Activo → Cortado

Cortado → Activo

Activo → Exonerado

Exonerado → Activo

```
### **Reacciones sistémicas**
- Al cambiar a *Cortado*: ejecutar corte vía SmartOLT.
- Al cambiar a *Activo*: ejecutar reconexión.

---

## **5.5 Prórroga**

### **Reglas**

- Solo se aplica si el contrato está Activo.
- Extiende la fecha límite de pago N días.
- Durante prórroga no se ejecutan cortes.
- Si el día de la prórroga no ha cancelado, cortar automáticamente.

---
## **5.6 Planes**
### **Atributos**
- Nombre del plan
- Precio base
- Relación con paquetes de megas
### **Reglas**

- Cambiar de plan puede generar facturación prorrateada.

---
## **5.7 Paquetes de Megas**
### **Reglas**
- Estará asignado a un plan. 

---
## **5.8 Equipo**

### **Reglas**
- Debe estar correctamente registrado en SmartOLT.
- Puede cambiarse.
- Debe quedar historial de cambios.
---
## **5.9 Movimientos de Saldo (Ledger)**
Escritura contable del contrato.
### **Tipos de movimientos**
- ABONO
- PAGO
- DESCUENTO
- AJUSTE
- DEUDA DE EQUIPO
### **Reglas**
- Todo movimiento debe ser trazable.
- El saldo final es la suma de movimientos.

---
# **6. Reglas de Facturación**

### **6.1 Tipos de facturación**

**Prepago**
- Se factura antes de consumo.
- Si no paga, no se activa el servicio.

**Pospago**

- Se factura por consumo del mes anterior.
- Si paga parcial: debe facturarse prorrateo del nuevo mes.

### **6.2 Prorrateos**

- Si un cliente entra a mitad de mes, se factura proporcional.
- Si cambia de plan, se ajusta proporcional al consumo.
- 
### **6.3 Ciclo de facturación**

- Generación automática 1er día del mes.
- Si no paga → Estado Cortado.
- Si paga → Estado Activo.