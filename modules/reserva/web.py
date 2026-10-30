"""Rotas e controladores Web do módulo Reserva."""

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from modules.shared.exceptions import LivrariaError

reserva_bp = Blueprint("reserva", __name__)


@reserva_bp.route("/reservas", methods=["GET"])
def listar():
    reserva_service = current_app.config["RESERVA_SERVICE"]
    reservas = reserva_service.listar_reservas()
    return render_template("reserva/listar.html", reservas=reservas)


@reserva_bp.route("/reservas", methods=["POST"])
def criar():
    reserva_service = current_app.config["RESERVA_SERVICE"]
    isbn = request.form.get("isbn", "").strip()
    unidade = request.form.get("unidade", "").strip()

    if not isbn or not unidade:
        flash("Informe o ISBN e a unidade desejada.", "error")
        return redirect(url_for("catalogo.index"))

    try:
        reserva = reserva_service.criar_reserva(isbn=isbn, unidade=unidade)
        flash(f"Reserva {reserva.codigo} realizada com sucesso na unidade {unidade}!", "success")
        return redirect(url_for("reserva.listar"))
    except LivrariaError as e:
        flash(str(e), "error")
        return redirect(url_for("catalogo.detalhes", isbn=isbn))


@reserva_bp.route("/reservas/<codigo>/cancelar", methods=["POST"])
def cancelar(codigo: str):
    reserva_service = current_app.config["RESERVA_SERVICE"]
    try:
        reserva = reserva_service.cancelar_reserva(codigo)
        flash(
            f"Reserva {reserva.codigo} cancelada com sucesso! O exemplar foi devolvido ao estoque da unidade {reserva.unidade}.",
            "success",
        )
    except LivrariaError as e:
        flash(str(e), "error")

    return redirect(url_for("reserva.listar"))
