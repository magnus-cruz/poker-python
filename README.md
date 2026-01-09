# 🎲 Arena Texas Hold'em Poker - Aprendendo Probabilidade de Forma Divertida

## 📖 Descrição

**Arena Texas Hold'em Poker** é um simulador educacional de poker desenvolvido em Python com Pygame, criado especificamente para ajudar alunos a compreender e se apaixonar por conceitos matemáticos através da probabilidade aplicada.

O programa transforma o aprendizado de matemática em uma experiência interativa e visual, onde os estudantes podem observar em tempo real como as probabilidades mudam a cada rodada do jogo, entendendo na prática conceitos como:

- **Probabilidade condicional**: Como as chances mudam com cada carta revelada
- **Combinatória**: Quantas combinações possíveis existem em cada situação
- **Análise de dados**: Comparação de forças entre diferentes mãos
- **Estatística**: Cálculo de porcentagens e frequências de vitória

## 🎯 Objetivo Educacional

Este projeto foi desenvolvido com o propósito de tornar a matemática mais acessível e interessante para estudantes, mostrando que conceitos complexos como probabilidade e estatística estão presentes em situações do dia a dia e podem ser compreendidos de forma prática e divertida.

## ✨ Características Principais

- 🎮 **Interface Gráfica Intuitiva**: Desenvolvida com Pygame para uma experiência visual agradável
- 👥 **Modo Multiplayer Local**: Suporta até 4 jogadores simultâneos
- 📊 **Cálculo de Probabilidades em Tempo Real**: Mostra a porcentagem de chance de vitória para cada jogador
- 🃏 **Mecânicas Autênticas de Texas Hold'em**: Inclui Flop, Turn e River
- 🏆 **Sistema de Pontuação**: Acompanha o desempenho de cada jogador ao longo das rodadas
- 🔄 **Interface Responsiva**: Adapta-se a diferentes tamanhos de tela
- 🎨 **Visual Atraente**: Utiliza imagens personalizadas para cartas e fundos

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Pygame 2.0 ou superior

## 🚀 Como Instalar

1. **Clone ou baixe este repositório:**
   ```bash
   cd poker.14version
   ```

2. **Instale as dependências:**
   ```bash
   pip install pygame
   ```

3. **Certifique-se de que as pastas de recursos estão presentes:**
   - `cartas/` - Contém as imagens das 52 cartas do baralho
   - `fundos/` - Contém as imagens de fundo do jogo

## 🎮 Como Jogar

1. **Execute o programa:**
   ```bash
   python main.py
   ```

2. **Tela Inicial:**
   - Pressione qualquer tecla para começar

3. **Cadastro de Jogadores:**
   - Digite o nome de cada um dos 4 jogadores
   - Pressione ENTER após cada nome

4. **Durante o Jogo:**
   - **Pressione qualquer tecla** para avançar pelas etapas:
     - Distribuição de cartas iniciais
     - Flop (3 cartas comunitárias)
     - Turn (4ª carta comunitária)
     - River (5ª carta comunitária)
     - Avaliação final e determinação do vencedor
   
5. **Controles:**
   - `QUALQUER TECLA` - Avança para a próxima etapa
   - `ESC` - Sai do jogo
   - A janela é **redimensionável** - arraste para ajustar o tamanho

## 📊 Compreendendo as Informações na Tela

Durante o jogo, cada jogador verá:

- **Nome do Jogador**: Identificação do participante
- **Cartas da Mão**: Duas cartas privadas de cada jogador
- **Cartas Comunitárias**: Até 5 cartas compartilhadas no centro da mesa
- **Tipo de Mão**: Nome da combinação formada (Par, Trinca, Flush, etc.)
- **Pontos**: Número de rodadas vencidas
- **Probabilidade (Prob)**: Porcentagem que representa a força relativa da mão em comparação aos outros jogadores

### 🎯 Hierarquia das Mãos (da mais forte para a mais fraca):

