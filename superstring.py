import subprocess
from argparse import ArgumentParser

## Veľká časť kódu je prebratá zo vzorového riešenia od pána doktora Jiřího Švancaru Mgr. Ph.D.

def load_input(input_file):
    # input je vo formáte k (najväčšia dĺžka superstringu) a potom r_1 ... r_n (reťazce)
    with open(input_file, 'r') as file:
        k = int(file.readline().strip())
        strings = [line.strip() for line in file if line.strip()]
    return k, strings

def encode(k, strings):
    # tu vytvoríme CNF formulu pre problém superstringu
    cnf = []
    nr_vars = k # prvých k premenných sú tie možné znaky stringu
    for r in strings: # vytvárame pre každý string
        m = len(r) 
        beggining_of_match_vars = nr_vars + 1 # odsadenie pomocných premenných od premenných výsledného stringu
        matches = []
        for p in range(k-m+1):
            match = []
            nr_vars += 1
            actual_match = beggining_of_match_vars + p # posun indexu pre match premenné
            matches.append(actual_match)
            for j in range(m): # tvorba premennej match pre posun p (pridanie medzi premenné + zadefinovanie logiky)
                literal = -(p+j+1) if r[j]=='0' else (p+j+1)  # odvolanie sa na premenné superstringu podľa toho či je to 0 alebo 1 - = \neg
                match.append(-literal)
                cnf.append([-actual_match, literal, 0]) # ¬m ∨ v_j
            cnf.append(match + [actual_match, 0]) # ¬v_1 ∨ ¬v_2 ∨ ... ∨ ¬v_m ∨ m
        cnf.append(matches + [0]) # or cez všetky mathch v rámci jedného r 
    return cnf, nr_vars


def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    # print CNF into formula.cnf in DIMACS format
    print(f"CLAUSES: {len(cnf)}")
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + '\n')

    # call the solver and return the output
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity) , output_name], stdout=subprocess.PIPE, text=True)

def print_result(result, k):
    # interpret Glucose output
    lines = result.stdout.splitlines()
    for line in lines:
        if line.startswith('v '):
            parts = line[2:].split()
            w = ''
            for i in range(1, k+1):
                val = int(parts[i-1])
                w += '1' if val > 0 else '0'
            print("Superstring:", w)
            return
    print("No solution found")

if __name__ == "__main__":

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="test-input.in",
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e. the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0,2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()

    # get the input instance
    k, strings = load_input(args.input)

    # encode the problem to create CNF formula
    cnf, nr_vars = encode(k, strings)

    # call the SAT solver and get the result
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)

    # interpret the result and print it in a human-readable format
    print_result(result, k)

