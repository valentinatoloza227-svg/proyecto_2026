// GALAXY - juego Phaser de PROA Arcade
// Django prepara la página y le entrega la configuración del nivel.
// Este archivo juega la partida y, al terminar, le avisa el resultado a Django.

// TODO 2: leer la configuración que manda Django y usarla para armar las reglas del nivel.
const NOMBRE_NIVEL = "Nivel de prueba";
const META = 50;
const VIDAS_INICIALES = 3;
const VELOCIDAD_ENEMIGOS = 2;
const FRAMES_ENTRE_ENEMIGOS = 70;

const ANCHO = 800;
const ALTO = 500;
const VELOCIDAD = 5;

const configuracion = {
    type: Phaser.AUTO,
    width: ANCHO,
    height: ALTO,
    backgroundColor: "#071027",
    parent: "juego",
    scene: {
        create: create,
        update: update
    }
};

const juego = new Phaser.Game(configuracion);

let escena;
let nave;
let cursores;
let teclaEspacio;
let balas = [];
let enemigos = [];
let puntos = 0;
let vidas = VIDAS_INICIALES;
let contador = 0;
let terminado = false;
let textoPuntos;
let textoVidas;
let textoMensaje;

// create se ejecuta UNA vez, cuando empieza el juego.
function create() {
    escena = this;
    crearEstrellas();
    nave = this.add.triangle(ANCHO / 2, ALTO - 60, 0, 34, 24, 0, 48, 34, 0x4deeea);

    // TODO 3: preparar las flechas y la barra espaciadora.

    const estiloHud = { fontFamily: "Arial", fontSize: "20px", color: "#7dd3fc" };
    this.add.text(ANCHO / 2, 12, NOMBRE_NIVEL + " (meta: " + META + ")", estiloHud).setOrigin(0.5, 0);
    textoPuntos = this.add.text(16, 12, "Puntos: 0", estiloHud);
    textoVidas = this.add.text(ANCHO - 16, 12, "Vidas: " + vidas, estiloHud).setOrigin(1, 0);
    textoMensaje = this.add.text(ANCHO / 2, ALTO / 2, "", {
        fontFamily: "Arial", fontSize: "32px", color: "#ffffff", align: "center"
    }).setOrigin(0.5);
}

// update se ejecuta MUCHAS veces por segundo (unas 60).
function update() {
    if (terminado) {
        return;
    }
    moverNave();
    if (Phaser.Input.Keyboard.JustDown(teclaEspacio)) {
        disparar();
    }
    moverBalas();

    contador++;
    if (contador % FRAMES_ENTRE_ENEMIGOS === 0) {
        crearEnemigo();
    }
    moverEnemigos();
    detectarChoques();
    detectarChoquesConNave();
}

function moverNave() {
    // TODO 4: mover la nave con las flechas y mantenerla dentro de la pantalla.
}

// ----- Reglas del juego (las estudiamos en la clase 13) -----

function disparar() {
    const bala = escena.add.circle(nave.x, nave.y - 24, 5, 0xffe066);
    balas.push(bala);
}

function moverBalas() {
    for (let i = balas.length - 1; i >= 0; i--) {
        balas[i].y -= 8;
        if (balas[i].y < -10) {
            balas[i].destroy();
            balas.splice(i, 1);
        }
    }
}

function crearEnemigo() {
    const x = Phaser.Math.Between(30, ANCHO - 30);
    const enemigo = escena.add.circle(x, -20, 16, 0xff5c8a);
    enemigos.push(enemigo);
}

function moverEnemigos() {
    for (let i = enemigos.length - 1; i >= 0; i--) {
        enemigos[i].y += VELOCIDAD_ENEMIGOS;
        if (enemigos[i].y > ALTO + 20) {
            enemigos[i].destroy();
            enemigos.splice(i, 1);
        }
    }
}

function detectarChoques() {
    for (let i = balas.length - 1; i >= 0; i--) {
        for (let j = enemigos.length - 1; j >= 0; j--) {
            const distancia = Phaser.Math.Distance.Between(balas[i].x, balas[i].y, enemigos[j].x, enemigos[j].y);
            if (distancia < 21) {   // radio del enemigo (16) + radio de la bala (5)
                balas[i].destroy();
                balas.splice(i, 1);
                enemigos[j].destroy();
                enemigos.splice(j, 1);
                sumarPuntos(10);
                break;
            }
        }
    }
}

function detectarChoquesConNave() {
    for (let j = enemigos.length - 1; j >= 0; j--) {
        const distancia = Phaser.Math.Distance.Between(nave.x, nave.y, enemigos[j].x, enemigos[j].y);
        if (distancia < 32) {   // radio del enemigo (16) + radio aproximado de la nave (16)
            enemigos[j].destroy();
            enemigos.splice(j, 1);
            perderVida();
        }
    }
}

function sumarPuntos(cantidad) {
    puntos += cantidad;
    textoPuntos.setText("Puntos: " + puntos);
    if (puntos >= META) {
        terminarPartida(true);
    }
}

function perderVida() {
    vidas--;
    textoVidas.setText("Vidas: " + vidas);
    if (vidas <= 0) {
        terminarPartida(false);
    }
}

// ----- Comunicación con Django -----

function terminarPartida(gano) {
    if (terminado) {
        return;
    }
    terminado = true;
    textoMensaje.setText(gano ? "¡Nivel superado!\nGuardando resultado..." : "Se acabaron las vidas\nGuardando resultado...");
    enviarResultado(gano, puntos);
}

function enviarResultado(gano, puntosFinales) {
    // TODO 6: enviar el resultado a Django (POST con JSON y token CSRF) e ir a la pantalla que indique la respuesta.
    console.log("Resultado (todavía sin enviar):", gano, puntosFinales);
}

function crearEstrellas() {
    for (let i = 0; i < 40; i++) {
        const x = Phaser.Math.Between(0, ANCHO);
        const y = Phaser.Math.Between(0, ALTO);
        escena.add.circle(x, y, Phaser.Math.Between(1, 2), 0xffffff, 0.7);
    }
}
