# Conversor de maquinas Sipser-Fita Infita
Desenvolvido para o trabalho prático de TEC 2024/1. Aceita entradas para o [simulador de Anthony Morphett](https://morphett.info/turing/turing.html) onde
cada linha possui uma tupla no formato `<current state> <current symbol> <new symbol> <direction> <new state>`.

## Como executar
Este repositório possuí exemplos de possíveis entradas na pasta `examples`. É necessário que a máquina possua identificação `;I` para maquina com fita infinita
ou `;S` para maquina de Sipser, essa identificação deve ser feita na primeira linha da entrada. As entradas devem ser salvas no arquivo `input.in` e para executar
basta usar o interpretador de python através do comando 

```python3 turing.py```

O resultado será salvo no arquivo `output.out` e deverá ser executado no simulador mencionado acima.

### Dependencias
* Python 3 - Testes executados na versão `3.10.12`

