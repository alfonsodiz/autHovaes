# autHovaes

Sistema de pre-recheo asistido (no automático) para el formulario ED434A de la Xunta de Galicia, a partir de un PDF manuscrito escaneado. Todo el procesamiento es local. Sin instalación, sin admin, sin registro.

## Documentación

Toda la documentación está en [`docs/`](docs/). Punto de entrada: [`docs/README.md`](docs/README.md).

## Estado

Ver [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md).

## Restricciones

Ver [`docs/AGENTS.md`](docs/AGENTS.md) y [`docs/architecture/DEPLOYMENT_CONSTRAINTS.md`](docs/architecture/DEPLOYMENT_CONSTRAINTS.md).

## Catálogo territorial

El catálogo territorial (`recursos/catalogo-hovaes-lugares-galicia-completo.json`) **no se incluye en este repositorio**. Motivos:

1. Su licencia original (Hovaes) no está confirmada.
2. El proyecto prevé sustituirlo a medio plazo por un extracto propio del Nomenclátor del INE (dominio público).

Ver [`docs/architecture/CATALOGS.md`](docs/architecture/CATALOGS.md) para la estructura esperada y el proceso de obtención.

## Bundle de despliegue

Los binarios (`python-portable/`, `paddleocr-json/`, `libs/`) **no se versionan**. Se distribuyen aparte, en un `.zip` o en una release. Ver [`docs/architecture/DEPLOYMENT_CONSTRAINTS.md`](docs/architecture/DEPLOYMENT_CONSTRAINTS.md).

## Licenza

Pendiente de decisión. Ver [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) §Riesgos.