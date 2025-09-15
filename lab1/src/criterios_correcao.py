def get_correction_criteria():
    return str({
        "Prazo": [],

        "Arquivo": [
            "Errou nome do arquivo de entrada por maiúscula ou underline (-1)",
            "Errou nome do arquivo de saída por maiúscula ou underline (-1)",
            "Errou nome do arquivo de entrada completamente (-3)",
            "Errou nome do arquivo de saída completamente (-3)"
        ],

        "Saída": [
            "Sem 5 linhas no cabeçalho (-3)",
            "Nao começou string de erro ou aviso com 'ERRO' ou 'AVISO' (-1)",
            "Colocou 'ERRO' ao invés de 'AVISO' ou o contrário (-1)",
            "Nao começou string dia seguinte vazio com 'Agenda' (-1)",
            "Nao fez mensagem de dia seguinte sem tarefas (-5)"
        ],

        "Identação": [
            "Erros de identação (-1)" 
        ],

        "Bronco": [
            "Fez if(variavel_bool) em vez de so retornar o bool (-1)",
            "Fez if(variavel_bool == true) (-1)",
            "Criou vetor desnecessario que armazena toda tarefa lida podendo ultrapassar o tamanho máximo da agenda (-15)",
            "Declara muitas variaveis desnecessarias/redundantes para a logica do codigo (-5)",
            "Passou a agenda e um atributo da agenda como argumentos de uma função podendo ter passado apenas agenda (-5 cada)",
            "Copiou string char por char (-5)",
            "Deu malloc posicao por posicao em vez de alocar o vetor inteiro (-10)",
            "Criou uma funcao auxiliar para {fazer algo} mas isso deveria ser feito em {Inserir, ConsultarMax, RemoverMax, Inicializar, Finalizar, FilaVazia ou FilaCheia}  (-5)",
            "{Inserir outras pequenas coisas broncas em geral} (-2 cada)"
        ],

        "Índice 0": [
            "Utilizou o vetor de atividades a partir do índice 0 de forma generalizada (-10)",
            "Utilizou o índice zero explicitamente em uma parte do código, apesar de no resto fazer 1-indexado como pedido (-5 cada)",
            "Não usou índice zero mas usou malloc com MAX posições (deveria ser MAX+1) (-7)"
        ],

        "Str. Descrição": [
            "Armazenou prioridade+descricao na string descrição da agenda (-5)",
            "Descricao de tamanho maior que 42 (-5)",
            "Descricao de tamanho menor que 41 (-5)"
        ],

        "Agenda": [
            "Vetor de atividades decrescente (-25)",
            "Vetor de atividades crescente mas ConsultarMax é O(n) (-10)",
            "Vetor de atividades crescente mas RemoverMax é O(n) (-10)",
            "Fez ConsultarMaxDescricao e ConsultarMaxPrioridade em vez de um único ConsultarMax (-5)",
            "Fez retornar descrição e prioridade em ConsultarMax (por referencia) em vez de retornar o struct tarefa (-5)"
        ],

        "R.A.TAD": [
            "Inicializou {atributo(s) A,B,C e D} do struct na main} (-5 cada)",
            "ConsultarMAX retorna índice forçando acesso indevido na main (-5)",
            "No loop do dia seguinte, faz o loop percorrendo os indices do vetor em vez de usar FilaVazia, ConsultarMAX e RemoverMAX (-10)",
            "Criou função que {faz algo que deveria ser feito na main} e nela acessou o TAD diretamente (-5)",
            "Main acessa campos do TAD diversas vezes (-20)"
        ],

        "L/E/main": [
            "Leitura de arquivo fora da main (-10)",
            "Escrita de arquivo fora da main (-10)"
        ],

        "Global": [
            "Uso de variáveis globais {A,B,C e D} (-5 cada, teto -20)"
        ],

        "Busca Binária": [
            "Não fez busca binária para inserção (-25)",
            "Erro na busca binária (-10)"
        ],

        "Func. Públicas": [
            "Não implementou {a(s) funções públicas {Inserir, ConsultarMax, RemoverMax, Inicializar, Finalizar, FilaVazia ou FilaCheia}.  (-10 cada)"
        ],

        "fclose/free": [
            "Não deu free {na(s) variáveis A,B,C e D}.(-5 cada)",
            "Faltou fclose {no(s) arquivos A,B,C e D} (-5 cada)"
        ],

        "Outros": [
            "[Erros de lógica] {Inserir erro específico de lógica} (-10 cada)",
            "[Erros off-by-one] {Inserir erro específico off-by-one} (-5 cada)",
            "Não inicializa {a(s) strings A,B,C e D} antes de usar strcmp (-5 cada)",
            "Não inicializa {a(s) variáveis A,B,C e D}, mas não faz o código funcionar errado em geral (-5 cada)",
            "Não inicializa {a(s) variáveis A,B,C e D} e isso faz o código funcionar errado (-10 cada)",
            "Ponteiros desnecessários para int/bool (-1)",
            "Ponteiros duplos desnecessários (-2)",
            "Código pouco legível (-2)",
            "Atribuir NULL a um inteiro é uma má prática (-1)"
        ],

        "Observações (sem desconto na nota)": [
            "Zerar descricao e prioridade em RemoverMAX",
            "Passar agenda por valor em finalizar",
            "Malloc desnecessario no struct fila",
            "Malloc desnecessário em variáveis em geral",
            "[Outras observações] {Incluir observações curtas}"
        ]
    })


