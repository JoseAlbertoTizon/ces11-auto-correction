from lab1_corrector import Lab1Corrector

lab_folder_path = "./lab1"

testcases_path = lab_folder_path + "/testcases"

alunos_path = lab_folder_path + "/labs-alunos-t1"
#alunos_path = lab_folder_path + "/labs-alunos-t2"
#alunos_path = lab_folder_path + "/labs-teste"

sheet_path = "Planilha.xlsx"
numero_lab = 1

#corrector = Lab1Corrector(alunos_path, testcases_path, sheet_path, numero_lab, use_ai=True)
corrector = Lab1Corrector(alunos_path, testcases_path, sheet_path, numero_lab, use_ai=False)
#corrector = Lab1Corrector(alunos_path, testcases_path, sheet_path, numero_lab, use_ai=False, aluno='')

corrector.make_correction()