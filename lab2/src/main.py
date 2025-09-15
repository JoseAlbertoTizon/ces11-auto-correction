from lab2_corrector import Lab2Corrector

lab_folder_path = "./lab2"

testcases_path = lab_folder_path + "/testcases"

#alunos_path = lab_folder_path + "/labs-alunos-t1"
#alunos_path = lab_folder_path + "/labs-alunos-t2"
alunos_path = lab_folder_path + "/labs-teste"

sheet_path = "Planilha.xlsx"
numero_lab = 2

#corrector = Lab2Corrector(alunos_path, testcases_path, sheet_path, numero_lab, use_ai=True)
corrector = Lab2Corrector(alunos_path, testcases_path, sheet_path, numero_lab, use_ai=False)
#corrector = Lab2Corrector(alunos_path, testcases_path, sheet_path, numero_lab, use_ai=False, aluno='Cauã_de_Lima_Rios')

corrector.make_correction()