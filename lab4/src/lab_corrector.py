import os
import subprocess
import glob
import shutil
import traceback
import json
import re
from src.bronco_finder_agent import CorrectorAgent
import src.utils as utils

class CorrectionFailed(Exception):
    def __init__(self, student, error_type, message):
        student.error_type = error_type
        student.logs.append(message)
        super().__init__(message)

class CompilationError(CorrectionFailed):
    def __init__(self, student, message):
        super().__init__(student, "ERRO-COMPILACAO", message)

class WrongFilePathError(CorrectionFailed):
    def __init__(self, student, message):
        super().__init__(student, "ARQUIVO-NOME-ERRADO", message)

class OutputFormattingError(CorrectionFailed):
    def __init__(self, student, message):
        super().__init__(student, "FORMATACAO-OUTPUT-ERRADA", message)

class FailedTestcaseError(CorrectionFailed):
    def __init__(self, student, message):
        super().__init__(student, "ERRO-CASOS-TESTE", message)

class Student():
    def __init__(self, student_path):
        self.path = student_path
        self.name = os.path.basename(student_path)
        self.error_type = None
        self.logs = []
        self.num_total_testcases = 0
        self.num_passed_testcases = 0

class LabCorrector():
    def __init__(self, dados_lab):
        self.numero_lab = dados_lab.numero_lab
        self.testcases_path = dados_lab.testcases_path
        self.student_errors_path = dados_lab.student_errors_path
        self.students_path = dados_lab.students_path
        self.error_type_to_correct = dados_lab.error_type_to_correct
        self.do_bronco_detection = dados_lab.do_bronco_detection
        self.student_to_correct = dados_lab.student_to_correct
        self.run_timeout = dados_lab.run_timeout
        self.compile_timeout = dados_lab.compile_timeout
        self.student_folder_files = dados_lab.student_folder_files
        self.use_json_to_get_line_patterns = dados_lab.use_json_to_get_line_patterns
        self.json_field_with_array = dados_lab.json_field_with_array
        self.array_regexes = dados_lab.array_regexes
        self.value_to_regexes = dados_lab.value_to_regexes        

        # If only one student, correct using all criteria
        if self.student_to_correct:
            self.error_type_to_correct = 'ALL'

        self.student = None

        self.error_files = [
            "ARQUIVO-NOME-ERRADO.txt",
            "ERRO-COMPILACAO.txt",
            "FORMATACAO-OUTPUT-ERRADA.txt",
            "ERRO-CASOS-TESTE.txt",
            "NO-ERRORS.txt"
        ]

        self.create_student_folders()
        self.students = self.get_students_list()

        self.remove_error_type_txts()

    def get_students_list(self):
        if self.student_to_correct:
            student_path = os.path.join(self.students_path, self.student_to_correct)
            return [Student(student_path)]

        students = []

        for folder in os.listdir(self.students_path):
            student_path = os.path.join(self.students_path, folder)
            students.append(Student(student_path))

        for file in self.error_files:
            error_file_path = os.path.join(self.student_errors_path, file)
            os.makedirs(self.student_errors_path, exist_ok=True)
            if not os.path.isfile(error_file_path):
                continue
            with open(error_file_path, "r") as f:
                for line in f:
                    student_name = line.strip()
                    if student_name:
                        for student in students:
                            if student.name == student_name:
                                student.error_type = file[:-4]
        return sorted(students, key=lambda x: x.name)                          
            
    def clear_logs_file(self):
        logs_correcao_path = self.student.path + "/logs_correcao_auto.txt"
        open(logs_correcao_path, "w").close()

    def log_errors(self, encoding):
        logs_correcao_path = self.student.path + "/logs_correcao_auto.txt"
        with open(logs_correcao_path, "a", encoding=encoding) as logs:
            print(f"{self.student.error_type}\n", file=logs)                
            for error_log in self.student.logs:
                print(error_log, file=logs)

    def add_log(self, message, encoding):
        logs_correcao_path = self.student.path + "/logs_correcao_auto.txt"
        with open(logs_correcao_path, "a", encoding=encoding) as logs:
            print(message, file=logs)                

    def create_student_folders(self):
        lowercase_files = glob.glob(os.path.join(self.students_path, "lab*"))
        for file_path in lowercase_files:
            filename = os.path.basename(file_path)
            new_filename = filename.replace('lab', 'Lab')
            os.rename(file_path, os.path.join(self.students_path, new_filename))

        CPP_files = glob.glob(os.path.join(self.students_path, "Lab*.CPP"))
        for file_path in CPP_files:
            filename = os.path.basename(file_path)
            new_filename = filename.replace('.CPP', '.cpp')
            os.rename(file_path, os.path.join(self.students_path, new_filename))

        cpp_files = glob.glob(os.path.join(self.students_path, "Lab*.cpp"))
        for file_path in cpp_files:
            filename = os.path.basename(file_path) 
            folder_name = filename[5:].replace('.cpp','')
            new_folder_path = os.path.join(self.students_path, folder_name)
            os.makedirs(new_folder_path, exist_ok=True)
            shutil.move(file_path, os.path.join(new_folder_path, filename))  

    def remove_outputs_folder(self):
        outputs_path = os.path.join(self.student.path, "outputs")
        if os.path.exists(outputs_path) and os.path.isdir(outputs_path):
            shutil.rmtree(outputs_path)

    def remove_unwanted_files(self):
        for f in os.listdir(self.student.path):
            full_path = os.path.join(self.student.path, f)
            _, extension = os.path.splitext(f)            
            if f not in self.student_folder_files and extension not in self.student_folder_files:
                if os.path.isfile(full_path):
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)

    def remove_error_type_txts(self):
        for file in self.error_files:
            error_file_path = os.path.join(self.student_errors_path, file)
            if os.path.isfile(error_file_path):
                os.remove(error_file_path)

    def create_error_type_txts(self):
        for student in self.students:
            error_file = f"{student.error_type}.txt"
            error_file_path = os.path.join(self.student_errors_path, error_file)
            with open(error_file_path, "a") as file:
                file.write(student.name + "\n")

    def get_and_process_output(self, testcase):
        output_path = glob.glob(f'{self.student.path}/Lab*.txt')
        if not output_path:
            raise FailedTestcaseError(self.student, "Nao criou o arquivo txt de saida\n")
        output_folder = os.path.join(self.student.path, 'outputs')
        os.makedirs(output_folder, exist_ok=True)
        final_output_path = os.path.join(output_folder, f"{testcase}.txt")
        shutil.copy(output_path[0], final_output_path)
        os.remove(output_path[0])
        try:
            with open(final_output_path, encoding='utf-8') as output_file:
                lines = output_file.readlines()
        except UnicodeDecodeError:           
            with open(final_output_path, encoding='latin1') as output_file:
                lines = output_file.readlines()
        return [utils.convert_special_caracters(line) for line in lines]

        
    def get_student_code(self):
        cpp_path = glob.glob(f'{self.student.path}/Lab*.cpp')
        if not cpp_path:
            raise WrongFilePathError(self.student, "Nao enviou o arquivo .cpp\n")
        with open(cpp_path[0], encoding='latin-1') as cpp_file:
            return cpp_file.read()

    def compile_student_code(self):
        if os.path.isdir(self.student.path):
            cpp_path = os.path.join(f'{self.student.path}/Lab*.cpp')
            try:
                result = subprocess.run(
                    f'g++ {cpp_path} -o {self.student.path}/a.out',
                    shell=True, 
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    timeout=self.compile_timeout
                )
                if result.returncode == 0 and result.stderr:
                    self.add_log(f"WARNINGS NA COMPILACAO:\n{result.stderr.decode('utf-8', errors='replace')}", encoding="utf-8")
            except subprocess.CalledProcessError as e:
                raise CompilationError(self.student, f"Codigo de saida: {e.returncode}\n")
            except subprocess.TimeoutExpired:
                raise CompilationError(self.student, f"Tempo limite de compilacao excedido.")
            except Exception as e:
                raise CompilationError(self.student, f"Ocorreu um erro inesperado na compilacao: {e}\n")

    def run_student_code(self, testcase):
        testcase_path = os.path.join(self.testcases_path, testcase)
        input_file = os.path.join(testcase_path, f"entrada{self.numero_lab}.txt")
        shutil.copy(input_file, self.student.path)
        input_file = os.path.join(testcase_path, f"Entrada{self.numero_lab}.txt")
        shutil.copy(input_file, self.student.path)

        try:
            subprocess.run(
                './a.out', 
                cwd=self.student.path, 
                shell=True, 
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=self.run_timeout
            )
        except subprocess.CalledProcessError as e:
            raise FailedTestcaseError(self.student, f"Erro na execucao do caso teste {testcase}.\nCodigo de saida: {e.returncode}\n")
        except subprocess.TimeoutExpired:
            raise FailedTestcaseError(self.student, f"Tempo limite de execucao do caso teste {testcase} excedido")
        except Exception as e:
            raise FailedTestcaseError(self.student, f"Ocorreu um erro inesperado na execucao do caso teste {testcase}: {e}\n")

    def check_fopen_path(self, student_code):
        pattern_entrada = fr'fopen\s*\(\s*"[Ee]ntrada{self.numero_lab}\.txt"\s*,\s*".*?"\s*\)'
        pattern_saida = fr'fopen\s*\(\s*"Lab{self.numero_lab}_[a-zA-Z0-9_]+\.txt"\s*,\s*".*?"\s*\)'
        nome_entrada_correto = re.search(pattern_entrada, student_code) is not None
        nome_saida_correto = re.search(pattern_saida, student_code) is not None
        if not nome_entrada_correto or not nome_saida_correto:
            raise WrongFilePathError(self.student, "Erro no nome dos arquivos de entrada ou saída\n")

    def correct_code(self):
        code = self.get_student_code()
        self.check_fopen_path(code)
        if self.do_bronco_detection:
            self.detect_bronco(code)
        
    def correct_output(self, testcase):
        self.run_student_code(testcase)
        output = self.get_and_process_output(testcase)
        self.process_student_output(testcase, output)

    def process_student_output(self, testcase, output):    
        lines = [line.rstrip('\n') for line in output] 

        if len(lines) < 2:
            raise OutputFormattingError(
                self.student,
                f"Output vazio no caso teste {testcase}"
            )
        
        # Get the correct answers and line matching patterns
        answers_path = os.path.join(self.testcases_path, testcase, f'saida{self.numero_lab}.json')
        with open(answers_path, "r", encoding="utf-8") as answers_file:
            answers = json.load(answers_file)
            line_regexes_from_json = []
            for string in answers[self.json_field_with_array]:
                line_regexes_from_json.append(utils.make_regex_to_match_string(utils.convert_special_caracters(string)))
        
        # Correct all values the student should print on output
        wrong_values = []
        for value_name in self.value_to_regexes:
            student_value = utils.get_first_match_in_first_matching_line(lines, self.value_to_regexes[value_name]["lines"], self.value_to_regexes[value_name]["values"])
            # If can't find a value, raise error asap
            if student_value is None:
                raise OutputFormattingError(self.student, f"Nao imprimiu {value_name.upper()}")
            # If value is diff from the answer, continue correction
            if int(student_value) != answers[value_name]:
                wrong_values.append(value_name)
            
        wrong_values_error_message = ""
        for value_name in wrong_values:
            wrong_values_error_message += f"Caso teste {testcase}: {value_name.upper()} errado\n"
        if wrong_values_error_message:
            raise FailedTestcaseError(
                self.student, 
                wrong_values_error_message
            )
        
        # Correct list of values the student printed on output
        line_regexes = line_regexes_from_json if self.use_json_to_get_line_patterns else self.array_regexes["lines"]
        student_values = utils.get_first_matches_in_many_matching_lines(lines, line_regexes, self.array_regexes["values"])
        # If student list is not right, raise error
        if student_values != answers[self.json_field_with_array]:
            raise FailedTestcaseError(
                self.student,
                f"Caso teste: {testcase}: ORDENACAO ERRADA"
            )

    def detect_bronco(self, code):
        corrector_agent = CorrectorAgent()
        
        prompt = '''
        **Sua função principal**: Você irá identificar no código do aluno processos que tornem o código repetitivo ou que realizam operações
        desnecessárias. Por exemplo, dar malloc em cada posição de um vetor em vez de dar um único malloc no vetor inteiro, ou usar uma lógica
        muito complexa para fazer algo simples. Seja leniente para coisas mais bobas, como fazer if else para retornar bool no lugar
        de apenas retornar o bool diretamente, nâo identifique esse tipo de atitude. Também não identifique erros reais no código
        que façam ele não funcionar corretamente, como erros de lógica, esses já foram identificados na correção automática. Sua
        função não é achar o que está errado, mas o que está subótimo/repetitivo/feio porém funcional. Também identifique más
        práticas de código, como variáveis não inicializadas que geram acesso indevido, e falta de fclose/free, ou erros no free
        que gerem vazamento de memória. Repito, não identifique erros de lógica no código, apenas erros de práticas subótimas/erradas.
        Não seja pedântico.
        '''

        final_instructions = f'''
        **Formato da resposta**:  
        - Escreva em bullet points (um item por linha).
        - Se não houver nada a apontar em uma seção, escreva: “Nenhum problema identificado”.  

        Ex:
        Más práticas/repetições encontradas:
        1) Problema 1
        2) Problema 2

        Segue o código do aluno:

        {code}
        '''

        prompt = f"{prompt}\n\n{final_instructions}"

        response = corrector_agent.respond(prompt)
        
        logs_bronco_path = self.student.path + "/logs_correcao_bronco.txt"
        with open(logs_bronco_path, "w") as logs:
            for line in response:
                print(line, file=logs)                

    def make_student_correction(self):
        try:
            self.correct_code()
            self.compile_student_code()
        except (CompilationError, WrongFilePathError):
            return
        self.add_log(f"\n{"-"*25}\nRESULTADOS CASOS TESTE:\n{"-"*25}\n", encoding="utf-8")
        for testcase in os.listdir(self.testcases_path):
            try:
                self.correct_output(testcase)
                self.student.num_passed_testcases += 1
            except (FailedTestcaseError, FailedTestcaseError, OutputFormattingError):
                continue
        if not self.student.logs:
            self.student.error_type = "NO-ERRORS"
        

    def make_correction(self):
        progress = 1
        try:
            for student in self.students:
                if student.error_type is None:  # If any student error is missing, correct all
                    self.error_type_to_correct = 'ALL'
                    break
            if self.error_type_to_correct == 'ALL':
                students_to_correct = self.students
            else:
                students_to_correct = [student for student in self.students if student.error_type == self.error_type_to_correct]
            for student in students_to_correct:
                self.student = student
                print(f"Correcting... ({progress}/{len(students_to_correct)}). Current student: {student.name }")
                progress += 1
                self.clear_logs_file()
                self.remove_outputs_folder()
                self.make_student_correction()
                self.remove_unwanted_files()
                self.add_log(f"\n{"-"*25}\nLOGS ERROS:\n{"-"*25}\n", encoding="utf-8")
                self.log_errors(encoding="utf-8")
                self.remove_unwanted_files()
            self.create_error_type_txts()
            print("Correction ended successfully")
        except Exception as e:
            print(f"Correction failed due to error: {e}")
            traceback.print_exc()



