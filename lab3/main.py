import sys
from src.lab3_corrector import Lab3Corrector

class DadosLab:
    def __init__(self):
        self.lab_folder_path = "./lab3"
        self.testcases_path = self.lab_folder_path + "/testcases"
        self.student_errors_path = self.lab_folder_path + "/erros-alunos"

        #self.students_path = self.lab_folder_path + "/labs-alunos-t1"
        #self.students_path = self.lab_folder_path + "/labs-alunos-t2"
        self.students_path = self.lab_folder_path + "/labs-teste"
        #self.students_path = self.lab_folder_path + "/a"

        self.numero_lab = 3

        self.skip_passed_labs = True
        #self.skip_passed_labs = False

        #self.do_bronco_detection = True
        self.do_bronco_detection = False

        args = sys.argv

        if len(args) < 2:
            print("Uso: python script.py <tipo_erro> ou -s <aluno>")
            sys.exit(1)

        if args[1] != '-s':  # Correct a single student
            self.error_type_to_correct = args[1].upper()
            self.student_to_correct = None
        else: 
            self.error_type_to_correct = 'ALL'
            self.student_to_correct = args[2]
        
corrector = Lab3Corrector(DadosLab())

corrector.make_correction()