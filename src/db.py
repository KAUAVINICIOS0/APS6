import os
import sqlite3
from typing import Optional, Tuple, List


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sqlite")


def get_conn() -> sqlite3.Connection:

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(seed: bool = True) -> None:

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            nivel INTEGER NOT NULL CHECK(nivel IN (1,2,3)),
            imagem_registrada TEXT NOT NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS propriedades_rurais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            localizacao TEXT NOT NULL,
            agrotoxicos_proibidos TEXT NOT NULL,
            impacto TEXT NOT NULL,
            nivel_minimo INTEGER NOT NULL CHECK(nivel_minimo IN (1,2,3))
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS logs_acesso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            acao TEXT NOT NULL,
            sucesso INTEGER NOT NULL,
            criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        );
        """
    )

    conn.commit()

    if seed:
        seed_contexto(conn)

    conn.close()


def seed_contexto(conn: sqlite3.Connection) -> None:

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS c FROM propriedades_rurais")
    count = cur.fetchone()[0]
    if count > 0:
        return

    dados = [
        (
            "Fazenda Rio Doce",
            "Alta Floresta - MT",
            "Paraquat; Aldrin",
            "Risco elevado de contaminação de lençóis freáticos",
            1,
        ),
        (
            "Sítio Boa Esperança",
            "Luís Eduardo Magalhães - BA",
            "DDT",
            "Monitoramento de resíduos em afluentes do Rio Grande",
            2,
        ),
        (
            "AgroVale",
            "Barreiras - BA",
            "Lindano; Endossulfam",
            "Incidências críticas em pontos de captação urbana",
            3,
        ),
    ]

    cur.executemany(
        """
        INSERT INTO propriedades_rurais (nome, localizacao, agrotoxicos_proibidos, impacto, nivel_minimo)
        VALUES (?, ?, ?, ?, ?)
        """,
        dados,
    )

    conn.commit()


def criar_usuario(nome: str, nivel: int, imagem_registrada: str) -> int:

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuarios (nome, nivel, imagem_registrada) VALUES (?, ?, ?)",
        (nome, nivel, imagem_registrada),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def buscar_usuario_por_id(user_id: int) -> Optional[sqlite3.Row]:

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def listar_usuarios() -> List[sqlite3.Row]:

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuarios ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return list(rows)


def registrar_log(usuario_id: Optional[int], acao: str, sucesso: bool) -> None:

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs_acesso (usuario_id, acao, sucesso) VALUES (?, ?, ?)",
        (usuario_id, acao, 1 if sucesso else 0),
    )
    conn.commit()
    conn.close()


def consultar_propriedades_por_nivel(nivel_usuario: int) -> List[sqlite3.Row]:

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, nome, localizacao, agrotoxicos_proibidos, impacto, nivel_minimo
        FROM propriedades_rurais
        WHERE nivel_minimo <= ?
        ORDER BY nivel_minimo DESC, id ASC
        """,
        (nivel_usuario,),
    )
    rows = cur.fetchall()
    conn.close()
    return list(rows)


