import threading
from time import sleep
from rich.live import Live
import readchar
from rich.layout import Layout
from rich.panel import Panel
from views import view_resumo, view_cpu, view_ram, view_disco, view_rede
class MonitorApp:
    def __init__(self):
        self.selected_index = 0
        self.options = ["Resumo Geral", "Processador (CPU)", "Memória RAM", "Disco", "Rede"]
        self.running = True

    def get_layout(self):
        layout = Layout()
        layout.split_row(
            Layout(name="menu", size=30),
            Layout(name="conteudo")
        )
        
        menu_text = ""
        for i, opt in enumerate(self.options):
            if i == self.selected_index:
                menu_text += f"[bold reverse cyan] > {opt} [/]\n"
            else:
                menu_text += f"   {opt} \n"
        
        layout["menu"].update(Panel(menu_text, title="Menu", border_style="cyan"))
        layout["conteudo"].update(self.render_content())
        return layout

    def render_content(self):
        opt = self.options[self.selected_index]
        mapping = {
            "Resumo Geral": view_resumo,
            "Processador (CPU)": view_cpu,
            "Memória RAM": view_ram,
            "Disco": view_disco,
            "Rede": view_rede
        }
        return mapping[opt]()

    def run(self):
        # Thread para capturar o teclado sem travar a atualização da tela
        def check_input():
            while self.running:
                key = readchar.readkey()
                if key == readchar.key.UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                elif key == readchar.key.DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                elif key.lower() == 'q' or key == readchar.key.ESC:
                    self.running = False

        # Inicia a thread de input como "daemon" para fechar junto com o app
        input_thread = threading.Thread(target=check_input, daemon=True)
        input_thread.start()

        # O Live agora atualiza a tela automaticamente 4 vezes por segundo
        # independente de você apertar teclas ou não.
        with Live(self.get_layout(), refresh_per_second=0.5, screen=True) as live:
            while self.running:
                #sleep(2)  # Pequena pausa para reduzir uso de CPU
                live.update(self.get_layout())
                # O loop principal apenas mantém o Live vivo
                # psutil será chamado dentro de get_layout() -> render_content()