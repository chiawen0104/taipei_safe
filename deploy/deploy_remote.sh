gcloud functions deploy demo \
  --gen2 \
  --runtime python39 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point main \
  --region asia-east1