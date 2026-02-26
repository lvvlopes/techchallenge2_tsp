# Guia de Implementação — Tech Challenge Fase 2 (Projeto 2)

Este guia transforma os requisitos do enunciado em um checklist prático para o projeto **Otimização de Rotas para Distribuição de Medicamentos e Insumos**.

## Resposta direta: o que implementar x o que entregar

### O que implementar (resumo executivo)
1. **Otimizador de rotas com Algoritmo Genético** (base TSP evoluída para VRP).
2. **Restrições obrigatórias**: prioridade de entrega, capacidade, autonomia e múltiplos veículos.
3. **Visualização das rotas** com comparação entre baseline e solução otimizada.
4. **Integração com LLM** para instruções operacionais, relatórios e perguntas em linguagem natural.
5. **Qualidade de engenharia**: estrutura de projeto, logging, métricas e testes automatizados.

### O que entregar (resumo executivo)
1. **Repositório Git completo** (código + docs + scripts/notebooks de demo).
2. **Relatório técnico** cobrindo implementação, estratégias de restrições, LLM, comparativos e análises.
3. **Vídeo de demonstração** (até 15 minutos) mostrando sistema fim a fim.

---

## 1) O que implementar no sistema (escopo técnico)

### 1.1 Núcleo de otimização com Algoritmo Genético (GA)
- Adaptar o código-base de TSP para o contexto hospitalar.
- Definir representação genética da rota:
  - TSP simples: cromossomo como permutação de pontos de entrega.
  - VRP (múltiplos veículos): cromossomo com separadores de rotas por veículo ou codificação por alocação + sequência.
- Implementar operadores genéticos especializados:
  - Seleção (ex.: torneio/roleta);
  - Crossover para permutações (ex.: OX/PMX);
  - Mutação (ex.: swap, inversion, scramble).
- Implementar função de fitness multi-critério com pesos e penalidades para:
  - Distância total;
  - Prioridade das entregas (críticas vs regulares);
  - Violação de capacidade do veículo;
  - Violação de autonomia máxima;
  - (Opcional) tempo estimado e janelas de atendimento.
- Rodar experimentos com parâmetros diferentes do GA (população, taxa de mutação, gerações, elitismo) e registrar resultados.

### 1.2 Restrições realistas (obrigatórias no Projeto 2)
- Prioridades de entrega (medicamentos críticos com maior peso na função objetivo).
- Capacidade de carga de cada veículo.
- Autonomia máxima por veículo (distância máxima).
- Múltiplos veículos (evolução de TSP para VRP).
- Outras restrições relevantes (opcional, para enriquecer):
  - tempo máximo de rota,
  - janela de atendimento,
  - custo de combustível/pedágio,
  - balanceamento de carga entre veículos.

### 1.3 Visualização das rotas
- Exibir rotas otimizadas em mapa/plot para interpretação rápida.
- Mostrar informações por veículo:
  - sequência de paradas,
  - distância da rota,
  - carga utilizada,
  - status de violações (se houver).
- Gerar gráficos comparativos entre soluções (ex.: baseline x GA com restrições).

### 1.4 Integração com LLM (obrigatória)
- Usar LLM para:
  - Gerar instruções operacionais para motoristas/equipes com base nas rotas;
  - Produzir relatório diário/semanal de eficiência (distância, tempo, economia);
  - Sugerir melhorias do processo logístico.
- Criar prompts específicos e reutilizáveis:
  - Prompt de instruções por rota/veículo;
  - Prompt de relatório executivo;
  - Prompt de Q&A para perguntas em linguagem natural sobre entregas.
- Definir mecanismo de avaliação da saída da LLM:
  - clareza,
  - aderência aos dados,
  - utilidade operacional,
  - risco de alucinação.

### 1.5 Estrutura de projeto, qualidade e observabilidade
- Organizar projeto Python com ambiente virtual (venv/Poetry/Pipenv).
- Estruturar módulos (sugestão):
  - `core/ga` (operadores + evolução),
  - `core/vrp` (restrições e fitness),
  - `visualization/` (mapas e gráficos),
  - `llm/` (prompts e geração de textos),
  - `api/` ou `app/` (opcional),
  - `tests/`.
