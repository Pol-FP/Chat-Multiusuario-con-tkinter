# 🔐 Chat TCP Multicliente con Python

Aplicación de **chat cliente-servidor desarrollada en Python**, utilizando sockets TCP para la comunicación entre usuarios, `threading` para gestionar múltiples clientes simultáneamente y **SSL/TLS** para cifrar las comunicaciones.

El proyecto está dividido en dos partes principales:

* 🖥️ **Servidor:** gestiona las conexiones, usuarios y distribución de mensajes.
* 💬 **Cliente:** proporciona una interfaz gráfica mediante Tkinter para interactuar con el chat.

---

## 📌 Características

* Comunicación mediante **sockets TCP**.
* Arquitectura **cliente-servidor**.
* Soporte para múltiples clientes simultáneos.
* Gestión de clientes mediante **hilos (`threading`)**.
* Identificación de usuarios mediante nombre de usuario.
* Envío y recepción de mensajes en tiempo real.
* Interfaz gráfica desarrollada con **Tkinter**.
* Visualización de usuarios conectados.
* Sistema para abandonar el chat.
* Comunicación cifrada mediante **SSL/TLS**.
* Uso de certificados para establecer conexiones seguras.

---

## 🏗️ Estructura del proyecto

```text
chat-python/
│
├── client.py
├── server.py
├── server-cert.pem
├── server-key.key
└── README.md
```

### `client.py`

Se encarga de la parte del cliente. Sus principales funciones son:

* Establecer una conexión TCP con el servidor.
* Crear una conexión SSL/TLS.
* Solicitar el nombre de usuario.
* Crear la interfaz gráfica.
* Enviar mensajes.
* Recibir mensajes mediante un hilo independiente.
* Solicitar el listado de usuarios conectados.
* Cerrar correctamente la conexión.

### `server.py`

Se encarga de gestionar el servidor:

* Escuchar conexiones entrantes.
* Establecer conexiones SSL/TLS.
* Gestionar múltiples clientes simultáneamente.
* Registrar los nombres de usuario.
* Distribuir los mensajes entre los clientes.
* Mostrar los usuarios conectados.
* Gestionar las desconexiones.

---

## ⚙️ Tecnologías utilizadas

| Tecnología     | Uso                           |
| -------------- | ----------------------------- |
| 🐍 Python      | Lenguaje principal            |
| 🔌 `socket`    | Comunicación TCP              |
| 🧵 `threading` | Gestión de múltiples clientes |
| 🖼️ `tkinter`  | Interfaz gráfica              |
| 🔐 `ssl`       | Cifrado TLS/SSL               |

Todas las librerías utilizadas forman parte de la **biblioteca estándar de Python**, por lo que no es necesario instalar paquetes externos.

---

## 🔄 Funcionamiento

La aplicación utiliza una arquitectura cliente-servidor.

```text
                    ┌─────────────────┐
                    │     SERVIDOR    │
                    │                 │
                    │   TCP + SSL     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              │              │              │
        ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
        │  CLIENTE  │  │  CLIENTE  │  │  CLIENTE  │
        │     1     │  │     2     │  │     3     │
        └───────────┘  └───────────┘  └───────────┘
```

Cuando un cliente se conecta:

1. Se establece una conexión TCP con el servidor.
2. La conexión se protege mediante **SSL/TLS**.
3. El cliente introduce su nombre de usuario.
4. El servidor registra al usuario.
5. Se crea un hilo independiente para gestionar al cliente.
6. Los mensajes enviados se distribuyen al resto de clientes conectados.

---

## 🧵 Gestión de múltiples clientes

El servidor utiliza `threading` para poder gestionar diferentes clientes simultáneamente.

Cada vez que se conecta un nuevo cliente, se crea un hilo independiente:

```python
thread = threading.Thread(
    target=client_thread,
    args=(client_socket, clients, usernames, address)
)

thread.daemon = True
thread.start()
```

De esta manera, el servidor puede continuar aceptando nuevas conexiones mientras gestiona las comunicaciones de los clientes existentes.

---

## 🔐 Cifrado mediante SSL/TLS

Una de las características principales del proyecto es la incorporación de **SSL/TLS** para proteger las comunicaciones.

El servidor utiliza un certificado y una clave privada:

```python
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

context.load_cert_chain(
    certfile="server-cert.pem",
    keyfile="server-key.key"
)
```

Posteriormente, el socket del servidor se envuelve utilizando el contexto SSL:

```python
server_socket = context.wrap_socket(
    server_socket,
    server_side=True
)
```

El cliente también establece una conexión utilizando SSL:

```python
client_socket = ssl._create_unverified_context().wrap_socket(
    client_socket,
    server_hostname="localhost"
)
```

