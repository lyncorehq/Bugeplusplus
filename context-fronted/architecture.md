# Arquitectura Frontend - ProyectoM (Versión Definitiva)

Has seleccionado la **Arquitectura por Tipo (Clásica)**. Esta estructura organiza los archivos según su rol técnico en la aplicación (Componentes, Hooks, Páginas, etc.). Es intuitiva y muy común en proyectos de React.

---

## 1. Estructura de Directorios Detallada

Así es como organizaremos tu proyecto. Cada carpeta tiene un propósito único.

```text
src/
├── assets/                  # Archivos estáticos
│   ├── images/              # Logos, banners, ilustraciones
│   └── icons/               # Iconos SVG (si no usas una librería)
│
├── component/               # TODOS los bloques de construcción de la UI
│   ├── common/              # Componentes genéricos (Botones, Inputs, Modales, Cards)
│   ├── layout/              # Componentes de estructura (Navbar, Sidebar, Footer)
│   └── domain/              # Componentes específicos del negocio (Ej: TablaFacturas, InfoCliente)
│       ├── billing/         # Opcional: Subcarpetas si hay muchos componentes de facturación
│       └── clients/
│
├── context/                 # Estado Global de la aplicación (React Context)
│   ├── AuthContext.tsx      # Manejo de sesión de usuario
│   └── ThemeContext.tsx     # Modo claro/oscuro (si aplica)
│
├── hooks/                   # Lógica reutilizable (Custom Hooks)
│   ├── useAuth.ts           # Lógica de login/logout
│   ├── useFetch.ts          # Hook genérico para peticiones API
│   └── useForm.ts           # Manejo de formularios
│
├── pages/                   # Las Vistas/Páginas (Rutas de la URL)
│   ├── Login/               # Carpeta por página para incluir sus estilos o tests específicos
│   │   └── LoginPage.tsx
│   ├── Dashboard/
│   │   └── DashboardPage.tsx
│   ├── Clients/
│   │   ├── ClientListPage.tsx
│   │   └── ClientCreatePage.tsx
│   └── Billing/
│       └── InvoicesPage.tsx
│
├── services/                # Comunicación con el Backend (Django)
│   ├── api.ts               # Configuración de Axios (Base URL, Interceptors)
│   ├── authService.ts       # Endpoints de login, registro, token
│   ├── clientService.ts     # Endpoints CRUD de clientes
│   └── billingService.ts    # Endpoints de facturación
│
├── types/                   # Definiciones de TypeScript (Interfaces/Types)
│   ├── user.types.ts
│   ├── client.types.ts
│   └── invoice.types.ts
│
├── utils/                   # Funciones auxiliares puras (Helpers)
│   ├── formatDate.ts        # Formateo de fechas
│   ├── currency.ts          # Formateo de dinero
│   └── validations.ts       # Validaciones de regex (email, rut/dni)
│
├── App.tsx                  # Componente Raíz (Configuración de Rutas)
└── main.tsx                 # Punto de entrada (Mount del DOM)
```

---

## 2. Reglas de Oro para esta Arquitectura

Como esta arquitectura mezcla un poco las cosas, necesitamos disciplina para que no se desordene.

### Regla 1: Componentes "Tontos" vs "Inteligentes"
*   **En `components/common`**: Solo componentes "tontos" (Presentacionales). Reciben datos por `props` y muestran UI. No llaman a la API. (Ej: Un botón azul).
*   **En `pages/`**: Componentes "inteligentes". Son los encargados de llamar a los hooks, pedir datos a la API y pasárselos a los componentes hijos.

### Regla 2: Mantén `App.tsx` limpio
`App.tsx` solo debe contener la configuración de Rutas (React Router) y los Providers (Contextos). No escribas lógica de negocio ahí.

### Regla 3: No repitas lógica (DRY)
Si ves que estás escribiendo la misma función para calcular el IVA en dos páginas diferentes, **muévela a `utils/`**.
Si ves que estás escribiendo el mismo `useEffect` para traer datos en dos lugares, **crea un `hook`**.

---

## 3. Flujo de Trabajo Típico

Cuando te toque desarrollar una nueva funcionalidad (ej: *"Lista de Clientes"*), seguirás este orden:

1.  **Types**: Defines la interfaz `Client` en `types/client.types.ts`.
2.  **Service**: Creas la función `getClients()` en `services/clientService.ts` para llamar al backend.
3.  **Component**: Creas una `ClientTable.tsx` en `components/domain/clients/` que sepa cómo mostrar esa lista.
4.  **Page**: Creas `ClientListPage.tsx` en `pages/Clients/`. Esta página llama al servicio (o a un hook) y le pasa los datos a la `ClientTable`.
5.  **Route**: Agregas la ruta `/clientes` en `App.tsx` apuntando a esa página.

---

## 4. Tecnologías Base (Confirmación)
Para que esta arquitectura brille, sugiero este stack estándar:
*   **Vite**: Para crear el proyecto (Rápido y moderno).
*   **React Router Dom**: Para la navegación entre páginas.
*   **Axios**: Para las peticiones HTTP (más fácil que fetch para manejar errores).
*   **TailwindCSS**: Para los estilos (opcional, pero recomendado para avanzar rápido).
*   **React Hook Form + Zod**: Para manejar los formularios complejos del ERP.

¿Listo para crear el proyecto base con los comandos iniciales?
