#!/bin/bash

send_success_notification() {
  MESSAGE_TEXT="Migration Succeeded :rocket:"
  SLACK_TEXT_TITLE="AWS Deployment"
  SLACK_DEPLOYMENT_TEXT=":tada: ${MESSAGE_TEXT}"
  COLOR="good"
  ACTION_BUTTON="$(echo \
    "{\"type\": \"button\", \"text\": \"Rebuild\", \"url\": \"${REBUILD_URL}\"}", \
  )"

  curl -X POST --data-urlencode \
  "payload={
      \"channel\": \"test-migration-errors\",
      \"username\": \"DeployNotification\",
      \"attachments\": [{
          \"fallback\": \"Migrations notification\",
          \"color\": \"${COLOR}\",
          \"title\": \"${SLACK_TEXT_TITLE}\",
          \"title_link\": \"\",
          \"text\": \"${SLACK_DEPLOYMENT_TEXT}\",
          \"actions\": [${ACTION_BUTTON}]
      }]
  }" \
  "${SLACK_WEBHOOK_MIGRATIONS}"
}

send_success_notification