Esto permite que los datos enviados entre cliente y servidor viajen **cifrados**.

> ⚠️ **Nota:** el cliente utiliza un contexto que no verifica el certificado del servidor. Esta configuración es apropiada para realizar pruebas en un entorno local, pero no debería utilizarse tal cual en un entorno de producción.

---

## 💬 Funcionalidades del cliente

La interfaz gráfica permite:

### Enviar mensajes

El usuario puede escribir un mensaje y enviarlo mediante el botón **Enviar** o pulsando `Enter`.

Los mensajes se envían con el siguiente formato:

```text
usuario > mensaje
```

### Listar usuarios

El botón **Listar Usuarios** envía al servidor el comando:

```text
/usuarios
```

El servidor responde mostrando los usuarios conectados actualmente.

### Salir

El botón **Salir** informa al resto de usuarios de que el cliente ha abandonado el chat y cierra la conexión.

---

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/USUARIO/REPOSITORIO.git
cd REPOSITORIO
```

### 2. Comprobar la versión de Python

Se recomienda utilizar **Python 3.10 o superior**.

```bash
python --version
```

### 3. Generar o proporcionar los certificados

El servidor necesita los siguientes archivos:

```text
server-cert.pem
server-key.key
```

Estos archivos deben encontrarse en el mismo directorio que `server.py`.

Para un entorno de pruebas local pueden generarse certificados autofirmados mediante OpenSSL.

### 4. Iniciar el servidor

En una terminal:

```bash
python server.py
```

Debería aparecer un mensaje similar a:

```text
[+] El servidor está en escucha de conexiones entrantes...
```

### 5. Iniciar los clientes

En una o varias terminales diferentes:

```bash
python client.py
```

Cada cliente podrá introducir un nombre de usuario y acceder al chat.

---

## 🧪 Ejemplo de funcionamiento

Una vez conectados varios clientes, el servidor puede mostrar:

```text
[+] Se ha conectado un nuevo cliente: ('127.0.0.1', 54321)

[+] Estamos en client_thread

[+] El usuario Pol se ha conectado al chat
```

Mientras que los clientes pueden recibir mensajes como:

```text
[+] El usuario Alex ha entrado al chat

Pol > Hola!

Alex > Buenas!
```

Al solicitar los usuarios:

```text
[+] Listado de usuarios disponibles: Pol, Alex
```

---

## 📚 Objetivos del proyecto

Este proyecto ha sido desarrollado con el objetivo de poner en práctica diferentes conceptos de **programación en Python y redes**, entre ellos:

* Programación con sockets.
* Modelo cliente-servidor.
* Protocolo TCP.
* Comunicación entre procesos mediante red.
* Programación concurrente con `threading`.
* Interfaces gráficas con Tkinter.
* Comunicación cifrada mediante SSL/TLS.
* Gestión de conexiones y desconexiones.
* Manejo de excepciones.
* Gestión de múltiples usuarios.

---

## 🔮 Posibles mejoras

Algunas mejoras que podrían implementarse en futuras versiones:

* [ ] Verificación real de certificados en el cliente.
* [ ] Sistema de autenticación con contraseña.
* [ ] Persistencia de usuarios.
* [ ] Historial de mensajes.
* [ ] Mensajes privados entre usuarios.
* [ ] Creación de diferentes salas de chat.
* [ ] Indicador de usuarios conectados.
* [ ] Mejor gestión de errores y desconexiones.
* [ ] Configuración del servidor mediante archivo `.json` o `.env`.
* [ ] Registro de eventos mediante `logging`.
* [ ] Mejora de la interfaz gráfica.
* [ ] Envío de archivos.
* [ ] Implementación de una arquitectura más escalable.

---

## ⚠️ Consideraciones de seguridad

Este proyecto está planteado principalmente como **proyecto educativo y de práctica**.

Aunque utiliza SSL/TLS para cifrar las comunicaciones, existen aspectos que deberían mejorarse antes de utilizarlo en un entorno real, especialmente:

* Validación del certificado en el cliente.
* Autenticación de usuarios.
* Gestión segura de credenciales.
* Validación y sanitización de mensajes.
* Gestión robusta de errores.
* Control de conexiones maliciosas.
* Protección frente a ataques de denegación de servicio.
* Gestión segura de certificados y claves privadas.

Por tanto, **no se recomienda utilizar esta implementación directamente como servicio de producción** sin realizar previamente una revisión de seguridad.

---

## 👨‍💻 Autor

**Pol Castaño Meneses**

Proyecto desarrollado como práctica de **Python, programación de redes, sockets, concurrencia y comunicaciones seguras mediante SSL/TLS**.
