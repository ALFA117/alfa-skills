# Estándar de producción /videoV2 (brief maestro generalizado)

Versión adaptable a cualquier idea del brief «Duolingo — The Path» que pasó el usuario el 26-oct-2026. Donde el original decía
Duolingo, Duo o «la línea verde», aquí dice **marca**, **protagonista** e **hilo visual**. Llénalos con la idea del usuario.

## 0. Directiva
Trabaja como un equipo de clase mundial: dirección creativa, dirección de cine publicitario, fotografía CGI, VFX, render,
motion 3D, animación de personaje, simulación, iluminación, arte y materiales, diseño sonoro, música, color y composición.
Presupuesto creativo simulado: **US$1,000,000**. Es la vara de calidad, no dinero real.
Meta: que el espectador piense «¿cómo hicieron esto?». Cada segundo lleva decisiones deliberadas de diseño, cámara,
animación, luz y sonido. Prohibido: efectos genéricos, transiciones predeterminadas, cámara sin intención, geometría pobre.
La complejidad sirve a **una idea extraordinariamente clara**.

## 1. Cinco cualidades
1. **Simplicidad conceptual:** un solo **hilo visual** conecta todo. Puede ser una línea de luz, un objeto, un color o
   una forma que se transforma.
2. **Complejidad técnica invisible:** física, cámara 3D, animación avanzada y composición multicapa.
3. **Personalidad de marca:** la estética y la energía de la marca son inconfundibles.
4. **Satisfacción visual:** cada pulsación, encendido, aterrizaje y transición se siente bien a la vista y al oído.
5. **Calidad cinematográfica:** nada delata límites de render, geometría, materiales o animación.

**Referencias de ejecución** (no copiar escenas, solo adoptar el estándar): Apple (films de producto), Buck, Ordinary
Folk, ManvsMachine, Tendril, Giant Ant.

## 2. Técnica no negociable
- 60 fps.
- Vertical 1080×1920 y horizontal 1920×1080. Cada relación de aspecto lleva **su propia composición**, nunca un recorte.
- Una sola trayectoria de cámara continua, sin cortes evidentes. Aplica en el motor 3D; en reels con voz se permiten
  cortes motivados.
- Python orquesta todo. NumPy, Pillow y ffmpeg sirven para texturas, composición y control de frames.
- 3D real (Blender 4.3 con Cycles/OptiX o EEVEE Next):
  - geometría, cámara en perspectiva y materiales PBR;
  - luces y sombras 3D, reflejos y oclusión ambiental;
  - HDR (AgX), profundidad de campo y motion blur.
- Prohibido simular 3D con imágenes 2D escaladas.
- Antialias alto. Trabaja en espacio lineal hasta el grade.
- Cero:
  - parpadeo de luz o material;
  - banding en degradados;
  - transparencias rotas.
- Negros profundos con detalle.

## 3. Dirección de arte: el mundo físico de la marca
La interfaz o el tema deja de estar en una pantalla y se vuelve **un universo físico**:
- los botones tienen peso;
- las tarjetas tienen espesor;
- las barras transportan energía;
- la música hace vibrar objetos.

**Ambiente oscuro con profundidad real.** Logra la profundidad con:
- gradientes volumétricos muy suaves y bruma casi imperceptible;
- geometría abstracta lejana;
- reflejos sutiles, sombras de contacto y luz rebotada;
- pocas partículas, dirigidas.

Nada de estrellas, partículas de sobra, sci-fi genérico ni neón barato. La sofisticación sale del control, no de la cantidad.

**Materiales PBR coherentes:**
- **Botones:** satinados, con biseles perfectos y base inferior más oscura. Proyectan sombra de contacto al presionarse y
  varían ligeramente su rugosidad.
- **Tarjetas:** mate premium, con espesor visible, bordes redondeados y luz de separación.
- **Hilo visual:**
  - núcleo brillante controlado con halo suave;
  - volumen real;
  - refleja en lo cercano y responde al movimiento;
  - nunca un trazo 2D con glow encima.

