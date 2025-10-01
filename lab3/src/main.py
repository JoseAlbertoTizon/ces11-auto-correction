from lab3_corrector import Lab3Corrector

class DadosLab:
    def __init__(self):
        self.lab_folder_path = "./lab3"
        self.testcases_path = self.lab_folder_path + "/testcases"
        self.student_errors_path = self.lab_folder_path + "/erros-alunos"

        #self.students_path = self.lab_folder_path + "/labs-alunos-t1"
        #self.students_path = self.lab_folder_path + "/labs-alunos-t2"
        #self.students_path = self.lab_folder_path + "/labs-teste"
        self.students_path = self.lab_folder_path + "/a"

        self.numero_lab = 3

        self.skip_passed_labs = True
        #self.skip_passed_labs = False

        #self.do_bronco_detection = True
        self.do_bronco_detection = False


corrector = Lab3Corrector(DadosLab())

#corrector.make_correction(skip_passed_labs=False)
corrector.make_correction()