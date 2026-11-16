# FORM ANALYSIS

## Formulario

ED434A (sede electrónica de la Xunta de Galicia).

## Comportamiento observado

El formulario carga dinámicamente cada nivel territorial:

- **Provincia -> Concellos**:
  `GET /hovaes/LugarJson-buscarConcellos.action?filtroCodProvincia=15`
  (`15` = Coruña (A))

- **Localidad -> Lugares**:
  `GET /hovaes/LugarJson-buscarLugares.action?filtroCodLocalidade=3205401`
  (`3205401` = localidad de Ourense)

Estas llamadas **no se integran en el diseño**. Son internas del formulario, pueden cambiar. Se usan solo como evidencia.

## Vocabulario del formulario

| Nivel | Nombre en el formulario | Dígitos | Ejemplo |
|---|---|---|---|
| Provincia | provincia | 2 | 15 |
| Concello | concello | 5 | 32054 |
| Localidad | localidade | 7 | 3205401 |
| Lugar | lugar | 9 | 320540100 |

El formulario llama «localidade» al nivel de 7 dígitos. El proyecto adopta este término.

## Selectores documentados

Extraídos del HTML real del formulario (página `Homologacion-inicial.action`). Sirven para que la extensión Chrome pueda localizar cada campo e inyectar el valor. Se documentan `id` y `name`; cuando el campo es un radio o un select con opciones cerradas, se documentan también los `value`.

**Convención**: `id` es el identificador único en el DOM (recomendado para `document.getElementById`); `name` es el nombre que se envía al servidor. Cuando ambos difieren, se indica.

### Bloque: Datos de la persona solicitante

| Campo | `id` | `name` | Tipo | Required |
|---|---|---|---|---|
| Nombre | `nome` | `solicitude.nomeSolicitante` | text | ✅ |
| Primer apellido | `primeiroApelido` | `solicitude.apelido1Solicitante` | text | ✅ |
| Segundo apellido | `segundoApelido` | `solicitude.apelido2Solicitante` | text | — |
| Tipo DNI/NIE | (select sin `id`) | `solicitude.codTipoDoiSolicitante` | select | — |
| DNI/NIE | `doiSolicitante` | `solicitude.doiSolicitante` | text | ✅ |
| Fecha de nacimiento | `formularioHomologacion_solicitude_dataNacementoSolicitante` | `solicitude.dataNacementoSolicitante` | text (dd/mm/yyyy) | ✅ |
| Género (F) | `formularioHomologacion_solicitude_xeneroSolicitanteF` | `solicitude.xeneroSolicitante` | radio, `value="F"` | — |
| Género (M) | `formularioHomologacion_solicitude_xeneroSolicitanteM` | `solicitude.xeneroSolicitante` | radio, `value="M"` | — |

**Valores del select `solicitude.codTipoDoiSolicitante`**:

| `value` | Etiqueta |
|---|---|
| `1` | DNI |
| `2` | NIE |
| `3` | Pasaporte |
| `4` | Documento UE |

### Bloque: Dirección del solicitante (`enderezoSolicitante.*`)

