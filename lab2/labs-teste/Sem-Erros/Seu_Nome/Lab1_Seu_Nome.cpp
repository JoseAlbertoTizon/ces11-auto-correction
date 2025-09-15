#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_DESC 41  // 40 + '\0'

// -------- Estruturas --------
typedef struct {
    char descricao[MAX_DESC];
    int prioridade;
} Tarefa;

typedef struct {
    Tarefa *vetor;
    int qtd;
    int capacidade;
} FilaPrioridade;

// -------- Funções privadas --------
int buscaPosicao(FilaPrioridade *fila, int prioridade) {
    int esq = 1, dir = fila->qtd, meio;
    while (esq <= dir) {
        meio = (esq + dir) / 2;
        if (fila->vetor[meio].prioridade < prioridade)
            esq = meio + 1;
        else
            dir = meio - 1;
    }
    return esq;
}

// -------- Funções públicas --------
void Inicializar(FilaPrioridade *fila, int capacidade) {
    fila->vetor = (Tarefa*) malloc((capacidade+1) * sizeof(Tarefa));
    fila->qtd = 0;
    fila->capacidade = capacidade;
}

void Finalizar(FilaPrioridade *fila) {
    free(fila->vetor);
    fila->vetor = NULL;
    fila->qtd = 0;
    fila->capacidade = 0;
}

bool FilaVazia(FilaPrioridade *fila) {
    return fila->qtd == 0;
}

bool FilaCheia(FilaPrioridade *fila) {
    return fila->qtd == fila->capacidade;
}

int Inserir(FilaPrioridade *fila, Tarefa t) {
    if (FilaCheia(fila)) return -1;
    int pos = buscaPosicao(fila, t.prioridade);
    for (int i = fila->qtd; i >= pos; i--)
        fila->vetor[i+1] = fila->vetor[i];
    fila->vetor[pos] = t;
    fila->qtd++;
    return 0;
}

int ConsultarMax(FilaPrioridade *fila, Tarefa *t) {
    if (FilaVazia(fila)) return 0;
    *t = fila->vetor[fila->qtd];
    return 1;
}

void RemoverMax(FilaPrioridade *fila) {
    if (FilaVazia(fila)) return;
    fila->qtd--;
}

// -------- MAIN --------
int main() {
    FILE *fin = fopen("entrada1.txt", "r");
    FILE *fout = fopen("Lab1_Seu_Nome.txt", "w");
    if (!fin || !fout) {
        printf("Erro ao abrir arquivos!\n");
        return 1;
    }

    char buffer[200];

    // procurar até achar "Numero maximo"
    while (fgets(buffer, sizeof(buffer), fin)) {
        if (strstr(buffer, "Numero maximo") != NULL) break;
    }

    // agora lê a capacidade
    int capacidade;
    fscanf(fin, "%d", &capacidade);
    // descarta o resto da linha
    fgets(buffer, sizeof(buffer), fin);


    // ignorar linhas até "TAREFA..."
    while (fgets(buffer, sizeof(buffer), fin)) {
        if (strstr(buffer, "TAREFA") != NULL) break;
    }
    // ignorar linha de traços
    fgets(buffer, sizeof(buffer), fin);

    FilaPrioridade agenda;
    Inicializar(&agenda, capacidade);

    // vamos guardar as respostas para consultas
    char respostas[1000][100]; 
    int qtdResp = 0;

    char comando[20];
    while (fscanf(fin, "%s", comando) != EOF) {
        if (strcmp(comando, "NOVA") == 0) {
            Tarefa t;
            fscanf(fin, "%d", &t.prioridade);
            fgetc(fin); // espaço
            fgets(t.descricao, MAX_DESC, fin);
            t.descricao[strcspn(t.descricao, "\n")] = 0;
            if (Inserir(&agenda, t) == -1) {
                sprintf(respostas[qtdResp++], 
                        "ERRO     Agenda cheia. Impossivel inserir.");
            }
        }
        else if (strcmp(comando, "PROXIMA") == 0) {
            Tarefa t;
            if (!ConsultarMax(&agenda, &t)) {
                sprintf(respostas[qtdResp++], 
                        "AVISO    Nao ha tarefas na agenda  :-)");
            } else {
                sprintf(respostas[qtdResp++], "%-3d      %s", 
                        t.prioridade, t.descricao);
                RemoverMax(&agenda);
            }
        }
        else if (strcmp(comando, "FIM") == 0) {
            break;
        }
    }

    // --- CABEÇALHO DE SAÍDA ---
    fprintf(fout, "Agenda Eletronica - Exemplo de arquivo de saida.\n");
    fprintf(fout, "Pode colocar qualquer texto no cabecalho.\n");
    fprintf(fout, "O cabecalho deve ter exatamente 5 linhas.\n");
    fprintf(fout, "Neste caso, a quinta linha estah em branco  :-)\n");
    fprintf(fout, "\n");

    // --- RESPOSTAS ---
    fprintf(fout, "--------------------------------------------------\n");
    fprintf(fout, "RESPOSTAS DAS CONSULTAS\n");
    fprintf(fout, "--------------------------------------------------\n");
    for (int i = 0; i < qtdResp; i++)
        fprintf(fout, "%s\n", respostas[i]);

    // --- FICA PARA O DIA SEGUINTE ---
    fprintf(fout, "\n--------------------------------------------------\n");
    fprintf(fout, "FICA PARA O DIA SEGUINTE\n");
    fprintf(fout, "--------------------------------------------------\n");
    if (FilaVazia(&agenda)) {
        fprintf(fout, "Agenda vazia! Nao restam tarefas para o dia seguinte.\n");
    } else {
        while (!FilaVazia(&agenda)) {
            Tarefa t;
            ConsultarMax(&agenda, &t);
            fprintf(fout, "%-3d      %s\n", t.prioridade, t.descricao);
            RemoverMax(&agenda);
        }
    }

    Finalizar(&agenda);
    fclose(fin);
    fclose(fout);
    return 0;
}