def get_correction_instructions():
    return '''
        Para aplicar os critérios de correção fornecidos a seguir, você irá utilizar as seguintes instruções:

        **INSTRUÇÕES DE CORREÇÃO**

        1) Sempre gerar resposta em formato de dicionário incluindo todos os tipos de desconto, mesmo que nenhum erro ocorra.
        2) Texto entre [] é explicativo e **não deve aparecer**; texto entre {} deve ser substituído corretamente.
        3) Use exatamente os pontos indicados (-x ou -x cada). Se "-x cada", some todos os erros.
        4) Evite penalizar o mesmo erro duas vezes.
        5) Só aplique desconto se a função realmente puder falhar.
        6) Não incluir observações inúteis como "Código compila sem warnings no gcc".
        7) Não alterar os critérios passados, deve utilizar EXATAMENTE as mesmas mensagens presentes no dicionário, 
           exceto quando houver [] ou {}. Não adicionar critérios novos além dos fornecidos.
        8) Lembre-se que o output gerado deve ser um json. Portanto, sem comentários nem nada que torne o json inválido. Se baseie
           no exemplo fornecido de resposta da ia para entender a formatação.

        **ARQUIVOS**
        - Entrada: "entrada1.txt"
        - Saída: "Lab1_Seu_Nome.txt" (maiúsculas, underline e espaços exatos)
        - Lab1_Jose_Tizon.txt está correto
        - Lab1_jose_alberto_tizon.txt está correto
        - Lab1_Pedro_Oliveira.txt está correto
        - lab1_joao_pedro.txt está errado (colocou lab em vez de Lab)
        - Arquivos totalmente incorretos: ex: "saida1.txt", "LAB_1_Jose Tizon.txt"

        **SAÍDA**
        - Cabeçalho: 5 linhas antes da linha de hífens que inicia as respostas.
        - Mensagens:
            - "ERRO {mensagem}" ao tentar inserir em agenda cheia
            - "AVISO {mensagem}" ao tentar consultar em agenda vazia
            - "Agenda {mensagem}" se não sobram tarefas
        - Capitalização de ERRO/AVISO/Agenda não importa.
        - Deve haver um espaço após "ERRO"/"AVISO"/"Agenda", sem ":".
        - Desconto "Nao começou string de erro ou aviso..." aplicado apenas **uma vez**.

        **BRONCO**
        - Código funciona mas é subótimo ou repetitivo; repetir fgets ou leitura de linhas não é bronco.

        **ÍNDICE**
        - Vetor 1-indexado; não usar índice zero explicitamente, exceto no malloc se necessário.

        **STR.DESCRIÇÃO**
        - Campo `descricao` no struct tamanho 41 ou 42.

        **AGENDA**
        - Vetor crescente; Inserção: busca binária + deslocamento; Remoção: decrementar qtd.
        - ConsultarMax deve retornar struct completo.
        - ConsultarMaxDescricao e ConsultarMaxPrioridade separados não são corretos.
        - RemoverMax deve decrementar qtd sem zerar campos (observação opcional).
        - Deve usar um struct para tarefa com campos importância (int) e descriçao (string)
        - Deve usar um struct para agenda com campos para vetor de tarefas (tarefa[] mallocado), quantidade de tarefas (int) e quantidade máxima (int))

        **R.A.TAD**
        - Não acessar campos internos na main; usar apenas funções públicas.
        - Soma máxima de desconto por violação do TAD: -20.
        - Evite penalizar duas vezes pelo mesmo erro.

        **L/E/MAIN**
        - Não ler/escrever arquivos fora da main.

        **GLOBAL**
        - Não usar variáveis globais; soma máxima: -20.

        **BUSCA BINÁRIA**
        - Inserção deve usar busca binária.

        **FUNÇÕES PÚBLICAS**
        - Implementar: Inserir, ConsultarMax, RemoverMax, Inicializar, Finalizar, FilaVazia, FilaCheia.
        - Funções públicas extras permitidas se não violarem critérios.

        **fclose/free**
        - Deve liberar todas as alocações e fechar arquivos corretamente.

        **OUTROS**
        - Off-by-one, inicializações de strings e variáveis, ponteiros desnecessários, código pouco legível, variáveis redundantes, atribuir NULL a int: aplicar descontos conforme critérios.

        **OBSERVAÇÕES (sem desconto)**
        - Malloc desnecessário, passar structs por valor ou referência, outras observações curtas.

        ** EXEMPLO DE RESPOSTA DA IA **

        {
        "Prazo": [
        ],

        "Arquivo": [
            "Errou nome do arquivo de entrada por maiúscula ou underline (-1)",
            "Errou nome do arquivo de saída completamente (-3)"
        ],

        "Saída": [
            "Sem 5 linhas no cabeçalho (-3)",
            "Nao começou string de erro ou aviso com 'ERRO' ou 'AVISO' (-1)"        
        ],

        "Identação": [
        ],

        "Bronco": [
            "Fez if(variavel_bool == true) (-1)",
            "Copiou string char por char (-5)",
        ],

        "Índice 0": [
            "Utilizou o índice zero explicitamente em uma parte do código, apesar de no resto fazer 1-indexado como pedido (-5)"
        ],

        "Str. Descrição": [
            "Descricao de tamanho maior que 42 (-5)",
        ],

        "Agenda": [
            "Vetor de atividades crescente mas ConsultarMax é O(n) (-10)",
        ],

        "R.A.TAD": [
            "Inicializou atributo capacidade do struct na main (-5)",
            "Main acessa campos do TAD diversas vezes (-20)"
        ],

        "L/E/main": [
            "Leitura de arquivo feita fora da main (-10)"
        ],

        "Global": [
            "Uso de variáveis globais posicao e velocidade (-10)"
        ],

        "Busca Binária": [
            "Não implementou busca binária para inserção (-25)"
        ],

        "Func. Públicas": [
            "Não implementou as funções públicas FilaVazia e FilaCheia (-10)
        ],

        "fclose/free": [
            "Faltou fclose no arquivo de saída (-5)",
            "Faltou free da fila alocada (-5)"
        ],

        "Outros": [
            "Loop de inserção deslocando elementos do vetor vai até 'qtd' em vez de 'qtd-1', causando erro (-5)",
            "Ponteiros desnecessários para int/bool (-1)",
        ],

        "Observações (sem desconto na nota)": [
            "Malloc desnecessário no struct fila"
        ]
        }
        
        ** EXEMPLO DE CÓDIGO CORRETO (RESUMIDO) **

        - Inclui bibliotecas padrão: stdio.h, stdlib.h, string.h, stdbool.h
        - Define MAX_DESC = 41
        - Structs:
            - Tarefa: descricao[MAX_DESC], prioridade
            - FilaPrioridade: vetor de Tarefa, qtd, capacidade
        - Funções privadas:
            - buscaPosicao(fila, prioridade): retorna posição de inserção usando busca binária
        - Funções públicas:
            - Inicializar(fila, capacidade): aloca vetor, inicializa qtd e capacidade
            - Finalizar(fila): libera vetor, zera qtd e capacidade
            - FilaVazia(fila), FilaCheia(fila): retornam boolean
            - Inserir(fila, Tarefa t): insere usando buscaPosicao, desloca elementos à direita
            - ConsultarMax(fila, Tarefa* t): retorna tarefa com maior prioridade
            - RemoverMax(fila): decrementa qtd
        - Main:
            - Abre arquivos "entrada1.txt" e "Lab1_Seu_Nome.txt"
            - Lê capacidade da agenda
            - Lê comandos (NOVA, PROXIMA, FIM) e atualiza agenda:
                - NOVA: insere tarefa, imprime "ERRO ..." se cheia
                - PROXIMA: consulta/remove tarefa, imprime "AVISO ..." se vazia
            - Imprime cabeçalho de 5 linhas
            - Imprime respostas das consultas
            - Imprime tarefas restantes no dia seguinte ou "Agenda ..." se vazia
            - Fecha arquivos e libera memória

    '''

