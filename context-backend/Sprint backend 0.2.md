🚀 Sprint Backend 0.2 — Negocio Operativo
🎯 Objetivo del sprint

Pasar de backend técnico a backend de negocio.
Que el frontend ya pueda operar el ERP con reglas reales.

Sprint 0.1 = “existe el sistema”
Sprint 0.2 = “el sistema trabaja”

🧱 Alcance del Sprint 0.2 (lo que SÍ entra)
1️⃣ Roles & Permisos reales

Objetivo: que cada rol vea y haga lo que le toca.

Definir permisos por rol:

ADMIN: todo

MANAGER: gestión (sin settings críticos)

SELLER: ventas (clientes + contratos)

Permisos a nivel:

endpoint

queryset (por franquicia)

📌 Resultado:

Un SELLER no ve datos de otra franquicia

El frontend confía en el backend

2️⃣ Vendedores completos

Objetivo: que un vendedor sea usable en producción.

CRUD de vendedores

Activar / desactivar vendedor

Validar:

user → role = SELLER

user → franchise obligatoria

📌 Resultado:

Frontend puede gestionar su equipo comercial

3️⃣ Planes (versión negocio)

Objetivo: planes listos para contratos reales.

Campos mínimos:

nombre

precio

tipo (residencial / empresarial)

activo

Validaciones:

no se puede contratar plan inactivo

Filtrado por franquicia (si aplica)

📌 Resultado:

Planes listos para facturación

4️⃣ Clientes (ciclo real)

Objetivo: clientes operativos, no solo registros.

Estados:

PROSPECT

ACTIVE

INACTIVE

Búsqueda por:

nombre

documento

Asociados a franquicia

📌 Resultado:

Flujo comercial completo

5️⃣ Contratos – lógica de estado

Objetivo: contratos con reglas claras.

Estados:

PENDING

ACTIVE

SUSPENDED

CANCELLED

Endpoint dedicado:

PATCH /api/contracts/{id}/state


Validar transiciones permitidas

📌 Resultado:

El frontend no rompe reglas

Base para automatizaciones futuras

❌ Fuera de alcance (IMPORTANTE)

🚫 Facturación
🚫 Ledger
🚫 SmartOLT
🚫 Automatizaciones
🚫 Reportes

Eso es Sprint 0.3+