| Campo | `id` | `name` | Tipo | Required |
|---|---|---|---|---|
| Tipo de vía | `enderezoSolicitanteTipoVia` | `enderezoSolicitante.tipoVia` | text | — |
| Nombre de la vía | `enderezoSolicitanteNomeVia` | `enderezoSolicitante.nomeVia` | text | ✅ |
| Número | `enderezoSolicitanteNumero` | `enderezoSolicitante.numero` | text | — |
| Bloque | `enderezoSolicitanteBloque` | `enderezoSolicitante.bloque` | text | — |
| Piso | `enderezoSolicitanteAndar` | `enderezoSolicitante.andar` | text | — |
| Puerta | `enderezoSolicitantePorta` | `enderezoSolicitante.porta` | text | — |
| País | `enderezoSolicitanteCodPais` | `enderezoSolicitante.codPais` | select | ✅ |
| CP | `enderezoSolicitanteCp` | `enderezoSolicitante.cp` | text | — |
| Provincia | `enderezoSolicitanteCodProvincia` | `enderezoSolicitante.codProvincia` | select | ✅ |
| Concello | `enderezoSolicitanteCodConcello` | `enderezoSolicitante.codConcello` | select (vacío inicialmente, carga por JS) | ✅ |
| Localidad | `enderezoSolicitanteCodLocalidade` | `enderezoSolicitante.localidade` | select (vacío inicialmente, carga por JS) | ✅ |
| Parroquia | `enderezoSolicitanteParroquia` | `enderezoSolicitante.parroquia` | text | — |
| Lugar | `enderezoSolicitanteCodLugar` | `enderezoSolicitante.lugar` | select (vacío inicialmente, carga por JS) | — |
| Teléfono | `telefono` | `enderezoSolicitante.telefono` | text | — |
| Teléfono móvil | `mobil` | `enderezoSolicitante.mobil` | text | — |
| Correo electrónico | `mail` | `enderezoSolicitante.mail` | text | — |

**Nota**: el `name` del select de localidad es `enderezoSolicitante.localidade` (sin `cod`), pero el `id` es `enderezoSolicitanteCodLocalidade`. La extensión debe precargar por `id`, no por `name`, para evitar ambigüedad.

**Valores del select `enderezoSolicitante.codProvincia`** (solo se listan los de Galicia; el formulario incluye las 52 provincias españolas):

| `value` | Etiqueta |
|---|---|
| `15` | Coruña (A) |
| `27` | Lugo |
| `32` | Ourense |
| `36` | Pontevedra |
| `99` | Non hai provincia |

**Valor del select `enderezoSolicitante.codPais`**: código de 3 dígitos (ISO 3166-1 numérico, p. ej. `724` = España). El formulario incluye ~200 países, con algunas entradas `(descatalogado)`.

### Bloque: Representante (`solicitude.*Representante`)

| Campo | `id` | `name` | Tipo | Required |
|---|---|---|---|---|
| Nombre / Razón social | `nomeRepresentante` | `solicitude.nomeRepresentante` | text | — |
| Primer apellido | `apelido1Representante` | `solicitude.apelido1Representante` | text | — |
| Segundo apellido | `apelido2Representante` | `solicitude.apelido2Solicitante` | text | — |
| Tipo de documento | `codTipoDoiRepresentante` | `solicitude.codTipoDoiRepresentante` | select | — |
| Número | `doiRepresentante` | `solicitude.doiRepresentante` | text | — |

**Valores del select `solicitude.codTipoDoiRepresentante`**:

| `value` | Etiqueta |
|---|---|
| `1` | DNI |
| `2` | NIE |
| `3` | Pasaporte |
| `4` | Documento UE |
| `5` | CIF |

**Nota**: si se selecciona `5` (CIF), el formulario borra y bloquea los apellidos del representante (`readonly`). Comportamiento implementado en `comprobarCIFRepresentante()`.

### Bloque: Notificación (`enderezoNotificacion.*`)

Réplica de la estructura de `enderezoSolicitante.*`, con los mismos campos y los mismos `id`/`name` pero con el prefijo `enderezoNotificacion`. Los campos territoriales son:

| Campo | `id` | `name` | Tipo |
|---|---|---|---|
| Provincia | `enderezoNotificacionCodProvincia` | `enderezoNotificacion.codProvincia` | select |
| Concello | `enderezoNotificacionCodConcello` | `enderezoNotificacion.codConcello` | select (carga por JS) |
| Localidad | `enderezoNotificacionCodLocalidade` | `enderezoNotificacion.localidade` | select (carga por JS) |
| Lugar | `enderezoNotificacionCodLugar` | `enderezoNotificacion.lugar` | select (carga por JS) |

Además, en este bloque:

