# Livraria Mackenzie — Monólito Modular (Exercícios 8.3 e 8.4)

Projeto desenvolvido para a disciplina de **Engenharia de Software** (Laboratório 8: Microsserviços e Nanosserviços — Prof. Dr. Rodrigo Juliani).

---

## 1. Objetivos dos Exercícios

- **Exercício 8.3**: Refatorar o MVP da livraria para a **Arquitetura Monolítica Modular** baseada na decomposição de microsserviços (módulos delimitados: `catalogo`, `estoque`, `reserva` e `shared`).
- **Exercício 8.4**: Configurar e preparar o projeto para **Deploy em Nuvem** (Render, Docker, Procfile, Railway).

---

## 2. Padrão Arquitetural: Monólito Modular

Ao contrário de um monólito espaguete tradicional, o **Monólito Modular (Modular Monolith)** estrutura o sistema em módulos coesos e desacoplados dentro de uma única base de código implantável. Cada módulo possui seus próprios modelos, persistência e serviços, comunicando-se através de contratos de serviço e eventos de domínio assíncronos em memória (`EventBus`).

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Aplicação Flask (app.py)                        │
├───────────────────┬──────────────────────┬─────────────────────────────┤
│  Módulo Catálogo  │    Módulo Estoque    │       Módulo Reserva        │
│  (modules/catalogo)│   (modules/estoque)  │      (modules/reserva)      │
│  - Livro          │   - EstoqueUnidade   │   - Reserva, Status         │
│  - CatalogoRepo   │   - EstoqueRepo      │   - ReservaRepo             │
│  - CatalogoService│   - EstoqueService   │   - ReservaService          │
│  - Web Blueprint  │   - Event Listeners  │   - Web Blueprint           │
└─────────┬─────────┴──────────┬───────────┴──────────────┬──────────────┘
          │                    │                          │
          └────────────────────┼──────────────────────────┘
                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Módulo Shared / Kernel                          │
│               - EventBus (Barramento em memória)                       │
│               - Exceções de Domínio (LivrariaError, etc.)              │
│               - Eventos: ReservaCriadaEvent, ReservaCanceladaEvent     │
└────────────────────────────────────────────────────────────────────────┘
```

### Principais Características da Modularity:
1. **Módulo `catalogo`**: Gerencia títulos, autores, preços e buscas textuais.
2. **Módulo `estoque`**: Responsável pelo inventário de exemplares físicos por unidade (Higienópolis, Paulista, Pinheiros) e localização física (setor/corredor/prateleira).
3. **Módulo `reserva`**: Controla o fluxo de criação e cancelamento de reservas (`RES-XXXX`). Não altera estoques diretamente: emite eventos `ReservaCriadaEvent` e `ReservaCanceladaEvent`, que são escutados pelo módulo `estoque`.
4. **Módulo `shared`**: Contém o `EventBus` e as exceções canônicas de domínio, garantindo desacoplamento temporal e estrutural.

---

## 3. Estrutura de Pastas

```
mackenzie-es-livraria-monolito-modular/
├── app.py                      # Fábrica da aplicação e injeção de dependências
├── requirements.txt            # Dependências de produção e testes
├── Dockerfile                  # Containerização para deploy
├── Procfile                    # Comando de inicialização para Render / Heroku
├── render.yaml                 # Blueprint declarativo para Render
├── .gitignore
├── README.md                   # Documentação arquitetural
├── modules/
│   ├── shared/                 # Exceções e EventBus
│   │   ├── events.py
│   │   └── exceptions.py
│   ├── catalogo/               # Módulo de Catálogo
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── web.py
│   ├── estoque/                # Módulo de Estoque
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── service.py
│   └── reserva/                # Módulo de Reserva
│       ├── models.py
│       ├── repository.py
│       ├── service.py
│       └── web.py
├── templates/                  # Views HTML Jinja2 responsivas
│   ├── base.html
│   ├── catalogo/
│   │   ├── index.html
│   │   └── detalhes.html
│   └── reserva/
│       └── listar.html
├── static/                     # CSS moderno e responsivo
│   └── css/
│       └── style.css
└── tests/                      # Bateria de testes automatizados com pytest
    ├── test_catalogo.py
    ├── test_estoque.py
    ├── test_reserva.py
    └── test_monolito_integration.py
```

---

## 4. Como Executar Localmente

### Pré-requisitos
- Python 3.10+ instalado.

### Instalação e Execução
```bash
# 1. Clonar ou navegar até a pasta
cd mackenzie-es-livraria-monolito-modular

# 2. Criar e ativar ambiente virtual (opcional)
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar a aplicação
python app.py
```
Acesse no navegador: `http://localhost:5000`

---

## 5. Como Executar os Testes

```bash
pytest -v
```

Todos os testes unitários dos módulos e o fluxo de integração ponta a ponta (busca, reserva, cancelamento e devolução de exemplar ao estoque físico) devem passar com 100% de sucesso.

---

## 6. Deploy em Nuvem (Exercício 8.4)

O projeto está 100% configurado para deploy imediato no **Render**:

1. Acesse [render.com](https://render.com) e conecte sua conta do GitHub.
2. Clique em **New +** -> **Web Service**.
3. Selecione o repositório `mackenzie-es-livraria-monolito-modular`.
4. O Render detectará automaticamente o `render.yaml` / `Procfile`:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Clique em **Deploy**. Sua aplicação estará online em um link público (ex.: `https://mackenzie-es-livraria-monolito-modular.onrender.com`).

Também é possível executar via **Docker**:
```bash
docker build -t livraria-monolito .
docker run -p 5000:5000 livraria-monolito
```