- Implementar logging e métricas mínimas:
  - melhor fitness por geração,
  - tempo de execução,
  - taxa de soluções inválidas,
  - custo final por rota.
- Criar testes automatizados:
  - unitários de fitness e operadores genéticos,
  - integração do pipeline (entrada -> otimização -> relatório).

## 2) Matriz requisito -> implementação -> evidência

| Requisito | Implementação mínima | Evidência para entrega |
|---|---|---|
| GA para roteamento | Seleção + crossover + mutação + elitismo | Gráfico fitness por geração + tabela de configuração |
| Prioridade de entregas | Peso maior para entregas críticas na fitness | Cenário de teste com prioridade e resultado comparado |
| Capacidade de carga | Penalidade/invalidação de rotas acima da capacidade | Relatório por veículo com carga total |
| Autonomia do veículo | Restrição de distância máxima por veículo | Indicador de violações por rota |
| Múltiplos veículos (VRP) | Codificação com divisão de rotas por veículo | Visualização com cores por veículo |
| Integração LLM | Geração de instruções + relatório + Q&A | Exemplos de prompts/saídas no relatório |
| Visualização | Mapa/plot de rotas + comparativo baseline | Figuras no README e no relatório técnico |

## 3) O que entregar (entregáveis da Fase 2)

### 3.1 Repositório Git
- Código-fonte completo.
- Scripts/notebooks de demonstração.
- Documentação de uso (README) e, se aplicável, documentação da API.
- (Opcional extra) Arquivos de implantação em nuvem e IaC.

### 3.2 Relatório técnico (Projeto 2)
O relatório deve cobrir explicitamente:
1. Implementação do GA para roteamento a partir do código base TSP.
2. Estratégias para restrições adicionais:
   - prioridades,
   - capacidade,
   - autonomia,
   - múltiplos veículos.
3. Integração com LLM:
   - abordagem,
   - prompts utilizados,
   - exemplos de saída,
   - limitações e mitigação.
4. Comparativo de desempenho com outras abordagens (baseline guloso, rota aleatória, etc.).
5. Visualizações e análises das rotas otimizadas.
6. Desafios técnicos e decisões de arquitetura.
7. (Opcional extra) Arquitetura em nuvem, se adotada.

### 3.3 Vídeo de demonstração (até 15 minutos)
- Sistema rodando ponta a ponta.
- Explicação dos componentes (GA + restrições + visualização + LLM).
- Demonstração dos resultados de otimização.
- Demonstração da geração de instruções/relatórios com LLM.
- Publicar no YouTube/Vimeo (público ou não listado).

## 4) Plano sugerido de execução (4 sprints)

- **Sprint 1**: modelagem de dados, função fitness, baseline e GA inicial.
- **Sprint 2**: restrições obrigatórias completas (prioridade/capacidade/autonomia/VRP).
- **Sprint 3**: visualização, métricas, experimentos comparativos e testes.
- **Sprint 4**: integração LLM, documentação final, gravação do vídeo e revisão de entrega.

## 5) Checklist final (pronto para submissão)

### Implementação
- [ ] GA de roteamento implementado e funcional.
- [ ] Restrições obrigatórias implementadas (prioridade, capacidade, autonomia, múltiplos veículos).
- [ ] Visualização de rotas disponível.
- [ ] Integração LLM para instruções + relatórios + Q&A.
- [ ] Testes automatizados criados e executando.

### Documentação
- [ ] README com setup, execução, exemplos e limitações.
- [ ] Relatório técnico completo com resultados e comparativos.
- [ ] Evidências visuais (gráficos/mapas) no relatório.
- [ ] Prompts e estratégia de avaliação da LLM documentados.

### Entrega
- [ ] Repositório organizado e versionado.
- [ ] Vídeo publicado (link válido).
- [ ] Todos os links e instruções revisados.

## 6) Critérios para priorizar esforço (recomendação)
1. Primeiro garantir **restrições obrigatórias + fitness robusta**.
2. Depois consolidar **múltiplos veículos (VRP)**.
3. Em seguida, incluir **integração LLM com prompts bons e rastreáveis**.
4. Finalizar com **comparativos, visualizações e narrativa do relatório/vídeo**.
