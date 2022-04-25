# ChessGame

Esse projeto é uma base para se implementar uma engine de xadrez em python utilizando as libs pygame, python-chess e chessdotcom.  

**pygame**: Utilizado para implementação de jogos simples em 2D. [Detalhes do pygame](https://www.pygame.org/docs/)   
**python-chess**: Utilizado para implementar tabuleiro e jogos de xadrez. [Detalhes do python-chess](https://python-chess.readthedocs.io/en/latest/)   
**chessdotcom**: Realiza a conexão com a API do site [chess.com](https://www.chess.com/) e posui métodos para requisitar diversos dados, como puzzles e jogos. [Detalhes do chessdotcom](https://chesscom.readthedocs.io/en/latest/)   

No diretório [Game](https://github.com/heigon77/ChessGame/tree/master/Game) temos os principais arquivos.  
O arquivo [ChessMain.py](https://github.com/heigon77/ChessGame/blob/master/Game/ChessMain.py) possui a implementação base do jogo de xadrez de um player contra uma engine. Pode iniciar um jogo novo ou começar de uma posição definida através da notação [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation).   
O arquivo [DumbChessEngine.py](https://github.com/heigon77/ChessGame/blob/master/Game/DumbChessEngine.py) escolhe um movimento legal aleatório de uma posição de um tabuleiro de xadrez e o [DailyPuzzle.py](https://github.com/heigon77/ChessGame/blob/master/Game/DailyPuzzle.py) requisita aleatóriamente um dos puzzles diários  do chess.com    
O arquivo [EngineVsEngine.py](https://github.com/heigon77/ChessGame/blob/master/Game/EngineVsEngine.py) apenas executa 10 partidas entre duas engines, no caso, a DumbChessEngine.   

No [main.py](https://github.com/heigon77/ChessGame/blob/master/main.py) temos a inicialização do jogo, com a opção de escolher um novo jogo com as peças branca ou com as peças pretas ou começar um jogo a partir de um puzzle do chess.com.   

##Vídeo

Nesse [link](https://drive.google.com/file/d/1egYDC5uKpj0qZKllFJyJlOUHIaWYwmtc/view?usp=sharing) tem um vídeo rápido de demonstração das atuais funcionalidades. Inicia um jogo com algumas das cores contra a DumbChessEngine, inicia um jogo a partir de uma posição de um puzzle aleatório do chess.com contra a DumbChessEngine e, por fim, roda 10 partidadas entre as engines.