def get_main_prompt(correction_criteria_prompt, correction_instructions_prompt, student_code):
    return f'''
        Você é um agente corretor especializado em C++. Sua tarefa é analisar códigos de alunos
        para o laboratório "Agenda + Vetor Simples" (CES-11), que implementam um TAD fila de prioridade usando vetor.

        Utilize os seguintes prompts como referência para sua correção:

        1) Critérios de correção:
        {correction_criteria_prompt}

        2) Instruções detalhadas de correção:
        {correction_instructions_prompt}

        3) Código do aluno:
        {student_code}

        Sua função é aplicar os descontos exatamente como definido, sem inventar novos, e gerar um **dict Python válido**
        (contendo todas as categorias de desconto, mesmo que não haja erros em alguma delas). Apresente o resultado como
        se fosse o retorno direto de uma função Python, não em JSON.

    '''

def get_refined_prompt(correction_criteria_prompt, correction_instructions_prompt, student_code, first_correction):
    return f'''
        Você é um agente corretor de segunda instância especializado em C++. Sua tarefa é revisar e refinar
        a correção fornecida por uma primeira IA para o laboratório "Agenda + Vetor Simples" (CES-11). 

        Utilize os seguintes prompts como referência:

        1) Critérios de correção:
        {correction_criteria_prompt}

        2) Instruções detalhadas de correção:
        {correction_instructions_prompt}

        3) Código do aluno:
        {student_code}

        4) Correção inicial da primeira IA:
        {first_correction}

        ** ORIENTAÇÕES DE SEGUNDA INSTÂNCIA **
        - Avalie se todos os critérios foram aplicados corretamente.
        - Verifique se não houve excesso ou duplicação de descontos.
        - Corrija ou refine a distribuição de pontos conforme os critérios exatos.
        - Não invente novos tipos de desconto.
        - Produza um dicionário Python final, incluindo todas as categorias de desconto, mesmo que nenhuma seja aplicável.
        - Apresente o resultado como se fosse o retorno direto de uma função Python, não em JSON.
    '''

