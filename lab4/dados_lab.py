import argparse
import sys
import os
import re

class DadosLab:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Correcao de lab"
        )

        parser.add_argument(
            "students_path", 
            help="Pasta com os alunos a serem corrigidos"
        )

        parser.add_argument(
            "-s", "--student",
            help="Corrigir apenas um aluno específico"
        )

        parser.add_argument(
            "-b", "--bronco",
            action="store_true",
            help="Ativa detecção de bronco"
        )

        parser.add_argument(
            "error_type",
            nargs="?",
            default="ALL",
            help="Tipo de erro a corrigir (padrão: ALL)"
        )

        args = parser.parse_args()
        argv = sys.argv

        self.numero_lab = int(re.search(r"\d+", argv[0]).group())
        self.lab_folder_path = f"./lab{self.numero_lab}"

        self.testcases_path = os.path.join(self.lab_folder_path, "testcases")
        self.student_errors_path = os.path.join(self.lab_folder_path, "erros-alunos")
        self.students_path = os.path.join(self.lab_folder_path, args.students_path)

        self.error_type_to_correct = args.error_type
        self.do_bronco_detection = args.bronco
        self.student_to_correct = args.student

        self.compile_timeout = 5

        # Increase this if a testcase takes long to run
        self.run_timeout = 5

        self.student_folder_files = ["logs_correcao_auto.txt", "logs_correcao_bronco.txt", "outputs", ".cpp"]

        # The field in "saida*.json" which contains the correct order of output
        self.json_field_with_array = "order"

        self.array_regexes = {
            "lines": [],
            "values": [
                r"^(.*\S).*$"
            ]
        }

        # If you want to use values in json field array to quickly build a regex
        # Which overwrites field lines of self.array_regexes
        self.use_json_to_get_line_patterns = True

        # Dict to find int values on the output txt
        # Keys need to be on the EXACT order
        self.value_to_regexes = {
            "num_comparacoes": {
                "lines": [
                    r"\bcomparacoes\b",
                    r"\bfeitas\b"
                ],
                "values": [
                    r"-?\d+"
                ]
            }
        }

