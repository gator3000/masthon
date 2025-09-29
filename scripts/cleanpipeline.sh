#!/bin/bash

# Configuration
GITLAB_API="${CI_API_V4_URL:-https://gitlab.com/api/v4}"
PROJECT_ID="${CI_PROJECT_ID}"
ACCESS_TOKEN="${AUTO_REMOVE_TOKEN}"  # À définir dans les variables GitLab
DAYS_THRESHOLD=30

# Calcul de la date limite
CUTOFF_DATE=$(date -u -d "-$DAYS_THRESHOLD days" +"%Y-%m-%dT%H:%M:%S")

# Pagination
PAGE=1
while true; do
  RESPONSE=$(curl --silent --header "PRIVATE-TOKEN: $ACCESS_TOKEN" \
    "$GITLAB_API/projects/$PROJECT_ID/pipelines?per_page=100&page=$PAGE")

  PIPELINE_IDS=$(echo "$RESPONSE" | jq -r '.[] | select(.created_at < "'$CUTOFF_DATE'") | .id')

  if [ -z "$PIPELINE_IDS" ]; then
    echo "✅ Aucun pipeline à supprimer sur la page $PAGE"
    break
  fi

  for ID in $PIPELINE_IDS; do
    DELETE=$(curl --silent --request DELETE \
      --header "PRIVATE-TOKEN: $ACCESS_TOKEN" \
      "$GITLAB_API/projects/$PROJECT_ID/pipelines/$ID")

    echo "🗑️ Pipeline $ID supprimé"
  done

  PAGE=$((PAGE + 1))
done
