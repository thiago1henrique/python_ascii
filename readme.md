## 1. Descrição do Problema Resolvido

O projeto resolve o problema de conversão de imagens digitais em arte ASCII, uma representação visual que usa caracteres de texto para recriar imagens. Isso permite:
```
   * Visualizar imagens em ambientes restritos a texto
   * Compartilhar representações artísticas de imagens via texto
   * Processar múltiplas imagens simultaneamente com priorização
   * Manter histórico de conversões
   * Aplicar transformações na arte gerada (como ordenação)
```

## 2. Justificativa da Escolha do Tema

A escolha se baseou em:
```
    * Relevância técnica: Combina processamento de imagens com estruturas de dados
    * Aplicabilidade prática: Útil para desenvolvedores, artistas digitais e entusiastas
    * Adequação aos requisitos: Permite implementar múltiplas estruturas de dados
    * Potencial educativo: Demonstra aplicação prática de algoritmos estudados
    * Desafio técnico: Equilíbrio entre qualidade visual e desempenho
```

## 3. Estruturas de Dados Aplicadas

a) Fila de Prioridade (Heap)

Aplicação:
```
* Gerenciamento de tarefas de conversão
* Priorização por tamanho de arquivo (imagens menores primeiro)
```

Implementação:
````
Uso do módulo heapq do Python
Tuplas (tamanho_arquivo, id_heap, task_id) como elementos
````
Justificativa:
```
* Eficiência O(log n) nas operações de inserção/remoção
* Garante que tarefas mais rápidas sejam processadas primeiro
* Melhora tempo de resposta percebido pelo usuário
```

* b) Lista Encadeada

    Aplicação:

        Armazenamento do histórico de tarefas concluídas

        Limitação ao último N itens (10 por padrão)

    Implementação:

        Classe HistoricoNode com ponteiro next

        Ponteiros head e tail para gerenciamento

    Justificativa:

        Inserção/remoção O(1) no início/fim

        Uso eficiente de memória para dados voláteis

        Ideal para histórico de tamanho limitado

c) Algoritmo Heapsort

Aplicação:

```
Ordenação da arte ASCII por densidade de caracteres
Transformação visual opcional para o usuário
```

Implementação:
```
Funções ordenar_arte_ascii() e heapify()
Ordenação baseada em densidade (caracteres não-espaço)
Funções ordenar_arte_ascii() e heapify()
Ordenação baseada em densidade (caracteres não-espaço)
```

Justificativa:
```
Complexidade O(n log n) garantida
Relação natural com a estrutura heap já utilizada
Demonstração prática do algoritmo estudado
```

## 4. Desafios Enfrentados e Soluções

* Desafio 1: Processamento Assíncrono 
    Problema: Bloqueio da interface durante conversão
    Solução: Sistema de filas com thread worker separada
<br/><br/>
* Desafio 2: Gerenciamento de Prioridades
    Problema: Tarefas grandes bloqueando pequenas
    Solução: Heap prioritário baseado em tamanho de arquivo
<br/><br/>
* Desafio 3: Manutenção de Histórico
    Problema: Armazenamento eficiente com limite máximo
    Solução: Lista encadeada com corte automático
<br/><br/>
* Desafio 4: Qualidade Visual ASCII
    Problema: Representação inadequada de imagens
    Solução: Ajuste na escala de cinza e caracteres selecionados
<br/><br/>
Desafio 5: Ordenação de Arte Multilinha
    Problema: Manter estrutura visual após ordenação
    Solução: Divisão por linhas e ordenação baseada em densidade
<br/><br/>
5. Instruções para Executar o Projeto

Pré-requisitos:

    Python 3.6+

    Bibliotecas: Flask, Pillow

Passo a passo:

    Configurar ambiente:

bash

# Criar ambiente virtual (opcional)
python -m venv venv

# Ativar ambiente
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependências
pip install Flask Pillow

    Estrutura de arquivos:

text

projeto/
├── app.py
├── conversor_ascii.py
└── templates/
    └── index.html

    Executar aplicação:

bash

python app.py

    Acessar interface:
    Abra o navegador em: http://localhost:5000

Operação:

    Na página inicial, clique na área tracejada ou arraste imagens

    Selecione uma ou mais imagens (formatos: JPG, PNG, GIF, BMP)

    Clique em "Converter Imagens"

    Acompanhe o status do processamento

    Para arte concluída:

        Visualize o resultado

        Clique em "Ordenar Arte" para aplicar transformação

    Clique em "Carregar Histórico" para ver tarefas recentes

Recursos Adicionais:

    API de status: /status/<task_id>

    API de histórico: /historico

    API de ordenação: POST /ordenar/<task_id>

Arquivos de Exemplo:
Imagens de teste podem ser colocadas na pasta uploads/ (criada automaticamente)

Encerramento:
Pressione Ctrl+C no terminal para parar o servidor