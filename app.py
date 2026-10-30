"""Fábrica da aplicação Monolítica Modular da Livraria Mackenzie."""

import os
from typing import Optional
from flask import Flask

from modules.shared.events import EventBus
from modules.catalogo.repository import CatalogoRepository
from modules.catalogo.service import CatalogoService
from modules.catalogo.web import catalogo_bp
from modules.estoque.repository import EstoqueRepository
from modules.estoque.service import EstoqueService
from modules.reserva.repository import ReservaRepository
from modules.reserva.service import ReservaService
from modules.reserva.web import reserva_bp


def create_app(
    catalogo_repo: Optional[CatalogoRepository] = None,
    estoque_repo: Optional[EstoqueRepository] = None,
    reserva_repo: Optional[ReservaRepository] = None,
    event_bus: Optional[EventBus] = None,
) -> Flask:
    """Instancia a aplicação Flask e orquestra a injeção dos módulos e barramento de eventos."""
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "mackenzie-modular-secret-key-2026")

    bus = event_bus or EventBus()
    c_repo = catalogo_repo or CatalogoRepository()
    e_repo = estoque_repo or EstoqueRepository()
    r_repo = reserva_repo or ReservaRepository()

    c_service = CatalogoService(c_repo)
    e_service = EstoqueService(e_repo)
    e_service.registrar_listeners(bus)
    r_service = ReservaService(r_repo, c_service, e_service, bus)

    # Armazena serviços no config da aplicação para injeção limpa
    app.config["EVENT_BUS"] = bus
    app.config["CATALOGO_SERVICE"] = c_service
    app.config["ESTOQUE_SERVICE"] = e_service
    app.config["RESERVA_SERVICE"] = r_service

    # Registro dos Blueprints modulares
    app.register_blueprint(catalogo_bp)
    app.register_blueprint(reserva_bp)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
