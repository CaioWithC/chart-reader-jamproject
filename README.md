# chart-reader-jamproject <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
Calculador de dificuldade baseado em um arquivo .chart, com o resultado saindo com um contador de estrelas e patterns dividido entre ALL HOPOs e ALL STRUMs (+ .txt com os mesmo resultados)

# Usage
```python
python.exe file.py (nome_do_arquivo).chart
```
num CMD ou Terminal e.g: ``python.exe file.py example_chart.chart``  

Ou arraste o .chart em cima do .py

<details>
  <summary>
    Detalhes Resumidos
  </summary>
<h3>Funcionalidades</h3><br>
  
- Leitura de Chart<br>
- Lê arquivos .chart diretamente<br>

#### Suporta:<br>
  - Dados de notas (lanes e tempo)<br>
  - Resolução<br>
  - Mudanças de BPM (SyncTrack)<br>

#### Sistema de Tempo Preciso<br>
  - Converte ticks em tempo real usando mudanças de BPM<br>
  - Garante espaçamento correto das notas e cálculos de velocidade<br>

### Classificação de Notas<br>
  Diferencia entre:<br>
  - Notas de strum (maior dificuldade)<br>
  - Notas HOPO (tap) (menor dificuldade)<br>
  - Usa limites de tempo para determinar o estilo de execução<br>

### Detecção de Padrões<br>
Detecta padrões comuns de jogos de ritmo que afetam a dificuldade:<br>
  - Trills (notas alternadas rápidas)<br>
  - Zig-zags (saltos largos entre lanes)<br>
  - Streams (sequências rápidas consistentes)<br>
  - Chord streams (múltiplas notas ao mesmo tempo repetidamente)

### Esses padrões influenciam a classificação final de dificuldade.
---

### Sistema de Dificuldade Baseado em Esforço
#### - Calcula a dificuldade ao longo do tempo em vez de usar médias simples
#### - Foca nas partes mais difíceis do chart
### Inclui:
  - Esforço de velocidade
  - Esforço de movimentação (saltos entre lanes)

### Avaliação de Dificuldade em Dois Tipos
O sistema gera duas avaliações de dificuldade diferentes para o mesmo chart:
  - All Strums
    - Assume que todas as notas precisam ser strummadas
    - Representa o pior caso físico (mais difícil)
  - All HOPOs
    - Assume que todas as notas podem ser tocadas como HOPO/tap
    - Representa o caso mais leve (mais fácil)

</details>

---
### Exemplo de Saida:
CMD/Terminal:
<img width="720" height="179" alt="image" src="https://github.com/user-attachments/assets/45ba2523-c85f-4961-bcb3-1e6e1cada194" />


Arquivo TXT: 
<img width="310" height="602" alt="image" src="https://github.com/user-attachments/assets/866082d6-47d4-4e6e-ad24-607be0bc52dd" />

---

### Alguns Problemas Notaveis
1. A contagem de estrela de alguns charts que testei, estavam dando a media de 7~8, talvez o resultado pode ser repetitivo.
2. Contagem de Patterns podem não ser 100% precisas
3. Arquivos .osz, .osu e de Stepmania/Etterna não são lidos, por cada um desses já haverem dificuldades baseados em estrelas

---

### Feito especialmente e carinhosamente para o [JamProject](https://jamproject.net) ⸜(｡˃ ᵕ ˂ )⸝♡
> Pull Requests são bem vindos!
