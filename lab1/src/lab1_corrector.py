import os
import re
import glob
import json
from abstract_corrector import AbstractCorrector, CorrectionFailed
from corrector_agent import CorrectorAgent
from criterios_correcao import get_correction_criteria, get_correction_instructions, get_main_prompt, get_refined_prompt

class Lab1Corrector(AbstractCorrector):
    def test_cabecalho(self, aluno_path, testcase, output):
        hyphen_pattern = r' *-+\s*'
        if not re.fullmatch(hyphen_pattern, output[5]): 
            raise CorrectionFailed('Nao colocou exatamente 5 linhas no cabecalho', aluno_path)

    def test_resposta(self, aluno_path, testcase, output):
        hyphen_pattern = r'^ *-{10,}\s*$'
        hyphen_lines = []
        for i, line in enumerate(output):
            if re.fullmatch(hyphen_pattern, line):
                hyphen_lines.append(i)
        if len(hyphen_lines) != 4:
            raise CorrectionFailed(f'Quantidade de linhas divisorias diferente de 4 em {testcase}. Corrigir manualmente no cpp', aluno_path)
        values_respostas_consultas = []
        values_dia_seguinte = []
        testcase_path = os.path.join(self.testcases_path, testcase)
        correct_output_path = glob.glob(f'{testcase_path}/saida*.json')
        with open(correct_output_path[0], 'r') as correct_output_file:
            correct_output = json.load(correct_output_file)
        i = hyphen_lines[1]+1
        while i < len(output):
            line = output[i]
            blank_line_pattern = r'^\s*$'
            hyphen_pattern = r' *-+\s*'
            if re.match(blank_line_pattern, line):
                i += 1
                continue
            if re.match(hyphen_pattern, line):
                i = hyphen_lines[3]+1
                continue
            splitted_line = line.split(maxsplit=1)
            importance_value = splitted_line[0]
            task_name = splitted_line[1][0:-1] if len(splitted_line) > 1 else  None
            if importance_value.isnumeric():  # It can be a noun like "AVISO" or "Agenda" if no activities
                importance_value = int(importance_value)
                if task_name not in correct_output['task_importance_values']:
                    raise CorrectionFailed(f'Leitura errada do nome das tarefas no caso teste {testcase}', aluno_path)
                if correct_output['task_importance_values'][task_name] != importance_value:
                    raise CorrectionFailed(f'O valor de importancia da tarefa {task_name.upper()} esta errado no caso teste {testcase}', aluno_path)
            else:
                importance_value = importance_value.upper()
            if i < hyphen_lines[2]:
                values_respostas_consultas.append(importance_value)
            elif i > hyphen_lines[3]:
                values_dia_seguinte.append(importance_value)
            i += 1
        if values_respostas_consultas != correct_output['values']['respostas_consultas'] or values_dia_seguinte != correct_output['values']['dia_seguinte']:
            raise CorrectionFailed(f'Ordem de importancia errada no caso teste {testcase}', aluno_path)
            
    def correct_output(self, aluno_path, testcase):
        try:
            self.run_student_code(aluno_path, testcase)
            output = self.get_and_handle_output(aluno_path, testcase)
            self.test_cabecalho(aluno_path, testcase, output)
            self.test_resposta(aluno_path, testcase, output)
        except CorrectionFailed:
            return

    def do_ai_correction(self, aluno_path, student_code):
        correction_criteria_prompt = get_correction_criteria()
        correction_instructions_prompt = get_correction_instructions()
        corrector_agent = CorrectorAgent(aluno_path)
        prompt = get_main_prompt(correction_criteria_prompt, correction_instructions_prompt, student_code)
        response = corrector_agent.respond(prompt)
        refined_prompt = get_refined_prompt(correction_criteria_prompt, correction_instructions_prompt, student_code, response)
        refined_response = corrector_agent.respond(refined_prompt)
        for line in response:
            self.print_log(line, aluno_path, tipo_correcao="ia", encoding='utf-8')
        self.print_log('', aluno_path, tipo_correcao="ia", encoding='utf-8')
        for line in refined_response:
            self.print_log(line, aluno_path, tipo_correcao="ia", encoding='utf-8')
        self.print_log('', aluno_path, tipo_correcao="ia", encoding='utf-8')
        return refined_response
    





