from lab2_corrector import Lab2Corrector

class DadosLab:
    def __init__(self):
        self.lab_folder_path = "./lab2"
        self.testcases_path = self.lab_folder_path + "/testcases"
        self.student_errors_path = self.lab_folder_path + "/erros-alunos"

        self.students_path = self.lab_folder_path + "/labs-alunos-t1"
        #self.students_path = self.lab_folder_path + "/labs-alunos-t2"
        #self.students_path = self.lab_folder_path + "/labs-teste"

        self.numero_lab = 2

        self.aluno=None
        #self.aluno='Aluno_Teste_1'


corrector = Lab2Corrector(DadosLab())

#corrector.make_correction(skip_passed_labs=False)
corrector.make_correction(skip_passed_labs=True)