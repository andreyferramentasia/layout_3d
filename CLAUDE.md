# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Visão geral

Aplicação Django 6.1 (Python 3.13, gerenciada com `uv`) para o escritório "Rafael Castro Arquitetos": usuários autenticados cadastram projetos e fazem upload de modelos 3D (glTF/GLB ou Rhino `.3dm`), visualizados no navegador com Three.js. Interface e textos em pt-BR.

## Comandos

```sh
uv sync                                   # instala dependências em .venv
uv run python manage.py runserver         # servidor de desenvolvimento
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py test              # todos os testes
uv run python manage.py test projects3d   # um app
uv run python manage.py test projects3d.tests.MinhaClasse.test_metodo  # um teste
```

Não há linter, formatter nem pipeline de build front-end configurados. `tests.py` dos apps ainda estão vazios.

## Arquitetura

- `app/` — projeto Django (settings, urls raiz). Banco SQLite (`db.sqlite3`, versionado no git). Uploads vão para `media/`, servidos via `static()` em `app/urls.py` (só funciona com `DEBUG=True`). Obs.: `app/urls.py` faz `from app import settings`, sobrescrevendo o `django.conf.settings` importado antes.
- `accounts/` — login/logout/registro com o `User` padrão do Django (sem model próprio). Views são CBVs (`LoginView`, `LogoutView`, `CreateView` com `CustomUserCreationForm`). Telas de login/registro usam `accounts/static/accounts/css/castro.css` e incluem partials `_painel_obras_*.html` com imagens de obras.
- `projects3d/` — CRUD do model `Project` (`name`, `description`, `model_file`) com CBVs genéricas, todas com `LoginRequiredMixin`. A listagem tem paginação (9) e busca por `?search=` em `name`. Um sinal `post_delete` (`projects3d/signals.py`, registrado em `Projects3DConfig.ready()`) apaga o arquivo do disco ao excluir o projeto.
- URLs usam namespaces: `accounts:login|logout|register`, `projects3d:project-list|project-detail|project-create|project-update|project-delete`. `LOGIN_URL`, `LOGIN_REDIRECT_URL` e `LOGOUT_REDIRECT_URL` em settings apontam para esses nomes.
- `src/projeto3d/` é só o stub gerado pelo `uv init` (entry point `projeto3d:main`); não faz parte da aplicação web.

### Front-end

Tudo via CDN, sem bundler:
- `templates/base_1.html` (base de todas as páginas) carrega Tailwind v4 browser build, daisyUI 5 e htmx 2. O tema (`@theme`: cores `areia`, `verde`, `preto`; fontes `font-sans`=Jost, `font-serifa`=DM Serif Display) e as classes de componentes reutilizáveis (`.sobretitulo`, `.rotulo`, `.campo`, `.botao`, `.botao-sm`, `.botao-linha`, `.botao-perigo`, `.textura`) ficam num `<style type="text/tailwindcss">` nesse arquivo — reutilize-as em vez de repetir utilitários.
- `templates/partials/_nav_bar.html` é incluído pelas páginas de `projects3d`.
- Visualizador 3D: `project_detail.html` define um importmap para `three@0.170.0` e carrega `projects3d/static/projects3d/js/viewer.js` (ES module). O script lê a URL do modelo de `#viewer[data-model]`, escolhe `Rhino3dmLoader` para `.3dm` (rotaciona Z-up→Y-up; biblioteca rhino3dm do CDN, mesma versão do three) ou `GLTFLoader` para o resto, enquadra a câmera pelo bounding box e usa `OrbitControls`. Ao mudar a versão do three, atualize o importmap e o `setLibraryPath` do rhino3dm juntos.