| Campo | `id` | `name` | Tipo | `value` |
|---|---|---|---|---|
| Notificar a: solicitante | `persoaNotificar1` | `persoaNotificar` | radio | `1` |
| Notificar a: representante | `persoaNotificar2` | `persoaNotificar` | radio | `2` |
| Notificación electrónica | `tipoNotificacionElectronica1` | `enderezoNotificacion.tipoNotificacion` | radio | `1` (checked por defecto) |
| Notificación postal | `tipoNotificacionPostal2` | `enderezoNotificacion.tipoNotificacion` | radio | `2` |

### Bloque: Datos específicos del procedimiento

| Campo | `id` | `name` | Tipo | Required |
|---|---|---|---|---|
| País del título | `codPais` | `solicitude.codPais` | select (código ISO numérico) | ✅ |
| Nombre del título extranjero | `nomeTituloExtranxeiro` | `solicitude.nomeTituloExtranxeiro` | text | ✅ |
| Nombre del centro | `nomeCentro` | `solicitude.nomeCentro` | text | — |
| Año académico | `codAnoAcademico` | `solicitude.codAnoAcademico` | select (código interno, no es el año) | — |
| Exámenes oficiales superados | `examesOficiaisSuperados` | `solicitude.examesOficiaisSuperados` | text | — |
| Nivel de estudios (1-9) | `formularioHomologacion_solicitude_codTipoNivelEstudosEsp1` … `...9` | `solicitude.codTipoNivelEstudosEsp` | radio | ✅ |
| Nombre del título español | `nomeTituloEspanol` | `solicitude.nomeTituloEspanol` | text | ✅ |

**Valores de los radios `solicitude.codTipoNivelEstudosEsp`**:

| `value` | Etiqueta |
|---|---|
| `1` | Educación secundaria obligatoria |
| `2` | Educación secundaria obligatoria y 1º de bachillerato |
| `3` | Educación secundaria obligatoria y bachillerato |
| `4` | 1º de bachillerato |
| `5` | Bachillerato |
| `6` | Ciclo formativo (de grado medio y/o superior) |
| `7` | Enseñanzas artísticas profesionales (música, danza, artes plásticas, diseño) |
| `8` | Enseñanzas deportivas |
| `9` | Enseñanzas artísticas superiores y/o máster |

**Nota sobre `codAnoAcademico`**: los `value` son códigos internos (`134` = 2025/2026, `133` = 2024/2025, …, `59` = 1950/1951), no el año en sí. La extensión debe mapear año → código, o buscar por el texto visible.

### Bloque: Documentación

Todos son checkboxes, salvo el último, que es un `textarea`.

| Campo | `id` | `name` | Tipo |
|---|---|---|---|
| Identidad | `docIdentidade` | `documentos.identidade` | checkbox |
| Representación | `docRepresentacion` | `documentos.representacion` | checkbox |
| Título | `docTitulo` | `documentos.titulo` | checkbox |
| Certificado académico | `docCertificadoAcademico` | `documentos.certificadoAcademico` | checkbox |
| Resguardo de pago | `docResgardoPago` | `documentos.resgardoPago` | checkbox |
| Anexo | `checkAnexo` | `documentos.anexo` | checkbox |
| Plan de estudios FP | `docPlanEstudosFP` | `documentos.planEstudosFP` | checkbox |
| Programa de materias FP | `docProgramaMateriasFP` | `documentos.programaMateriasFP` | checkbox |
| Experiencia laboral FP | `docExperienciaLaboralFP` | `documentos.experienciaLaboralFP` | checkbox |
| Justificante FP | `docXustificanteFP` | `documentos.xustificanteFP` | checkbox |
| Certificado académico FP | `docCertificadoAcademicoFP` | `documentos.certificadoAcademicoFP` | checkbox |
| Plan de estudios artes | `docPlanEstudosArtes` | `documentos.planestudosArtes` | checkbox |
| Otra documentación | `formularioHomologacion_documentos_outraDocumentacion` | `documentos.outraDocumentacion` | textarea |

**Nota**: los checkboxes van acompañados de un `hidden` con `name="__checkbox_<name>"` y `value="true"` (patrón habitual de Spring/Struts para distinguir "no marcado" de "no enviado"). La extensión debe marcar el checkbox, no el hidden.

