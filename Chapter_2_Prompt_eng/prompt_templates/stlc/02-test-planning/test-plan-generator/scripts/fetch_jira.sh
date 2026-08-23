#!/usr/bin/env bash
# Fetch a JIRA issue as JSON. Usage: ./fetch_jira.sh VOC-1234
# Needs env: JIRA_BASE_URL (e.g. https://yourco.atlassian.net), JIRA_EMAIL, JIRA_TOKEN
# ponytail: curl + jq, no SDK. Add pagination/attachments only if a ticket needs it.
set -euo pipefail

KEY="${1:?usage: fetch_jira.sh <ISSUE-KEY>}"
: "${JIRA_BASE_URL:?set JIRA_BASE_URL}"
: "${JIRA_EMAIL:?set JIRA_EMAIL}"
: "${JIRA_TOKEN:?set JIRA_TOKEN}"

if [[ ! "$KEY" =~ ^[A-Z][A-Z0-9_]*-[1-9][0-9]*$ ]]; then
  printf 'invalid JIRA issue key: use canonical form such as VOC-1234\n' >&2
  exit 2
fi

if [[ ! "$JIRA_BASE_URL" =~ ^https://[A-Za-z0-9.-]+(:[0-9]+)?(/[^[:space:]]*)?$ \
   || "$JIRA_BASE_URL" == *\?* || "$JIRA_BASE_URL" == *\#* ]]; then
  printf 'JIRA_BASE_URL must be an HTTPS base URL without whitespace, query, or fragment\n' >&2
  exit 2
fi
JIRA_BASE_URL=${JIRA_BASE_URL%/}

if [[ "$JIRA_EMAIL" == *:* || "$JIRA_EMAIL" == *$'\r'* || "$JIRA_EMAIL" == *$'\n'* \
   || "$JIRA_TOKEN" == *$'\r'* || "$JIRA_TOKEN" == *$'\n'* ]]; then
  printf 'JIRA_EMAIL/JIRA_TOKEN contains an unsupported delimiter or newline\n' >&2
  exit 2
fi

JIRA_EMAIL_CONFIG=${JIRA_EMAIL//\\/\\\\}
JIRA_EMAIL_CONFIG=${JIRA_EMAIL_CONFIG//\"/\\\"}
JIRA_TOKEN_CONFIG=${JIRA_TOKEN//\\/\\\\}
JIRA_TOKEN_CONFIG=${JIRA_TOKEN_CONFIG//\"/\\\"}
unset JIRA_EMAIL JIRA_TOKEN

# Feed Basic-auth credentials over stdin so the token is not exposed in curl's argv.
# curl reads this stream as config; the request remains a GET, so stdin is not a body.
printf 'user = "%s:%s"\n' "$JIRA_EMAIL_CONFIG" "$JIRA_TOKEN_CONFIG" \
| curl --silent --show-error --fail-with-body --config - \
  -H "Accept: application/json" \
  "${JIRA_BASE_URL}/rest/api/3/issue/${KEY}?fields=summary,description,issuetype,priority,components,labels,fixVersions,issuelinks,attachment" \
| jq '{
    key: .key,
    summary: .fields.summary,
    type: .fields.issuetype.name,
    priority: .fields.priority.name,
    components: [.fields.components[]?.name],
    labels: .fields.labels,
    fixVersions: [.fields.fixVersions[]?.name],
    description: .fields.description,
    links: [.fields.issuelinks[]? | {type: .type.name, key: (.outwardIssue.key // .inwardIssue.key)}],
    attachments: [.fields.attachment[]? | .filename]
  }'
