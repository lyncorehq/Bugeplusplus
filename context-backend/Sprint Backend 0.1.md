🚀 Sprint Backend 0.1 — Base Operativa
🎯 Objetivo

Que el frontend pueda trabajar sin bloqueos con:

Login

Franquicias

Vendedores

Planes

Clientes

Contratos (estado inicial)

🧱 Alcance (cerrado, sin creep)

✔ CRUD básicos
✔ JWT Auth
✔ Estados iniciales
❌ Facturación
❌ SmartOLT
❌ Automatizaciones

📦 Estructura de Apps (decisión clave)

Crea estas apps (ni más, ni menos):

apps/
├── core/          # auth, roles, franquicias
├── users/         # usuarios, vendedores
├── services/      # planes
├── customers/     # clientes
└── contracts/     # contratos + estados

🪜 Plan de trabajo (día a día)
🟦 Día 1 — Setup técnico

Checklist

 venv creado

 Django + DRF instalados

 Proyecto levantado

 PostgreSQL conectado

Comandos

python -m venv venv
source venv/bin/activate
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary python-dotenv
django-admin startproject erp_backend
cd erp_backend
python manage.py startapp core
python manage.py startapp users
python manage.py startapp services
python manage.py startapp customers
python manage.py startapp contracts
python manage.py runserver


Resultado: 🚀 servidor arriba.

🟦 Día 2 — Auth + Franquicias

Backend entrega

Login JWT

Endpoint /me

CRUD de franquicias

Endpoints

POST /api/auth/login/
GET  /api/auth/me/
GET  /api/franchises/
POST /api/franchises/


Notas:

Franquicia = tenant light

Todo usuario pertenece a una franquicia

🟦 Día 3 — Vendedores

Backend

CRUD vendedores

Relación: vendedor → franquicia

Rol: SELLER

Endpoints

GET  /api/sellers/
POST /api/sellers/

-- Me parece que habia llegado hasta aquí lo demas tendré que seguirlo con codex

--Falta continuar:
🟦 Día 4 — Planes

Backend

CRUD planes

Activo / inactivo

Endpoints

GET  /api/plans/
POST /api/plans/

🟦 Día 5 — Clientes

Backend

CRUD clientes

Asociados a franquicia

Endpoints

GET  /api/clients/
POST /api/clients/

🟦 Día 6 — Contratos

🔥 Clave del sprint

Backend

Crear contrato

Estado inicial: por_instalar

Relación cliente + plan

Endpoints

GET   /api/contracts/
POST  /api/contracts/
PATCH /api/contracts/{id}/state/

🟦 Día 7 — Pulido + contrato API

 Validaciones

 Respuestas consistentes

 API_CONTRACT.md

 Revisión con frontend

🔐 Roles mínimos (Sprint 0.1)
ADMIN      → todo
MANAGER    → gestión
SELLER     → clientes + contratos

🧠 Criterios de “Sprint aprobado”

✔ Frontend puede loguearse
✔ Puede crear franquicia
✔ Crear vendedor
✔ Crear plan
✔ Crear cliente
✔ Crear contrato

Si eso pasa → Sprint 0.1 DONE ✅

🚫 Prohibiciones del sprint

❌ “Ya que estamos, metamos facturación”
❌ “Probemos SmartOLT”
❌ “Hagamos microservicios”

Disciplina = velocidad.

