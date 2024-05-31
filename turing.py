# Constants
INPUT_FILENAME = "input.in"
OUTPUT_FILENAME = "output.out"
ALPHABET_DEFAULT = {"★"}

def parse_transitions(transitions):
    """Retorna as transições, os estados e símbolos do alfabeto."""
    parsed_transitions = []
    nodes = set()
    alphabet = ALPHABET_DEFAULT.copy()

    for line in transitions:
        parts = line.split()
        curr_node, curr_char, new_char, direction, next_node = parts

        curr_node = str(int(curr_node) + 1) if curr_node.isdigit() else curr_node
        next_node = str(int(next_node) + 1) if next_node.isdigit() else next_node

        nodes.update([curr_node, next_node])
        alphabet.update([curr_char, new_char])
        parsed_transitions.append(f"{curr_node} {curr_char} {new_char} {direction} {next_node}")

    return parsed_transitions, nodes, alphabet

def generate_left_transitions(node):
    """Gera transições para lidar com o espaço à esquerda da fita."""
    return [
        f"{node} % % r L_{node}",
        f"L_{node} * * r L_{node}",
        f"L_{node} | # r M_{node}",
        f"M_{node} _ | l B_{node}",
        f"B_{node} # # l B_{node}"
    ]

def generate_shift_transitions(node, alphabet):
    """Gera transições para fazer o shift de símbolos na fita."""
    transitions = []
    for char in alphabet:
        transitions.extend([
            f"B_{node} {char} # r S_{node}_{char}",
            f"S_{node}_{char} # {char} l B_{node}"
        ])
    return transitions

def generate_right_transitions(node):
    """Gera transições para lidar com o espaço à direita da fita."""
    return [
        f"B_{node} % % r R_{node}",
        f"R_{node} # _ l R_{node}",
        f"R_{node} % % r {node}",
        f"{node} | _ r E_{node}",
        f"E_{node} _ | l {node}"
    ]

def generate_init_final_transitions(alphabet):
    """Gera transições iniciais e finais para o modelo de fita."""
    transitions = []
    for char in alphabet:
        transitions.extend([
            f"0 {char} % r I_{char}",
            f"I_{char} * * r I_{char}",
            f"I_{char} _ # r F_{char}",
            f"F_{char} _ | l C_{char}",
            f"C_{char} # # l C_{char}"
        ])
        for s in alphabet:
            transitions.extend([
                f"C_{char} {s} # r S_{char}_{s}",
                f"S_{char}_{s} # {s} l C_{char}"
            ])
        transitions.extend([
            f"C_{char} % % r E_{char}",
            f"E_{char} # {char} l E_{char}",
            f"E_{char} % % r 1"
        ])
    return transitions

def to_sipser_tape(nodes, alphabet):
    """Converte as transições para o modelo de fita de Sipser."""
    new_transitions = []
    for node in nodes:
        new_transitions.extend(generate_left_transitions(node))
        new_transitions.extend(generate_right_transitions(node))
        new_transitions.extend(generate_shift_transitions(node, alphabet))
    new_transitions.extend(generate_init_final_transitions(alphabet))
    return new_transitions

def to_infinite_tape(nodes):
    """Converte as transições para o modelo de fita infinita."""
    new_transitions = [
        "0 * * l %_START",
        "%_START _ # r 1"
    ]
    for node in nodes:
        new_transitions.append(f"{node} # # r {node}")
    return new_transitions

def parse_input(filename):
    """Lê o arquivo de entrada e retorna o modelo e as transições do autômato."""
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        
    if not lines:
        return "", []
    
    model = lines[0]
    transitions = [line for line in lines[1:] if line and line[0] != ';']
    return model, transitions

def save_output(filename, model, transitions):
    """Salva as transições processadas no arquivo de saída."""
    with open(filename, 'w') as file:
        file.write(model + '\n')
        for transition in transitions:
            file.write(transition + '\n')

def main():
    input_file = INPUT_FILENAME
    output_file = OUTPUT_FILENAME

    # Lê o modelo e as transições do arquivo de entrada
    model, transitions = parse_input(input_file)
    if not model:
        return

    # Ajusta as transições e obtém os estados e alfabeto
    adjusted_transitions, nodes, alphabet = parse_transitions(transitions)

    # Converte para o modelo apropriado de acordo com a entrada
    if model == ";S":
        additional_transitions = to_infinite_tape(nodes)
        output_model = ";I"
    elif model == ";I":
        additional_transitions = to_sipser_tape(nodes, alphabet)
        output_model = ";S"
    else:
        return

    # Combina as transições ajustadas com as transições adicionais e salva no arquivo de saída
    adjusted_transitions.extend(additional_transitions)
    save_output(output_file, output_model, adjusted_transitions)

if __name__ == "__main__":
    main()