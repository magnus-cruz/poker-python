# poker_game.py
import random
import os
import pygame
import sys
from collections import Counter

# ===========================
# Inicializacao do Pygame
# ===========================
pygame.init()

# Configurações de tela ajustáveis
BASE_WIDTH, BASE_HEIGHT = 800, 600
CURRENT_WIDTH, CURRENT_HEIGHT = BASE_WIDTH, BASE_HEIGHT

def get_scale_factor():
    """Retorna o fator de escala baseado no tamanho atual da tela"""
    return min(CURRENT_WIDTH / BASE_WIDTH, CURRENT_HEIGHT / BASE_HEIGHT)

def scale_pos(x, y):
    """Escala uma posição baseada no fator de escala atual"""
    scale = get_scale_factor()
    return int(x * scale), int(y * scale)

def scale_size(width, height):
    """Escala um tamanho baseado no fator de escala atual"""
    scale = get_scale_factor()
    return int(width * scale), int(height * scale)

SCREEN = pygame.display.set_mode((CURRENT_WIDTH, CURRENT_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(" Arena Texas Hold'em Poker")

def load_scaled_font():
    """Carrega uma fonte escalada baseada no tamanho da tela"""
    scale = get_scale_factor()
    font_size = max(int(36 * scale), 12)  # Mínimo de 12px
    return pygame.font.SysFont(None, font_size)

FONT = load_scaled_font()

def load_scaled_image(path, default_size=None):
    """Carrega uma imagem escalada para o tamanho atual da tela com alta qualidade"""
    try:
        img = pygame.image.load(path).convert_alpha()
        if default_size:
            img = pygame.transform.smoothscale(img, default_size)
        # Escala a imagem para o tamanho atual da tela com suavização
        scale = get_scale_factor()
        new_width = int(img.get_width() * scale)
        new_height = int(img.get_height() * scale)
        return pygame.transform.smoothscale(img, (new_width, new_height))
    except:
        # Retorna uma superfície padrão se não conseguir carregar
        if default_size:
            width, height = scale_size(*default_size)
        else:
            width, height = scale_size(CURRENT_WIDTH, CURRENT_HEIGHT)
        surf = pygame.Surface((width, height))
        surf.fill((50, 50, 100))
        return surf

# Carregamento das imagens de fundo
FUNDO_INICIAL = None
FUNDO_MESA = None
FUNDO_NOMES = None

def load_backgrounds():
    """Carrega os fundos escalados"""
    global FUNDO_INICIAL, FUNDO_MESA, FUNDO_NOMES
    FUNDO_INICIAL = load_scaled_image('fundos/fundo_inicial.png', (BASE_WIDTH, BASE_HEIGHT))
    FUNDO_MESA = load_scaled_image('fundos/fundo_mesa.png', (BASE_WIDTH, BASE_HEIGHT))
    FUNDO_NOMES = load_scaled_image('fundos/fundo_nomes.png', (BASE_WIDTH, BASE_HEIGHT))

load_backgrounds()

# ===========================
# Constantes e Cores
# ===========================
BRANCO = (255, 255, 255)
AZUL = (70, 130, 180)
VERMELHO = (255, 100, 100)
PRETO = (0, 0, 0)

def get_positions():
    """Retorna as posições dos jogadores escaladas para o tamanho atual"""
    # Margem mínima para maximizar o aproveitamento do espaço
    margin_x = 5   # Reduzido de 20 para 5 - o mais à esquerda possível
    margin_y = 30  # Reduzido de 50 para 30
    card_width = 72
    card_height = 96
    
    # Calculamos o espaço disponível dinamicamente
    available_width = CURRENT_WIDTH / get_scale_factor()
    
    base_positions = [
        (margin_x, margin_y),  # Jogador 1 - superior esquerdo
        (available_width - margin_x - 2 * card_width - 20, margin_y),  # Jogador 2 - superior direito  
        (margin_x, BASE_HEIGHT - margin_y - card_height - 100),  # Jogador 3 - inferior esquerdo
        (available_width - margin_x - 2 * card_width - 20, BASE_HEIGHT - margin_y - card_height - 100)  # Jogador 4 - inferior direito
    ]
    return [scale_pos(x, y) for x, y in base_positions]

# ===========================
# Classes
# ===========================
class Carta:
    BASE_WIDTH = 72
    BASE_HEIGHT = 96

    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
        self.imagem = self.carregar_imagem()

    @property
    def width(self):
        return scale_size(self.BASE_WIDTH, self.BASE_HEIGHT)[0]
    
    @property
    def height(self):
        return scale_size(self.BASE_WIDTH, self.BASE_HEIGHT)[1]

    def carregar_imagem(self):
        nome = f"{self.valor}{self.naipe[0]}.png"
        path = os.path.join('cartas', nome)
        try:
            img = pygame.image.load(path).convert_alpha()
            width, height = scale_size(self.BASE_WIDTH, self.BASE_HEIGHT)
            return pygame.transform.smoothscale(img, (width, height))
        except:
            width, height = scale_size(self.BASE_WIDTH, self.BASE_HEIGHT)
            surf = pygame.Surface((width, height))
            surf.fill((200, 200, 200))
            pygame.draw.rect(surf, PRETO, surf.get_rect(), max(1, int(2 * get_scale_factor())))
            return surf

    def valor_numerico(self):
        ordem = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                 '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return ordem[self.valor]


class Baralho:
    def __init__(self):
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        naipes = ['Copas', 'Ouros', 'Paus', 'Espadas']
        self.cartas = [Carta(v, n) for v in valores for n in naipes]
        random.shuffle(self.cartas)

    def distribuir(self):
        return self.cartas.pop() if self.cartas else None


class Jogador:
    def __init__(self, nome, position):
        self.nome = nome
        self.mao = []
        self.position = position
        self.resultado = ""
        self.mao_nome = ""
        self.pontuacao = 0
        self.probabilidade = 0.0

    def receber(self, carta):
        if carta:
            self.mao.append(carta)


class Mesa:
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.reset()

    def reset(self):
        self.baralho = Baralho()
        self.cartas_comunitarias = []
        for j in self.jogadores:
            j.mao.clear()
            j.resultado = ""
            j.mao_nome = ""
            j.probabilidade = 0.0

    def distribuir_mao(self):
        for _ in range(2):
            for j in self.jogadores:
                j.receber(self.baralho.distribuir())

    def revelar_flop(self):
        self.baralho.distribuir()
        self.cartas_comunitarias = [self.baralho.distribuir() for _ in range(3)]

    def revelar_turn(self):
        self.baralho.distribuir()
        self.cartas_comunitarias.append(self.baralho.distribuir())

    def revelar_river(self):
        self.baralho.distribuir()
        self.cartas_comunitarias.append(self.baralho.distribuir())

    def avaliar_maos(self):
        for jogador in self.jogadores:
            todas = jogador.mao + self.cartas_comunitarias
            jogador.resultado, jogador.mao_nome = avaliar_mao(todas)

        vencedores = sorted(self.jogadores, key=lambda j: j.resultado, reverse=True)
        maior_pontuacao = vencedores[0].resultado
        ganhadores = [j for j in vencedores if j.resultado == maior_pontuacao]

        for g in ganhadores:
            g.pontuacao += 1

        self.calcular_probabilidades()
        return ganhadores

    def calcular_probabilidades(self):
        total = sum(j.resultado[0] * 10 + j.resultado[1] for j in self.jogadores)
        for j in self.jogadores:
            valor = j.resultado[0] * 10 + j.resultado[1]
            j.probabilidade = round((valor / total) * 100, 1) if total > 0 else 0.0

# ===========================
# Avaliacao de Maos
# ===========================
def avaliar_mao(cartas):
    valores = [c.valor_numerico() for c in cartas]
    naipes = [c.naipe for c in cartas]
    contagem = Counter(valores)
    is_flush = any(naipes.count(n) >= 5 for n in set(naipes))
    valores_unicos = sorted(set(valores), reverse=True)

    def is_straight(vals):
        vals = sorted(set(vals))
        for i in range(len(vals) - 4):
            if vals[i + 4] - vals[i] == 4:
                return True, vals[i + 4]
        if set([14, 2, 3, 4, 5]).issubset(vals):
            return True, 5
        return False, 0

    straight, high_card = is_straight(valores_unicos)

    if straight and is_flush:
        return (8, high_card), "Straight Flush"
    quadras = [v for v, c in contagem.items() if c == 4]
    if quadras:
        return (7, quadras[0]), "Quadra"
    trincas = [v for v, c in contagem.items() if c == 3]
    pares = [v for v, c in contagem.items() if c == 2]
    if trincas and pares:
        return (6, trincas[0]), "Full House"
    if is_flush:
        return (5, max(valores)), "Flush"
    if straight:
        return (4, high_card), "Straight"
    if trincas:
        return (3, trincas[0]), "Trinca"
    if len(pares) >= 2:
        return (2, max(pares)), "Dois Pares"
    if pares:
        return (1, pares[0]), "Um par"
    return (0, max(valores)), "Carta Alta"

# ===========================
# Funcoes de Tela
# ===========================
def desenhar_texto(texto, x, y, cor=BRANCO):
    img = FONT.render(texto, True, cor)
    SCREEN.blit(img, (x, y))

def handle_resize(new_width, new_height):
    """Manipula o redimensionamento da tela"""
    global CURRENT_WIDTH, CURRENT_HEIGHT, SCREEN, FONT
    CURRENT_WIDTH, CURRENT_HEIGHT = new_width, new_height
    SCREEN = pygame.display.set_mode((CURRENT_WIDTH, CURRENT_HEIGHT), pygame.RESIZABLE)
    FONT = load_scaled_font()
    load_backgrounds()

def tela_inicial():
    while True:
        # Escala o fundo para o tamanho atual da tela com alta qualidade
        fundo_escalado = pygame.transform.smoothscale(FUNDO_INICIAL, (CURRENT_WIDTH, CURRENT_HEIGHT))
        SCREEN.blit(fundo_escalado, (0, 0))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event.w, event.h)
            if event.type == pygame.KEYDOWN:
                return


def tela_nomes():
    nomes = []
    texto_atual = ''
    while len(nomes) < 4:
        fundo_escalado = pygame.transform.smoothscale(FUNDO_NOMES, (CURRENT_WIDTH, CURRENT_HEIGHT))
        SCREEN.blit(fundo_escalado, (0, 0))
        
        # Centraliza o texto de entrada na tela
        texto_prompt = f"Digite o nome do Jogador {len(nomes) + 1}: {texto_atual}"
        texto_surface = FONT.render(texto_prompt, True, BRANCO)
        texto_rect = texto_surface.get_rect()
        texto_rect.centerx = CURRENT_WIDTH // 2
        texto_rect.centery = CURRENT_HEIGHT // 2
        SCREEN.blit(texto_surface, texto_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event.w, event.h)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and texto_atual.strip():
                    nomes.append(texto_atual.strip())
                    texto_atual = ''
                elif event.key == pygame.K_BACKSPACE:
                    texto_atual = texto_atual[:-1]
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    texto_atual += event.unicode
    return nomes


def exibir_mesa(mesa, ganhadores):
    fundo_escalado = pygame.transform.scale(FUNDO_MESA, (CURRENT_WIDTH, CURRENT_HEIGHT))
    SCREEN.blit(fundo_escalado, (0, 0))
    
    # Cartas comunitárias no centro
    if mesa.cartas_comunitarias:
        espac = int(10 * get_scale_factor())
        carta_width = mesa.cartas_comunitarias[0].width if mesa.cartas_comunitarias else scale_size(72, 96)[0]
        total = len(mesa.cartas_comunitarias) * carta_width + (len(mesa.cartas_comunitarias) - 1) * espac
        start_x = (CURRENT_WIDTH - total) // 2
        y = CURRENT_HEIGHT // 2 - (mesa.cartas_comunitarias[0].height if mesa.cartas_comunitarias else scale_size(72, 96)[1]) // 2

        for i, c in enumerate(mesa.cartas_comunitarias):
            SCREEN.blit(c.imagem, (start_x + i * (carta_width + espac), y))

    # Jogadores
    positions = get_positions()
    for idx, j in enumerate(mesa.jogadores):
        j.position = positions[idx]  # Atualiza a posição do jogador
        x0, y0 = j.position
        espac = int(10 * get_scale_factor())
        
        # Cartas do jogador
        for k, c in enumerate(j.mao):
            SCREEN.blit(c.imagem, (x0 + k * (c.width + espac), y0))
        
        # Informações do jogador - posicionamento otimizado e mais compacto
        offset_y = int(20 * get_scale_factor())  # Reduzido de 25 para 20
        line_height = int(20 * get_scale_factor())  # Reduzido de 25 para 20
        card_height = j.mao[0].height if j.mao else scale_size(72, 96)[1]
        
        # Nome do jogador
        desenhar_texto(j.nome, x0, y0 - offset_y)
        
        # Nome da mão (mais próximo das cartas)
        desenhar_texto(j.mao_nome, x0, y0 + card_height + 3, 
                      VERMELHO if j in ganhadores else BRANCO)
        
        # Pontos e probabilidade em linhas compactas
        desenhar_texto(f"Pontos: {j.pontuacao}", x0, y0 + card_height + 3 + line_height)
        desenhar_texto(f"Prob: {j.probabilidade}%", x0, y0 + card_height + 3 + 2 * line_height, AZUL)

    # Resultado centralizado no topo
    if ganhadores:
        texto = "Empate!" if len(ganhadores) > 1 else f"{ganhadores[0].nome} venceu!"
        texto_surface = FONT.render(texto, True, AZUL)
        texto_rect = texto_surface.get_rect()
        texto_rect.centerx = CURRENT_WIDTH // 2
        texto_rect.y = int(15 * get_scale_factor())  # Reduzido de 20 para 15
        SCREEN.blit(texto_surface, texto_rect)

    pygame.display.flip()


# ===========================
# Funcao Principal
# ===========================
def main():
    tela_inicial()
    nomes = tela_nomes()
    positions = get_positions()
    jogadores = [Jogador(nomes[i], positions[i]) for i in range(4)]
    mesa = Mesa(jogadores)

    etapa = 'inicio'
    ganhadores = []

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.VIDEORESIZE:
                handle_resize(event.w, event.h)
                # Recriar as cartas com o novo tamanho
                if etapa != 'inicio':
                    for jogador in mesa.jogadores:
                        for carta in jogador.mao:
                            carta.imagem = carta.carregar_imagem()
                    for carta in mesa.cartas_comunitarias:
                        carta.imagem = carta.carregar_imagem()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                elif etapa == 'inicio':
                    mesa.reset()
                    mesa.distribuir_mao()
                    etapa = 'flop'
                    ganhadores = []
                elif etapa == 'flop':
                    mesa.revelar_flop()
                    etapa = 'turn'
                elif etapa == 'turn':
                    mesa.revelar_turn()
                    etapa = 'river'
                elif etapa == 'river':
                    mesa.revelar_river()
                    ganhadores = mesa.avaliar_maos()
                    etapa = 'fim'
                elif etapa == 'fim':
                    etapa = 'inicio'

        exibir_mesa(mesa, ganhadores)

    pygame.quit()

if __name__ == '__main__':
    main()