## 4. Iluminación
Diseña la luz escena por escena:
- **Key** amplia y suave.
- **Fill** muy controlada.
- **Rim** de separación.
- **Practicals:** el hilo visual ilumina lo cercano.
- **Bounce** del color de cada estación.

La luz cuenta la historia. Cada estación tiñe sutilmente lo que la rodea: naranja para la racha, azul para matemáticas,
morado para música.

Restricciones:
- no quemar blancos ni sobresaturar;
- nada de glow gigante;
- ninguna luz encima del texto;
- nada de lens flare en cada transición.

Debe sentirse cara pero nunca ostentosa.

## 5. Cámara
Una cámara, un viaje. Nunca se teletransporta. Cada cambio de escena se explica por:
- movimiento espacial o seguimiento del hilo;
- transformación de geometría;
- ocultación natural tras un objeto;
- cambio de escala o rotación orbital;
- transición de profundidad, o atravesar la interfaz.

**Sistema de cámara:**
- distancia focal variable con motivo;
- profundidad de campo animada con foco en el objetivo;
- curvas spline con aceleración no lineal y orientación a puntos de interés;
- horizonte controlado;
- movimiento secundario muy sutil y motion blur coherente.

Cada movimiento tiene motivación, un inicio compuesto, una trayectoria interesante, una aceleración expresiva, un
aterrizaje preciso y conexión con lo siguiente.

**Alterna tres energías:** explosiva, fluida y contemplativa (para leer). El contraste entre energía y calma es lo que
lo hace cine.

## 6. Animación
Todo movimiento lleva intención, peso y personalidad. Usa:
- curvas propias y anticipación;
- squash & stretch y acciones superpuestas;
- movimiento secundario e inercia;
- seguimiento de partes;
- oscilación amortiguada, colisiones y rebotes controlados;
- desfases y desaceleraciones.

**Regla:** ningún objeto importante aparece o desaparece solo con opacidad. Entra o sale con una acción física motivada.

**Microanimaciones** que se perciben sin distraer:
- alas, parpadeos y pupilas;
- compresión de botones, oscilación de fichas y vibración residual;
- rebote secundario y reacción lumínica de materiales;
- pequeño seguimiento de cámara tras impactos.

No todo rebota: el comportamiento cambia según material, peso y función.

## 7. Protagonista (si hay personaje)
Es el corazón emocional, no un logo que se mueve. Separa:
- cuerpo, extremidades y alas;
- ojos, pupilas y párpados;
- boca o pico, y expresión.

Personalidad: confianza, energía, simpatía, curiosidad, humor sutil y alegría por el progreso del usuario.

- Las extremidades llevan desfase entre sí, nunca rígidas y sincronizadas.
- Los ojos reaccionan; los parpadeos tienen intención.
- El volumen se conserva en el squash.
- El aterrizaje final parece animado a mano.

Si no hay personaje, la persona real del usuario (sus fotos) cumple ese papel. Ver «Fotos del usuario» en SKILL.md.

## 8. Guion visual (plantilla de 10 escenas, ajustar a la duración)
1. **Impacto (0–8 %):** casi negro, se concentra la energía, entran fibras con paralaje y el protagonista llega a gran
   velocidad. Impacto heroico en el 1 %:
   - compresión del cuerpo;
   - extremidades con retraso;
   - sacudida breve y direccional;
   - fragmentos y subgrave.

   Mira a cámara y parpadea; luego el hilo revela la marca. *Objetivo: sorpresa, reconocimiento, personalidad.*
2. **El universo (8–14 %):** el hilo desciende y se abre un mundo 3D que se revela con la cámara. Nodos con peso se
   encienden uno a uno. Un botón grande se hunde y libera una onda; de él sale el dispositivo y la cámara entra a su pantalla.
