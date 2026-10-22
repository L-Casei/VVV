# Primera subida privada (Steam Workshop)

1. Ejecuta `python -m tools.package` desde el repositorio.
2. Extrae `dist/VVV-0.1.0.zip` en la carpeta `mod` de CK3 en Documentos/Paradox Interactive/Crusader Kings III. Deben quedar `mod/VVV.mod` y `mod/VVV/descriptor.mod`. No subas el repositorio completo ni el ZIP como contenido del mod.
3. Activa Veni, Vidi, Vici en un playset del launcher y realiza las pruebas de `docs/TESTING.md`. La compatibilidad 1.20.* es el objetivo declarado, no una certificacion de pruebas en el juego.
4. En el launcher, abre las herramientas de mods / Upload Mod, selecciona Veni, Vidi, Vici y Steam Workshop. Si aparece un selector de visibilidad, elige Private / Privado. Si no puedes confirmar que la nueva subida comienza privada, cancela y comprueba el flujo del launcher antes de continuar.
5. Tras subirlo, abre la ficha de Workshop con tu cuenta y comprueba que indica **Privado** y muestra la portada. No cambies la visibilidad a Publico ni a No listado: no son lo mismo que Privado. La privacidad se controla en Steam, no mediante descriptor.mod ni la privacidad de tu perfil.
6. Conserva el `remote_file_id` generado por el launcher para actualizar la misma ficha. Haz copia del descriptor instalado antes de reemplazarlo con un paquete nuevo; no pierdas ese identificador al actualizar.

Descripcion sugerida: "Primera alpha de Veni, Vidi, Vici: un campo de maniobras de tres sectores para CK3. Permite mover un regimiento simbolico y ensayar ordenes. Todavia no controla ejercitos ni modifica las batallas reales."

La portada original se incluye como `thumbnail.png` en la raiz del mod y ambos descriptores la referencian. Es un PNG cuadrado de menos de 1 MB. La imagen representa a Napoleon: se conserva como identidad visual, aunque no corresponde a la epoca medieval de CK3. Que un mod local no muestre portada en el launcher no basta para concluir que fallara en Workshop; comprueba la ficha tras la subida.

El paquete contiene unicamente descriptor, portada, common, events, gui y localization. El archivo VVV.mod va fuera de la carpeta que se sube. No contiene Python, pruebas, historial Git ni documentos internos.

No se ha realizado ninguna subida ni verificacion visual dentro del juego o de Workshop durante esta revision.

Referencia de Steam sobre previews y visibilidad: https://partner.steamgames.com/doc/api/ISteamUGC