### Bloque: Comprobación de datos

| Campo | `id` | `name` | Tipo |
|---|---|---|---|
| Opóngome a la consulta del DNI/NIE del solicitante | `formularioHomologacion_solicitude_oponseComprobarSolicitante` | `solicitude.oponseComprobarSolicitante` | checkbox |
| Opóngome a la consulta del DNI/NIE del representante | `formularioHomologacion_solicitude_oponseComprobarRepresentante` | `solicitude.oponseComprobarRepresentante` | checkbox |

## Comportamiento dinámico

Los siguientes elementos **no están cargados en el HTML inicial** y se rellenan por JavaScript:

1. **Selects de concello, localidad y lugar** (tanto en `enderezoSolicitante` como en `enderezoNotificacion`). En el HTML solo aparece `<option value="">-- Seleccione un elemento --</option>`.
2. **La carga se dispara con `cargarComponentesEnderezo(prefijo)`**, llamada en `$(document).ready()`. Presumiblemente hace una llamada AJAX a `/hovaes/LugarJson-buscar*` y rellena el select correspondiente.
3. **Dependencias en cascada**:
   - Cambiar provincia → recarga concellos.
   - Cambiar concello → recarga localidades.
   - Cambiar localidad → recarga lugares.
4. **El formulario tiene `noscript`** con botones `action:recargar` para cada nivel, lo que confirma que la carga es server-side y se simula con AJAX cuando hay JS.

**Implicación para la extensión**: no basta con `select.value = codigo`. Hay que:
- Esperar a que el select tenga las opciones cargadas (o disparar el `change` del nivel superior y esperar).
- Posiblemente disparar `change` en cascada y esperar entre niveles.

## Implicación para la precarga

- Cada nivel se precarga por **código INE**, no por nombre.
- El catálogo local ya contiene los códigos de concello (5), localidad (7) y lugar (9).
- El código de provincia (2) se deriva de los dos primeros dígitos del concello.
- **Precargar por `id`**, no por `name` (el `name` de localidad no lleva `cod`).
- **Esperar la carga dinámica** de los selects de concello/localidad/lugar antes de intentar setear el valor.

## Alcance del OCR (decisión de sesión)

El PDF físico de la solicitud tiene 3 hojas. **El OCR se aplica solo a la primera hoja**, que es la que contiene los datos de identificación, dirección y datos específicos del procedimiento. Las hojas 2 y 3 (documentación, anexo III, comprobación de datos) no se procesan por OCR.

El límite de la primera hoja, a efectos de campos OCR, termina en el bloque «Datos específicos del procedimiento»: nombre del título extranjero, país, nombre del centro, año académico. Los campos posteriores (exámenes oficiales, nivel de estudios, título español, documentación, comprobación, anexo III) quedan fuera del alcance del OCR de la primera hoja.

## Pendiente

- Verificar cómo presenta los duplicados (ej. `BETANZOS` vs `Betanzos` en Betanzos). **Nota**: el catálogo completo confirma que el patrón de duplicados es más general de lo que decía `CATALOGS.md`: no es solo «capital vs entidad», es «parroquia (MAIÚSCULAS con paréntesis) vs lugar (Capitalizado sin paréntesis)». Ver actualización propuesta para `CATALOGS.md` más abajo.
- Decidir si la extensión precarga solo el bloque del solicitante, solo el de notificación, o ambos (por defecto: solicitante; si el usuario marca «notificar en el mismo domicilio», copiar).
- Verificar el endpoint exacto que usa `cargarComponentesEnderezo` (no aparece en el HTML pegado; probablemente sea el mismo `/hovaes/LugarJson-buscarConcellos.action` y `/hovaes/LugarJson-buscarLugares.action` ya documentados, pero hay que confirmarlo en DevTools).
- Confirmar el mapeo completo de `codAnoAcademico` (año → código interno) si la extensión va a precargarlo. **Nota**: el usuario indica que este mapeo está en el JSON de datos que acompaña al formulario; pendiente de recibirlo.