3. **La satisfacción (14–23 %):** la interfaz es un espacio físico. Las piezas se ensamblan magnéticamente, cada contacto
   comprime y suena, y llega el «¡correcto!». El hilo llena la barra de progreso y escapa.
4. **La constancia (23–34 %):** el hilo se transforma (por ejemplo en una llama). Un único destello y la luz cambia de
   color. Un contador de anchura fija salta 1 → 7 → 30 → 100 → 365 con una órbita corta.
5. **El ascenso (34–44 %):** una tabla 3D en la que la tarjeta del usuario sube del #7 al #1 desplazando a las demás
   físicamente. Una onda recorre la tabla.
6. **Lo humano (44–54 %):** una ventana de videollamada o una conversación. El hilo se vuelve una onda de audio 3D que
   reacciona a la voz real. *Objetivo: la habilidad se vuelve real.*
7. **Muchos mundos, un camino (54–69 %):** el hilo se divide en ramas con identidad propia (color, luz y objeto físico
   satisfactorio) y la cámara sube para revelar que son una sola estructura.
8. **La gran idea (69–78 %):** las ramas convergen y el hilo se vuelve la base de una tipografía limpísima, sin efectos 3D
   en las letras. El mensaje principal va en dos golpes con pausa. El mundo contiene la respiración.
9. **El cierre (78–91 %):** la música se retira y un sonido invertido crece. El protagonista aterriza justo con el golpe
   grave: se comprime, sus extremidades siguen por inercia y sale una onda. El hilo revela el logo centrado y suena la
   locución con el nombre de marca. Pequeño gesto de alegría.
10. **Firma (últimos 2 s):** pantalla final minimalista con la **portada y el handle**. Resonancia musical, sin animación
    innecesaria.

## 9. Locución
- Voz natural en español latino, con sonrisa perceptible.
- Nada robótico, sin tono publicitario impostado ni pronunciación forzada.
- Interpretación continua. Si el motor es TTS, se genera por réplica pero se mezcla como una sola toma.
- Haz 2–3 pruebas y elige la más natural. No aceleres artificialmente; ajusta pausas y coreografía.
- Define **anclas** palabra→segundo y valídalas con la transcripción real.

## 10. Música original
- Compuesta para la pieza: tempo, tonalidad e instrumentación premium (por ejemplo marimba, percusión melódica, teclados
  suaves, subgrave redondo, bombo, palmas y shaker).
- Optimista sin ser infantil.
- Cada cambio de energía está diseñado para la acción.
- Entradas de percusión, crecimiento, resolución hacia el mensaje, pausa dramática, acorde final con golpe grave y fanfarria.

## 11. Diseño sonoro
Categorías:
- movimiento (whooshes de varias escalas);
- materiales (contactos, pulsaciones, deslizamientos, rebotes);
- energía (encendidos, pulsos, propagación);
- personaje (saltos, aterrizajes);
- sonidos de marca, solo con permiso. Si no hay permiso, se crean originales.

**Jerarquía:** lo secundario es discreto para que lo importante sobresalga.

Mezcla:
- voz siempre inteligible y música ≥12 dB debajo de la voz;
- **−14 LUFS integrados y pico ≤ −1.25 dBTP**;
- revisión en mono y en bocina de teléfono, sin clipping.

## 12. Composición y acabado
- Pases según corresponda: beauty, profundidad, normales, vectores, máscaras, emisión, reflejos, sombras y AO.
- Acabado:
  - grade coherente con contraste y saturación controlados;
  - bloom muy contenido;
  - grano fino;
  - profundidad de campo y motion blur;
  - nitidez controlada.
- **Prohibido:** glow excesivo, aberración evidente, distorsión gratuita, shake constante, grano visible, partículas
  aleatorias, flares repetidos, sombras falsas, modelos pobres, texto deformado, interpolación lineal y transiciones genéricas.

