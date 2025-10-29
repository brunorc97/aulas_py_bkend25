import csv
import os

DATA_DIR = "dados_biblioteca"
os.makedirs(DATA_DIR, exist_ok=True)

def salvar_csv(nome_arquivo, dados, campos):
    with open(os.path.join(DATA_DIR, nome_arquivo), mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

def carregar_csv(nome_arquivo, campos):
    caminho = os.path.join(DATA_DIR, nome_arquivo)
    if os.path.exists(caminho):
        with open(caminho, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    return []
import flet as ft

# Listas globais para armazenar os dados
emprestimos = []
avaliacoesLivros = []
avaliacoesBiblioteca = []

def main(page: ft.Page):
    global emprestimos, avaliacoesLivros, avaliacoesBiblioteca
    emprestimos = carregar_csv("emprestimos.csv", ["livro", "aluno", "data"])
    avaliacoesLivros = carregar_csv("avaliacoes_livros.csv", ["usuario", "livro", "nota", "comentario"])
    avaliacoesBiblioteca = carregar_csv("avaliacoes_atendimento.csv", ["usuario", "nota", "comentario"])
    page.theme = ft.Theme()
    page.theme.font_family = "Poppins"
    page.title = "Gerenciamento de Biblioteca"
    page.window_width = 600
    page.window_height = 500
    page.bgcolor = "#007AFF"
    page.session.set("tema_botao", "#007AFF")
    page.session.set("tema_container", "white")
    page.padding = 20
    # Tema claro/escuro
    page.theme_mode = ft.ThemeMode.LIGHT
    page.update()

    # Dialog global para feedback visual
    dialog = ft.AlertDialog(
        title=ft.Text("Sucesso"),
        content=ft.Text("Operação concluída com sucesso!"),
        actions=[ft.TextButton("OK", on_click=lambda _: fechar_dialog())],
    )
    def fechar_dialog():
        dialog.open = False
        page.update()

    def cor_texto():
        return "#FFFFFF" if page.theme_mode == ft.ThemeMode.DARK else "#1C1C1E"

    def criar_botao(texto, on_click, cor_fundo=None):
        if not cor_fundo:
            cor_fundo = page.session.get("tema_botao") or ("#3A3A3C" if page.theme_mode == ft.ThemeMode.DARK else "#007AFF")
        btn = ft.ElevatedButton(
            texto,
            on_click=on_click,
            bgcolor=cor_fundo,
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(24, 16, 24, 16),
                overlay_color="#339CFF",
                text_style=ft.TextStyle(font_family="Poppins", size=15, weight=ft.FontWeight.W_600),
            ),
        )
        btn.scale = ft.Scale(1.0)
        btn.animate_scale = ft.Animation(200, "easeOut")

        def on_hover(e):
            btn.scale = ft.Scale(1.08 if e.data == "true" else 1.0)
            btn.update()

        btn.on_hover = on_hover
        return btn

    def criar_textfield(label_text, width=320, multiline=False):
        return ft.TextField(
            label=label_text,
            width=min(page.window_width * 0.8, 500),
            border=None,
            border_radius=10,
            bgcolor="#2C2C2E" if page.theme_mode == ft.ThemeMode.DARK else "white",
            color=cor_texto(),
            filled=True,
            multiline=multiline,
            content_padding=ft.Padding(12, 10, 12, 10),
            label_style=ft.TextStyle(
                color="#FFFFFF" if page.theme_mode == ft.ThemeMode.DARK else "#1C1C1E",
                weight=ft.FontWeight.W_500,
                font_family="Poppins",
            ),
            text_style=ft.TextStyle(font_family="Poppins", size=14),
            cursor_color="#007AFF",
        )

    def voltar_ao_menu(e=None):
        # Animação suave de fade para transição
        page.controls.clear()
        container = conteudo_menu()
        container.opacity = 0
        page.add(container)
        container.animate_opacity = ft.Animation(400, "easeOut")
        container.opacity = 1
        page.update()

    def conteudo_menu():
        gif = ft.Image(
            src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDdpOGgxeDlyMXIzNHRnaHpsdzI3eXVnNHlzOXBlbDFtbWVvaGM5dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0HlMEi55YsfXyzMk/giphy.gif",
            width=180,
            height=180,
            border_radius=20,
            fit=ft.ImageFit.COVER,
        )
        titulo = ft.Text(
            "Gerenciamento de Biblioteca",
            size=26,
            weight=ft.FontWeight.BOLD,
            color=cor_texto(),
            text_align=ft.TextAlign.CENTER,
            font_family="Poppins",
            italic=True,
        )
        # Grid estilo Zul
        botoes = ft.GridView(
            expand=False,
            runs_count=2,
            max_extent=230,
            spacing=20,
            run_spacing=20,
            child_aspect_ratio=1,
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(name=ft.Icons.BOOK, size=50, color="white"),
                            ft.Text("Cadastrar Empréstimo", weight=ft.FontWeight.BOLD, color="white", text_align=ft.TextAlign.CENTER),
                            ft.Text("Registrar empréstimo", size=12, color="white", text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    bgcolor="#007AFF",
                    border_radius=20,
                    padding=25,
                    alignment=ft.alignment.center,
                    on_click=lambda e: cadastrar_emprestimo(),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(name=ft.Icons.STAR, size=50, color=cor_texto()),
                            ft.Text("Avaliar Livro", weight=ft.FontWeight.BOLD, color=cor_texto(), text_align=ft.TextAlign.CENTER),
                            ft.Text("Avaliar leitura", size=12, color=cor_texto(), text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    bgcolor=page.session.get("tema_container"),
                    border_radius=20,
                    padding=25,
                    alignment=ft.alignment.center,
                    on_click=lambda e: avaliar_livro(),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(name=ft.Icons.CHAT, size=50, color=cor_texto()),
                            ft.Text("Avaliar Atendimento", weight=ft.FontWeight.BOLD, color=cor_texto(), text_align=ft.TextAlign.CENTER),
                            ft.Text("Avaliar serviço", size=12, color=cor_texto(), text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    bgcolor=page.session.get("tema_container"),
                    border_radius=20,
                    padding=25,
                    alignment=ft.alignment.center,
                    on_click=lambda e: avaliar_atendimento(),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(name=ft.Icons.INSIGHTS, size=50, color=cor_texto()),
                            ft.Text("Gerar Relatório", weight=ft.FontWeight.BOLD, color=cor_texto(), text_align=ft.TextAlign.CENTER),
                            ft.Text("Ver resultados", size=12, color=cor_texto(), text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    bgcolor=page.session.get("tema_container"),
                    border_radius=20,
                    padding=25,
                    alignment=ft.alignment.center,
                    on_click=gerar_relatorio,
                ),
            ],
        )
        # Botão de alternância de tema
        def alternar_tema(e):
            if page.theme_mode == ft.ThemeMode.LIGHT:
                page.theme_mode = ft.ThemeMode.DARK
                page.bgcolor = "#121212"
                page.session.set("tema_botao", "#3A3A3C")
                page.session.set("tema_container", "#2C2C2E")
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                page.bgcolor = "#007AFF"
                page.session.set("tema_botao", "#007AFF")
                page.session.set("tema_container", "white")
            voltar_ao_menu()
            page.update()
        theme_toggle = ft.ElevatedButton(
            text="Alternar tema",
            icon=ft.Icons.BRIGHTNESS_6_OUTLINED,
            on_click=alternar_tema,
            bgcolor=page.session.get("tema_botao") or ("#3A3A3C" if page.theme_mode == ft.ThemeMode.DARK else "#007AFF"),
            color="white",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(14, 10, 14, 10),
                overlay_color="#339CFF",
            ),
        )
        container = ft.Container(
            content=ft.Column([gif, titulo, botoes], spacing=50, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=page.session.get("tema_container") or "white",
            border_radius=20,
            padding=40,
            alignment=ft.alignment.center,
            width=min(page.window_width * 0.8, 500),
            expand=False,
            shadow=None,
        )
        col = ft.Column(
            [
                ft.Row(
                    [theme_toggle],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Row(
                    [container],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    height=page.window_height,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        return col

    def cadastrar_emprestimo():
        livro = criar_textfield("Nome do Livro")
        aluno = criar_textfield("Nome do Aluno")
        data = criar_textfield("Data do Empréstimo (DD/MM/AAAA)")

        def salvar_emprestimo(e):
            if not livro.value or not aluno.value or not data.value:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha todos os campos."))
                page.snack_bar.open = True
                page.update()
                return
            emprestimos.append({
                "livro": livro.value.strip(),
                "aluno": aluno.value.strip(),
                "data": data.value.strip()
            })
            salvar_csv("emprestimos.csv", emprestimos, ["livro", "aluno", "data"])
            dialog.title = ft.Text("Sucesso")
            dialog.content = ft.Text("Empréstimo cadastrado com sucesso!")
            dialog.open = True
            page.dialog = dialog
            page.update()
            voltar_ao_menu()

        gif = ft.Image(
            src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3bDAya2p3eGllNjhta2FuZWhwZmRiMjR5NTc5OG00ZXFqdWZuODEwaiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/toSMxU7Mguxnq/giphy.gif",
            width=200,
            height=200,
            border_radius=20,
            fit=ft.ImageFit.COVER,
        )
        titulo = ft.Text(
            "Cadastrar Empréstimo",
            size=26,
            weight=ft.FontWeight.BOLD,
            color=cor_texto(),
            text_align=ft.TextAlign.CENTER,
        )

        btn_salvar = criar_botao("Salvar", salvar_emprestimo)
        btn_voltar = criar_botao("Voltar ao Menu", voltar_ao_menu, cor_fundo="red")

        form = ft.Column(
            [gif, titulo, livro, aluno, data, btn_salvar, btn_voltar],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        container = ft.Container(
            content=form,
            bgcolor=page.session.get("tema_container") or "white",
            border_radius=20,
            padding=40,
            alignment=ft.alignment.center,
            width=min(page.window_width * 0.8, 500),
            expand=False,
        )

        # Animação suave de fade
        page.controls.clear()
        col = ft.Column(
            [
                ft.Row(
                    [container],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    height=page.window_height,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        col.opacity = 0
        page.add(col)
        col.animate_opacity = ft.Animation(400, "easeOut")
        col.opacity = 1
        page.update()

    def avaliar_livro():
        # Dropdowns para usuário e livro, baseados em emprestimos
        if emprestimos:
            usuario_options = [ft.dropdown.Option(emp["aluno"]) for emp in emprestimos]
            livro_options = [ft.dropdown.Option(emp["livro"]) for emp in emprestimos]
        else:
            usuario_options = [ft.dropdown.Option("Nenhum empréstimo cadastrado")]
            livro_options = [ft.dropdown.Option("Nenhum empréstimo cadastrado")]

        usuario_dropdown = ft.Dropdown(
            label="Nome do Usuário",
            options=usuario_options,
            width=min(page.window_width * 0.8, 500),
        )
        livro_dropdown = ft.Dropdown(
            label="Livro",
            options=livro_options,
            width=min(page.window_width * 0.8, 500),
        )
        avaliacao = criar_textfield("Nota (0-5)")
        comentarios = criar_textfield("Comentários", multiline=True)

        def salvar_avaliacao(e):
            if not usuario_dropdown.value or not livro_dropdown.value or not avaliacao.value:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha os campos obrigatórios."))
                page.snack_bar.open = True
                page.update()
                return
            # Não permite selecionar placeholder como valor válido
            if usuario_dropdown.value == "Nenhum empréstimo cadastrado" or livro_dropdown.value == "Nenhum empréstimo cadastrado":
                page.snack_bar = ft.SnackBar(ft.Text("Não há empréstimos cadastrados para avaliar."))
                page.snack_bar.open = True
                page.update()
                return
            try:
                nota_txt = avaliacao.value.replace(',', '.').strip()
                nota_float = float(nota_txt)
                if nota_float < 0 or nota_float > 5:
                    raise ValueError
            except:
                page.snack_bar = ft.SnackBar(ft.Text("Nota deve ser um número entre 0 e 5."))
                page.snack_bar.open = True
                page.update()
                return
            usuario = usuario_dropdown.value.strip()
            livro_avaliado = livro_dropdown.value.strip()
            # Verifica se o usuário realmente pegou o livro emprestado
            encontrado = any(emp for emp in emprestimos if emp["livro"].lower() == livro_avaliado.lower() and emp["aluno"].lower() == usuario.lower())
            if not encontrado:
                page.snack_bar = ft.SnackBar(ft.Text("Aviso: não há empréstimo registrado para esse usuário/livro. Avaliação salva mesmo assim."))
                page.snack_bar.open = True
                page.update()
            avaliacoesLivros.append({
                "usuario": usuario,
                "livro": livro_avaliado,
                "nota": nota_float,
                "comentario": comentarios.value.strip() if comentarios.value else "",
            })
            salvar_csv("avaliacoes_livros.csv", avaliacoesLivros, ["usuario", "livro", "nota", "comentario"])
            dialog.title = ft.Text("Sucesso")
            dialog.content = ft.Text("Avaliação cadastrada com sucesso!")
            dialog.open = True
            page.dialog = dialog
            page.update()
            voltar_ao_menu()

        gif = ft.Image(
            src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3d2tqamlqeXlqd2dhZWMxNHl1dTB4M2cwc21zMmhla3k0bHhjY3ZrNiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/oKVo9lyuryCqNMVN2t/giphy.gif",
            width=200,
            height=200,
            border_radius=20,
            fit=ft.ImageFit.COVER,
        )
        titulo = ft.Text(
            "Avaliar Livro",
            size=26,
            weight=ft.FontWeight.BOLD,
            color=cor_texto(),
            text_align=ft.TextAlign.CENTER,
        )

        btn_salvar = criar_botao("Salvar", salvar_avaliacao)
        btn_voltar = criar_botao("Voltar ao Menu", voltar_ao_menu, cor_fundo="red")

        form = ft.Column(
            [gif, titulo, usuario_dropdown, livro_dropdown, avaliacao, comentarios, btn_salvar, btn_voltar],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        container = ft.Container(
            content=form,
            bgcolor=page.session.get("tema_container") or "white",
            border_radius=20,
            padding=40,
            alignment=ft.alignment.center,
            width=min(page.window_width * 0.8, 500),
            expand=False,
        )

        # Animação suave de fade
        page.controls.clear()
        col = ft.Column(
            [
                ft.Row(
                    [container],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    height=page.window_height,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        col.opacity = 0
        page.add(col)
        col.animate_opacity = ft.Animation(400, "easeOut")
        col.opacity = 1
        page.update()

    def avaliar_atendimento():
        # Dropdown para usuário baseado em emprestimos
        if emprestimos:
            usuario_options = [ft.dropdown.Option(emp["aluno"]) for emp in emprestimos]
        else:
            usuario_options = [ft.dropdown.Option("Nenhum empréstimo cadastrado")]

        usuario_dropdown = ft.Dropdown(
            label="Nome do Usuário",
            options=usuario_options,
            width=min(page.window_width * 0.8, 500),
        )
        nota = criar_textfield("Nota (0-10)")
        comentario = criar_textfield("Comentários", multiline=True)

        def salvar_atendimento(e):
            if not usuario_dropdown.value or not nota.value:
                page.snack_bar = ft.SnackBar(ft.Text("Por favor, preencha os campos obrigatórios."))
                page.snack_bar.open = True
                page.update()
                return
            if usuario_dropdown.value == "Nenhum empréstimo cadastrado":
                page.snack_bar = ft.SnackBar(ft.Text("Não há empréstimos cadastrados para avaliar atendimento."))
                page.snack_bar.open = True
                page.update()
                return
            try:
                nota_int = int(nota.value)
                if nota_int < 0 or nota_int > 10:
                    raise ValueError
            except:
                page.snack_bar = ft.SnackBar(ft.Text("Nota deve ser um número inteiro entre 0 e 10."))
                page.snack_bar.open = True
                page.update()
                return
            avaliacoesBiblioteca.append({
                "usuario": usuario_dropdown.value.strip(),
                "nota": nota_int,
                "comentario": comentario.value.strip() if comentario.value else "",
            })
            salvar_csv("avaliacoes_atendimento.csv", avaliacoesBiblioteca, ["usuario", "nota", "comentario"])
            dialog.title = ft.Text("Sucesso")
            dialog.content = ft.Text("Avaliação cadastrada com sucesso!")
            dialog.open = True
            page.dialog = dialog
            page.update()
            voltar_ao_menu()

        gif = ft.Image(
            src="https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3aHh4MXl3eTh0NWh5NW0zamtjNDU3NDBmcnlobG9nMXZpd2R1eGQ1ZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Ue4dqNqYHBepmsqkbN/giphy.gif",
            width=200,
            height=200,
            border_radius=20,
            fit=ft.ImageFit.COVER,
        )
        titulo = ft.Text(
            "Avaliar Atendimento",
            size=26,
            weight=ft.FontWeight.BOLD,
            color=cor_texto(),
            text_align=ft.TextAlign.CENTER,
        )

        btn_salvar = criar_botao("Salvar", salvar_atendimento)
        btn_voltar = criar_botao("Voltar ao Menu", voltar_ao_menu, cor_fundo="red")

        form = ft.Column(
            [gif, titulo, usuario_dropdown, nota, comentario, btn_salvar, btn_voltar],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        container = ft.Container(
            content=form,
            bgcolor=page.session.get("tema_container") or "white",
            border_radius=20,
            padding=40,
            alignment=ft.alignment.center,
            width=min(page.window_width * 0.8, 500),
            expand=False,
        )

        # Animação suave de fade
        page.controls.clear()
        col = ft.Column(
            [
                ft.Row(
                    [container],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    height=page.window_height,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        col.opacity = 0
        page.add(col)
        col.animate_opacity = ft.Animation(400, "easeOut")
        col.opacity = 1
        page.update()

    def gerar_relatorio(e=None):
        # GIF centralizado no topo
        gif = ft.Image(
            src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDdpOGgxeDlyMXIzNHRnaHpsdzI3eXVnNHlzOXBlbDFtbWVvaGM5dCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/l0HlMEi55YsfXyzMk/giphy.gif",
            width=180,
            height=180,
            border_radius=20,
            fit=ft.ImageFit.COVER,
        )

        titulo = ft.Text(
            "Relatório Completo",
            size=26,
            weight=ft.FontWeight.BOLD,
            color=cor_texto(),
            text_align=ft.TextAlign.CENTER,
            font_family="Poppins",
            italic=True,
        )

        def criar_card(titulo_texto, conteudo_widgets):
            cabecalho = ft.Text(
                titulo_texto,
                size=18,
                weight=ft.FontWeight.BOLD,
                color=cor_texto(),
                font_family="Poppins",
            )
            # Definir cor de fundo levemente acinzentada (claro) ou mais escura (escuro)
            if page.theme_mode == ft.ThemeMode.DARK:
                card_bgcolor = "#232325"
            else:
                card_bgcolor = "#F4F4F7"
            card_container = ft.Container(
                content=ft.Column(conteudo_widgets, spacing=8),
                bgcolor=card_bgcolor,
                padding=20,
                border_radius=15,
                width=min(page.window_width * 0.84, 500),
                expand=False,
                margin=ft.Margin(0, 10, 0, 10),
                shadow=ft.BoxShadow(blur_radius=8, color="#00000020", offset=ft.Offset(0, 2)),
            )
            # Retorna o cabeçalho acima do container, alinhando à esquerda
            return ft.Column([cabecalho, card_container], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.START)

        # Empréstimos
        emprestimos_widgets = []
        if emprestimos:
            for i, emp in enumerate(emprestimos, start=1):
                emprestimos_widgets.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=ft.Icons.BOOK_OUTLINED, color=cor_texto(), size=20),
                            ft.Column([
                                ft.Text(f"📘 {emp['livro']}", size=15, weight=ft.FontWeight.BOLD, color=cor_texto()),
                                ft.Text(f"👤 {emp['aluno']}  |  📅 {emp['data']}", size=13, color=cor_texto())
                            ], spacing=2)
                        ]),
                        padding=10,
                        bgcolor="#FFFFFF10" if page.theme_mode == ft.ThemeMode.DARK else "#F9F9F9",
                        border_radius=10,
                        margin=ft.Margin(0, 4, 0, 4),
                    )
                )
        else:
            emprestimos_widgets.append(
                ft.Text("Nenhum empréstimo registrado.", size=14, color=cor_texto(), font_family="Poppins")
            )

        # Avaliações de Livros
        avaliacoes_livros_widgets = []
        if avaliacoesLivros:
            for i, av in enumerate(avaliacoesLivros, start=1):
                avaliacoes_livros_widgets.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=ft.Icons.STAR_OUTLINE, color="#FFD700", size=20),
                            ft.Column([
                                ft.Text(f"📖 {av['livro']} ({av['nota']}/5)", size=15, weight=ft.FontWeight.BOLD, color=cor_texto()),
                                ft.Text(f"👤 {av['usuario']}", size=13, color=cor_texto()),
                                ft.Text(f"💬 {av['comentario']}", size=12, color=cor_texto(), italic=True),
                            ], spacing=2)
                        ]),
                        padding=10,
                        bgcolor="#FFFFFF10" if page.theme_mode == ft.ThemeMode.DARK else "#F9F9F9",
                        border_radius=10,
                        margin=ft.Margin(0, 4, 0, 4),
                    )
                )
        else:
            avaliacoes_livros_widgets.append(
                ft.Text("Nenhuma avaliação de livro registrada.", size=14, color=cor_texto(), font_family="Poppins")
            )

        # Avaliações de Atendimento
        avaliacoes_atendimento_widgets = []
        if avaliacoesBiblioteca:
            for i, av in enumerate(avaliacoesBiblioteca, start=1):
                avaliacoes_atendimento_widgets.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(name=ft.Icons.SUPPORT_AGENT, color="#0A84FF", size=20),
                            ft.Column([
                                ft.Text(f"👤 {av['usuario']}  |  ⭐ {av['nota']}/10", size=15, weight=ft.FontWeight.BOLD, color=cor_texto()),
                                ft.Text(f"💬 {av['comentario']}", size=12, color=cor_texto(), italic=True),
                            ], spacing=2)
                        ]),
                        padding=10,
                        bgcolor="#FFFFFF10" if page.theme_mode == ft.ThemeMode.DARK else "#F9F9F9",
                        border_radius=10,
                        margin=ft.Margin(0, 4, 0, 4),
                    )
                )
        else:
            avaliacoes_atendimento_widgets.append(
                ft.Text("Nenhuma avaliação de atendimento registrada.", size=14, color=cor_texto(), font_family="Poppins")
            )

        card_emprestimos = criar_card("Empréstimos", emprestimos_widgets)
        card_avaliacoes_livros = criar_card("Avaliações de Livros", avaliacoes_livros_widgets)
        card_avaliacoes_atendimento = criar_card("Avaliações de Atendimento", avaliacoes_atendimento_widgets)

        btn_voltar = criar_botao("Voltar ao Menu", voltar_ao_menu, cor_fundo="red")

        # Divider para separação visual
        divider = ft.Divider(height=10, thickness=1, color="#CCCCCC40")

        # Conteúdo centralizado estilo cartão, com divisores suaves entre cards principais
        conteudo = ft.Column(
            [
                gif,
                titulo,
                card_emprestimos,
                divider,
                card_avaliacoes_livros,
                divider,
                card_avaliacoes_atendimento,
                btn_voltar,
            ],
            spacing=30,  # espaço maior acima do botão
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=min(page.window_width * 0.9, 500),
            expand=False,
        )
        # Centralizar título
        conteudo.spacing = 25
        conteudo.controls[1].text_align = ft.TextAlign.CENTER

        container = ft.Container(
            content=ft.Column(
                [conteudo],
                scroll=ft.ScrollMode.AUTO,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=page.session.get("tema_container") or "white",
            border_radius=20,
            padding=40,
            alignment=ft.alignment.center,
            width=min(page.window_width * 0.98, 540),
            expand=False,
            shadow=None,
        )

        # Animação suave de fade e centralização vertical/horizontal
        print("Gerando relatório...")
        page.controls.clear()
        page.update()
        col = ft.Column(
            [
                ft.Row(
                    [container],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                    height=page.window_height,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        col.opacity = 0
        page.add(col)
        col.animate_opacity = ft.Animation(400, "easeOut")
        col.opacity = 1
        page.update()

    voltar_ao_menu()  # Inicializa com o menu principal

if __name__ == "__main__":
    ft.app(target=main)
