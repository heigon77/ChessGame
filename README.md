# ChessGame

Esse projeto é uma base para se implementar uma engine de xadrez em python utilizando as libs pygame, chess e chessdotcom.  

**pygame**: Utilizado para implementação de jogos simples em 2D.   
**chess**: Utilizado para implementar tabuleiro e jogos de xadrez.   
**chessdotcom**: Realiza a conexão com a API do site chess.com e posui métodos para requisitar diversos dados, como puzzles e jogos.  

No diretório Game temos os principais arquivos.  
O arquivo ChessMain.py possui a implementação base do jogo de xadrez de um player contra uma engine. Pode iniciar um jogo novo ou começar de uma posição definida através da notação FEN.   
O arquivo DumbChessEngine.py escolhe um movimento legal aleatório de uma posição de um tabuleiro de xadrez e o DailyPuzzle.py requisita aleatóriamente um dos puzzles diários  do chess.com