1. **Straight Flush** - Sequência do mesmo naipe
2. **Quadra** - Quatro cartas do mesmo valor
3. **Full House** - Trinca + Par
4. **Flush** - Cinco cartas do mesmo naipe
5. **Straight** - Sequência de cinco cartas
6. **Trinca** - Três cartas do mesmo valor
7. **Dois Pares** - Dois pares de cartas
8. **Um Par** - Duas cartas do mesmo valor
9. **Carta Alta** - Nenhuma combinação

## 🧮 Conceitos Matemáticos Explorados

### 1. Probabilidade Básica
O jogo calcula e exibe a probabilidade de vitória de cada jogador com base na força da mão atual.

### 2. Probabilidade Condicional
A cada carta revelada (Flop, Turn, River), as probabilidades são recalculadas, demonstrando como novas informações afetam as chances.

### 3. Combinatória
O programa avalia milhares de combinações possíveis para determinar a melhor mão de 5 cartas entre as 7 disponíveis (2 da mão + 5 comunitárias).

### 4. Análise Comparativa
Os alunos podem observar como diferentes mãos se comparam em termos de força relativa.

## 🎓 Sugestões de Uso em Sala de Aula

1. **Exercício de Observação**: Peça aos alunos para anotarem as probabilidades a cada rodada e observarem como elas mudam

2. **Cálculo Manual**: Desafie os estudantes a calcularem manualmente as probabilidades e compararem com o programa

3. **Análise Estatística**: Após várias rodadas, analise qual tipo de mão aparece com mais frequência

4. **Simulação de Cenários**: Pause o jogo em momentos específicos e discuta as possibilidades matemáticas

5. **Projeto de Extensão**: Incentive os alunos a modificarem o código para adicionar novas funcionalidades

## 🛠️ Estrutura do Código

```
poker.14version/
│
├── main.py              # Código principal do jogo
├── README.md            # Este arquivo
│
├── cartas/              # Imagens das cartas (52 cartas)
│   ├── 2C.png
│   ├── 2E.png
│   └── ...
│
└── fundos/              # Imagens de fundo
    ├── fundo_inicial.png
    ├── fundo_mesa.png
    └── fundo_nomes.png
```

## 🔧 Personalizações Possíveis

O código foi desenvolvido de forma modular para facilitar personalizações:

- Alterar o número de jogadores
- Modificar o sistema de pontuação
- Adicionar novos modos de jogo
- Incluir histórico de jogadas
- Implementar análises estatísticas mais detalhadas
- Adicionar sons e efeitos

## 🤝 Contribuindo

Este é um projeto educacional aberto a melhorias! Sugestões de aprimoramento incluem:

- Sistema de dicas probabilísticas para iniciantes
- Modo de treinamento com explicações matemáticas
- Gráficos de evolução de probabilidades
- Exportação de dados para análise em planilhas
- Modo de jogo contra IA com diferentes níveis

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais.

## 👨‍🏫 Para Educadores

Este programa pode ser utilizado como:

- **Atividade Prática**: Complemento para aulas de probabilidade e estatística
- **Projeto de Programação**: Exemplo para ensinar Python e Pygame
- **Ferramenta de Demonstração**: Visualização de conceitos matemáticos abstratos
- **Trabalho em Grupo**: Base para projetos colaborativos de programação

## 🎮 Dicas para Iniciantes em Poker

Se você nunca jogou poker, não se preocupe! O objetivo educacional é entender a matemática, não se tornar um jogador profissional. O jogo é simples:

1. Cada jogador recebe 2 cartas privadas
2. São reveladas 5 cartas comunitárias em etapas
3. O objetivo é formar a melhor combinação de 5 cartas
4. Quem tiver a melhor mão vence!

---

**Desenvolvido com 💙 para tornar a matemática mais divertida e acessível!**

*Versão 1.4 - Janeiro 2026*
