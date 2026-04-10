# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `transacoes.csv` | CSV | Analisar padrão de gastos do cliente |

---

## Estratégia de Integração

### Como os dados são carregados?

Os arquivos de dados (JSON e CSV) são carregados localmente na incialização da aplicação conectada ao Ollama. Os dados de `transacoes.csv` e `perfil_investidor.json` são processados e enviados junto às mensagens do usuário como contexto prévio.

### Como os dados são usados no prompt?

Os dados formatados do usuário (identificação de gênero para uso de amigão/amigona, histórico de transações e perfil de investimentos) são inseridos de forma consolidada no System Prompt. Isso fornece munição suficiente para o Amigão julgar gastos passados antes de recomendar formas de criar uma reserva de emergência.

---

## Exemplo de Contexto Montado

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
