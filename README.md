# in1116-pacman

Resource: http://ai.berkeley.edu/multiagent.html

## TODO

### Para o PACMAN: (Sugestão para Artur fazer)

- [x] Fazer a questão 1 (Agente de Regras)\
  Objetivo: Aqui o nosso pacman criado deve ganhar na maioria das vezes pra os fantasmas básicos já fornecidos.
- [x] Fazer a questão 2 (Agente Minimax)\
  Objetivo: Nessa questão o objetivo é que o nosso fantasma criado ganhe na maioria das vezes desse pacman.
- [x] Fazer a questão 4 (Agente Expectmax)\
  Objetivo: Nessa questão o objetivo é que o nosso fantasma criado ganhe na maioria das vezes desse pacman.

### Para os FANTASMAS: (Sugestão para Walber fazer)

- [x] Estratégia Multi-Agente para ganhar dos pacmans na questão 2 e 4.
- [ ] Fixar bugs no código dos fantasmas

### Relatório:
- [ ] Fazer o relatório colaborativamente

## DATAS IMPORTANTES
- Entrega do projeto: 2 de julho de 2019.
- Entrega do relatório: 4 de julho de 2019.

## Testando

#### Open Classic Maze

```
$ python pacman.py -p ReflexAgent -l openClassic -q -n 10
$ python pacman.py -p MinimaxAgent -l openClassic -a depth=3 -q -n 10
$ python pacman.py -p ExpectimaxAgent -l openClassic -a depth=3 -q -n 10
```

#### Small Classic Maze

```
$ python pacman.py -p ReflexAgent -l smallClassic -q -n 10
$ python pacman.py -p MinimaxAgent -l smallClassic -a depth=3 -q -n 10
$ python pacman.py -p ExpectimaxAgent -l smallClassic -a depth=3 -q -n 10
```

#### Medium Classic Maze

```
$ python pacman.py -p ReflexAgent -l mediumClassic -q -n 10
$ python pacman.py -p MinimaxAgent -l mediumClassic -a depth=3 -q -n 10
$ python pacman.py -p ExpectimaxAgent -l mediumClassic -a depth=3 -q -n 10
```

#### Tricky Classic Maze

```
$ python pacman.py -p ReflexAgent -l trickyClassic -q -n 10
$ python pacman.py -p MinimaxAgent -l trickyClassic -a depth=3 -q -n 10
$ python pacman.py -p ExpectimaxAgent -l trickyClassic -a depth=3 -q -n 10
```

#### Minimax Classic Maze

```
$ python pacman.py -p ReflexAgent -l minimaxClassic -q -n 10
$ python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=3 -q -n 10
$ python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3 -q -n 10
```

#### Trapped Classic Maze

```
$ python pacman.py -p ReflexAgent -l trappedClassic -q -n 10
$ python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3 -q -n 10
$ python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
```