## 13. Vertical real
- Nueva proyección del mismo mundo: el protagonista dentro de la zona dominante.
- Nodos reorganizados a lo alto y textos reencuadrados.
- Trayectorias y escalas adaptadas, nada importante fuera del cuadro.

## 14. Control de calidad
**Técnico:**
- duración exacta, resolución y fps;
- frames íntegros, sin frames negros ni archivos faltantes;
- sincronía audiovisual y continuidad de cámara;
- sin geometría atravesada, con luz consistente y texto legible;
- LUFS y pico real dentro de rango.

**Artístico:** califica cada escena del 1 al 10 en cinco criterios:
1. **Composición:** ¿la mirada sabe a dónde ir?
2. **Movimiento:** ¿tiene intención, peso y personalidad?
3. **Luz:** ¿parece render de primer nivel?
4. **Narrativa:** ¿la idea es clara?
5. **Satisfacción:** ¿se siente memorable?

Menos de 9 en algo importante obliga a revisar. Anota **los defectos observados y la corrección hecha**. Nunca declares
calidad sin mirar los frames.

## 15. Pipeline
- **A. Preproducción:** guion→frames, animática, posiciones de estaciones, una sola trayectoria de cámara, transiciones
  geométricas, legibilidad y anclas de música y voz.
- **B. Audio:** pruebas de voz, toma final, anclas, maqueta musical e impactos.
- **C. Mundo:** geometría, materiales, hilo visual, estaciones, cámara y luz preliminar.
- **D. Animación:** blocking, timing, anticipación e inercia, protagonista, interfaces, secundarias y pulido de curvas.
- **E. Acabado:** luz y materiales finales, render, composición, grade, música final, SFX y mezcla/master.
- **F. Validación:** preview completo, inspección de impactos, corrección, máster horizontal y vertical, y verificación
  de los archivos.

## 16. Entregables
- Máster(es) MP4 con audio final.
- Código y proyecto: scripts, geometría, materiales, cámara y configuración de render.
- Recursos: locución, música y SFX.
- Reporte QC con capturas de frames clave y la lista de problemas corregidos.
- En /videoV2, además: **portada** (PNG/JPG del cuadro final) y **pie de Instagram**.

## 17. Reglas absolutas
1. No sacrificar calidad por comodidad.
2. 3D real donde la perspectiva lo exige.
3. No usar disolvencias entre escenas inconexas.
4. Nada de VFX sin propósito narrativo.
5. Nada de materiales genéricos.
6. Nada de interpolación lineal en movimientos importantes.
7. La legibilidad va antes que el espectáculo.
8. Personaje consistente.
9. No recrear logos de memoria: usar assets oficiales permitidos o tipografía propia.
10. No terminar en el primer render.
11. No dar por validado sin inspeccionar.
12. No sustituir entregas por descripciones.
13. No fingir herramientas: documentar límites y usar la mejor alternativa.
14. El vertical no es un recorte.
15. La técnica no eclipsa la personalidad.

## 18. Prueba definitiva
- ¿El primer medio segundo detiene el scroll?
- ¿El protagonista parece animado por un experto?
- ¿La cámara se mueve como cine?
- ¿Los materiales son extraordinarios?
- ¿Las transiciones parecen imposibles pero naturales?
- ¿La música y el movimiento son una sola cosa?
- ¿Se entiende en un teléfono?
- ¿Se reconoce la marca sin leerla?
- ¿El cierre deja recuerdo?

Si algo falla, se corrige.

## 19. Ejecución
Es un brief operativo, no una referencia de estilo.

**Prioridades de pulido:**
1. el impacto inicial;
2. la continuidad de cámara;
3. la calidad física;
4. la personalidad;
5. las transformaciones del hilo;
6. el ritmo audiovisual;
7. el cierre de marca.

**Criterios de decisión:**
- Si un efecto es espectacular pero confunde, gana la claridad.
- Si una animación es correcta pero no tiene personalidad, se rediseña.
- Si un efecto es llamativo pero genérico, se elimina.
