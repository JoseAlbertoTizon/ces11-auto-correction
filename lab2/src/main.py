from lab2_corrector import Lab2Corrector

lab_folder_path = "./lab2"

testcases_path = lab_folder_path + "/testcases"

#alunos_path = lab_folder_path + "/labs-alunos-t1"
alunos_path = lab_folder_path + "/labs-alunos-t2"
#alunos_path = lab_folder_path + "/labs-teste"

numero_lab = 2

#corrector = Lab2Corrector(alunos_path, testcases_path, numero_lab, use_ai=True)
corrector = Lab2Corrector(alunos_path, testcases_path, numero_lab, use_ai=False)
#corrector = Lab2Corrector(alunos_path, testcases_path, numero_lab, use_ai=False, aluno='Aluno_Teste_1')

corrector.make_correction()