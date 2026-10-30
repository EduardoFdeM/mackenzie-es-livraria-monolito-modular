"""Rotas e controladores Web do módulo Catálogo."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from modules.shared.exceptions import LivroNaoEncontradoError

catalogo_bp = Blueprint("catalogo", __name__)


@catalogo_bp.route("/")
def index():
    catalogo_service = current_app.config["CATALOGO_SERVICE"]
    estoque_service = current_app.config["ESTOQUE_SERVICE"]

    termo = request.args.get("q", "").strip()
    if termo:
        livros = catalogo_service.buscar_por_termo(termo)
    else:
        livros = catalogo_service.listar_todos()

    # Monta visão com resumo de estoque disponível
    livros_com_estoque = []
    for livro in livros:
        estoques = estoque_service.listar_estoques_livro(livro.isbn)
        total_exemplares = sum(e.quantidade for e in estoques)
        livros_com_estoque.append({
            "livro": livro,
            "estoques": estoques,
            "total_exemplares": total_exemplares,
        })

    return render_template("catalogo/index.html", itens=livros_com_estoque, termo=termo)


@catalogo_bp.route("/livros/<isbn>")
def detalhes(isbn: str):
    catalogo_service = current_app.config["CATALOGO_SERVICE"]
    estoque_service = current_app.config["ESTOQUE_SERVICE"]

    try:
        livro = catalogo_service.obter_por_isbn(isbn)
    except LivroNaoEncontradoError:
        flash(f"Livro com ISBN '{isbn}' não foi encontrado no catálogo.", "error")
        return redirect(url_for("catalogo.index"))

    estoques = estoque_service.listar_estoques_livro(isbn)

    return render_template("catalogo/detalhes.html", livro=livro, estoques=estoques)
