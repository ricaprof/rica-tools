import threading
from time import sleep
import psutil
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich import box
from rich.text import Text
import readchar
from datetime import datetime

# Importação das suas views
from views import view_resumo, view_cpu, view_ram, view_disco, view_rede

class MonitorApp:
    def __init__(self):
        self.selected_index = 0
        self.options = ["Resumo Geral", "Processador (CPU)", "Memória RAM", "Disco", "Rede"]
        self.running = True
        
        # Cache de dados para evitar IO Blocking
        self.data_cache = {
            "cpu": [], "ram": None, "disco": None, "rede": None, "freq": None
        }
        
        # Inicializa dados para não abrir vazio
        self._update_data()

    def _update_data(self):
        """Coleta dados do sistema de forma rápida"""
        self.data_cache["cpu"] = psutil.cpu_percent(percpu=True)
        self.data_cache["ram"] = psutil.virtual_memory()
        self.data_cache["disco"] = psutil.disk_usage('/')
        self.data_cache["rede"] = psutil.net_io_counters()
        self.data_cache["freq"] = psutil.cpu_freq()

    def _background_collector(self):
        """Thread 1: Atualiza o hardware a cada 1 segundo"""
        while self.running:
            self._update_data()
            sleep(1)

    def _input_handler(self):
        """Thread 2: Captura teclas sem travar a tela"""
        while self.running:
            key = readchar.readkey()
            if key == readchar.key.UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif key == readchar.key.DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif key.lower() == 'q' or key == readchar.key.ESC:
                self.running = False
                #print("Desligando")

    def render_content(self):
        """Decide o que desenhar com base na seleção e nos dados do cache"""
        opt = self.options[self.selected_index]
        
        # Mapeamento para as funções do views.py
        # Passamos os dados do cache como argumentos
        if opt == "Resumo Geral":
            return view_resumo(self.data_cache)
        elif opt == "Processador (CPU)":
            return view_cpu(self.data_cache["cpu"], self.data_cache["freq"])
        elif opt == "Memória RAM":
            return view_ram(self.data_cache["ram"])
        elif opt == "Disco":
            return view_disco(self.data_cache["disco"])
        elif opt == "Rede":
            return view_rede(self.data_cache["rede"])
        
        return Panel("Selecione uma opção válida.")

    def get_layout(self):
        layout = Layout()
        
        # Divide a tela em 3 partes verticais
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Divide o corpo em Menu e Conteúdo
        layout["body"].split_row(
            Layout(name="menu", size=30),
            Layout(name="conteudo")
        )

        # 1. Renderização do Header (Relógio + Título)
        hora_atual = datetime.now().strftime("%H:%M:%S")
        layout["header"].update(
            Panel(
                f"[bold cyan]RICA-MONITOR v1.0[/] | [dim]Sistema Ativo[/] [bold white]—[/] [yellow]{hora_atual}[/]",
                border_style="blue",
                box=box.ROUNDED
            )
        )

        # 2. Renderização do Menu Lateral
        menu_items = []
        for i, opt in enumerate(self.options):
            if i == self.selected_index:
                menu_items.append(f"[bold reverse cyan] > {opt} [/]")
            else:
                menu_items.append(f"   {opt} ")
        layout["menu"].update(Panel("\n".join(menu_items), title="Menu", border_style="cyan"))

        # 3. Conteúdo Central (Chama as views)
        layout["conteudo"].update(self.render_content())

        # 4. Renderização do Footer (Atalhos)
        footer_text = Text.assemble(
            (" ARROWS ", "bold black on cyan"), " Navegar  ",
            (" Q ", "bold black on red"), " Sair  ",
            (" ESC ", "bold black on white"), " Fechar ",
            justify="center"
        )
        layout["footer"].update(Panel(footer_text, border_style="dim"))

        return layout

    def run(self):
        """Loop principal de renderização"""
        # Inicia as threads de suporte
        threading.Thread(target=self._background_collector, daemon=True).start()
        threading.Thread(target=self._input_handler, daemon=True).start()

        # O Live gerencia a tela. screen=True cria o efeito de 'App' (limpa o terminal ao sair)
        # refresh_per_second controla a fluidez da interface
        with Live(self.get_layout(), refresh_per_second=10, screen=True) as live:
            while self.running:
                # O loop principal agora apenas redesenha a tela com os dados mais recentes
                live.update(self.get_layout())
                sleep(0.1) # Taxa de atualização da interface (100ms)

if __name__ == "__main__":
    app = MonitorApp()
    app.run()