 📦 Sistema de Controle de Pátio de Contêineres

Sistema de linha de comando (CLI) para gerenciar a movimentação e o
armazenamento de contêineres em um pátio portuário: cadastro, busca,
atualização de status, movimentação entre posições e estatísticas de
ocupação.

Este projeto nasceu da minha experiência prática em terminais portuários,
onde já geri controles de pátio manualmente em planilhas. A proposta aqui
foi recriar esse processo como uma aplicação real, aplicando lógica de
programação e banco de dados.

 Funcionalidades

- Cadastro de contêineres (número, tipo, cliente/navio, posição no pátio)
- Listagem com filtro por status
- Busca por número do contêiner
- Atualização de status (Aguardando → Armazenado → Em Trânsito → Carregado/Saída)
- Movimentação entre bloco/fileira/andar
- Estatísticas: total de contêineres, distribuição por status e ocupação por bloco

 Tecnologias

- Python 3 (sem dependências externas)
- SQLite (banco de dados local, via módulo `sqlite3` da biblioteca padrão)

 Estrutura do projeto

```
patio-conteineres/
 main.py           Menu do terminal (interação com o usuário)
 operacoes.py       Regras de negócio (cadastrar, buscar, atualizar...)
 database.py         Conexão e criação da tabela no SQLite
 README.md
```

 Como rodar

Não precisa instalar nenhuma dependência — só Python 3.

```bash
git clone https://github.com/FabianoSeara/patio-conteineres.git
cd patio-conteineres
python3 main.py
```

O banco de dados (`patio.db`) é criado automaticamente na primeira execução.

## Exemplo de uso

```
==================================================
   SISTEMA DE CONTROLE DE PÁTIO DE CONTÊINERES
==================================================
1. Cadastrar novo container
2. Listar containers
3. Buscar container por número
4. Atualizar status de um container
5. Mover container (bloco/fileira/andar)
6. Estatísticas do pátio
0. Sair
==================================================
```

 Próximos passos

- [ ] Exportar relatórios em CSV
- [ ] Adicionar histórico de movimentações por contêiner
- [ ] Interface web (Flask) como evolução do projeto

---

Projeto desenvolvido por [Fabiano Seára](https://github.com/FabianoSeara) como parte do meu portfólio de transição de carreira para desenvolvimento de software.
