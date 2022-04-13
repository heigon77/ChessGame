# ChessGame

Esse projeto é uma base para se implementar uma engine de xadrez em python utilizando as libs pygame, chess e chessdotcom.  

**pygame**: Utilizado para implementação de jogos simples em 2D.   
**chess**: Utilizado para implementar tabuleiro e jogos de xadrez.   
**chessdotcom**: Realiza a conexão com a API do site [chess.com](https://www.chess.com/) e posui métodos para requisitar diversos dados, como puzzles e jogos.  

No diretório [Game](https://github.com/heigon77/ChessGame/tree/master/Game) temos os principais arquivos.  
O arquivo [ChessMain.py](https://github.com/heigon77/ChessGame/blob/master/Game/ChessMain.py) possui a implementação base do jogo de xadrez de um player contra uma engine. Pode iniciar um jogo novo ou começar de uma posição definida através da notação [FEN](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation).   
O arquivo [DumbChessEngine.py](https://github.com/heigon77/ChessGame/blob/master/Game/DumbChessEngine.py) escolhe um movimento legal aleatório de uma posição de um tabuleiro de xadrez e o [DailyPuzzle.py](https://github.com/heigon77/ChessGame/blob/master/Game/DailyPuzzle.py) requisita aleatóriamente um dos puzzles diários  do chess.com    

No [main.py](https://github.com/heigon77/ChessGame/blob/master/main.py) temos a inicialização do jogo, com a opção de escolher um novo jogo com as peças branca ou com as peças pretas ou começar um jogo a partir de um puzzle do chess.com.
