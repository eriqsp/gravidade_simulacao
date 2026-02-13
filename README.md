<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/6cf493a2-13dd-4e85-99d9-a56f635da623" />

# Simulação da Gravidade Newtoniana
Nesse projeto eu simulo a gravidade descrita pela teoria de Newton usando Python, OpenGL e Pygame.


## Estrutura
- `corpo_massivo.py`: descreve um objeto massivo
- `fisica.py`: responsável por calcular o movimento dos corpos
- `simulacao.py`: script final que junta OpenGL, Pygame e a dinâmica entre objetos

## Tecnologias
- **Python** 3.9
- **OpenGL** e **Pygame** para renderização e interação com objetos
- **numpy** para lidar com vetores

## Como rodar
1. Clone o repositório:
   ```bash
   git clone https://github.com/eriqsp/gravidade_simulacao.git
   cd gravidade_simulacao
2. Instale as depedências
   ```bash
   pip install -r requirements.txt
3. Rodar simulação
   ```bash
   python simulacao.py
