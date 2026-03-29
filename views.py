import psutil
from rich.panel import Panel
from rich.table import Table
from rich.progress import ProgressBar
from rich.text import Text
from rich import box


def view_resumo(data_cache):
    """
    Recebe o dicionário completo e mostra os dois indicadores principais.
    """
    table = Table.grid(expand=True)
    table.add_column(width=10)
    table.add_column(ratio=1)
    
    # Pegamos os dados do cache (já coletados em background)
    # Calculamos a média da lista de CPUs para o resumo
    cpu_list = data_cache.get("cpu", [0])
    cpu_avg = sum(cpu_list) / len(cpu_list) if cpu_list else 0
    ram_pct = data_cache.get("ram").percent if data_cache.get("ram") else 0

    # Linha da CPU
    cpu_bar = ProgressBar(total=100, completed=cpu_avg, width=None)
    table.add_row(
        Text(" CPU ", style="bold cyan"),
        cpu_bar,
        Text(f" {cpu_avg:>5.1f}%", style="bold cyan")
    )
    
    # Linha da RAM
    ram_bar = ProgressBar(total=100, completed=ram_pct, width=None)
    table.add_row(
        Text(" RAM ", style="bold magenta"),
        ram_bar,
        Text(f" {ram_pct:>5.1f}%", style="bold magenta")
    )

    return Panel(
        table, 
        title="[bold white]Resumo do Sistema[/]", 
        subtitle="[dim]Dados atualizados em tempo real[/]",
        border_style="blue",
        box=box.ROUNDED
    )

def view_cpu(usage, freq):
    #usage = psutil.cpu_percent(percpu=True, interval=1)
    #freq = psutil.cpu_freq()
    
    # Criamos a grade principal para os núcleos
    grid = Table.grid(expand=True)
    grid.add_column(ratio=1) # Esquerda
    grid.add_column(ratio=1) # Direita
    
    num_cores = len(usage)
    half = (num_cores + 1) // 2
    
    for i in range(half):
        left_idx = i
        right_idx = i + half if i + half < num_cores else None
        
        # Helper para criar a mini-tabela de cada núcleo
        def create_core_row(idx, pct):
            if idx is None: return ""
            
            color = "green" if pct < 50 else "yellow" if pct < 80 else "red"
            
            # Criamos uma tabela interna para alinhar: Texto | Barra | Porcentagem
            core_table = Table.grid(expand=True)
            core_table.add_column(width=7)  # "CPU 0 "
            core_table.add_column(ratio=1)  # Barra
            core_table.add_column(width=7, justify="right") # " 50.0%"
            
            core_table.add_row(
                Text(f"CPU{idx:<2}", style="dim"),
                ProgressBar(total=100, completed=pct, width=None, pulse=False),
                Text(f"{pct:>5.1f}%", style=f"bold {color}")
            )
            return core_table

        grid.add_row(
            create_core_row(left_idx, usage[left_idx]),
            create_core_row(right_idx, usage[right_idx] if right_idx is not None else None)
        )

    # Rodapé com frequência
    freq_str = f"{freq.current:.0f}MHz" if freq and freq.current else "N/A"
    
    # Layout final combinando Grid + Frequência
    main_layout = Table.grid(expand=True)
    main_layout.add_row(grid)
    main_layout.add_row(Text(f"\nFrequência Atual: {freq_str}", style="dim magenta", justify="center"))

    return Panel(
        main_layout,
        title="[bold green]Processador[/]",
        border_style="green",
        box=box.ROUNDED
    )
def view_ram(ram):
    #ram = psutil.virtual_memory()
    bar_width = 30
    filled = int(ram.percent / 100 * bar_width)
    bar = "█" * filled + "░" * (bar_width - filled)
    return Panel(f"Uso: {ram.percent}%\n[{bar}]\n\nTotal: {ram.total/1024**3:.1f}GB\nLivre: {ram.available/1024**3:.1f}GB", title="Detalhes RAM")

def view_disco(disco):
    """
    Recebe o objeto psutil.disk_usage('/') do cache.
    """
    if not disco:
        return Panel("Carregando dados do disco...", title="Disco")

    # Cores baseadas no perigo (enchendo o disco)
    pct = disco.percent
    color = "green" if pct < 70 else "yellow" if pct < 90 else "red"
    
    # Criamos uma grade para organizar as informações
    grid = Table.grid(expand=True)
    grid.add_column(ratio=1)
    
    # Linha 1: Barra de Progresso Grande
    bar = ProgressBar(total=100, completed=pct, width=None)
    
    # Linha 2: Estatísticas detalhadas em colunas
    stats_table = Table.grid(expand=True)
    stats_table.add_column(justify="left", ratio=1)
    stats_table.add_column(justify="center", ratio=1)
    stats_table.add_column(justify="right", ratio=1)
    
    stats_table.add_row(
        Text(f"Total: {disco.total/1024**3:.1f} GB", style="dim cyan"),
        Text(f"Usado: {disco.used/1024**3:.1f} GB ({pct}%)", style=f"bold {color}"),
        Text(f"Livre: {disco.free/1024**3:.1f} GB", style="dim green")
    )

    # Montando o conteúdo do Painel
    content = Table.grid(expand=True)
    content.add_row(Text("Partição Raiz (/)", style="bold white"))
    content.add_row(Text("")) # Espaçador
    content.add_row(bar)      # Barra visual
    content.add_row(Text("")) # Espaçador
    content.add_row(stats_table)

    return Panel(
        content,
        title="[bold yellow]Armazenamento[/]",
        border_style="yellow",
        box=box.ROUNDED,
        padding=(1, 2)
    )

def view_rede(net):
    if not net:
        return Panel("Carregando rede...")

    grid = Table.grid(expand=True)
    grid.add_column(width=15)
    grid.add_column(ratio=1)

    # Formatação de bytes para MB/GB
    sent = net.bytes_sent / 1024**2
    recv = net.bytes_recv / 1024**2

    grid.add_row(
        Text("📥 Download", style="bold green"),
        Text(f"{recv:.2f} MB", style="green")
    )
    grid.add_row(
        Text("📤 Upload", style="bold blue"),
        Text(f"{sent:.2f} MB", style="blue")
    )

    return Panel(grid, title="[bold cyan]Tráfego de Rede[/]", border_style="cyan", box=box.ROUNDED)