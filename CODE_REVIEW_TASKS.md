# Revisão da base de código — problemas encontrados e tarefas sugeridas

## 1) Tarefa para corrigir erro de digitação
**Problema encontrado**
- O README orienta executar `python tps.py`, mas o arquivo existente é `tsp.py`.

**Tarefa sugerida**
- Corrigir o comando no `README.md` de `python tps.py` para `python tsp.py`.
- Validar rapidamente com uma checagem simples de existência de arquivo para evitar regressão (`test -f tsp.py`).

---

## 2) Tarefa para corrigir um bug
**Problema encontrado**
- Em `genetic_algorithm.py`, existe uma redefinição de `calculate_fitness` com assinatura diferente.
- No bloco `if __name__ == '__main__':`, a chamada `calculate_fitness(individual)` usa a assinatura antiga, o que pode causar `TypeError` ao executar o módulo diretamente.

**Tarefa sugerida**
- Renomear uma das implementações (ex.: `calculate_basic_fitness` e `calculate_constrained_fitness`) e atualizar os pontos de chamada para usar a função correta.
- Ajustar o bloco de demonstração no final do arquivo para passar todos os argumentos necessários, ou removê-lo se estiver obsoleto.
- Adicionar teste de execução mínima do caminho de demonstração para garantir que o módulo não quebre quando executado diretamente.

---

## 3) Tarefa para ajustar comentário de código/discrepância de documentação
**Problema encontrado**
- O docstring de `mutate` diz que a mutação é feita “inverting a segment”, mas a implementação atual apenas troca dois elementos adjacentes.

**Tarefa sugerida**
- Atualizar docstring/comentários para refletir o comportamento real (swap adjacente), **ou** alterar a implementação para realmente inverter um segmento, mantendo docstring e código consistentes.
- Revisar outros comentários “temporários” (ex.: debug) para evitar divergências entre intenção e comportamento.

---

## 4) Tarefa para melhorar um teste
**Problema encontrado**
- Não há suíte de testes automatizados para operadores genéticos e invariantes básicos (permutações válidas, tamanho de população, ordenação de fitness, etc.).

**Tarefa sugerida**
- Criar `tests/test_genetic_algorithm.py` com casos para:
  1. `order_crossover` preserva todos os genes sem duplicar/perder cidades.
  2. `mutate` mantém tamanho e conjunto de cidades da rota.
  3. `sort_population` retorna fitness em ordem crescente e mantém pares indivíduo/fitness corretos.
  4. `calculate_fitness` aplica penalidade quando `route[0] != start_city`.
- Executar os testes com `pytest` no CI para prevenir regressões.

